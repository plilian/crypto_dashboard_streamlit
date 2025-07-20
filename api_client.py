# api_client.py (English Version)
import requests
import urllib.parse
from datetime import datetime
from collections import defaultdict
import os

# Base URL for CoinGecko API
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
# Base URL for DexScreener API
DEXSCREENER_BASE_URL = "https://api.dexscreener.com"

# --- CoinGecko API Functions ---

def fetch_search_data(query: str) -> tuple[dict | None, str | None]:
    """
    Searches for a coin by query and fetches its price details.

    Args:
        query (str): The search query for the coin.

    Returns:
        tuple[dict | None, str | None]: A tuple containing the coin data (dict)
                                         or None, and an error message (str) or None.
    """
    search_url = f"{COINGECKO_BASE_URL}/search?query={query}"
    headers = {"accept": "application/json"}
    try:
        search_response = requests.get(search_url, headers=headers)
        search_response.raise_for_status()
        search_data = search_response.json()

        if search_data.get("coins"):
            first_coin = search_data["coins"][0]
            coin_id = first_coin["api_symbol"]
            name = first_coin["name"]
            market_cap_rank = first_coin.get("market_cap_rank", "N/A")
            symbol = first_coin["symbol"]

            price_url = f"{COINGECKO_BASE_URL}/simple/price?ids={coin_id}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&precision=10"
            price_response = requests.get(price_url, headers=headers)
            price_response.raise_for_status()
            price_data = price_response.json()

            price_info = price_data.get(coin_id, {})
            usd_price = price_info.get("usd", "N/A")
            usd_market_cap = price_info.get("usd_market_cap", "N/A")
            usd_24h_vol = price_info.get("usd_24h_vol", "N/A")
            usd_24h_change = price_info.get("usd_24h_change", "N/A")

            return {
                "coin_id": coin_id,
                "name": name,
                "market_cap_rank": market_cap_rank,
                "symbol": symbol,
                "usd_price": usd_price,
                "usd_market_cap": usd_market_cap,
                "usd_24h_vol": usd_24h_vol,
                "usd_24h_change": usd_24h_change,
            }, None
        else:
            return None, "No results found for your query. Please try again."
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_trending_data() -> tuple[list | None, str | None]:
    """
    Fetches trending cryptocurrencies.

    Returns:
        tuple[list | None, str | None]: A tuple containing a list of trending coins (list of dicts)
                                         or None, and an error message (str) or None.
    """
    url = f"{COINGECKO_BASE_URL}/search/trending"
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        coins = data.get("coins", [])[:5]
        if not coins:
            return None, "No trending results available at the moment, please try again later."

        trending_coins_data = []
        for coin_data in coins:
            item = coin_data.get("item", {})
            usd_price = item.get("data", {}).get("price", "N/A")
            if isinstance(usd_price, (float, int)):
                if usd_price > 1:
                    usd_price = f"{usd_price:.2f}"
                elif 0.0001 < usd_price <= 1:
                    usd_price = f"{usd_price:.6f}"
                elif usd_price <= 0.0001:
                    usd_price = f"{usd_price:.10f}"
            else:
                usd_price = "N/A"

            trending_coins_data.append({
                "name": item.get("name", "N/A"),
                "symbol": item.get("symbol", "N/A"),
                "rank": item.get("market_cap_rank", "N/A"),
                "usd_price": usd_price,
                "market_cap": item.get("data", {}).get("market_cap", "N/A"),
                "market_cap_btc": item.get("data", {}).get("market_cap_btc", "N/A"),
                "total_volume": item.get("data", {}).get("total_volume", "N/A"),
                "total_volume_btc": item.get("data", {}).get("total_volume_btc", "N/A"),
            })
        return trending_coins_data, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_dominance_data() -> tuple[dict | None, str | None]:
    """
    Fetches global market dominance data.

    Returns:
        tuple[dict | None, str | None]: A tuple containing dominance data (dict)
                                         or None, and an error message (str) or None.
    """
    url = f"{COINGECKO_BASE_URL}/global"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("data", {})

        active_cryptocurrencies = data.get("active_cryptocurrencies", "N/A")
        market_cap_percentage = data.get("market_cap_percentage", {})
        btc_dominance = market_cap_percentage.get("btc", "N/A")
        eth_dominance = market_cap_percentage.get("eth", "N/A")
        usdt_dominance = market_cap_percentage.get("usdt", "N/A")
        market_cap_change_24h = data.get("market_cap_change_percentage_24h_usd", "N/A")

        return {
            "active_cryptocurrencies": active_cryptocurrencies,
            "btc_dominance": btc_dominance,
            "eth_dominance": eth_dominance,
            "usdt_dominance": usdt_dominance,
            "market_cap_change_24h": market_cap_change_24h,
        }, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_companies_data(coin_id: str) -> tuple[dict | None, str | None]:
    """
    Fetches public treasury data for companies holding a specific coin.

    Args:
        coin_id (str): The ID of the coin (e.g., "bitcoin", "ethereum").

    Returns:
        tuple[dict | None, str | None]: A tuple containing companies data (dict)
                                         or None, and an error message (str) or None.
    """
    url = f"{COINGECKO_BASE_URL}/companies/public_treasury/{coin_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        total_holdings = data.get("total_holdings", "N/A")
        total_value_usd = data.get("total_value_usd", "N/A")
        market_cap_dominance = data.get("market_cap_dominance", "N/A")
        companies = data.get("companies", [])[:5]

        return {
            "total_holdings": total_holdings,
            "total_value_usd": total_value_usd,
            "market_cap_dominance": market_cap_dominance,
            "companies": companies,
        }, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_categories_data() -> tuple[list | None, str | None]:
    """
    Fetches top cryptocurrency categories.

    Returns:
        tuple[list | None, str | None]: A tuple containing a list of categories (list of dicts)
                                         or None, and an error message (str) or None.
    """
    url = f"{COINGECKO_BASE_URL}/coins/categories?order=market_cap_change_24h_desc"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        top_categories = data[:3]
        return top_categories, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_coin_details_by_name(user_query: str) -> tuple[dict | None, str | None]:
    """
    Fetches coin details by name or symbol.

    Args:
        user_query (str): The name or symbol of the coin.

    Returns:
        tuple[dict | None, str | None]: A tuple containing coin details (dict)
                                         or None, and an error message (str) or None.
    """
    search_url = f"{COINGECKO_BASE_URL}/search?query={user_query}"
    try:
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        search_data = search_response.json()

        coins_list = search_data.get("coins", [])
        if not coins_list:
            return None, f"No results found for '{user_query}'. Please try another query."

        first_coin = coins_list[0]
        coin_id = first_coin.get("id", None) # Use 'id' for details API
        if not coin_id:
            return None, "Could not find a valid coin ID. Please try again."

        details_url = f"{COINGECKO_BASE_URL}/coins/{coin_id}"
        details_response = requests.get(details_url)
        details_response.raise_for_status()
        details_data = details_response.json()

        return details_data, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_coin_details_by_address(platform: str, contract_address: str) -> tuple[dict | None, str | None]:
    """
    Fetches coin details by platform and contract address.

    Args:
        platform (str): The blockchain platform (e.g., "ethereum", "solana").
        contract_address (str): The contract address of the token.

    Returns:
        tuple[dict | None, str | None]: A tuple containing coin details (dict)
                                         or None, and an error message (str) or None.
    """
    if platform not in ["ethereum", "solana"]:
        return None, "Invalid platform. Only `ethereum` and `solana` are supported."

    details_url = f"{COINGECKO_BASE_URL}/coins/{platform}/contract/{contract_address}"
    try:
        details_response = requests.get(details_url)
        details_response.raise_for_status()
        details_data = details_response.json()
        return details_data, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_ohlc_data(coin_symbol: str, days: str) -> tuple[dict | None, str | None]:
    """
    Fetches Open-High-Low-Close (OHLC) data for a coin.

    Args:
        coin_symbol (str): The symbol of the coin.
        days (str): The number of days (1, 7, or 14).

    Returns:
        tuple[dict | None, str | None]: A tuple containing OHLC data (dict)
                                         or None, and an error message (str) or None.
    """
    if days not in ["1", "7", "14"]:
        return None, "Invalid number of days! Please use 1, 7, or 14."

    encoded_query = urllib.parse.quote(coin_symbol)
    headers = {"accept": "application/json"}

    try:
        search_url = f"{COINGECKO_BASE_URL}/search?query={encoded_query}"
        search_response = requests.get(search_url, headers=headers)
        search_response.raise_for_status()
        search_data = search_response.json()

        if search_data.get("coins") and len(search_data["coins"]) > 0:
            first_coin = search_data["coins"][0]
            coin_id = first_coin.get("id")
            name = first_coin.get("name")
            if not coin_id:
                return None, f"Error: No valid coin ID found for `{coin_symbol}`."
        else:
            return None, f"No coin found matching query: {coin_symbol}."

        ohlc_url = f"{COINGECKO_BASE_URL}/coins/{coin_id}/ohlc?vs_currency=usd&days={days}"
        ohlc_response = requests.get(ohlc_url, headers=headers)
        ohlc_response.raise_for_status()
        ohlc_data = ohlc_response.json()

        if not ohlc_data:
            return None, f"No OHLC data found for {name} in the last {days} days."

        daily_bop = defaultdict(list)
        for entry in ohlc_data:
            timestamp, open_price, high_price, low_price, close_price = entry
            date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
            if high_price != low_price:
                bop = (close_price - open_price) / (high_price - low_price)
                daily_bop[date].append(bop)

        aggregated_bop = {date: sum(values) / len(values) for date, values in daily_bop.items()}
        if not aggregated_bop:
            return None, f"No valid BOP data found for {name}."

        return {"name": name, "bop_data": aggregated_bop}, None
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching OHLC data: {e}"

