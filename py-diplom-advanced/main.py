from random import randrange

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = input('Token: ')

# token = 'cce07f199ea32d10e6cd991f5e6291bcae8f4f1e82e95abf7442d14e3ddc8e08c7f2fbc34c21f37458973'

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
init_search = False


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.text == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif event.text == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")

def add_search_attr():
    init_search = True