from fastapi.testclient import TestClient
from homework.main import app
import pytest

client = TestClient(app)


@pytest.fixture
def key_value_json():
    return {'key': 'test_key', 'value': 'test_value'}


def test_get_hello():
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.content.decode() == 'HSE One Love!'
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'


def test_get_hello_with_headers_and_params():
    headers = {'X-Custom-Header': 'custom-value'}
    params = {'arg1': 'value1', 'arg2': 'value2'}

    response = client.get('/hello', headers=headers, params=params)

    assert response.status_code == 200
    assert response.content.decode() == 'HSE One Love!'
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'


def test_set_key_value(key_value_json):
    response = client.post('/set', json=key_value_json)
    assert response.status_code == 200


def test_set_key_value_with_extra_fields():
    key_value_json = {'key': 'test_key', 'value': 'test_value', 'extra_field': 'extra_data'}
    response = client.post('/set', json=key_value_json)
    assert response.status_code == 200


def test_set_key_value_invalid_data():
    response = client.post('/set', json={'key': 'test_key'})
    assert response.status_code == 400


def test_set_key_value_invalid_content_type(key_value_json):
    response = client.post('/set', json=key_value_json,
                           headers={'Content-Type': 'text/plain; charset=utf-8'})
    assert response.status_code == 415


def test_get_key_value(key_value_json):
    client.post('/set', json=key_value_json)

    response = client.get('/get/test_key')
    assert response.status_code == 200
    assert response.json() == key_value_json
    assert response.headers['Content-Type'] == 'application/json'


def test_get_key_value_not_found():
    response = client.get('/get/nonexistent_key')
    assert response.status_code == 404


def test_divide_numbers():
    response = client.post('/divide', json={'dividend': 10, 'divider': 2})
    assert response.status_code == 200
    assert response.text == '5.0'


def test_divide_numbers_invalid_data():
    response = client.post('/divide', json={'dividend': 10, 'divider': 0})
    assert response.status_code == 400


def test_catch_all():
    response_get = client.get('/some_invalid_path')
    assert response_get.status_code == 405
    response_post = client.post('/some_invalid_path', headers={'Content-Type': 'application/json'})
    assert response_post.status_code == 405
    response_put = client.put('/some_invalid_path', headers={'Content-Type': 'application/json'})
    assert response_put.status_code == 405
    response_patch = client.patch('/some_invalid_path', headers={'Content-Type': 'application/json'})
    assert response_patch.status_code == 405
    response_delete = client.delete('/some_invalid_path')
    assert response_delete.status_code == 405
