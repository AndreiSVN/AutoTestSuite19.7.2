import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    def get_api_key(self, email: str, password: str):
        """Метод получает делает запрос и получает результат в формате json с подтверждением
        авторизаци на сайте PetFriends с указанными емейлом и паролем"""

        header = {'email': email,
                  'password': password
                  }
        resp = requests.get(self.base_url + '/api/key', headers=header)
        status = resp.status_code
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        print(result)
        return status, result

    def get_list_pets(self, auth_key: json, filter: str = ''):
        """Метод делает запрос и получает ответ в формате json со списком всех питомцев
        зарегистрированных на сайте PetFriends. С помощью фильтра my_pets можно получить список питомцев,
        внесенных пользователем"""

        header = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        resp = requests.get(self.base_url + '/api/pets', headers=header, params=filter)
        status = resp.status_code
        result = resp.json()
        return status, result

    def post_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str):
        """Метод предназначен для добавления нового питомца на сайт PetFriends с помощью запроса POST,
        переданного в формате JSON и multipart-данных"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        header = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        resp = requests.post(self.base_url + '/api/pets', headers=header, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        print(result)
        return status, result

    def negative_addition_new_pet(self, auth_key: json, animal_type: str, age: str, pet_photo: str):
        """Метод предназначен для добавления нового питомца на сайт PetFriends с помощью запроса POST,
        переданного в формате JSON и multipart-данных"""

        data = MultipartEncoder(
            fields={
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        header = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        resp = requests.post(self.base_url + '/api/pets', headers=header, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str):
        """Метод предназначен для удаления питомца с сайта PetFriends, посылая запрос DELETE в формате JSON"""

        header = {'auth_key': auth_key['key']}
        resp = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=header)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        print(result)
        return status, result

    def update_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str):
        """Метод предназначен для обновления информации о питомце с помощью запроса PUT в формате JSON"""
        data = {'name': name,
                'animal_type': animal_type,
                'age': age
                }
        header = {'auth_key': auth_key['key']}
        resp = requests.put(self.base_url + '/api/pets/' + pet_id, headers=header, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        return status, result

    def create_new_pet(self, auth_key: json, name: str, animal_type: str, age: str):
        """Метод предназначен для создания нового питомца на сайте PetFriends с помощью запроса POST,
        переданного в формате JSON"""

        data = {'name': name,
                'animal_type': animal_type,
                'age': age,
                }
        header = {'auth_key': auth_key['key']}
        resp = requests.post(self.base_url + '/api/create_pet_simple', headers=header, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        print(result)
        return status, result

    def set_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str):
        """Метод предназначен для создания нового питомца на сайте PetFriends с помощью запроса POST,
        переданного в формате JSON"""

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                    })
        header = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        resp = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=header, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        print(result)
        return status, result
