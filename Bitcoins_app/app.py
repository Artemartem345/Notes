import fastapi
import database
import pydantic_models
import config
from fastapi import Request
import copy
from database import crud
api = fastapi.FastAPI()


# response = {"Ответ": "Который возвращает сервер"}
# response0 = {'answer': 'response'}

# @api.get('/')
# def index():
#     return response0


# @api.get('/hello')
# def hello():
#     return "hello"

# @api.get('/about/us')
# def about():
#     return {"We Are":"Legion"}


# @api.get('/static/path')
# def hello():
#     return "hello"


# fake_database = {'users': [
#     {
#         "id": 1,             # тут тип данных - число
#         "name": "Anna",      # тут строка
#         "nick": "Anny42",    # и тут
#         "balance": 15300   # а тут float
#     },

#     {
#         "id": 2,             # у второго пользователя
#         "name": "Dima",      # такие же
#         "nick": "dimon2319",  # типы
#         "balance": 160.23   # данных
#     }, {
#         "id": 3,             # у третьего
#         "name": "Vladimir",  # юзера
#         "nick": "Vova777",   # мы специально сделаем
#         "balance": 25000     # нестандартный тип данных в его балансе
#     }
# ], }


# @api.get('/get_info_by_user_id/{id:int}')
# def get_info_about_user(id):
#     return fake_database['users'][id-1]


# @api.get('/get_user_balance_by_id/{id:int}')
# def get_user_balance(id):
#     return fake_database['users'][id-1]['balance']


# @api.get('/get_total_balance')
# def get_total_balance():
#     total_balance: float = 0.0
#     for user in fake_database['users']:
#         total_balance += user['balance']
#     return total_balance

# @api.get('/')       # метод для обработки get запросов
# @api.post('/')      # метод для обработки post запросов
# @api.put('/')       # метод для обработки put запросов
# @api.delete('/')    # метод для обработки delete запросов
# def index(request: Request):  # тут request - будет объектом в котором хранится вся информация о запросе
#     return {"Request": [request.method,    # тут наш API вернет клиенту метод, с которым этот запрос был совершен
#                         request.headers]}


# fake_database = {'users': [
#     {
#         "id": 1,
#         "name": "Anna",
#         "nick": "Anny42",
#         "balance": 15300
#     },

#     {
#         "id": 2,
#         "name": "Dima",
#         "nick": "dimon2319",
#         "balance": 160.23
#     },
#     {
#         "id": 3,
#         "name": "Vladimir",
#         "nick": "Vova777",
#         "balance": 200.1
#     }
# ], }


# @api.put('/user/{user_id}')
# # используя fastapi.Body() мы явно указываем, что отправляем информацию в теле запроса
# def update_user(user_id: int, user: pydantic_models.User = fastapi.Body()):
#     # так как в нашей бд юзеры хранятся в списке, нам нужно найти их индексы внутри этого списка
#     for index, u in enumerate(fake_database['users']):
#         if u['id'] == user_id:
#             # обновляем юзера в бд по соответствующему ему индексу из списка users
#             fake_database['users'][index] = user
#             return user


# @api.post('/user/create')
# def index(user: pydantic_models.User):
#     fake_database['users'].append(user)
#     return {'User Created!': user}


# @api.get('/get_info_by_user_id/{id:int}')
# def get_info_about_user(id):
#     return fake_database['users'][id-1]


# @api.get('/get_user_balance_by_id/{id:int}')
# def get_info_about_user(id):
#     return fake_database['users'][id-1]['balance']


# @api.get('/get_total_balance')
# def get_info_about_user():
#     total_balance: float = 0.0
#     for user in fake_database['users']:
#         total_balance += pydantic_models.User(**user).balance
#     return total_balance


# @api.get("/users/")
# def get_users(skip: int = 0, limit: int = 10):
#     return fake_database['users'][skip: skip + limit]


# @api.get("/user/{user_id}")
# def read_user(user_id: str, query: str | None = None):
#     if query:
#         return {"item_id": user_id, "query": query}
#     return {"item_id": user_id}