def fetch_market_chart_data(coin_symbol: str, days: int, interval: str) -> tuple[list | None, str | None]:
    """
    Fetches market chart data for RSI calculation.

    Args:
        coin_symbol (str): The symbol of the coin.
        days (int): The number of days for the chart data.
        interval (str): The interval (e.g., 'daily').

    Returns:
        tuple[list | None, str | None]: A tuple containing a list of prices (list of floats)
                                         or None, and an error message (str) or None.
    """
    search_url = f"{COINGECKO_BASE_URL}/search?query={coin_symbol}"
    try:
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        search_data = search_response.json()

        coins_list = search_data.get("coins", [])
        if not coins_list:
            return None, f"No results found for '{coin_symbol}'. Please try another search."

        first_coin = coins_list[0]
        coin_id = first_coin.get("id", None)
        if not coin_id:
            return None, "Could not find a valid coin ID. Please try again."

        # CG_API_KEY is not strictly necessary for public endpoints, but keeping it if it's in .env
        cg_api_key = os.getenv("CG_API_KEY")
        url = f"{COINGECKO_BASE_URL}/coins/{coin_id}/market_chart?vs_currency=usd&days={days}&interval={interval}"
        headers = {"accept": "application/json"}
        if cg_api_key:
            headers["x-cg-demo-api-key"] = cg_api_key

        chart_response = requests.get(url, headers=headers)
        chart_response.raise_for_status()
        chart_data = chart_response.json()

        prices = chart_data.get('prices', [])
        if not prices:
            return None, f"Price data not available for {coin_symbol}. Please try again later."

        closing_prices = [price[1] for price in prices]
        return closing_prices, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

