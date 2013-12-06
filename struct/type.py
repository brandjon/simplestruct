"""Type checking and type coercion."""

# Spare me the "It's not the Python way" lectures. I've lost too much
# time to type errors in places where I never had any intention of
# allowing duck-typed alternative values.


__all__ = [
    'checktype',
    'checktype_seq',
]


def strtype(val):
    """Get a string describing val's type."""
    return type(val).__name__

def checktype(val, typ):
    """Raise TypeError if val is not of type typ."""
    if not isinstance(val, typ):
        exp = typ.__name__
        got = strtype(val)
        raise TypeError('Expected {}; got {}'.format(exp, got))

def checktype_seq(seq, typ):
    """Raise TypeError if seq is not a sequence of type typ.
    
    As a special case to catch a common error, a string is not
    considered to be a sequence of strings but rather an atomic
    type. 
    """
    exp = typ.__name__
    
    # Make sure we have a sequence.
    try:
        iterator = iter(seq)
        # Generators aren't sequences. This avoids a confusing case
        # where we consume a generator by type-checking it, and leave
        # only an exhausted iterator for the user code.
        len(seq)
    except (TypeError, AssertionError):
        got = strtype(seq)
        raise TypeError('Expected sequence of {}; '
                        'got {} instead of sequence'.format(exp, got))
    
    if typ is str:
        if isinstance(seq, str):
            raise TypeError('Expected sequence of str; got single str '
                            '(strings do not count as character sequences)')
        
    for i, item in enumerate(iterator):
        if not isinstance(item, typ):
            got = strtype(item)
            raise TypeError('Expected sequence of {}; '
                            'got sequence with {} at position {}'.format(
                            exp, got, i))
