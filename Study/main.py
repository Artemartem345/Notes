import requests
import json
import time
# API Binance
url = 'https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT'
# Определяем максимальную цену 
max_price = 0
while True:
    # Получаем актуальную цену XRP/USDT с Binance
    response = requests.get(url)
    # Декодируем JSON-ответ в словарь Python
    data = json.loads(response.text)
    # Выводим текущую цену XRP/USDT на экран
    current_price = float(data['price'])
    print('Current price: %f' % current_price)
    # Обновляем максимальную цену, если требуется
    if current_price > max_price:
        max_price = current_price
    # Сравниваем текущую цену с максимальной, и если она упала на 1%, то выводим сообщение
    if (max_price - current_price)/max_price >= 0.01:
        print('Price dropped by 1%!')
    # Ожидаем 5 секунд, чтобы получить актуальный JSON-ответ
    time.sleep(5)
    
    
'''
Чтобы наша программа обрабатывала 
не только XRP И USDT, 
можно улучшить код, спарсив уже другую валюту 
и соотвественно выводя ее на экран
'''


