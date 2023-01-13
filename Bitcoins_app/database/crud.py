from datetime import datetime
import config
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
    # flush()
    return wallet


@db_session
def create_transaction(
    sender: User,
    amount_btc_without_fee: float,
    receiver_address: str,
    fee: float | None = None,
    testnet: bool = False
):
    """
    :param amount_btc_without_fee:  количество биткоинов исключая комиссию, значение в сатоши
    :param receiver_address: адрес получателя, строка с адресом
    :param amount_btc_with_fee: количество биткоинов включая комиссию, значение в сатоши
    :param fee: абсолютная комиссия, исчисляем в сатоши - необязательно.
    :param testnet: в тестовой сети ли мы работаем
    :return: Transaction object
    """

    # тут мы загружаем в переменную wallet_of_sender кошелек отправителя
    # и если мы в тестовой сети, то соответственно мы загружаем кошелек из тестовой сети
    wallet_of_sender = bit.Key(sender.wallet.private_key) if not testnet else bit.PrivateKeyTestnet(
        sender.wallet.private_key)
    sender.wallet.balance = wallet_of_sender.get_balance()  # Получаем баланс кошелька
    if not fee:
        # получаем стоимость транзакции sat/B и умножаем на 1000
        fee = bit.network.fees.get_fee() * 1000
    amount_btc_with_fee = amount_btc_without_fee + \
        fee  # находим сумму включая комиссию
    if amount_btc_without_fee + fee > sender.wallet.balance:
        return f"Too low balance: {sender.wallet.balance}"

    # подготавливаем кортеж в списке с данными для транзакции
    output = [(receiver_address, amount_btc_without_fee, 'satoshi')]

    # отправляем транзакцию и получаем её хеш
    tx_hash = wallet_of_sender.send(output, fee, absolute_fee=True)

    # создаем объект транзакции и сохраняем его тем самым в нашей БД
    transaction = Transaction(sender=sender,
                              sender_wallet=sender.wallet,
                              fee=fee,
                              sender_address=sender.wallet.address,
                              receiver_address=receiver_address,
                              amount_btc_with_fee=amount_btc_with_fee,
                              amount_btc_without_fee=amount_btc_without_fee,
                              date_of_transaction=datetime.now(),
                              tx_hash=tx_hash)
    return transaction
