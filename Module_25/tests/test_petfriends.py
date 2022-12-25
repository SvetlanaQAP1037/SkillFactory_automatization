import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#pytest -v --driver Chrome --driver-path //chromedriver.exe test_petfriends.py

def test_show_all_pets(testing):
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

def test_all_my_pets_are_on_the_page(testing):
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    # явные ожидания элементов страницы
    WebDriverWait(pytest.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[class=".col-sm-8 right fill"]')))
    quantity_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    count_pets = pytest.driver.find_element(By.CSS_SELECTOR, 'div[class=".col-sm-4 left"]').text

    assert "Питомцев: " + str(len(quantity_pets)) == count_pets.split('\n')[1]

def test_half_of_the_my_pets_have_photos(testing):
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    # неявные ожидания элемента фото
    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets > table > tbody > tr > th > img')
    quantity_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')

    assert int(len(quantity_pets)) // 2 <= int(len(images))

def test_all_my_pets_have_name_age_breed(testing):
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()

    # неявные ожидания элемента name
    pytest.driver.implicitly_wait(10)
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')

    # неявные ожидания элемента age
    pytest.driver.implicitly_wait(10)
    age = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[3]')

    # неявные ожидания элемента breed
    pytest.driver.implicitly_wait(10)
    breed = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[2]')

    for i in range(len(names)):
        assert names[i].text != ''
        assert age[i] != ''
        assert breed[i].text != ''

def test_all_my_pets_have_different_names(testing):
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
    list_names = []
    for i in range(len(names)):
        list_names.append(names[i].text)
    unique_names = list(set(list_names))

    assert unique_names.sort() == list_names.sort()

def test_no_duplicate_pets_in_the_list(testing):
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[1]')
    breed = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[2]')
    age = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr/td[3]')
    description_pet = []
    for i in range(len(names)):
        description_pet.append(names[i].text + '_' + (breed[i].text) + '_' + (age[i].text))
    unique_pets = list(set(description_pet))

    assert unique_pets.sort() == description_pet.sort()