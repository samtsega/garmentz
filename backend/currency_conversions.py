import requests

# API base URL - for Free Currency API (replace with your own API key)
API_URL = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_AtcpIMpdjpbOFPPzF4Vpg7z2FdJSJOzimoO5jC77"

def get_conversion_rate(base_currency, target_currency):
    """
    Fetch the conversion rate from base_currency to target_currency using the API.
    
    Args:
        base_currency (str): Currency to convert from (e.g., 'USD')
        target_currency (str): Currency to convert to (e.g., 'EUR')
    
    Returns:
        float or None: Conversion rate, or None if failed
    """
    try:
        # The API expects base currency as a query param, not in the URL path
        # So we include base_currency as the "base_currency" param
        url = f"{API_URL}&base_currency={base_currency.upper()}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        rates = data.get('data')  # FreeCurrencyAPI returns rates under 'data'

        if not rates:
            raise ValueError("No rates data in response")

        rate = rates.get(target_currency.upper())
        if rate is None:
            raise ValueError(f"Conversion rate not found for currency: {target_currency}")
        return rate

    except Exception as e:
        print(f"Error fetching conversion rate: {e}")
        return None


def convert_currency(amount, base_currency, target_currency):
    """
    Convert an amount from base_currency to target_currency.
    
    Args:
        amount (float): Amount to convert
        base_currency (str): Currency to convert from
        target_currency (str): Currency to convert to
    
    Returns:
        float or None: Converted amount or None if conversion failed
    """
    rate = get_conversion_rate(base_currency, target_currency)
    if rate is not None:
        return round(amount * rate, 2)
    else:
        return None
