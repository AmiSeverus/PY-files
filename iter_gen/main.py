class FlatIterator:

    def __init__(self, array):
        self.main_list = array

    def __iter__(self):
        self.main_list_cursor = 0  # курсор основного списка
        self.nested_list_cursor = -1  # курсор списка вложенного в основной список
        return self

    def __next__(self):
        self.nested_list_cursor += 1

        if len(self.main_list) == self.nested_list_cursor:
            self.main_list_cursor += 1
            self.nested_list_cursor = 0

        if self.main_list_cursor == len(self.main_list):
            raise StopIteration
        
        print(self.main_list[self.main_list_cursor][self.nested_list_cursor])
        return self.main_list[self.main_list_cursor][self.nested_list_cursor]

        # # увеличиваем nested_list_cursor

        # if ...:# если во вложенном списке элементы закончились,
        #     ...
        #     # то переходи на следующий список увеличив main_list_cursor
        #     # и обнуляем main_list_cursor

        # if ...:
        #     raise StopIteration

        # return self.main_list[self.main_list_cursor][self.nested_list_cursor]

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