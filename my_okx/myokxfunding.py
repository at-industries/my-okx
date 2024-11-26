from logging import Logger
from requests import Response
from typing import Union, Tuple

import hmac
import json
import base64
import datetime
import requests
import inspect

from .data.constants import *
from .models.networkinfo import *
from .models.assetbalance import *


class MyOkxFunding:
    name = NAME_OKX
    net = NET_COM

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
            api_key: Optional[str] = None,
            secret_key: Optional[str] = None,
            passphrase: Optional[str] = None,
            proxy: Optional[str] = None,
            logger: Optional[Logger] = None,
    ):
        """
        MyOkxFunding is a convenient library for interacting with the OKX Funding API.
        OKX API Documentation: https://www.okx.cab/docs-v5/en/#overview

        :param api_key: API Key (generated on the OKX website)
        :param secret_key: Secret Key (generated on the OKX website)
        :param passphrase: Passphrase (created by the user during API key generation on OKX)
        :param proxy: HTTP/HTTPS proxy (e.g., user12345:abcdef@12.345.67.890:1234)
        :param logger: Logger object (used to log received responses)
        """
        self._api_key = api_key
        self._api_secret = secret_key
        self._passphrase = passphrase
        self._proxy = proxy
        self._logger = logger
        self._httpClient = requests.Session()

    async def check_keys(self) -> Tuple[int, Union[bool, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/account/balance'
            method = 'GET'
            body = ''
            response = self._http_request(endpoint, method, body)
            self._log_debug(f'RESPONSE: {response.json()}')
            status_code = str(response.status_code)
            json = response.json()
            if status_code == '200':
                return 0, True
            else:
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | No msg!')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def get_balance(self, currency: str) -> Tuple[int, Union[float, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/asset/balances'
            method = 'GET'
            body = f'?ccy={currency}'
            response = self._http_request(endpoint, method, body)
            self._log_debug(f'RESPONSE: {response.json()}')
            return 0, float(response.json()['data'][0]['availBal'])
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def get_ticker_price(self, ticker: str) -> Tuple[int, Union[float, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/public/price-limit'
            method = 'GET'
            body = f'?instId={ticker}-USDT'
            response = self._http_request(endpoint, method, body)
            self._log_debug(f'RESPONSE: {response.json()}')
            data = response.json()['data'][0]
            return 0, round((float(data['buyLmt']) + float(data['sellLmt'])) / 2, 2)
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def get_network(self, ticker: str, chain: str) -> Tuple[int, Union[NetworkInfo, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/asset/currencies'
            method = 'GET'
            body = f'?ccy={ticker}'
            response = self._http_request(endpoint, method, body)
            self._log_debug(f'RESPONSE: {response.json()}')
            data = response.json()['data']
            for ntw in data:
                if str(ntw['chain']) == chain:
                    network = NetworkInfo(
                        ticker=ticker,
                        chain=str(ntw['chain']),
                        wd_bool=bool(ntw['canWd']),
                        min_wd=float(ntw['minWd']),
                        max_wd=float(ntw['maxWd']),
                        min_fee=float(ntw['minFee']),
                        max_fee=float(ntw['maxFee']),
                        precision=int(ntw['wdTickSz']),
                    )
                    return 0, network
            else:
                return -1, Exception(f'{log_process} | No such a network!')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def convert_usd_to_native(
            self,
            value: float,
            ticker: str, network: str,
    ) -> Tuple[int, Union[float, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.get_ticker_price(ticker=ticker)
            if status != -1:
                price: float = result
                status, result = await self.get_network(ticker=ticker, chain=network)
                if status != -1:
                    return 0, round(value/price, result.precision)
                else:
                    return -1, Exception(f'{log_process} | {result}')
            else:
                return -1, Exception(f'{log_process} | {result}')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def post_withdrawal_on_chain(
            self,
            ticker: str, chain: str,
            address: str, amount: float, fee: float,
    ) -> Tuple[int, Union[str, Exception]]:
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
                'chain': chain
            }
            response = self._http_request(endpoint, method, body)
            self._log_debug(f'RESPONSE: {response.json()}')
            status_code = str(response.status_code)
            json = response.json()
            if status_code == '200':
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
                        return -1, Exception(f'{log_process} | No msg!')
            else:
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | No msg!')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def get_withdrawal_history(self, wd_id: str) -> Tuple[int, Union[dict, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/asset/withdrawal-history'
            method = 'GET'
            body = f'?wdId={wd_id}'
            response = self._http_request(endpoint, method, body)
            self._log_debug(f'RESPONSE: {response.json()}')
            data = response.json()['data']
            if data:
                if data[0]['wdId'] == wd_id:
                    return 0, data[0]
                else:
                    return -1, Exception(f'{log_process} | Wrong withdrawal[{wd_id}] json!')
            else:
                return -1, Exception(f'{log_process} | No such a withdrawal!')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def check_withdrawal(self, wd_id: str) -> Tuple[int, Union[bool, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            status, result = await self.get_withdrawal_history(wd_id=wd_id)
            if status != -1:
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

    async def get_subaccount_names(self, ) -> Tuple[int, Union[list, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/users/subaccount/list'
            method = 'GET'
            body = ''
            response = self._http_request(endpoint, method, body)
            self._log_debug(f'RESPONSE: {response.json()}')
            data = response.json()['data']
            subaccounts_list = []
            for subaccount_dict in data:
                subaccounts_list.append(subaccount_dict['subAcct'])
            if subaccounts_list:
                return 0, subaccounts_list
            else:
                return -1, Exception(f'{log_process} | Empty subaccounts list!')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def get_subaccount_balance(self, subaccount_name: str, currency: str) -> Tuple[int, Union[float, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/asset/subaccount/balances'
            method = 'GET'
            body = f'?subAcct={subaccount_name}&ccy={currency}'
            response = self._http_request(endpoint, method, body)
            self._log_debug(f'RESPONSE: {response.json()}')
            data = response.json()['data']
            return 0, float(data[0]['availBal'])
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    async def transfer_from_subacc_to_main(
            self,
            subaccount_name: str,
            currency: str, amount: float,
    ) -> Tuple[int, Union[str, Exception]]:
        log_process = f'{inspect.currentframe().f_code.co_name}'
        try:
            endpoint = '/api/v5/asset/transfer'
            method = 'POST'
            body = {
                'type': 2,
                'ccy': currency,
                'amt': amount,
                'from': 6,
                'to': 6,
                'subAcct': subaccount_name,
            }
            response = self._http_request(endpoint, method, body)
            self._log_debug(f'RESPONSE: {response.json()}')
            status_code = str(response.status_code)
            json = response.json()
            if status_code == '200':
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
                        return -1, Exception(f'{log_process} | No msg!')
            else:
                if 'msg' in json:
                    return -1, Exception(f'{log_process} | {json["msg"]}')
                else:
                    return -1, Exception(f'{log_process} | No msg!')
        except Exception as e:
            return -1, Exception(f'{log_process} | {e}')

    @staticmethod
    def _get_time() -> str:
        now = datetime.datetime.utcnow()
        time = now.isoformat('T', 'milliseconds')
        return time + 'Z'

    def _get_proxies(self, ) -> Union[dict, None]:
        if self._proxy is not None:
            return {
                'http': f'http://{self._proxy}',
                'https': f'http://{self._proxy}',
            }
        else:
            return None

    def _get_signature(self, timestamp: str, method: str, endpoint: str, body: Union[str, dict]) -> bytes:
        if method == 'POST':
            return self._generate_signature(timestamp, method, endpoint, json.dumps(body))
        else:
            return self._generate_signature(timestamp, method, endpoint, body)

    def _generate_signature(self, timestamp: str, method: str, endpoint: str, body: Union[str, dict]) -> bytes:
        message = str(timestamp) + str.upper(method) + endpoint + str(body)
        mac = hmac.new(bytes(self._api_secret, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        signature = base64.b64encode(mac.digest())
        return signature

    def _http_request(self, endpoint: str, method: str, body: Union[str, dict]) -> Response:
        url = (self.net + endpoint)
        timestamp = self._get_time()
        proxies = self._get_proxies()
        signature = self._get_signature(timestamp, method, endpoint, body)
        headers = {
            'OK-ACCESS-KEY': self._api_key,
            'OK-ACCESS-PASSPHRASE': self._passphrase,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-SIGN': signature,
        }
        if method == 'POST':
            return self._httpClient.post(url=url, headers=headers, json=body, proxies=proxies)
        else:
            return self._httpClient.request(method=method, url=(url + body), headers=headers, proxies=proxies)

    def _log_debug(self, message: str) -> None:
        if self._logger is not None:
            self._logger.debug(f'{self.name} | {message}')
