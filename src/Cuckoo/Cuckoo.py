maxelemconst = 2
maxrecconst = 16
numhashconst = 2

class Cuckoo:
    def __init__(self):
        self.size = 0
        self.capacity = maxelemconst
        self.maxrec = maxrecconst
        self.times_expanded = 0

    def __str__(self):
        return "( Capacity : " + str(self.capacity) + ", Number of expansions : " + str(self.times_expanded) + ", Average Load factor : " + (self.total_load_factor_percentage // self.times_expanded) + ")"

