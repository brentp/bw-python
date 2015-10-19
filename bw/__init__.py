from .bw import BigWig

__version__ = "0.0.1"

def doctests():
    from . import bw
    import doctest
    doctest.testmode(m=bw)
