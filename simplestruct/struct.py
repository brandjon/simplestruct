"""Provides field descriptors and the base and meta classes for struct."""


__all__ = [
    'Field',
    'MetaStruct',
    'Struct',
]


from collections import OrderedDict
from functools import reduce

from simplestruct.type import check_spec, normalize_kind, normalize_mods


def hash_seq(seq):
    """Given a sequence of hash values, return a combined xor'd hash."""
    return reduce(lambda x, y: x ^ y, seq, 0)


class Field:
    
    """Descriptor for declaring struct fields. Fields have a name
    and type spec (kind and mods). In addition to those specified
    in types.py, mods may include:
    
        '!': this field is derived data that should not be passed as
            an argument to the struct's constructor or consulted for
            equality/hashing
    
    The 'seq' mod will additionally convert the value to a tuple.
    
    All writes are type-checked according to the type spec. 
    Writing to a field will fail with AttributeError if the struct
    is immutable and has finished initializing.
    
    To use custom equality/hashing semantics, subclass Field and
    override eq() and hash(). Note that in the case of list-valued
    fields, these functions are called element-wise.
    """
    
    # TODO: It would be a pretty sweet/evil metacircularity to define
    # Field itself as a Struct.
    
    # The attribute "name" is assigned by MetaStruct.
    
    def __init__(self, kind, mods=()):
        self.kind = normalize_kind(kind)
        self.mods = normalize_mods(mods)
    
    def __get__(self, inst, value):
        if inst is None:
            raise AttributeError('Cannot retrieve field from class')
        return inst.__dict__[self.name]
    
    def __set__(self, inst, value):
        if inst._immutable and inst._initialized:
            raise AttributeError('Struct is immutable')
        
        check_spec(value, self.kind, self.mods)
        
        if 'seq' in self.mods:
            value = tuple(value)
        
        inst.__dict__[self.name] = value
    
    def _field_eq(self, val1, val2):
        """Compare two field values for equality."""
        if 'seq' in self.mods:
            if len(val1) != len(val2):
                return False
            return all(self.eq(e1, e2) for e1, e2 in zip(val1, val2))
        else:
            return self.eq(val1, val2)
    
    def _field_hash(self, val):
        """Hash a field value."""
        if 'seq' in self.mods:
            return hash_seq(self.hash(e) for e in val)
        else:
            return self.hash(val)
    
    def eq(self, val1, val2):
        """Compare two values of this field's kind."""
        return val1 == val2
    
    def hash(self, val):
        """Hash a value of this field's kind."""
        return hash(val)


class MetaStruct(type):
    
    """Metaclass for Structs.
    
    Upon class definition (of a new Struct subtype), set class attribute
    _fields to be a tuple of the Field descriptors, in declaration
    order.
    
    Upon instantiation of a Struct subtype, set its _initialized
    attribute to True after __init__() returns.
    """
    
    @property
    def _primary_fields(cls):
        """Non-derived fields, i.e. fields that don't have a '!'
        modified.
        """
        return [f for f in cls._fields if '!' not in f.mods]
    
    # Use OrderedDict to preserve Field declaration order.
    @classmethod
    def __prepare__(mcls, name, bases, **kwds):
        return OrderedDict()
    
    # Construct the _fields attribute on the new class.
    def __new__(mcls, clsname, bases, namespace, **kwds):
        fields = []
        for fname, f in namespace.copy().items():
            if not isinstance(f, Field):
                continue
            
            f.name = fname
            fields.append(f)
        
        cls = super().__new__(mcls, clsname, bases, dict(namespace), **kwds)
        
        cls._fields = tuple(fields)
        
        return cls
    
    # Mark the class as _initialized after construction.
    def __call__(mcls, *args, **kargs):
        inst = super().__call__(*args, **kargs)
        inst._initialized = True
        return inst


class Struct(metaclass=MetaStruct):
    
    """A fixed structure class that supports default constructors,
    type-checking and coersion, immutable fields, pretty-printing,
    equality, and hashing.
    
    By default, __new__() will initialize the non-derived fields.
    If immutable, fields may still be written to until __init__()
    (of the last subclass) returns.
    
    Subclasses are not required to call super().__init__() if this
    is the only base class.
    """
    
    @property
    def _primary_fields(self):
        return self.__class__._primary_fields
    
    _immutable = True
    """Flag for whether to allow reassignment to fields after
    construction. Override with False in subclass to allow.
    """
    
    # TODO: Allow keyword arguments to constructor.
    # Might be implemented using inspect.Signature.
    
    # We expect there to be one constructor argument for each
    # non-derived field (i.e. a field without the '!' modifier),
    # in field declaration order.
    def __new__(cls, *args):
        inst = super().__new__(cls)
        inst._initialized = False
        
        pfields = cls._primary_fields
        
        if not len(args) == len(pfields):
            raise ValueError('{} expects {} args, got {}'.format(
                             cls.__name__, len(pfields), len(args)))
        
        # TODO: better error message here if typecheck fails
        for f, arg in zip(pfields, args):
            setattr(inst, f.name, arg)
        
        return inst
    
    def _fmt_helper(self, fmt):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}={}'.format(f.name, fmt(getattr(self, f.name)))
                      for f in self._primary_fields))
    
    def __str__(self):
        return self._fmt_helper(str)
    def __repr__(self):
        return self._fmt_helper(repr)
    
    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return NotImplemented
        
        return all(f._field_eq(getattr(self, f.name), getattr(other, f.name))
                   for f in self._primary_fields)
    
    def __neq__(self, other):
        return not (self == other)
    
    def __hash__(self):
        return hash_seq(f._field_hash(getattr(self, f.name))
                        for f in self._primary_fields)