# @api.delete('/user/{user_id}')
# # используя fastapi.Path() мы явно указываем, что переменную нужно брать из пути
# def delete_user(user_id: int = fastapi.Path()):
#     # так как в нашей бд юзеры хранятся в списке, нам нужно найти их индексы внутри этого списка
#     for index, u in enumerate(fake_database['users']):
#         if u['id'] == user_id:
#             # делаем полную копию объекта в переменную old_db, чтобы было с чем сравнить
#             old_db = copy.deepcopy(fake_database)
#             del fake_database['users'][index]    # удаляем юзера из бд
#             return {'old_db': old_db,
#                     'new_db': fake_database}


# {'users': [
#     {
#         "id": 1,
#         "name": "Anna",
#         "nick": "Anny42",
#         "balance": 15300
#     },

#     {
#         "id": 2,
#         "name": "Dima",
#         "nick": "dimon2319",
#         "balance": 160.23
#     },
    
#     {
#         "id": 3,
#         "name": "Vladimir",
#         "nick": "Vova777",
#         "balance": 200.1
#     },
#     {
         
#        "id": 4,
#        "name": "Maria",
#        "nick": "Mary",
#        "balance":0, 
#     }
        
# ]}
    




# @api.put('/user/{user_id}')
# def update_user(user_id: int, user: pydantic_models.User = fastapi.Body()): # используя fastapi.Body() мы явно указываем, что отправляем информацию в теле запроса
#     for index, u in enumerate(fake_database['users']): # так как в нашей бд юзеры хранятся в списке, нам нужно найти их индексы внутри этого списка
#         if u['id'] == user_id:
#             fake_database['users'][index] = user    # обновляем юзера в бд по соответствующему ему индексу из списка users
#             return user


# @api.delete('/user/{user_id}')
# def delete_user(user_id: int = fastapi.Path()): # используя fastapi.Path() мы явно указываем, что переменную нужно брать из пути
#     for index, u in enumerate(fake_database['users']): # так как в нашей бд юзеры хранятся в списке, нам нужно найти их индексы внутри этого списка
#         if u['id'] == user_id:
#             old_db = copy.deepcopy(fake_database) # делаем полную копию объекта в переменную old_db, чтобы было с чем сравнить
#             del fake_database['users'][index]    # удаляем юзера из бд
#             return {'old_db' : old_db,
#                     'new_db': fake_database}


# @api.post('/user/create')
# def create_user(user: pydantic_models.User):
#     fake_database['users'].append(user)
#     return {'User Created!': user}


# @api.get('/get_info_by_user_id/{id:int}')
# def get_info_about_user(id):
#     return fake_database['users'][id-1]


# @api.get('/get_user_balance_by_id/{id:int}')
# def get_user_balance_by_id(id):
#     return fake_database['users'][id-1]['balance']


# @api.get('/get_total_balance')
# def get_total_balance():
#     total_balance: float = 0.0
#     for user in fake_database['users']:
#         total_balance += pydantic_models.User(**user).balance
#     return total_balance


# @api.get("/users/")
# def get_users(skip: int = 0, limit: int = 10):
#     return fake_database['users'][skip: skip + limit]


@api.get("/user/{user_id}")
def read_user(user_id: str, query: str | None = None):
    if query:
        return {"item_id": user_id, "query": query}
    return {"item_id": user_id}


@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.User_to_update = fastapi.Body()):
    return crud.update_user(user).to_dict()


@api.delete('/user/{user_id}')
@crud.db_session
# используя fastapi.Path() мы явно указываем, что переменную нужно брать из пути
def delete_user(user_id: int = fastapi.Path()):
    crud.get_user_by_id(user_id).delete()
    return True


@api.post('/user/create')
def create_user(user: pydantic_models.User_to_create):
    return crud.create_user(tg_id=user.tg_ID,
                            nick=user.nick if user.nick else None).to_dict()


@api.get('/get_info_by_user_id/{user_id:int}')
@crud.db_session
def get_info_about_user(user_id):
    return crud.get_user_info(crud.User[user_id])


@api.get('/get_user_balance_by_id/{user_id:int}')
@crud.db_session
def get_user_balance_by_id(user_id):
    crud.update_wallet_balance(crud.User[user_id].wallet)
    return crud.User[user_id].wallet.balance

@api.get('/get_total_balance')
@crud.db_session
def get_total_balance():
    balance = 0.0
    crud.update_all_wallets()
    for user in crud.User.select()[:]:
        balance += user.wallet.balance
    return balance


@api.get("/users")
@crud.db_session
def get_users():
    users = []
    for user in crud.User.select()[:]:
        users.append(user.to_dict())
    return users
