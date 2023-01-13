from datetime import datetime
# import config
import pydantic_models
import bit
from db import *

# wallet = bit.Key()
# print(f'Balance: {wallet.get_balance()}')
# print(f'Address: {wallet.address}')
# print(f'Private key: {wallet.to_wif()}')


@db_session
def create_wallet(user: pydantic_models.User = None, private_key: str = None, testnet: bool = False):
    if not testnet:  # проверяем не тестовый ли мы делаем кошелек
        raw_wallet = bit.Key() if not private_key else bit.Key(private_key)
    else:
        raw_wallet = bit.PrivateKeyTestnet(
        ) if not private_key else bit.PrivateKeyTestnet(private_key)
    if user:
        wallet = Wallet(user=user, private_key=raw_wallet.to_wif(),
                        address=raw_wallet.address)
    else:
        wallet = Wallet(private_key=raw_wallet.to_wif(),
                        address=raw_wallet.address)
    flush()
    return wallet


@db_session
def create_user(tg_id: int, nick: str = None):
    if nick:
        user = User(tg_ID=tg_id, nick=nick,
                    create_date=datetime.now(), wallet=create_wallet())
    else:
        user = User(tg_ID=tg_id, create_date=datetime.now(),
                    wallet=create_wallet())
    flush()     # сохраняем объект в базе данных, чтобы получить его айди
    return user