# --- DexScreener API Functions ---

def fetch_top_boosted_tokens() -> tuple[list | None, str | None]:
    """
    Fetches the top boosted tokens from DexScreener.

    Returns:
        tuple[list | None, str | None]: A tuple containing a list of boosted tokens (list of dicts)
                                         or None, and an error message (str) or None.
    """
    url = f"{DEXSCREENER_BASE_URL}/token-boosts/top/v1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        top_tokens = data[:5]
        return top_tokens, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_latest_boosted_tokens() -> tuple[list | None, str | None]:
    """
    Fetches the latest boosted tokens from DexScreener.
    (Currently uses the same endpoint as top boosted, as per original code's logic)

    Returns:
        tuple[list | None, str | None]: A tuple containing a list of boosted tokens (list of dicts)
                                         or None, and an error message (str) or None.
    """
    url = f"{DEXSCREENER_BASE_URL}/token-boosts/top/v1" # Assuming latest is also from 'top' as per original
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        latest_tokens = data[:5] # Taking top 5 as "latest"
        return latest_tokens, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_token_orders(chain_id: str, token_address: str) -> tuple[list | None, str | None]:
    """
    Fetches token orders from DexScreener.

    Args:
        chain_id (str): The blockchain chain ID (e.g., "ethereum", "solana").
        token_address (str): The contract address of the token.

    Returns:
        tuple[list | None, str | None]: A tuple containing a list of orders (list of dicts)
                                         or None, and an error message (str) or None.
    """
    if chain_id not in ["ethereum", "solana"]:
        return None, "Invalid chain ID. Please use `ethereum` or `solana`."

    url = f"{DEXSCREENER_BASE_URL}/orders/v1/{chain_id}/{token_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data:
            return None, "No orders found for the specified token."
        return data, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

def fetch_trade_info(token_address: str) -> tuple[list | None, str | None]:
    """
    Fetches trade information for a given token address from DexScreener.

    Args:
        token_address (str): The contract address of the token.

    Returns:
        tuple[list | None, str | None]: A tuple containing a list of trade pairs (list of dicts)
                                         or None, and an error message (str) or None.
    """
    url = f"{DEXSCREENER_BASE_URL}/latest/dex/tokens/{token_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        pairs = data.get("pairs", [])
        if not pairs:
            return None, "No data found for the entered token address. Please try again."
        return pairs, None
    except requests.exceptions.RequestException as e:
        return None, f"An error occurred while fetching data: {e}"

