"""Core framework for Struct, its metaclass, and field descriptors."""


__all__ = [
    'Field',
    'MetaStruct',
    'Struct',
]


from collections import OrderedDict, Counter
from functools import reduce
from inspect import Signature, Parameter
from reprlib import recursive_repr


def hash_seq(seq):
    """Given a sequence of hash values, return a combined xor'd hash."""
    return reduce(lambda x, y: x ^ y, seq, 0)


class Field:
    
    """Descriptor for declaring fields on Structs.
    
    Writing to a field will fail with AttributeError if the Struct
    is immutable and has finished initializing.
    
    Subclasses may override __set__() to implement type restrictions
    or coercion, and may override eq() and hash() to implement custom
    equality semantics.
    """
    
    # TODO: The current copy() is not ideal because a subclass that
    # overrides it needs to know about the fields of the base class,
    # so that it can pass those to the newly constructed object.
    # For instance, TypedField needs to know to pass in
    # default=self.default.
    #
    # One possible solution is to get meta: make Field itself be a
    # Struct, and let attributes like default be Struct fields.
    # Then the use of copy() becomes _replace(name=new_name),
    # and subclasses simply set _inherit_fields = True.
    # This solution would require a new non-Struct BaseField class
    # for bootstrapping.
    
    NO_DEFAULT = object()
    
    def __init__(self, default=NO_DEFAULT):
        # name is the attribute name through which this field is
        # accessed from the Struct. This will be set automatically
        # by MetaStruct.
        self.name = None
        self.default = default
    
    def copy(self):
        # This is used by MetaStruct to get a fresh instance
        # of the field for each of its occurrences.
        return type(self)(default=self.default)
    
    @property
    def has_default(self):
        return self.default is not self.NO_DEFAULT
    
    def __get__(self, inst, value):
        if inst is None:
            return self
        return inst.__dict__[self.name]
    
    def __set__(self, inst, value):
        if inst._immutable and inst._initialized:
            raise AttributeError('Struct is immutable')
        inst.__dict__[self.name] = value
    
    def eq(self, val1, val2):
        """Compare two values for this field."""
        return val1 == val2
    
    def hash(self, val):
        """Hash a value for this field."""
        return hash(val)


class MetaStruct(type):
    
    """Metaclass for Structs.
    
    Upon class definition (of a new Struct subtype), set the class
    attribute _struct to be a tuple of the Field descriptors, in
    declaration order. If the class has attribute _inherit_fields
    and it evaluates to true, also include fields of base classes.
    (Names of inherited fields must not collide with other inherited
    fields or this class's fields.) Set class attribute _signature
    to be an inspect.Signature object to facilitate instantiation.
    
    Upon instantiation of a Struct subtype, set the instance's
    _initialized attribute to True after __init__() returns.
    Preprocess its __new__/__init__() arguments as well.
    """
    
    # Use OrderedDict to preserve Field declaration order.
    @classmethod
    def __prepare__(cls, name, bases, **kargs):
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
        for fname, f in namespace.items():
            # Using the Field class directly (or one of its subclasses)
            # is shorthand for making a Field instance with no args.
            if isinstance(f, type) and issubclass(f, Field):
                f = f()
            if isinstance(f, Field):
                # Fields need to be copied in case they're used
                # in multiple places (in this class or others).
                f = f.copy()
                f.name = fname
                fields.append(f)
            namespace[fname] = f
        # Ensure no name collisions.
        fnames = Counter(f.name for f in fields)
        collided = [k for k in fnames if fnames[k] > 1]
        if len(collided) > 0:
            raise AttributeError(
                'Struct {} has colliding field name(s): {}'.format(
                clsname, ', '.join(collided)))
        
        cls = super().__new__(mcls, clsname, bases, dict(namespace), **kargs)
        
        cls._struct = tuple(fields)
        
        params = []
        for f in cls._struct:
            default = f.default if f.has_default else Parameter.empty
            params.append(Parameter(f.name, Parameter.POSITIONAL_OR_KEYWORD,
                                    default=default))
        cls._signature = Signature(params)
        
        return cls
    
    def get_boundargs(cls, *args, **kargs):
        """Return an inspect.BoundArguments object for the application
        of this Struct's signature to its arguments. Add missing values
        for default fields as keyword arguments.
        """
        boundargs = cls._signature.bind(*args, **kargs)
        # Include default arguments.
        for param in cls._signature.parameters.values():
            if (param.name not in boundargs.arguments and
                param.default is not param.empty):
                boundargs.arguments[param.name] = param.default
        return boundargs
    
    # Mark the class as _initialized after construction.
    def __call__(cls, *args, **kargs):
        boundargs = cls.get_boundargs(*args, **kargs)
        inst = super().__call__(*boundargs.args, **boundargs.kwargs)
        inst._initialized = True
        return inst


