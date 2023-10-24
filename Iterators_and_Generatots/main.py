from Iterator import FlatIterator
from generator import flat_generaotor
nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
]

if __name__ == '__main__':
        for item in FlatIterator(nested_list):
                print(item)
        flat_list = [item for item in FlatIterator(nested_list)]
        print(flat_list)

        generator_list = [item for item in flat_generaotor(nested_list)]
        print(generator_list)