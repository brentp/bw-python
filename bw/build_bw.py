import sys
import glob
import os.path as op
from cffi import FFI
import subprocess

HERE = op.dirname(op.abspath(op.dirname(__file__))) or "."

p = subprocess.Popen("curl-config --prefix", stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

prefix = p.stdout.read().strip()
err = p.stderr.read().strip()
if err:
    sys.stdout.write(err)

ffi = FFI()


#include "curl/curl.h"

sources = glob.glob("{path}/libBigWig/*.c".format(path=HERE))
#print sources
#include "{path}/bw/curl_constants.h"
#include "{path}/libBigWig/bwValues.h"
ffi.set_source("bw._bigwig", """
#include "{path}/libBigWig/bigWig.h"
#include <stdlib.h>
""".format(path=HERE),
               libraries=["c", "curl"],
               sources=sources,
               include_dirs=["/usr/local/include/", "%s/include/" % prefix])

ffi.cdef(open("{path}/bw/curl_constants.h".format(path=HERE)).read())
ffi.cdef("""
typedef void CURL;

typedef struct { ...; } bwRTree_t;
typedef struct { ...; } URL_t;
typedef struct { ...; } bwOverlapBlock_t;
typedef struct { ...; } bwRTreeNode_t;
typedef struct { ...; } bigWigFile_t;

typedef struct {
    uint32_t l; /**<Number of intervals held*/
    uint32_t m; /**<Maximum number of values/intervals the struct can hold*/
    uint32_t *start; /**<The start positions (o-based half open)*/
    uint32_t *end; /**<The end positions (0-based half open)*/
    float *value; /**<The value associated with each position*/
} bwOverlappingIntervals_t;


bigWigFile_t *bwOpen(char *fname, CURLcode (*callBack)(CURL*), const char* mode);
void bwClose(bigWigFile_t *fp);

bwOverlappingIntervals_t *bwGetValues(bigWigFile_t *fp, char *chrom, uint32_t start, uint32_t end, int includeNA);
void bwDestroyOverlappingIntervals(bwOverlappingIntervals_t *o);

enum bwStatsType {
    doesNotExist = -1,
    mean = 0,
    average = 0,
    std = 1,
    stdev = 1,
    dev = 1,
    max = 2,
    min = 3,
    cov = 4,
    coverage = 4,
};

double *bwStats(bigWigFile_t *fp, char *chrom, uint32_t start, uint32_t end, uint32_t nBins, enum bwStatsType type);


uint32_t bwGetTid(bigWigFile_t *fp, char *chrom);

void free(void *);

\n""")


if __name__ == "__main__":
    ffi.compile()
