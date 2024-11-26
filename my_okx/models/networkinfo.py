from typing import Optional


class NetworkInfo:
    def __init__(
            self,
            ticker: Optional[str] = None,
            chain: Optional[str] = None,
            wd_bool: Optional[bool] = None,
            min_wd: Optional[float] = None,
            max_wd: Optional[float] = None,
            min_fee: Optional[float] = None,
            max_fee: Optional[float] = None,
            precision: Optional[int] = None,
    ):
        """
        :param ticker: ticker
        :param chain: chain name, e.g. USDT-ERC20, USDT-TRC20
        :param wd_bool: availability to withdraw to chain.
        :param min_wd: minimum withdrawal amount.json of the currency in a single transaction
        :param max_wd: maximum amount.json of currency withdrawal in a single transaction
        :param min_fee: minimum withdrawal fee
        :param max_fee: maximum withdrawal fee
        :param precision: precision of a coin
        """
        self.ticker = ticker
        self.chain = chain
        self.wd_bool = wd_bool
        self.min_wd = min_wd
        self.max_wd = max_wd
        self.min_fee = min_fee
        self.max_fee = max_fee
        self.precision = precision
