"""Fancier field subclasses."""


__all__ = [
    'TypedField',
]


from .struct import Field
from .type import normalize_kind, checktype, checktype_seq


class TypedField(Field):
    
    """A field with dynamically-checked type constraints.
    
    kind is a class or tuple of classes, as described in type.py.
    If seq is False, the field value must satisfy kind. Otherwise,
    the field value must be a sequence of elements that satisfy kind.
    The sequence gets converted to a tuple if it isn't already.
    If nodup is also True, the elements must be distinct (as
    determined by kind.__eq__()).
    """
    
    def __init__(self, kind, *, seq=False, nodups=False):
        super().__init__()
        self.kind = normalize_kind(kind)
        self.seq = seq
        self.nodups = nodups
    
    def copy(self):
        return type(self)(self.kind, seq=self.seq, nodups=self.nodups)
    
    def __set__(self, inst, value):
        if self.seq:
            checktype_seq(value, self.kind, self.nodups)
            value = tuple(value)
        else:
            checktype(value, self.kind)
        
        super().__set__(inst, value)
