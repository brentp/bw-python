from ._bigwig import lib, ffi
from collections import namedtuple
import array

Interval = namedtuple('Interval', ['chrom', 'start', 'end', 'value'])


class BigWig(object):
    """
    >>> b = BigWig("libBigWig/test/test.bw")
    >>> b
    BigWig('libBigWig/test/test.bw')
    >>> for interval in b("1", 0, 99):
    ...     interval
    Interval(chrom='1', start=0, end=1, value=0.10000000149011612)
    Interval(chrom='1', start=1, end=2, value=0.20000000298023224)
    Interval(chrom='1', start=2, end=3, value=0.30000001192092896)

    >>> b.values("1", 0, 9, False)
    array('f', [0.10000000149011612, 0.20000000298023224, 0.30000001192092896])
    >>> b.values("1", 0, 9, True)
    array('f', [0.10000000149011612, 0.20000000298023224, 0.30000001192092896, nan, nan, nan, nan, nan, nan])

    >>> b.close()
    """

    def __init__(self, path):
        self.bw = lib.bwOpen(path, ffi.NULL)
        self.path = path

    def close(self):
        return lib.bwClose(self.bw)

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self.path)

    def __call__(self, chrom, start, end, includeNA=False):
        intervals = lib.bwGetValues(self.bw, chrom, start, end, int(includeNA))
        for i in range(intervals.l):
            yield Interval(chrom, intervals.start[i], intervals.start[i] + 1, intervals.value[i])
        lib.bwDestroyOverlappingIntervals(intervals)

    def values(self, chrom, start, end, includeNA=False):
        intervals = lib.bwGetValues(self.bw, chrom, start, end, int(includeNA))
        a = array.array('f')
        if intervals.l != 0:
            a.fromstring(ffi.buffer(intervals.value[0:intervals.l]))
        lib.bwDestroyOverlappingIntervals(intervals)
        return a

if __name__ == "__main__":
    import doctest
    import sys
    sys.stderr.write(str(doctest.testmod()) + "\n")
