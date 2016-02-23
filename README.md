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

# get an array.array() for large numbers of values.
# default is to return nan's for missing values
>>> b.values("1", 0, 9)
array('f', [0.10000000149011612, 0.20000000298023224, 0.30000001192092896, nan, nan, nan, nan, nan, nan])

# we can also get missing, but won't know the base it's associated with. 
>>> b.values("1", 0, 9, False)
array('f', [0.10000000149011612, 0.20000000298023224, 0.30000001192092896])


# stats are ("mean", "std", "max", "min", "coverage")
>>> b.stats("1", 0, 9, stat="mean")
0.2000000054637591

>>> b.stats("1", 0, 9, stat="std")
0.10000000521540645

>>> b.stats("1", 0, 4, stat="coverage")
0.75
>>> b.stats("1", 0, 4, stat="coverage", nBins=2)
array('d', [1.0, 0.5])

# get the chromosomes and lengths as a list of tuples:
>>> b.chroms
[('1', 195471971), ('10', 130694993)]

>>> b.close()
```

An array.array can be turned into a numpy array with `np.frombuffer(a, dtype='f')`