class Struct(metaclass=MetaStruct):
    
    """Base class for Structs.
    
    Declare fields by assigning class attributes to an instance of
    the descriptor Field or one of its subclasses. As a convenience,
    assigning to the Field (sub)class itself is also permitted.
    The fields become the positional arguments to the class's
    constructor. Construction via keyword argument is also allowed,
    following normal Python parameter passing rules.
    
    If class attribute _inherit_fields is defined and evaluates to
    true, the fields of each base class are prepended to this class's
    list of fields in left-to-right order.
    
    A subclass may define __init__() to customize how fields are
    initialized, or to set other non-field attributes. If the class
    attribute _immutable evaluates to true, assigning to fields is
    disallowed once the last subclass's __init__() finishes.
    
    Structs may be pickled. Upon unpickling, __init__() will be
    called.
    
    Structs support structural equality. Hashing is allowed only
    for immutable Structs and after they are initialized.
    
    The methods _asdict() and _replace() behave as they do for
    collections.namedtuple.
    """
    
    _immutable = True
    """Flag for whether to allow reassignment to fields after
    construction. Override with False in subclass to allow.
    """
    
    def __new__(cls, *args, **kargs):
        inst = super().__new__(cls)
        # _initialized is read during field initialization.
        inst._initialized = False
        
        f = None
        try:
            boundargs = cls.get_boundargs(*args, **kargs)
            for f in cls._struct:
                setattr(inst, f.name, boundargs.arguments[f.name])
            f = None
        except TypeError as exc:
            if f is not None:
                where = "{} (field '{}')".format(cls.__name__, f.name)
            else:
                where = cls.__name__
            raise TypeError('Error constructing {}: {}'.format(
                            where, exc)) from exc
        
        return inst
    
    # str() and repr() both recurse over their fields with
    # whichever function was used initially. Both are protected
    # from recursive cycles with the help of reprlib.
    
    def _fmt_helper(self, fmt):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('{}={}'.format(f.name, fmt(getattr(self, f.name)))
                      for f in self._struct))
    
    @recursive_repr()
    def __str__(self):
        return self._fmt_helper(str)
    
    @recursive_repr()
    def __repr__(self):
        return self._fmt_helper(repr)
    
    def __eq__(self, other):
        # Succeed immediately if we're being tested against ourselves
        # (identical object in memory). This avoids an unnecessary
        # walk over the fields, which can be expensive if the field
        # values are themselves Structs, and so on.
        if self is other:
            return True
        
        # Two struct instances are equal if they have the same
        # type and same field values.
        if type(self) != type(other):
            # But leave the door open to subclasses providing
            # alternative equality semantics.
            return NotImplemented
        
        return all(f.eq(getattr(self, f.name), getattr(other, f.name))
                   for f in self._struct)
    
    def __hash__(self):
        if not self._immutable:
            raise TypeError('Cannot hash mutable Struct {}'.format(
                            self.__class__.__name__))
        if not self._initialized:
            raise TypeError('Cannot hash uninitialized Struct {}'.format(
                            self.__class__.__name__))
        return hash_seq(f.hash(getattr(self, f.name))
                        for f in self._struct)
    
    def __len__(self):
        return len(self._struct)
    
    def __iter__(self):
        return (getattr(self, f.name) for f in self._struct)
    
    def __getitem__(self, index):
        # Index may also be a slice.
        return tuple(getattr(self, f.name) for f in self._struct)[index]
    
    def __setitem__(self, index, value):
        if isinstance(index, slice):
            fnames = [f.name for f in self._struct][index]
            values = list(value)
            if len(values) < len(fnames):
                word = 'value' if len(values) == 1 else 'values'
                raise ValueError('need more than {} {} to '
                                 'unpack'.format(len(fnames), word))
            elif len(values) > len(fnames):
                raise ValueError('too many values to unpack (expected '
                                 '{})'.format(len(fnames)))
            for fname, v in zip(fnames, values):
                setattr(self, fname, v)
        else:
            setattr(self, self._struct[index].name, value)
    
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
        """Return a copy of this Struct with the same fields except
        with the changes specified by kargs.
        """
        fields = {f.name: getattr(self, f.name)
                  for f in self._struct}
        fields.update(kargs)
        return type(self)(**fields)
    
    # XXX: We could provide a copy() method as well, analogous to
    # list, dict, and other collections. Unlike the above methods,
    # it would not have an underscore prefix, and potentially clash
    # with a user-defined field named "copy". But in this case,
    # the user field should simply take precedence and shadow
    # this feature.
