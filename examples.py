import asyncio
from my_okx import MyOKX


my_okx = MyOKX(
    api_key='YOUR-API-KEY',
    secret_key='YOUR-SECRET-KEY',
    passphrase='YOUR-PASSPHRASE',
    asynchrony=True,
)


async def example_00():
    status, result = await my_okx.PUBLIC_get_price(ticker='BTC')
    if status == 0:
        print(f'00 | Price: {result}')
    else:
        print(f'00 | Error while getting price: {result}')

asyncio.run(example_00())


async def example_01():
    status, result = await my_okx.FUNDING_is_connected()
    if status == 0:
        print(f'01 | Connection: {result}')
    else:
        print(f'01 | Error while checking connection: {result}')

asyncio.run(example_01())


async def example_02():
    status, result = await my_okx.FUNDING_get_balance(ticker='BTC')
    if status == 0:
        print(f'02 | Balance: {result}')
    else:
        print(f'02 | Error while getting balance: {result}')

asyncio.run(example_02())


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


async def example_04():
    status, result = await my_okx.SUBACOUNT_get_subaccounts()
    if status == 0:
        print(f'04 | Subaccounts: {result}')
    else:
        print(f'04 | Error while getting subaccounts: {result}')

asyncio.run(example_04())


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
