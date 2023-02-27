import requests
from config import api_url

# для get-запросов используем метод .get() и первым аргументом ссылку куда отправить запрос
req = requests.get(f"{api_url}/users")
print(req.json())   # если ответ в формате json()


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_transactions(self):
        api_url = 'https://example.com/api/user/{}/transaction'.format(
            self.user_id)
        response = requests.get(api_url)
        transactions = response.json()
        return transactions
