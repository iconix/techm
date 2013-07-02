# modified from:
# http://data-matters.blogspot.com/2009/05/prefixspan-source-code-in-python.html


class PrefixSpan:
    def __init__(self, db=[]):
        self.db = db
        self.generate_sequence_db()

    def generate_sequence_db(self):
        self.db2sdb = {}
        self.sdb2db = []
        count = 0
        self.sdb = []
        for seq in self.db:
            newseq = []
            for item in seq:
                if item in self.db2sdb:
                    pass
                else:
                    self.db2sdb[item] = count
                    self.sdb2db.append(item)
                    count += 1
                newseq.append(self.db2sdb[item])
            self.sdb.append(newseq)
        self.item_count = count

    def run(self, min_sup=2):
        '''
        mine patterns with min_sup as the min support threshold
        '''
        self.min_sup = min_sup
        L1_patterns = self.gen_L1_patterns()
        patterns = self.gen_patterns(L1_patterns)
        self.sdbpatterns = L1_patterns + patterns

    def get_patterns(self):
        '''
        returns the set of the patterns, which is a list of
        tuples (sequence, support)
        '''
        ori_patterns = []
        for (pattern, sup, projection_db) in self.sdbpatterns:
            ori_pattern = []
            for item in pattern:
                ori_pattern.append(self.sdb2db[item])
            ori_patterns.append((ori_pattern, sup))
        return ori_patterns

    def gen_L1_patterns(self):
        '''
        generate length-1 patterns
        '''
        pattern = []
        sup = len(self.sdb)
        projection_db = [(i, 0) for i in range(len(self.sdb))]
        L1_prefixes = self.span((pattern, sup, projection_db))
        return L1_prefixes

    def gen_patterns(self, prefixes):
        '''
        generate length-(l+1) patterns from
        length-1 patterns
        '''
        results = []
        for prefix in prefixes:
            result = self.span(prefix)
            results += result
        if results != []:
            results += self.gen_patterns(results)
        return results

    def span(self, prefix):
        '''
        span current length-l prefix pattern set
        to length-(l+1) prefix pattern set.
        prefix is a tuple (pattern, sup, projection_db):
        pattern is a list representation of the pattern,
        sup is the absolute support of the pattern,
        projection_db is the projection database of the pattern,
        which is a list of tuples in teh form of (sid, pos).
        '''
        (pattern, sub, projection_db) = prefix
        item_sups = [0] * self.item_count
        for (sid, pid) in projection_db:
            item_appear = [0] * self.item_count
            for item in self.sdb[sid][pid:]:
                item_appear[item] = 1
            item_sups = map(lambda x, y: x + y, item_sups, item_appear)
        prefixes = []
        for i in range(len(item_sups)):
            if item_sups[i] >= self.min_sup:
                new_pattern = pattern + [i]
                new_sup = item_sups[i]
                new_projection_db = []
                for (sid, pid) in projection_db:
                    for j in range(pid, len(self.sdb[sid])):
                        item = self.sdb[sid][j]
                        if item == i:
                            new_projection_db.append((sid, j+1))
                            break
                prefixes.append((new_pattern, new_sup, new_projection_db))
                if (len(pattern) > 0):  # prevent counting sequences with gaps as patterns
                    break
        return prefixes
