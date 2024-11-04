import pytest
import requests

@pytest.fixture
def api_url():
    return 'http://127.0.0.1:17678/api'

def test_state(api_url):
    response = requests.get(f"{api_url}/state")
    assert response.status_code == 200
    data = response.json()
    assert data.get("state") == "OК"  # Сервер возвращает "OК"

@pytest.mark.parametrize("x, y, expected_result", [
    (42, 24, 66),
    (1, 1, 2),
    (0, 0, 0),
    (42, -24, 18),
    (1, -1, 0),
    (0, 0, 0)
])
def test_addition(api_url, x, y, expected_result):
    response = requests.post(f"{api_url}/addition", json={"x": x, "y": y})
    assert response.status_code == 200
    data = response.json()
    assert data.get("statusCode") == 0
    assert data.get("result") == expected_result

@pytest.mark.parametrize("x, y, expected_result", [
    (42, 24, 1008),
    (1, 1, 1),
    (0, 1, 0),
    (42, -24, -1008),
    (1, -1, -1),
    (0, -1, 0)
])
def test_multiplication(api_url, x, y, expected_result):
    response = requests.post(f"{api_url}/multiplication", json={"x": x, "y": y})
    assert response.status_code == 200
    data = response.json()
    assert data.get("statusCode") == 0
    assert data.get("result") == expected_result

@pytest.mark.parametrize("x, y, expected_result", [
    (42, 24, 1),
    (1, 1, 1),
    (42, 0, None),  # Обработать случай деления на ноль
    (42, -24, -2),
    (1, -1, -1),
    (-42, 0, None)  # Обработать случай деления на ноль
])
def test_division(api_url, x, y, expected_result):
    response = requests.post(f"{api_url}/division", json={"x": x, "y": y})
    print('NEVEROV_POPAL_1:', response.json(), x, y, expected_result)
    data = response.json()
    assert response.status_code == 200
    if y == 0:
        assert data.get("statusCode") == 8  # Неправильный формат тела запроса (деление на ноль)
        assert data.get("statusMessage") == 'Ошибка вычисления'
    else:
        assert data.get("statusCode") == 0
        assert data.get("result") == expected_result

@pytest.mark.parametrize("x, y, expected_result", [
    (42, 24, 18),
    (1, 1, 0),
    (42, 0, None),  # Обработать случай деления на ноль
    (42, -24, -6),
    (1, -1, 0),
    (-42, 0, None)  # Обработать случай деления на ноль
])
def test_remainder(api_url, x, y, expected_result):
    response = requests.post(f"{api_url}/remainder", json={"x": x, "y": y})
    print('NEVEROV_POPAL_2:', response.json(), x, y, expected_result)
    assert response.status_code == 200
    data = response.json()
    if y == 0:
        assert data.get("statusCode") == 8  # Неправильный формат тела запроса (деление на ноль)
        assert data.get("statusMessage") == 'Ошибка вычисления'
    else:
        assert data.get("statusCode") == 0
        assert data.get("result") == expected_result

@pytest.mark.parametrize("json_data, expected_error_code", [
    ({"x": 1, "y": 1, "extra": 1}, 0),  # Лишние ключи
    ({"x": 1}, 2),  # Не хватает ключей в теле запроса
    ({"x": "string", "y": 1}, 3),  # Одно из значений не является целым числом
    ({"x": 10000000000000000, "y": 1}, 4)  # Превышен размер одного из значений
])
def test_invalid_requests(api_url, json_data, expected_error_code):
    response = requests.post(f"{api_url}/addition", json=json_data)
    assert response.status_code == 200
    data = response.json()
    assert data.get("statusCode") == expected_error_code

    response = requests.post(f"{api_url}/multiplication", json=json_data)
    assert response.status_code == 200
    data = response.json()
    assert data.get("statusCode") == expected_error_code

    response = requests.post(f"{api_url}/division", json=json_data)
    assert response.status_code == 200
    data = response.json()
    assert data.get("statusCode") == expected_error_code

    response = requests.post(f"{api_url}/remainder", json=json_data)
    assert response.status_code == 200
    data = response.json()
    assert data.get("statusCode") == expected_error_code