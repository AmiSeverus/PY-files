# Задача 1

with open('recipes.txt') as file:
    cook_book = {}
    for dish in file:
        dish_name = dish.strip()
        counter = int(file.readline().strip())
        products = []
        for item in range(counter):
            ingredient_name, quantity, measure = file.readline().strip().split(' | ')
            product = {'ingredient_name':ingredient_name, 'quantity': int(quantity), 'measure':measure }
            products.append(product)
        cook_book[dish_name] = products
        file.readline()
print(cook_book)

# Задача 2

def get_shop_list_by_dishes(dishes, person_count):
    if person_count > 0:
        shop_list_by_dishes = {}
        for dish in dishes:
            if dish in cook_book:
                products = cook_book[dish]
                for product in products:
                    if product['ingredient_name'] in shop_list_by_dishes:
                        shop_list_by_dishes[product['ingredient_name']]['quantity'] += product['quantity'] * person_count
                    else:    
                        shop_list_by_dishes[product['ingredient_name']] = {'measure':product['measure'], 'quantity':product['quantity']*person_count}
            else:
                return(f'Нет такого блюда, как {dish}, в повареной книге')
        return shop_list_by_dishes
    else:
        return('Некоректное кол-во гостей')

print(get_shop_list_by_dishes(['Fahitos', 'Omlette'], 2))

# Задача 3

file_list = ['1.txt', '2.txt', '3.txt']

file_list_with_length = []
for file_name in file_list:
    with open(file_name) as file:
        file_lines = file.readlines()
        file_length = len(file_lines)
        file_list_with_length.append((file_name, file_length))

file_list_with_length_sorted = sorted(file_list_with_length, key=lambda file_list_with_length: file_list_with_length[1])

for file_fin in file_list_with_length_sorted:
    with open('result.txt', 'a', encoding='utf-8') as result:
        result.write(f'{file_fin[0]}\n{file_fin[1]}\n')
        with open(file_fin[0]) as file_st:
            for item in range(file_fin[1]):
                result.write(file_st.read())
            result.write('\n')