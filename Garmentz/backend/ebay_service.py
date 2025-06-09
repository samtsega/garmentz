class EbayService:
    def __init__(self):
        pass

    def get_price_estimate(self, condition: str) -> dict:
        """
        Returns a mocked price estimate based on condition.
        Replace this with real API logic using eBay's Finding API.
        """
        mock_prices = {
            'heavily worn': {'min': 10, 'avg': 15, 'max': 20},
            'lightly worn': {'min': 25, 'avg': 35, 'max': 45},
            'not worn': {'min': 50, 'avg': 65, 'max': 80}
        }
        return mock_prices.get(condition.lower(), {'min': 20, 'avg': 30, 'max': 40})
