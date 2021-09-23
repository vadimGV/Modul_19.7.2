import json

import requests

from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    """API библиотека к web-приложению Pet Friends"""
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self, email, password) -> json:
        """Метод делает запрос к API сервера и возвращает
            статус запроса в формате JSON с уникальным ключом
             пользователя, найденного по указанным email и паролем"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key:json, filter: str='') -> json:
        """Метод делает запрос к API и возвращает статус запроса и результат
        со списком найденных питомцев, совпадающих с фильтром."""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key:json, name:str, animal_type:str, age:str, pet_photo:str) -> json:
        """Метод отправляет на сервер данные о новом питомце и возвращает
        статус и результат в формате JSON с данными нового питомца"""
        data = MultipartEncoder(
            fields={
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key':auth_key['key'], 'Content-type':data.content_type}

        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key:json, pet_id:str) -> json:
        """Метод отправляет запрос на сервер на удаление питомца
        по указанному ID и возвращает статус запроса и результат
        в формате JSON с текстом уведомления об успешном удалении"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key:json, pet_id:str, name:str, animal_type:str, age:int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных
        питомца по указанному ID и возвращает статус запроса и
        результат в формате JSON с обновленными данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result












