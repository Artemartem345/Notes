import requests
from config import api_url

# для get-запросов используем метод .get() и первым аргументом ссылку куда отправить запрос
req = requests.get(f"{api_url}/users")
print(req.json())   # если ответ в формате json()
