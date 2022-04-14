from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }

def recipes(request, recipe_name):
    recipe = {}
    cnt = 1

    if recipe_name in DATA:
        if is_int(request.GET.get('servings', 1)) and int(request.GET.get('servings', 1)) > 1:
            cnt = int(request.GET.get('servings', 1))
        for ingredient, amount in DATA[recipe_name].items():
            recipe[ingredient] = cnt * amount

    context = {'recipe': recipe }

    return render(request, 'calculator/index.html', context)

def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
