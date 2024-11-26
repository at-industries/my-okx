from typing import Optional


class AssetBalance:
    def __init__(
            self, ticker: Optional[str] = None,
            balance: Optional[float] = None,
            avail_bal: Optional[float] = None,
            frozen_bal: Optional[float] = None,
    ):
        self.ticker = ticker
        self.balance = balance
        self.avail_bal = avail_bal
        self.frozen_bal = frozen_bal
