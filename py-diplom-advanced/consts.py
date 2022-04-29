from types import MappingProxyType


error_messages = MappingProxyType(
    {
        '200': "Поиск завершен",
        '206': "Не хватает всех данных для поиска пары",
        '400': "Ответ не понятен",
        '404_user': "Такой пользователь не найден",
        '404_pair': "По заданным пораметрам поиска ничего не найдено",
        '500': "Что-то пошло не так, поиск прерван",
    }
)


sex_attr = tuple(['0 - любой', '1 - женщина', '2 - мужчина'])


status_attr = tuple([
    '0 - любой',
    '1 - не женат (не замужем)',
    '2 - встречается',
    '3 - помолвлен(-а)',
    '4 - женат (замужем)',
    '5 — всё сложно',
    '6 — в активном поиске',
    '7 — влюблен(-а)',
    '8 — в гражданском браке'
])


attr_translation = MappingProxyType(
    {
        'sex': "пол",
        'age': "возраст",
        'hometown': "город",
        'status': "семейное положение"
    }
)
