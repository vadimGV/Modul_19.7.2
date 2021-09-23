from api import PetFriends

from settings import valid_email, valid_password, nonvalid_email, nonvalid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверка запрос api_key возвращает статус 200 в результате есть слово key"""
    status, result = pf.get_api_key(email, password)
    # Отправляем запрос и сохраняем полученный ответ код статуса в status, текст ответа в result
    assert status == 200
    # Ожидаем появление стауса 200
    assert 'key' in result
    # Ожидаем появление ключевого слова key в тексте ответа

def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем,что запрос списка питомцев возвращает не пустой лист
    Вначале получаем api_key, сохраняем его в переменную auth_key, далее
    используя этот ключ, запрашиваем список питомцев """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем api_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    # Ожидаем появление стауса 200
    assert len(result['pets']) > 0
    # Ожидаем, что список питомцев не пустой

def test_add_new_pet_with_valid_data(name='Аська', animal_type='такса', age='15', pet_photo='images/aska1.jpg'):
    """Проверяем возможность добавления нового питомца с корректными данными"""

    # Получаем полный путь фото питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем api_key и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert  result['name'] == name

def test_successful_delete_self_pet():
    """Проверка возможности удаления своего питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, если список питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Аська', 'такса', '15', 'images/aska1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берем ID первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Запрашиваем еще раз список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем, что статус равен 200 и в списке нет ID удаленного питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Асюта', animal_type='Собакен', age='98'):
    """Проверяем возможность изменения данных своего питомца"""

    # Получаем ключ авторизации и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, пробуем обновить данные
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем, что статус ответа равен 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # Если список пустой, то выдаем исключение об отстутствии питомцев
        raise Exception('Нет моих питомцев')

def test_get_api_key_for_nonvalid_user(email=nonvalid_email, password=nonvalid_password):
    """Проверяем возможность получения api_key постороннему пользователю,
    не зарегестрированному в приложении Pet Friends"""
    status, result = pf.get_api_key(email, password)

    # Отправляем запрос и сохраняем полученный ответ код статуса в status, текст ответа в result
    # Ожидаем, что статус ответа не будет равен 200, печатаем статус ответа
    assert status != 200
    print(status)
    # Ожидаем, что  ключевого слова key нет в тексте ответа
    assert 'key' not in result

def test_add_new_pet_with_nonvalid_data(name='Аська2', animal_type='такса', age='15', pet_photo='images/aska2.jpg'):
    """Проверяем возможность добавления нового питомца с некорректными данными"""

    # Получаем полный путь фото питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем api_key и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(nonvalid_email, nonvalid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert  result['name'] == name

def test_add_new_pet_without_name(name='', animal_type='такса', age='96', pet_photo='images/taksa.jpg'):
    """Проверяем возможность добавления нового питомца с некорректными данными"""

    # Получаем полный путь фото питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем api_key и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert  result['name'] == name

def test_add_new_pet_without_age_name(name='', animal_type='такса', age='', pet_photo='images/aska2.jpg'):
    """Проверяем возможность добавления нового питомца с некорректными данными"""

    # Получаем полный путь фото питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем api_key и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert  result['name'] == name

def test_add_new_pet_only_photo(name='', animal_type='', age='', pet_photo='images/cat.jpg'):
    """Проверяем возможность добавления нового питомца с некорректными данными"""

    # Получаем полный путь фото питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем api_key и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert  result['name'] == name





