from hashlib import md5
import timeit

N_SIZE=32
MAX_SEARCH=250


class ElementHandler:
    def __init__(self, key):
        self.key = key
        # self.value = value
        self.hashed_index = None


    def set_hashed_index(self, index):
        self.hashed_index = index


class HopschotchMap:
    def __init__(self, capacity):
        self.size = 0
        self.capacity = capacity
        self.elements = {}
        self.collisions = 0

    def hash(self, key):
        return int('0x'+md5(key.encode('utf-8')).hexdigest()[8:8+8], base=16)%self.capacity

    def num_collisions(self):
        return self.collisions

    def set_value(self, key):
        if self.size == self.capacity:
            return False
        element  = ElementHandler(key)
        index = self.hash(key)
        element.set_hashed_index(index)
        if index not in self.elements.keys():
            self.elements[index] = element
            self.size += 1
            return True
        limit = index + MAX_SEARCH
        capacity = self.capacity
        hashed_index = index
        while index < limit and index < capacity:
            if index not in self.elements.keys():
                break
            else:
                array_element = self.elements[index]
                if array_element.key == element.key:
                    # array_element.value = value
                    self.elements[index] = array_element
                    return True

            index += 1

        if index == capacity or index == limit:
            return False

        if index - hashed_index < N_SIZE:
            self.elements[index] = element
            self.size += 1
            return True

        current_index = 0
        poss_index = 0
        nh = N_SIZE - 1
        success = False
        self.elements[index] = 0
        temp = index

        while index - hashed_index > nh and index < capacity:
            poss_index = index - nh
            current_index = poss_index
            while current_index < index:
                current_element = self.elements[current_index]
                if current_element.hashed_index >= poss_index:
                    self.elements[index] = self.elements[current_index]
                    self.elements[current_index] = element
                    if current_index - hashed_index < N_SIZE:
                        success = True
                        self.size += 1
                    break
                current_index += 1 
            if current_index == index:
                break
            index = current_index

        if temp == index:
            self.elements.pop(temp, None)

        if not success and current_index != temp:
            self.elements.pop(current_index, None)
        if success != True:
            self.collisions += 1
        return success

    
    def get(self, key):
        index = self.hash(key)
        if index in self.elements:
            return self.elements[index].key
        return None 


    def delete(self, key):
        index = self.hash(key)
        if index in self.elements:
            self.elements.pop(index, None)
            return True

        return False

    

with open('../Dataset/data.txt', 'r', encoding='utf-8') as f:
    raw = f.read()
testdata = raw.split('\n')[:-1]

for m in [1000000, 5000000, 10000000]:
    hop_s = HopschotchMap(m)
    print("Hopscotch hashing with table size {}".format(m))
    start = timeit.default_timer()
    for value in testdata:
        hop_s.set_value(str(value))
    stop = timeit.default_timer()
    print("Inserted {} items, time: {}s".format(len(testdata), stop-start))

    print("# of collisions: {}".format(hop_s.num_collisions()))

    start = timeit.default_timer()
    for value in testdata:
        hop_s.delete(value)
    stop = timeit.default_timer()
    print("Searched {} items, time: {}s".format(len(testdata), stop-start))

    start = timeit.default_timer()
    for value in testdata:
        hop_s.get(value)
    stop = timeit.default_timer()
    print("Deleted {} items, time: {}s".format(len(testdata), stop-start))