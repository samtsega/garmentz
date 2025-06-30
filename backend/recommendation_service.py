class RecommendationService:
    def __init__(self):
        pass

    def get_recommendations(self, condition: str) -> list:
        """
        Placeholder logic for product or resale platform recommendations.
        """
        recommendations = {
            'heavily worn': [
                'Try recycling via local programs',
                'Consider donation drop-off services'
            ],
            'lightly worn': [
                'Sell on Depop or Facebook Marketplace',
                'Bundle with other clothes for higher value'
            ],
            'not worn': [
                'Sell on Vestiaire or eBay',
                'Mark as "new with tags" to increase price'
            ]
        }
        return recommendations.get(condition.lower(), ['No recommendations available'])
