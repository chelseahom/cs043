import os


class Simpledb:
    def __init__(self, datafile):
        self.datafile = datafile

    def __repr__(self):
        return ('<' + self.__class__.__name__ + ' datafile = ' + str(self.datafile) + '>')

    def insert(self, key, value):
        d = open(self.datafile, 'a')
        d.write(key + '\t' + value + '\n')
        d.close()

    def select_one(self, key):
        d = open(self.datafile, 'r')
        number = None
        for row in d:
            (k, v) = row.split('\t', 1)
            if k == key:
                number = v[:-1]
                break
        d.close()
        return number

    def delete(self, key):
        d = open(self.datafile, 'r')
        result = open('result.txt', 'w')
        for (row) in d:
            (k, v) = row.split('\t', 1)
            if k != key:
                result.write(row)
        d.close()
        result.close()
        os.replace('result.txt', self.datafile)

    def update(self, key, value):
        d = open(self.datafile, 'r')
        result = open('result.txt', 'w')
        for (row) in d:
            (k, v) = row.split('\t', 1)
            if k == key:
                result.write(key + '\t' + value + '\n')
            else:
                result.write(row)
        d.close()
        result.close()
        os.replace('result.txt', self.datafile)

