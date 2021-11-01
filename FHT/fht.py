from hashlib import md5
from collections import deque
import timeit


class fastHashTable:

    # @param {number} hashTableSize
    def __init__(self, m=100000):

        # Should probably be named HashTableEntry. You get the point.
        self.bucketSize = m
        self.buckets = [deque() for _ in range(self.bucketSize)]
        self.bloomFilter = [0 for _ in range(self.bucketSize)]

    def getMinIdx(self, key):
        hashVals = sorted([(self.bloomFilter[i], i) for i in self.hash(key)])
        return hashVals[0][1]

    # k = 4
    def hash(self, key):
        return set([int('0x'+md5(key.encode('utf-8')).hexdigest()[i:i+8], base=16)%self.bucketSize for i in range(0, 32, 8)])

    def insert(self, key):
        hashVals = self.hash(key)
        toInsert = {key}

        for idx in hashVals:
            self.bloomFilter[idx] += 1
            toInsert.update(self.buckets[idx])
            self.buckets[idx] = deque()

        for k in toInsert:
            idx = self.getMinIdx(k)
            self.buckets[idx].append(k)

    def delete(self, key):
        toInsert = set()
        hashVals = self.hash(key)
        for idx in hashVals:
            self.bloomFilter[idx] -= 1
            toInsert.update(self.buckets[idx])
            self.buckets[idx] = deque()

        toInsert.discard(key)
        for key in toInsert:
            idx = self.getMinIdx(key)
            self.buckets[idx].append(key)

    def search(self, key):
        hashVals = self.hash(key)
        for i in hashVals:
            if self.bloomFilter[i] == 0:
                return False
        idx = self.getMinIdx(key)
        for k in self.buckets[idx]:
            if k == key:
                return True

    def reportCollisions(self):
        chainLens = [i for i in map(len, self.buckets) if i != 0]
        return sum(chainLens) - len(chainLens)


with open('./data.txt', 'r') as f:
    raw = f.read()
testdata = raw.split('\n')[:-1]

for m in [1000000, 5000000, 10000000]:
    fht = fastHashTable(m)
    print(f"Fast Hash Table, with a bucket size = {fht.bucketSize}")
    start = timeit.default_timer()
    for k in testdata:
        fht.insert(k)
    stop = timeit.default_timer()
    print(f'Inserted {len(testdata)} items, Time: {stop - start}s')

    print(f"# of collisions: {fht.reportCollisions()}")

    start = timeit.default_timer()
    for k in testdata:
        assert fht.search(k)
    stop = timeit.default_timer()
    print(f'Searched {len(testdata)} items, Time: {stop - start}s')

    start = timeit.default_timer()
    for k in testdata:
        fht.delete(k)
    stop = timeit.default_timer()
    print(f'Deleted {len(testdata)} items, Time: {stop - start}s')
