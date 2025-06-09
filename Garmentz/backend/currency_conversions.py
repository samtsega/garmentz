import requests

# API base URL (for example, using a public currency conversion API like ExchangeRate-API or a similar service)
API_URL = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_AtcpIMpdjpbOFPPzF4Vpg7z2FdJSJOzimoO5jC77"

def get_conversion_rate(base_currency, target_currency):
    """ Fetch the conversion rate from base_currency to target_currency using an API.
    Args: base_currency (str): The currency to convert from (e.g., 'USD'). target_currency (str): The currency to convert to (e.g., 'EUR').
    Returns: float: Conversion rate from base_currency to target_currency. """
    try:
        # Build the request URL
        url = f"{API_URL}{base_currency}"
        response = requests.get(url)

        # Check if the request was successful

        if response.status_code == 200:
            data = response.json()
             # Extract the conversion rate
            rates = data['rates']
            if target_currency in rates: return rates[target_currency]
            else:
                raise (
        ValueError(f"Conversion rate not found for currency: {target_currency}"))
        else: response.raise_for_status()
    except Exception as e:
        print(f"Error fetching conversion rate: {e}")
        return None

def convert_currency(amount, base_currency, target_currency):
    """ Convert an amount from one currency to another.
    Args: amount (float): The amount to be converted. base_currency (str): The currency to convert from (e.g., 'USD'). target_currency (str): The currency to convert to (e.g., 'EUR').
    Returns: float: Converted amount in the target currency. """
    rate = get_conversion_rate(base_currency, target_currency)
    if rate:
        return amount * rate
    else: return None