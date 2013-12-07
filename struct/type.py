"""Type checking and type coercion."""

# Spare me the "It's not the Python way" lectures. I've lost too much
# time to type errors in places where I never had any intention of
# allowing duck-typed alternative values.

# A typelist is a tuple of types. A value satisfies a typelist if
# it is an instance of any of the types. For convenience, typelists
# may also be given as single types and as sequences besides tuples.

# A type specification is a typelist along with a tuple of modifier
# strings, which may include:
#   'seq': sequence of elements satisfying the typelist
#   'nodups': with 'seq', no duplicate elements allowed


__all__ = [
    'checktype',
    'checktype_seq',
    'check_spec',
]


def str_valtype(val):
    """Get a string describing the type of val."""
    return type(val).__name__

def normalize_tl(tl):
    """Make a typelist out of a single type or out of a non-tuple
    sequence.
    """
    if isinstance(tl, type):
        return (tl,)
    else:
        return tuple(tl)

def normalize_mods(mods):
    """Make a modifier list out of space-delimited string."""
    if isinstance(mods, str):
        return tuple(mods.split())
    else:
        return tuple(mods)

def str_tl(tl):
    """Get a string describing a typelist."""
    if len(tl) == 0:
        return '()'
    elif len(tl) == 1:
        return tl[0].__name__
    elif len(tl) == 2:
        return tl[0].__name__ + ' or ' + tl[1].__name__
    else:
        return 'one of {' + ', '.join(t.__name__ for t in tl) + '}'


def checktype(val, tl):
    """Raise TypeError if val does not satisfy tl."""
    tl = normalize_tl(tl)
    if not isinstance(val, tl):
        raise TypeError('Expected {}; got {}'.format(
                        str_tl(tl), str_valtype(val)))

def checktype_seq(seq, tl, nodups=False):
    """Raise TypeError if seq is not a sequence of elements satisfying
    tl. Optionally require elements to be unique.
    
    As a special case, a string is considered to be an atomic value
    rather than a sequence of single-character strings. (Thus,
    checktype_seq('foo', str) will fail.)
    """
    tl = normalize_tl(tl)
    exp = str_tl(tl)
    
    # Make sure we have a sequence.
    try:
        iterator = iter(seq)
        # Generators aren't sequences. This avoids a confusing bug
        # where we consume a generator by type-checking it, and leave
        # only an exhausted iterator for the user code.
        len(seq)
    except TypeError:
        got = str_valtype(seq)
        raise TypeError('Expected sequence of {}; '
                        'got {} instead of sequence'.format(exp, got))
    
    if isinstance(seq, str):
        raise TypeError('Expected sequence of {}; got single str '
                        '(strings do not count as character '
                        'sequences'.format(exp))
        
    for i, item in enumerate(iterator):
        if not isinstance(item, tl):
            got = str_valtype(item)
            raise TypeError('Expected sequence of {}; '
                            'got sequence with {} at position {}'.format(
                            exp, got, i))
    
    if nodups:
        seen = []
        for i, item in enumerate(seq):
            if item in seen:
                raise TypeError('Duplicate element {} at position {}'.format(
                                repr(item), i))
            seen.append(item)


def check_spec(val, tl, mods):
    """Raise TypeError if val does not match the type specification
    given by tl and mods.
    """
    mods = normalize_mods(mods)
    if 'seq' in mods:
        nodups = 'nodups' in mods
        checktype_seq(val, tl, nodups=nodups)
    else:
        checktype(val, tl)
