from ._bigwig import lib, ffi
from collections import namedtuple

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

"""
typedef struct {
    uint32_t l; /**<Number of intervals held*/
    uint32_t m; /**<Maximum number of values/intervals the struct can hold*/
    uint32_t *start; /**<The start positions (o-based half open)*/
    uint32_t *end; /**<The end positions (0-based half open)*/
    float *value; /**<The value associated with each position*/
} bwOverlappingIntervals_t;

  void printIntervals(bwOverlappingIntervals_t *ints, uint32_t start) {
      uint32_t i;
      if(!ints) return;
      for(i=0; i<ints->l; i++) {
          if(ints->start && ints->end) {
              printf("Interval %"PRIu32"\t%"PRIu32"-%"PRIu32": %f\n",i, ints->start[i], ints->end[i], ints->value[i]);
          } else if(ints->start) {
              printf("Interval %"PRIu32"\t%"PRIu32"-%"PRIu32": %f\n",i, ints->start[i], ints->start[i]+1, ints->value[i]);
          } else {
              printf("Interval %"PRIu32"\t%"PRIu32"-%"PRIu32": %f\n",i, start+i, start+i+1, ints->value[i]);
          }
      }
  }


"""

if __name__ == "__main__":
    import doctest
    import sys
    sys.stderr.write(str(doctest.testmod()) + "\n")
