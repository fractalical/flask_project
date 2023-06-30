import requests

# Создание нового пользователя
# response = requests.post('http://127.0.0.1:5000/user/',
#                          json={'username': 'user1', 'password': '123456789'})

# Получение данных о пользователе
# response1 = requests.get('http://127.0.0.1:5000/user/1')

# Создание нового пользователя
response1_1 = requests.patch('http://127.0.0.1:5000/user/13',
                             json={'username': 'admin'},
                             headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjoxM30.m6YnfD_SgwFUS4EjVXQw520xzQ1ektxL94LYFz-tiqg'})

# Аутентификация пользователя
response2 = requests.post('http://127.0.0.1:5000/auth_user/',
                          json={'username': 'user1', 'password': '123456789'})

# Создание статьи (токен нужно получить после аутентификации пользователя)
# response3 = requests.post('http://127.0.0.1:5000/advertisement/',
#                           json={'title': 'some title3', 'text': 'some text3'},
#                           headers={'Authorization': 'you token'})

# Получение данных о статье
# response4 = requests.get('http://127.0.0.1:5000/advertisement/1')

# Удаление статьи
# response5 = requests.delete('http://127.0.0.1:5000/advertisement/2')

if __name__ == '__main__':
    print(response1_1.json())
