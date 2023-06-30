# Примеры запросов

### Создание нового пользователя
```
requests.post('http://127.0.0.1:5000/user/',
              json={'username': 'user1', 'password': '123456789'})
```

### Получение данных о пользователе
```
response1 = requests.get('http://127.0.0.1:5000/user/1')
```

### Создание нового пользователя
```
requests.patch('http://127.0.0.1:5000/user/13',
               json={'username': 'admin'},
               headers={'Authorization': 'you token'})
```

### Аутентификация пользователя
```
requests.post('http://127.0.0.1:5000/auth_user/',
              json={'username': 'user1', 'password': '123456789'})
```

### Создание статьи (токен нужно получить после аутентификации пользователя)
```
requests.post('http://127.0.0.1:5000/advertisement/',
              json={'title': 'some title', 'text': 'some text'},
              headers={'Authorization': 'you token'})
```

### Получение данных о статье
```
requests.get('http://127.0.0.1:5000/advertisement/1')
```

### Удаление статьи
```
requests.delete('http://127.0.0.1:5000/advertisement/1')
```