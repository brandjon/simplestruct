"""Useful, small utilities. Some of these are not used within
simplestruct, but by other projects that depend on simplestruct.
"""


__all__ = [
    'trim',
    'frozendict',
    'make_frozen',
]


from collections import Mapping
from functools import reduce


def trim(text):
    """Like textwrap.dedent, but also eliminate leading and trailing
    lines if they are whitespace or empty.
    
    This is useful for writing code as triple-quoted multi-line
    strings.
    """
    from textwrap import dedent
    
    lines = text.split('\n')
    if len(lines) > 0:
        if len(lines[0]) == 0 or lines[0].isspace():
            lines = lines[1 : ]
    if len(lines) > 0:
        if len(lines[-1]) == 0 or lines[-1].isspace():
            lines = lines[ : -1]
    
    return dedent('\n'.join(lines))


# Inspired by a Stack Overflow answer by Mike Graham.
# http://stackoverflow.com/questions/2703599/what-would-be-a-frozen-dict

class frozendict(Mapping):
    
    """Analogous to frozenset."""
    
    def __init__(self, *args, **kargs):
        self.d = dict(*args, **kargs)
        self.hash = reduce(lambda a, b: a ^ hash(b), self.items(), 0)
    
    def __iter__(self):
        return iter(self.d)
    
    def __len__(self):
        return len(self.d)
    
    def __getitem__(self, key):
        return self.d[key]
    
    def __hash__(self):
        return self.hash


def make_frozen(v):
    """Normalize mutable dicts to frozendicts and lists to tuples,
    recursively.
    """
    if isinstance(v, (dict, frozendict)):
        return frozendict({make_frozen(k): make_frozen(v)
                           for k, v in v.items()})
    elif isinstance(v, (list, tuple)):
        return tuple(make_frozen(e) for e in v)
    else:
        return v
