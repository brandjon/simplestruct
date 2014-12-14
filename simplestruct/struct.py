"""Provides field descriptors and the base and meta classes for struct."""


__all__ = [
    'Field',
    'MetaStruct',
    'Struct',
]


from collections import OrderedDict
from functools import reduce
from inspect import Signature, Parameter

from simplestruct.type import (str_valtype, check_spec,
                               normalize_kind, normalize_mods)


def hash_seq(seq):
    """Given a sequence of hash values, return a combined xor'd hash."""
    return reduce(lambda x, y: x ^ y, seq, 0)


class Field:
    
    """Descriptor for declaring struct fields. Fields have a name
    and type spec (kind and mods).
    
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
    
    def __init__(self, kind=None, mods=()):
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
    _struct to be a tuple of the Field descriptors, in declaration
    order.
    
    Upon instantiation of a Struct subtype, set the instance's
    _initialized attribute to True after __init__() returns.
    """
    
    # Use OrderedDict to preserve Field declaration order.
    @classmethod
    def __prepare__(mcls, name, bases, **kargs):
        return OrderedDict()
    
    # Construct the _struct attribute on the new class.
    def __new__(mcls, clsname, bases, namespace, **kargs):
        fields = []
        # If inheriting, gather fields from base classes.
        if namespace.get('_inherit_fields', False):
            for b in bases:
                if isinstance(b, MetaStruct):
                    fields += b._struct
        # Gather fields from this class's namespace.
        for fname, f in namespace.copy().items():
            if not isinstance(f, Field):
                continue
            
            f.name = fname
            fields.append(f)
        
        cls = super().__new__(mcls, clsname, bases, dict(namespace), **kargs)
        
        cls._struct = tuple(fields)
        
        cls._signature = Signature(
            parameters=[Parameter(f.name, Parameter.POSITIONAL_OR_KEYWORD)
                        for f in cls._struct])
        
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
    
    By default, __new__() will initialize all fields.
    If immutable, fields may still be written to until __init__()
    (of the last subclass) returns.
    
    Subclasses are not required to call super().__init__() if this
    is the only base class.
    """
    
    _immutable = True
    """Flag for whether to allow reassignment to fields after
    construction. Override with False in subclass to allow.
    """
    
    # We expect there to be one constructor argument for each
    # field, in declaration order.
    def __new__(cls, *args, **kargs):
        inst = super().__new__(cls)
        inst._initialized = False
        
        try:
            boundargs = cls._signature.bind(*args, **kargs)
            for f in cls._struct:
                setattr(inst, f.name, boundargs.arguments[f.name])
        except TypeError as exc:
            raise TypeError('Error constructing ' + cls.__name__) from exc
        
        return inst
    
    def _fmt_helper(self, fmt):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}={}'.format(f.name, fmt(getattr(self, f.name)))
                      for f in self._struct))
    
    def __str__(self):
        return self._fmt_helper(str)
    def __repr__(self):
        return self._fmt_helper(repr)
    
    def __eq__(self, other):
        if not isinstance(self, other.__class__):
            return NotImplemented
        
        return all(f._field_eq(getattr(self, f.name), getattr(other, f.name))
                   for f in self._struct)
    
    def __neq__(self, other):
        return not (self == other)
    
    def __hash__(self):
        if not self._immutable:
            raise TypeError('Cannot hash mutable Struct {}'.format(
                            str_valtype(self)))
        if not self._initialized:
            raise TypeError('Cannot hash uninitialized Struct {}'.format(
                            str_valtype(self)))
        return hash_seq(f._field_hash(getattr(self, f.name))
                        for f in self._struct)
    
    def __reduce_ex__(self, protocol):
        # We use __reduce_ex__() rather than __getnewargs__() so that
        # the metaclass's __call__() will still run. This is needed to
        # trigger the user-defined __init__() and to set _immutable to
        # False.
        return (self.__class__, tuple(getattr(self, f.name)
                                      for f in self._struct))
    
    def _asdict(self):
        """Return an OrderedDict of the fields."""
        return OrderedDict((f.name, getattr(self, f.name))
                           for f in self._struct)
    
    def _replace(self, **kargs):
        """Return a copy of this struct with the same fields except
        with the changes specified by kargs.
        """
        fields = {f.name: getattr(self, f.name)
                  for f in self._struct}
        fields.update(kargs)
        return type(self)(**fields)
