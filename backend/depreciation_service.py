class DepreciationService:
    def __init__(self):
        self.depreciation_rates = {
            'heavily worn': 0.80,   # 80% loss
            'lightly worn': 0.40,   # 40% loss
            'not worn': 0.10        # 10% loss
        }

    def calculate(self, condition: str, original_price: float = 100.0) -> float:
        """
        Returns depreciated value based on general condition category.
        """
        rate = self.depreciation_rates.get(condition.lower(), 0.5)
        depreciated_price = original_price * (1 - rate)
        return round(depreciated_price, 2)

    def calculate_depreciation(self, brand, fabric, age_years, wear_level_score) -> float:
        """
        Rule-based depreciation score from multiple item attributes.
        Returns a float between 0 and 1 representing depreciation factor.
        """
        brand_score = 0.8 if brand.lower() in ['gucci', 'prada', 'lv'] else 0.6
        fabric_score = 0.9 if fabric.lower() in ['leather', 'wool'] else 0.7
        age_score = max(0, 1 - (age_years / 10))  # 10% value loss per year
        wear_score = 1 - wear_level_score         # Lower score = more depreciation

        depreciation = brand_score * fabric_score * age_score * wear_score
        return round(depreciation, 3)
