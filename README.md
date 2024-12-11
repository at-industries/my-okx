# MyOKX
MyOKX - это утилитарная библиотека для работы с биржей OKX.

## Общая информация
### Возможности
1. Асинхронное взаимодействие с биржей.
2. Подключение прокси.
3. Логирование результатов.
4. Работа с публичными данными (получение цен активов).
5. Работа с Funding аккаунтом (отправка токенов).
6. Работа с суб-аккаунтами (трансферы между аккаунтами).

### Методы
1.  `PUBLIC_get_price` - получение цены актива (в долларах).
2. `PUBLIC_get_price_limit` - получение цен макс./мин. лимитных ордеров на покупку/продажу.
3. `FUNDING_is_connected` - проверка подключения к Funding аккаунту.
4. `FUNDING_get_balance` - получение баланса Funding аккаунта.
5. `FUNDING_get_chain_info` - получение информации по конкретной сети актива. 
6. `FUNDING_get_chains_info` - получение информации по всем сетям актива. 
7. `FUNDING_convert_usd_to_native` - перевод суммы USD в нативную монету сети.
8. `FUNDING_post_withdrawal` - ончейн вывод средств на кошелек.
9. `FUNDING_get_withdrawal` - получение информации по ончейн выводу.
10. `FUNDING_check_withdrawal` - проверка ончейн вывода на успех.
11. `SUBACCOUNT_get_subaccounts` - получение списка всех суб-аккаунтов.
12. `SUBACCOUNT_get_balance` - получение баланса на суб-аккаунте.
13. `SUBACCOUNT_transfer_to_main` - перевод средств с основного аккаунта на суб-аккаунт.

### Особенности
1. Методы библиотеки разделены на 4 основных типа:
- Методы работы с публичными данными - это методы, которые работают с публичными данными биржи (для публичных ендпоинтов API ключи не нужны). Названия данных методов начинаются на `PUBLIC_`.
- Методы работы с Funding аккаунтом - это методы, которые работают с Funding аккаунтом. Названия данных методов начинаются на `FUNDING_`.
- Методы работы с суб-аккаунтами - это методы, которые работают суб-аккаунтами. Названия данных методов начинаются на `SUBACCOUNT_`.
- Утилитарные методы - это методы, которые выполняют утилитарные функции. Данные методы располагаются в самом конце класса.
2. Почти все методы класса возвращают кортежи с целым числом в качестве первого элемента, где:
- `0`: статус успеха (успешное завершение метода; второй элемент кортежа содержит результат)
- `-1`: статус ошибки (неуспешное завершение метода; второй элемент кортежа содержит ошибку)

## Примеры
### Импорт библиотек
Перед началом импортируем библиотеку `asyncio` для запуска асинхронных функций и сам класс `MyOKX`.
```python
import asyncio
from my_okx import MyOKX
```

### Создание экземпляра класса `MyOKX`
Создаем экземпляр класса `MyOKX` с обязательным параметрами `api_key`, `secret_key`, `passphrase` и опциональным параметром `asynchrony`. Подробнее о параметрах — в комментариях конструктора класса `MyWeb3`. 
```python
my_okx = MyOKX(
    api_key='YOUR-API-KEY',
    secret_key='YOUR-SECRET-KEY',
    passphrase='YOUR-PASSPHRASE',
    asynchrony=True,
)
```

### Пример использования метода `PUBLIC_get_price`
Метод `PUBLIC_get_price` получает цену актива по его тикеру. В нашем примере мы запрашиваем цену монеты `BTC`.
```python
async def example_00():
    status, result = await my_okx.PUBLIC_get_price(ticker='BTC')
    if status == 0:
        print(f'00 | Price: {result}')
    else:
        print(f'00 | Error while getting price: {result}')

asyncio.run(example_00())
```

### Пример использования метода `FUNDING_is_connected`
Метод `FUNDING_is_connected` проверяет подключение к `Funding` аккаунту OKX. Метод присылает (0, True), если подключение успешное, и (-1, Exception("...")), если нет.
```python
async def example_01():
    status, result = await my_okx.FUNDING_is_connected()
    if status == 0:
        print(f'01 | Connection: {result}')
    else:
        print(f'01 | Error while checking connection: {result}')

asyncio.run(example_01())
```

### Пример использования метода `FUNDING_get_balance`
Метод `FUNDING_get_balance` получает баланс `Funding` аккаунта (как для конкретного токена, так и всех активов сразу). В нашем примере мы получаем баланс монеты `BTC`. Чтобы получить баланс всех (ненулевых) активов, параметр `ticker` заполнять не нужно.
```python
async def example_02():
    status, result = await my_okx.FUNDING_get_balance(ticker='BTC')
    if status == 0:
        print(f'02 | Balance: {result}')
    else:
        print(f'02 | Error while getting balance: {result}')

asyncio.run(example_02())
```

### Пример использования метода `FUNDING_post_withdrawal`
Метод `FUNDING_post_withdrawal` выводит средства с биржи на сторонний кошелек. В нашем примере мы выводим `0.01` монеты `ETH` на кошелек `0xB293cFf00bA3f110C839fBDB59186BD944B144D5` в сети `Base` и платим `fee` в размере `0.00001`.
- Узнать список всех сетей можно в методе `FUNDING_get_chains_info`. 
- Узнать минимально возможный `fee` для вывода в необходимую сеть можно в методах `FUNDING_get_chain_info` и `FUNDING_get_chains_info`.
- Перевести доллар в нативную монету сети можно методом `FUNDING_convert_usd_to_native`.
```python
async def example_03():
    status, result = await my_okx.FUNDING_post_withdrawal(
        ticker='ETH',
        chain='ETH-Base',
        address='0xB293cFf00bA3f110C839fBDB59186BD944B144D5',
        amount=0.01,
        fee=0.00001,
    )
    if status == 0:
        print(f'03 | Withdrawal Id: {result}')
    else:
        print(f'03 | Error while posting withdrawal: {result}')

asyncio.run(example_03())
```

### Пример использования метода `SUBACCOUNT_get_subaccounts`
Метод `SUBACCOUNT_get_subaccounts` получает список имен всех созданных суб-аккаунтов.

```python
async def example_04():
    status, result = await my_okx.SUBACCOUNT_get_subaccounts()
    if status == 0:
        print(f'04 | Subaccounts: {result}')
    else:
        print(f'04 | Error while getting subaccounts: {result}')


asyncio.run(example_04())
```

### Пример использования метода `SUBACCOUNT_transfer_to_main`
Метод `SUBACCOUNT_transfer_to_main` переводит средства с суб-аккаунта на основной `Funding` аккаунт. В нашем примере мы переводим `100USDC` с суб-аккаунта под именем `SUBACCOUNT-NAME`.
```python
async def example_05():
    status, result = await my_okx.SUBACCOUNT_transfer_to_main(
        subaccount_name='SUBACCOUNT-NAME',
        ticker='USDC',
        amount=100.0,
    )
    if status == 0:
        print(f'05 | Transfer Id: {result}')
    else:
        print(f'05 | Error while transferring tokens from subaccount to main account: {result}')

asyncio.run(example_05())
```
