import os
from api import PetFriends
from settings import email, password


pet_friends = PetFriends()


def test_get_api_wrong_password(email=email, password='Aaaa'):
    """Проверка получения ключа API при условии, что введен неправильный пароль"""
    status, result = pet_friends.get_api_key(email, password)
    assert status == 403


def test_get_api_empty_email_password(email='qwerty@mail.ru', password=password):
    """Проверка получения ключа API при условии, что введен неправильный адрес электронной почты"""
    status, result = pet_friends.get_api_key(email, password)
    assert status == 403


def test_get_list(filter='my_pets'):
    """Проверка получения списка питомцев"""
    _, auth_key = pet_friends.get_api_key(email, password)
    status, result = pet_friends.get_list_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) == 7
    print(result['pets'])


def test_negative_addition_new_pet(animal_type='крокодил', age='15', pet_photo='images/huski1.jpg'):
    """Проверка возможности добавить нового питомца без имени"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pet_friends.get_api_key(email, password)
    status, result = pet_friends.negative_addition_new_pet(auth_key, animal_type, age, pet_photo)
    assert status == 400


def test_delete_pet():
    """Негативная проверка удаления чужого питомца по его id. Результат - успешный -> присутствует баг сервера (баг-репорт)"""
    _, auth_key = pet_friends.get_api_key(email, password)
    _, pets = pet_friends.get_list_pets(auth_key)
    pet_id = pets['pets'][0]['id']
    status, _ = pet_friends.delete_pet(auth_key, pet_id)
    _, pets = pet_friends.get_list_pets(auth_key)
    print(len(pets['pets']))
    assert status is 200
    assert pet_id not in pets.values()


def test_create_new_pet_age(name='Васька', animal_type='элитный двоворовой кот', age='старый'):
    """Негативная проверка добавления нового питомца с возрастом не в формате цифры. Результат - успешный -> присутствует
    баг сервера (баг-репорт)"""
    _, auth_key = pet_friends.get_api_key(email, password)
    status, result = pet_friends.create_new_pet(auth_key, name, animal_type, age)
    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    assert status == 200
    assert result['name'] == name


def test_create_new_pet_long_name(name='Именамогутидентифицироватьклассиликатегориювещей,илиопределённую вещь'
                                  'либоуникально,либовнекоторомзаданномконтексте.Именаиспользуютсятакжев'
                                  'такихобластяхдеятельности,какпрограммирование(именапеременных,'
                                  'пространстваимён)', animal_type='элитный двоворовой кот', age='5'):
    """Негативная проверка добавления нового питомца с именем длинной несколько строк. Результат - успешный -> присутствует
    баг сервера (баг-репорт)"""
    _, auth_key = pet_friends.get_api_key(email, password)
    status, result = pet_friends.create_new_pet(auth_key, name, animal_type, age)
    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    assert status == 200
    assert result['name'] == name


def test_update_info(name='Мурзилка', animal_type='wild python', age='22'):
    """Проверка обновления информации о питомце по его id"""
    _, auth_key = pet_friends.get_api_key(email, password)
    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][-1]['id']
    if len(my_pets['pets']) > 0:
        status, result = pet_friends.update_info(auth_key, pet_id, name, animal_type, age)
    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    assert status == 200
    assert result['name'] == name


def test_create_new_pet(name='', animal_type='', age=''):
    """Негативная проверка простого создания нового питомца c пустыми полями. Результат - успешный -> присутствует
    баг сервера (баг-репорт)"""
    _, auth_key = pet_friends.get_api_key(email, password)
    status, result = pet_friends.create_new_pet(auth_key, name, animal_type, age)
    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    assert status == 200
    assert result['name'] == name


def test_set_photo_pet(pet_photo='images/huski1.jpg'):
    """Проверка добавления фотографии к данным существующего питомца"""
    _, auth_key = pet_friends.get_api_key(email, password)
    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pet_friends.set_photo_pet(auth_key, pet_id, pet_photo)
    _, my_pets = pet_friends.get_list_pets(auth_key)
    assert status == 200
    assert result['pet_photo'] is not None
