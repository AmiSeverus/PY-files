class FlatIterator:

    def __init__(self, array):
        self.result = []
        self.array = array
        self.start = - 1
        self.end = len(array)

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start == self.end:
            raise StopIteration
        for elem in self.array[self.start]:
            print(elem)
            self.result.append(elem)
        return(self.result)

nested_list = [
	['a', 'b', 'c'],
	['d', 'e', 'f', 'h', False],
	[1, 2, None],
]

flat_list = [item for item in FlatIterator(nested_list)]

print(flat_list)

def flat_generator(nested_list):
        start = 0
        end = len(nested_list)

        while start < end:
            array = nested_list[start]
            for elem in array:
                yield elem
            start += 1


nested_list = [
	['a', 'b', 'c'],
	['d', 'e', 'f'],
	[1, 2, None],
]

for item in flat_generator(nested_list):
	print(item)