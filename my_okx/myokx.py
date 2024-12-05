from logging import Logger
from typing import Optional, Union, Tuple
from httpx import Client, AsyncClient, Response

import hmac
import json
import httpx
import base64
import inspect
import datetime

from .utils import afh


class MyOKX:
    name = 'OKX'
    host = 'https://www.okx.com'

    withdraw_native_chains = {
        'Arbitrum': 'ETH-Arbitrum One',
        'Avalanche': 'AVAX-Avalanche C-Chain',
        'Base': 'ETH-Base',
        'BSC': 'BNB-BSC',
        'Fantom': 'FTM-Fantom',
        'Optimism': 'ETH-Optimism',
        'Polygon': 'POL-Polygon',
        'zkSync': 'ETH-zkSync Era',
    }

    def __init__(
            self,
            api_key: str,
            secret_key: str,
            passphrase: str,
            proxy: Optional[str] = None,
            logger: Optional[Logger] = None,
            asynchrony: Optional[bool] = False,
    ):
        """
        MyOkxFunding is a convenient library for interacting with the OKX Funding API.
        For more details about OKX API, refer to the OKX Documentation: https://www.okx.cab/docs-v5/en/#overview

        Almost all class methods (except utility functions) return tuples, with an integer status as the first element:
        - `0`: Success status (indicates the method completed successfully; the second element in the tuple contains the result)
        - `-1`: Error status (indicates the method failed; the second element in the tuple contains an error message)

        :param api_key: API Key (generated on the OKX website).
        :param secret_key: Secret Key (generated on the OKX website).
        :param passphrase: Passphrase (created by the user during API key generation on OKX).
        :param proxy: HTTP/HTTPS proxy (e.g., user12345:abcdef@12.345.67.890:1234).
        :param logger: Logger object (used to log received responses).
        :param asynchrony: Enables asynchronous operations.
        """
        self._api_key = api_key
        self._secret_key = secret_key
        self._passphrase = passphrase
        self._proxy = proxy
        self._logger = logger
        self._asynchrony = asynchrony
        self._httpx_client = self._get_httpx_client()

    async def PUBLIC_get_price(self, ticker: str) -> Tuple[int, Union[float, Exception]]:
        """Gets the price (in USDT) of a specific coin by its ticker (e.g., BTC, ETH)."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.PUBLIC_get_price_limit(ticker=ticker)
            if status == 0:
                data = result['data'][0]
                buy_limit = float(data['buyLmt'])
                sell_limit = float(data['sellLmt'])
                return 0, round((buy_limit + sell_limit) / 2, 2)
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def PUBLIC_get_price_limit(self, ticker: str) -> Tuple[int, Union[dict, Exception]]:
        """Gets the buy and sell limits (in USDT) for a specific coin by its ticker (e.g., BTC, ETH)."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = f'/api/v5/public/price-limit'
            method = f'GET'
            body = f'?instId={ticker}-USDT'
            response = await self._httpx_request(
                endpoint=endpoint,
                method=method,
                body=body,
            )
            if response.status_code == 200:
                return 0, dict(response.json())
            else:
                json = response.json()
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | {json}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def FUNDING_is_connected(self, ) -> Tuple[int, Union[bool, Exception]]:
        """Checks the connection to the funding account."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = f'/api/v5/asset/balances'
            method = f'GET'
            body = f''
            response = await self._httpx_request(
                endpoint=endpoint,
                method=method,
                body=body,
            )
            if response.status_code == 200:
                return 0, True
            else:
                json = response.json()
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | {json}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def FUNDING_get_balance(self, ticker: Optional[str] = None) -> Tuple[int, Union[dict, Exception]]:
        """Gets the balance of the funding account for a specific coin and for all coins."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = f'/api/v5/asset/balances'
            method = f'GET'
            body = f'' if (ticker is None) else f'?ccy={ticker}'
            response = await self._httpx_request(
                endpoint=endpoint,
                method=method,
                body=body,
            )
            if response.status_code == 200:
                return 0, dict(response.json())
            else:
                json = response.json()
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | {json}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def FUNDING_get_chain_info(self, ticker: str, chain: str) -> Tuple[int, Union[dict, Exception]]:
        """Gets information about a specific currency chain (e.g., withdraw_min_value, withdraw_min_fee, withdraw_tick_size)."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.FUNDING_get_chains_info(ticker=ticker)
            if status == 0:
                for network in result['data']:
                    if str(network['chain']) == chain:
                        return 0, network
                else:
                    return -1, Exception(f'{log_process} | No such a chain!')
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def FUNDING_get_chains_info(self, ticker: Optional[str] = None) -> Tuple[int, Union[dict, Exception]]:
        """Gets information about all currency chains (e.g., withdraw_min_value, withdraw_min_fee, withdraw_tick_size)."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = f'/api/v5/asset/currencies'
            method = f'GET'
            body = f'' if (ticker is None) else f'?ccy={ticker}'
            response = await self._httpx_request(
                endpoint=endpoint,
                method=method,
                body=body,
            )
            if response.status_code == 200:
                return 0, dict(response.json())
            else:
                json = response.json()
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | {json}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def FUNDING_convert_usd_to_native(self, amount: float, ticker: str, chain: str) -> Tuple[int, Union[float, Exception]]:
        """
        Converts USD amount to the native chain coin amount, rounded to the chain's tick_size value
        (e.g., 100 USD converts to 0.02857143 ETH for an ETH price of 3500 USD).
        """
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.PUBLIC_get_price(ticker=ticker)
            if status == 0:
                price: float = result
                status, result = await self.FUNDING_get_chain_info(ticker=ticker, chain=chain)
                if status == 0:
                    precision = int(result['wdTickSz'])
                    return 0, round(amount / price, precision)
                else:
                    return -1, Exception(f'{log_process} | {result}')
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def FUNDING_post_withdrawal(self, ticker: str, chain: str, address: str, amount: float, fee: float) -> Tuple[int, Union[str, Exception]]:
        """Posts a withdrawal on the chain for a specific ticker and chain (withdrawals must be available for created API keys)."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/asset/withdrawal'
            method = 'POST'
            body = {
                'ccy': ticker,
                'amt': amount,
                'dest': 4,
                'toAddr': address,
                'fee': fee,
                'chain': chain,
            }
            response = await self._httpx_request(
                endpoint=endpoint,
                method=method,
                body=body,
            )
            json = response.json()
            if response.status_code == 200:
                data = json['data']
                if data:
                    wd_id = ''
                    for part in data:
                        wd_id = str(part['wdId'])
                    return 0, wd_id
                else:
                    if 'msg' in json:
                        return -1, Exception(f'{log_process} | {json["msg"]}')
                    else:
                        return -1, Exception(f'{log_process} | {json}')
            else:
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | {json}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def FUNDING_get_withdrawal(self, withdrawal_id: str) -> Tuple[int, Union[dict, Exception]]:
        """Gets information about a withdrawal (e.g., status, transaction_hash)."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/asset/withdrawal-history'
            method = 'GET'
            body = f'?wdId={withdrawal_id}'
            response = await self._httpx_request(
                endpoint=endpoint,
                method=method,
                body=body,
            )
            json = response.json()
            if response.status_code == 200:
                data = json['data']
                if data:
                    if data[0]['wdId'] == withdrawal_id:
                        return 0, data[0]
                    else:
                        return -1, Exception(f'{log_process} | Wrong withdrawal[{withdrawal_id}] json!')
                else:
                    return -1, Exception(f'{log_process} | No such a withdrawal!')
            else:
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | {json}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def FUNDING_check_withdrawal(self, withdrawal_id: str) -> Tuple[int, Union[bool, Exception]]:
        """Checks if the withdrawal is completed by its withdrawal_id (the withdrawal_id is returned after posting the withdrawal on the chain)."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.FUNDING_get_withdrawal(withdrawal_id=withdrawal_id)
            if status == 0:
                state = result['state']
                if state not in ['-3', '-2', '-1']:
                    if state == '2':
                        return 0, True
                    else:
                        return 0, False
                else:
                    return -1, Exception(f'{log_process} | Withdrawal canceled!')
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def SUBACOUNT_get_subaccounts(self, ) -> Tuple[int, Union[list, Exception]]:
        """Gets the names of all subaccounts created under the main OKX account."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/users/subaccount/list'
            method = 'GET'
            body = ''
            response = await self._httpx_request(
                endpoint=endpoint,
                method=method,
                body=body,
            )
            json = response.json()
            if response.status_code == 200:
                subaccounts_list = []
                for subaccount_dict in json['data']:
                    subaccounts_list.append(subaccount_dict['subAcct'])
                if subaccounts_list:
                    return 0, subaccounts_list
                else:
                    return -1, Exception(f'{log_process} | Empty subaccounts list!')
            else:
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | {json}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def SUBACCOUNT_get_balance(self, subaccount_name: str, ticker: str) -> Tuple[int, Union[float, Exception]]:
        """Gets the balance for a specific coin in a specific subaccount."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/asset/subaccount/balances'
            method = 'GET'
            body = f'?subAcct={subaccount_name}&ccy={ticker}'
            response = await self._httpx_request(
                endpoint=endpoint,
                method=method,
                body=body,
            )
            json = response.json()
            if response.status_code == 200:
                return 0, float(json['data'][0]['availBal'])
            else:
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | {json}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def SUBACCOUNT_transfer_to_main(self, subaccount_name: str, ticker: str, amount: float) -> Tuple[int, Union[str, Exception]]:
        """Transfers coins from a subaccount to the main account for a specific coin from a specific subaccount."""
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/asset/transfer'
            method = 'POST'
            body = {
                'type': 2,
                'ccy': ticker,
                'amt': amount,
                'from': 6,
                'to': 6,
                'subAcct': subaccount_name,
            }
            response = await self._httpx_request(
                endpoint=endpoint,
                method=method,
                body=body,
            )
            json = response.json()
            if response.status_code == 200:
                data = json['data']
                if data:
                    trans_id = ''
                    for part in data:
                        trans_id = str(part['transId'])
                    return 0, trans_id
                else:
                    if 'msg' in json:
                        return -1, Exception(f'{log_process} | {json["msg"]}')
                    else:
                        return -1, Exception(f'{log_process} | {json}')
            else:
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | {json}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    def _get_httpx_client(self, ) -> Union[Client, AsyncClient]:
        if self._asynchrony:
            httpx_client = httpx.AsyncClient(proxy=self.proxy)
        else:
            httpx_client = httpx.Client(proxy=self.proxy)
        return httpx_client

    async def _httpx_request(self, method: str, endpoint: str, body: Union[str, dict]) -> Response:
        timestamp = self.time
        signature = self._get_signature(timestamp, method, endpoint, body)
        headers = {
            'OK-ACCESS-KEY': self._api_key,
            'OK-ACCESS-PASSPHRASE': self._passphrase,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-SIGN': signature,
        }
        if method == 'GET':
            response = await afh(
                self._httpx_client.request, self._asynchrony,
                method=method, url=(self.host + endpoint + body), headers=headers,
            )
        else:
            response = await afh(
                self._httpx_client.request, self._asynchrony,
                method=method, url=(self.host + endpoint), headers=headers, json=body,
            )
        self._log_debug(response.json())
        return response

    def _get_signature(self, timestamp: str, method: str, endpoint: str, body: Union[str, dict]) -> bytes:
        message = timestamp + method.upper() + endpoint + (json.dumps(body) if isinstance(body, dict) else body)
        mac = hmac.new(bytes(self._secret_key, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        signature = base64.b64encode(mac.digest())
        return signature

    def _log_debug(self, message: str) -> None:
        if self._logger is not None:
            self._logger.debug(f'{self.name} | {message}')

    @property
    def time(self, ) -> str:
        now = datetime.datetime.utcnow()
        time = now.isoformat('T', 'milliseconds')
        return time + 'Z'

    @property
    def proxy(self, ) -> Optional[str]:
        return f'http://{self._proxy}' if self._proxy else None
