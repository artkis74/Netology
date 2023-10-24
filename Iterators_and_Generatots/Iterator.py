from itertools import chain


class FlatIterator:

    def __init__(self, list):
        self.list = list


    def __iter__(self):
        self.list = list(chain.from_iterable(self.list))
        self.cursor = len(self.list)
        self.index = -1
        return self

    def __next__(self):
        if self.cursor == 0:
            raise StopIteration
        self.cursor -= 1
        self.index += 1
        return self.list[self.index]


