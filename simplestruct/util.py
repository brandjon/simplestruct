"""Useful, small utilities. Some of these are not used within
simplestruct, but by other projects that depend on simplestruct.
"""


__all__ = [
    'trim',
]


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
