"""Type checking and type coercion.

Spare me the "It's not the Python way" lectures. I've lost too much
time to type errors in places where I never had any intention of
allowing duck-typed alternative values.
"""


__all__ = [
    'TypeChecker',
    'checktype',
    'checktype_seq',
]


class TypeChecker:
    
    """A simple type checker supporting sequences and unions.
    Suitable for use as a mixin.
    
    A "kind" is a tuple of types. A value satisfies a kind if it is
    an instance of any of the types.
    """
    
    def str_valtype(self, val):
        """Get a string describing the type of val."""
        if val is None:
            return 'None'
        return val.__class__.__name__
    
    def normalize_kind(self, kindlike):
        """Make a kind out of a possible shorthand. If the given
        argument is a sequence of types or a singular type, it becomes
        a kind that accepts exactly those types. If the given argument
        is None, it becomes a type that accepts anything.
        """
        if kindlike is None:
            return (object,)
        elif isinstance(kindlike, type):
            return (kindlike,)
        else:
            return tuple(kindlike)
    
    def str_kind(self, kind):
        """Get a string describing a kind."""
        if len(kind) == 0:
            return 'Nothing'
        elif len(kind) == 1:
            return kind[0].__name__
        elif len(kind) == 2:
            return kind[0].__name__ + ' or ' + kind[1].__name__
        else:
            return 'one of {' + ', '.join(t.__name__ for t in kind) + '}'
    
    def checktype(self, val, kind, **kargs):
        """Raise TypeError if val does not satisfy kind."""
        if not isinstance(val, kind):
            raise TypeError('Expected {}; got {}'.format(
                            self.str_kind(kind), self.str_valtype(val)))
    
    def checktype_seq(self, seq, kind, *, unique=False, **kargs):
        """Raise TypeError if seq is not a sequence of elements satisfying
        kind. Optionally require elements to be unique.
        
        As a special case, a string is considered to be an atomic value
        rather than a sequence of single-character strings. (Thus,
        checktype_seq('foo', str) will fail.)
        """
        exp = self.str_kind(kind)
        
        # Make sure we have a sequence.
        try:
            iterator = iter(seq)
            # Generators aren't sequences. This avoids a confusing bug
            # where we consume a generator by type-checking it, and leave
            # only an exhausted iterator for the user code.
            len(seq)
        except TypeError:
            got = self.str_valtype(seq)
            raise TypeError('Expected sequence of {}; '
                            'got {} instead of sequence'.format(exp, got))
        
        if isinstance(seq, str):
            raise TypeError('Expected sequence of {}; got single str '
                            '(strings do not count as character '
                            'sequences)'.format(exp))
        
        for i, item in enumerate(iterator):
            # Depend on checktype() to check individual elements,
            # but generate an error message that includes the position
            # of the failure.
            try:
                self.checktype(item, kind, **kargs)
            except TypeError:
                got = self.str_valtype(item)
                raise TypeError('Expected sequence of {}; '
                                'got sequence with {} at position {}'.format(
                                exp, got, i)) from None
        
        if unique:
            seen = []
            for i, item in enumerate(seq):
                if item in seen:
                    raise TypeError('Duplicate element {} at '
                                    'position {}'.format(repr(item), i))
                seen.append(item)


# We export some convenience methods so the caller doesn't have to
# instantiate TypeChecker. These methods automatically normalize kind.

checker = TypeChecker()

def checktype(val, kind):
    kind = checker.normalize_kind(kind)
    checker.checktype(val, kind)

def checktype_seq(val, kind, *, unique=False):
    kind = checker.normalize_kind(kind)
    checker.checktype_seq(val, kind, unique=unique)
