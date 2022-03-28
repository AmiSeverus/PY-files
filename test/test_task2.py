import pytest
import ya as cls_to_test

#Введите токен
test_token = ''
test_folder = 'test'

test_data = {
    'ya_test': cls_to_test.Ya(),
    'params': [(test_folder, test_token, 201), (test_folder, test_token, 409), (test_folder, 'test', 401),],
    # 201 - ok, 409 - папка уже существует, 401 - не авторизован
}

#Подготовка к тесту - удаление папки, если существует
test_data['ya_test'].delete_folder_Ya(test_folder, test_token)

def setup():
    print("method setup")   


def teardown():
    print("method teardown")


@pytest.mark.parametrize('path, token, res', test_data['params'])
def test_create_folder_Ya(path, token, res):
    assert test_data['ya_test'].create_folder_Ya(path, token) == res;
