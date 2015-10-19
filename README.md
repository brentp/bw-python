python wrapper to [Devon Ryan's bigwig library](https://github.com/dpryan79/libBigWig) using cffi

```Python
>>> from bw import BigWig
>>> b = BigWig("libBigWig/test/test.bw")
>>> b
BigWig('libBigWig/test/test.bw')
>>> for interval in b("1", 0, 99):
...     interval
Interval(chrom='1', start=0, end=1, value=0.10000000149011612)
Interval(chrom='1', start=1, end=2, value=0.20000000298023224)
Interval(chrom='1', start=2, end=3, value=0.30000001192092896)

>>> b.close()
```
