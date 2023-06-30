import requests

# response = requests.post('http://127.0.0.1:5000/user/',
#                          json={'username': 'user1', 'password': '123456789'})
#
# response1 = requests.get('http://127.0.0.1:5000/user/1')

response2 = requests.post('http://127.0.0.1:5000/auth_user/',
                          json={'username': 'user1', 'password': '123456789'},
                          headers={'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjoxfQ.bn_8y-YXjvzcB8ASqu4m6lU3tOMCbrOSitmIgjl-OsA'})

if __name__ == '__main__':
    print(response2.json())
