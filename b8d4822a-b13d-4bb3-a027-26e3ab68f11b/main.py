from surmount.base_class import Strategy, TargetAllocation
from surmount.data import CboeVolatilityIndexVix
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Assets to trade: Here, 'QQQ' represents tech-heavy Nasdaq
        # You might need a proxy or equivalent for actual VIX trading if desired.
        self.tickers = ["QQQ"]
        # Adding VIX data to the strategy's data list for monitoring market volatility.
        self.data_list = [CboeVolatilityIndexVix()]

    @property
    def interval(self):
        # Using daily data to assess market conditions.
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        try:
            # Accessing the most recent VIX value from the data provided.
            vix_value = data[("cboe_volatility_index_vix",)][-1]['value']
            log(f"VIX Value: {vix_value}")

            if vix_value < 15:
                # Low VIX value (<15) suggesting low market volatility (complacency).
                # Choosing a high-risk approach by allocating a substantial portion to QQQ.
                allocation = {"QQQ": 1.0}  # Going all-in on QQQ.
            elif vix_value > 30:
                # High VIX value (>30) indicating high market fear and potential downturns.
                # Taking a defensive stance by not holding QQQ.
                allocation = {"QQQ": 0}  # Moving to cash or cash equivalents.
            else:
                # For VIX values between 15 and 30, maintaining a balanced approach.
                allocation = {"QQQ": 0.5}  # Half in QQQ and half in cash or equivalents.
        except Exception as e:
            log(f"Error retrieving VIX value or allocating assets: {e}")
            allocation = {"QQQ": 0}  # Default to a defensive position in case of data access issues.

        return TargetAllocation(allocation)