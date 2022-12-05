import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os
from faker import Faker
import random

pf = PetFriends()
fake = Faker()
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)
def test_get_all_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name=fake.first_name(), animal_type='korgi',
                                     age=str(random.randint(1, 20)), pet_photo='images/korgi-sobaka.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, fake.first_name(), "кот", "3", "images/Cat_deadline.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name=fake.first_name(), animal_type='Кот', age=7):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_create_pet_simple(name=fake.first_name(), animal_type='енот',
                                     age=str(random.randint(1, 20))):
    """Проверяем, что можно успешно добавить питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_successful_add_photo_of_my_pet(pet_photo="images/raccoon2.jpeg"):
    """Проверяем, что можно обновить инфо о питомце и успешно добавить фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, fake.first_name(), "лиса", "2", "fox.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] is not None











