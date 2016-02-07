from bw import BigWig
from bw.bw import Interval
from array import array
from math import isnan

nan = float('nan')

def arr_equal(aa, bb):
    for i, a in enumerate(aa):
        if isnan(a):
            assert isnan(bb[i])
        else:
            assert a == bb[i]

def test_bw():
    b = BigWig("libBigWig/test/test.bw")

    assert repr(b) == "BigWig('libBigWig/test/test.bw')"


    intervals = list(b("1", 0, 99))

    assert intervals[0] == Interval(chrom='1', start=0, end=1, value=0.10000000149011612)
    assert intervals[1] == Interval(chrom='1', start=1, end=2, value=0.20000000298023224)
    assert intervals[2] == Interval(chrom='1', start=2, end=3, value=0.30000001192092896)

    # default is to include all values
    vals = b.values("1", 0, 9)
    exp = array('f', [0.10000000149011612, 0.20000000298023224, 0.30000001192092896, nan, nan, nan, nan, nan, nan])
    arr_equal(vals, exp)

    vals = b.values("1", 0, 9, False)
    exp = array('f', [0.10000000149011612, 0.20000000298023224, 0.30000001192092896])
    arr_equal(vals, exp)

    v = b.stats("1", 0, 9)
    assert v == 0.2000000054637591

    v = b.stats("1", 0, 9, stat="std")
    assert v == 0.10000000521540645

    v = b.stats("1", 0, 4, stat="coverage")
    assert v == 0.75

    v = b.stats("1", 0, 4, stat="coverage", nBins=2)
    assert v == array('d', [1.0, 0.5])


    b.close()

def test_bad_chr():
    b = BigWig("libBigWig/test/test.bw")
    assert b.stats("chr1", 0, 10) is None
    v = b.values("chr1", 0, 10)
    assert len(v) == 0, v
