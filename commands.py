# commands.py

import streamlit as st
import utils
import pandas as pd
from datetime import datetime
import uuid

class DummyAPIClient:
    def __getattr__(self, name):
        def dummy(*args, **kwargs):
            return None, f"[Dummy] Skipped {name}"
        return dummy

api_client = DummyAPIClient()

# --- Helper for company coin display (moved here for modularity)
coin_name_translations = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum"
}

def display_introduction():
    st.header("👋 Welcome to Pumpies!")
    st.markdown(
        """
        I'm here to help you stay updated with the latest cryptocurrency information.
        You can use the menu on the left to access my features.
        """
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(
            "<div style='text-align: center;'>",
            unsafe_allow_html=True
        )
        st.image("https://i.postimg.cc/Hn4j9GKB/photo-2024-12-21-15-21-12.jpg", width=250)
        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )
    st.markdown("<div style='margin-top: 20px; margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        💡 Command Descriptions:

        * Search Coin: Pick this to search for a crypto and get basic info like its name, symbol, and market rank.
        * Trending Coins: Choose this to see a list of cryptocurrencies that are currently trending based on market activity.
        * Market Dominance: This shows how much of the market big cryptos like Bitcoin and Ethereum control.
        * Companies Holdings: Get info on companies that hold a lot of specific cryptocurrencies (like Bitcoin or Ethereum).
        * Coin Categories: Shows the top 3 crypto categories based on how their market cap changed in the last 24 hours.
        * Coin Details (by Name): Get detailed info about a coin just by typing its name.
        * Coin Details (by Address): Get detailed info about a coin using its contract address (works for Solana or Ethereum).
        * Balance of Power (BOP): Calculates the BOP for a crypto over 1, 7, or 14 days. It's about buy/sell pressure.
        * Relative Strength Index (RSI): Calculates the RSI for a crypto over the last 14 days. Helps see if it's overbought or oversold.
        * Top Boosted Tokens: See which tokens are getting the most "boosts" on DexScreener.
        * Latest Boosted Tokens: Check out the newest tokens that have been boosted on DexScreener.
        * Token Orders: Get details about token orders for Ethereum or Solana.
        * Trade Info: This gives you trading data for a token, like price, volume, and recent transactions.

        Got questions or need more help? Just ask! ☺️
        """
    )

def display_search_coin():
    st.header("🔎 Search for a Coin")
    coin_query = st.text_input("Enter coin name or symbol (e.g., bitcoin, btc)", key="search_input")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Search"):
            if coin_query:
                utils.log_command_usage("/search", coin_query)
                with st.spinner(f"Searching for {coin_query}..."):
                    data, error = api_client.fetch_search_data(coin_query)
                    if data:
                        st.success("Search results found!")
                        st.markdown(f"""
                            🔎 Search Results
                            - ID: `{data['coin_id']}`
                            - Name: *{data['name']}*
                            - Market Rank: #{data['market_cap_rank']}
                            - Symbol: `{data['symbol'].upper()}`

                            Price Details (USD):
                            - Current Price: `${data['usd_price']:,.10f}`
                            - Market Cap: `${data['usd_market_cap']:,.2f}`
                            - 24h Trading Volume: `${data['usd_24h_vol']:,.2f}`
                            - 24h Change: `{data['usd_24h_change']:.2f}%`
                        """)
                    else:
                        st.error(error)
            else:
                st.warning("Please enter a coin name or symbol to search.")

def display_trending_coins():
    st.header("🔥 Trending Cryptocurrencies")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Trending Coins"):
            utils.log_command_usage("/trending", "")
            with st.spinner("Fetching trending coins..."):
                data, error = api_client.fetch_trending_data()
                if data:
                    st.success("Trending coins fetched successfully!")
                    message = "🔥 Trending Tokens:\n\n"
                    for coin in data:
                        message += (
                            f"- Name: *{coin['name']}*\n"
                            f"- Symbol: `{coin['symbol'].upper()}`\n"
                            f"- Rank: #{coin['rank']}\n"
                            f"- Current Price: `${coin['usd_price']}`\n"
                            f"- Market Cap: `{coin['market_cap']}`\n"
                            f"- Market Cap (BTC): `{coin['market_cap_btc']} BTC`\n"
                            f"- Total Volume (USD): `{coin['total_volume']}`\n"
                            f"- Total Volume (BTC): `{coin['total_volume_btc']} BTC`\n"
                            "---------------------------\n"
                        )
                    st.markdown(message)
                else:
                    st.error(error)

def display_market_dominance():
    st.header("📊 Crypto Market Dominance")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Dominance Data"):
            utils.log_command_usage("/dominance", "")
            with st.spinner("Fetching market dominance data..."):
                data, error = api_client.fetch_dominance_data()
                if data:
                    st.success("Market dominance data fetched successfully!")
                    st.markdown(f"""
                        📊 Crypto Market Dominance
                        - Active Cryptocurrencies: `{data['active_cryptocurrencies']}`
                        - BTC Dominance: `{data['btc_dominance']:.2f}%`
                        - ETH Dominance: `{data['eth_dominance']:.2f}%`
                        - USDT Dominance: `{data['usdt_dominance']:.2f}%`
                        - 24h Market Cap Change: `{data['market_cap_change_24h']:.2f}%`
                    """)
                else:
                    st.error(error)

def display_companies_holdings(coin_translations):
    st.header("🏦 Companies Public Treasury Holdings")
    company_coin_choice = st.selectbox(
        "Select Coin:",
        ("bitcoin", "ethereum"),
        key="company_coin_select"
    )
    translated_coin_name = coin_translations.get(company_coin_choice, company_coin_choice.capitalize())
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Companies Data"):
            utils.log_command_usage("/companies", company_coin_choice)
            with st.spinner(f"Fetching companies holding {translated_coin_name}..."):
                data, error = api_client.fetch_companies_data(company_coin_choice)
                if data:
                    st.success(f"Companies holding {translated_coin_name} fetched successfully!")
                    message = (
                        f"🏦 Companies Holding {translated_coin_name} 🏦\n"
                        f"- Total Holdings: `{data['total_holdings']}`\n"
                        f"- Total Value (USD): `${data['total_value_usd']:,.2f}`\n"
                        f"- Market Cap Dominance: `{data['market_cap_dominance']}%`\n\n"
                        f"Top Companies:\n\n"
                    )
                    for company in data['companies']:
                        message += (
                            f"- Name: *{company.get('name', 'N/A')}* ({company.get('symbol', 'N/A')})\n"
                            f"- Country: `{company.get('country', 'N/A')}`\n"
                            f"- Holdings: `{company.get('total_holdings', 'N/A')}`\n"
                            f"- Current Value (USD): `${company.get('total_current_value_usd', 'N/A'):,.2f}`\n"
                            f"- % of Total Supply: `{company.get('percentage_of_total_supply', 'N/A')}%`\n"
                            "---------------------------\n"
                        )
                    st.markdown(message)
                else:
                    st.error(error)

def display_coin_categories():
    st.header("🏅 Top Coin Categories")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Categories"):
            utils.log_command_usage("/categories", "")
            with st.spinner("Fetching top coin categories..."):
                data, error = api_client.fetch_categories_data()
                if data:
                    st.success("Coin categories fetched successfully!")
                    message = "🏅 Top 3 Coin Categories (by 24h Market Cap Change) 🏅\n\n"
                    for category in data:
                        name = category.get("name", "N/A")
                        market_cap = category.get("market_cap", 0)
                        market_cap_change = category.get("market_cap_change_24h", 0)
                        top_3_coins_id = category.get("top_3_coins_id", [])

                        message += (
                            f"- Category Name: `{name}`\n"
                            f"- Market Cap: `${market_cap:,.2f}`\n"
                            f"- 24h Change: `{market_cap_change:.2f}%`\n"
                            f"- Top 3 Tokens: `{', '.join(top_3_coins_id) if top_3_coins_id else 'N/A'}`\n"
                            "------------------------------------\n"
                        )
                    st.markdown(message)
                else:
                    st.error(error)

def display_coin_details_by_name():
    st.header("🪙 Coin Details by Name/Symbol")
    coin_name_query = st.text_input("Enter coin name or symbol (e.g., btc, ethereum)", key="coin_details_name_input")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Details by Name"):
            if coin_name_query:
                utils.log_command_usage("/coin_details_name", coin_name_query)
                with st.spinner(f"Fetching details for {coin_name_query}..."):
                    data, error = api_client.fetch_coin_details_by_name(coin_name_query)
                    if data:
                        st.success(f"Details for {coin_name_query} fetched successfully!")
                        description = data.get("description", {}).get("en", "No description available.")
                        truncated_description = description[:500] + "..." if len(description) > 500 else description

                        tickers = data.get("tickers", [])
                        first_ticker_info = {}
                        if tickers:
                            first_ticker = tickers[0]
                            first_ticker_info = {
                                "base": first_ticker.get("base"),
                                "target": first_ticker.get("target"),
                                "market_name": first_ticker.get("market", {}).get("name"),
                                "converted_last_usd": first_ticker.get("converted_last", {}).get("usd"),
                                "converted_volume_usd": first_ticker.get("converted_volume", {}).get("usd"),
                                "trust_score": first_ticker.get("trust_score"),
                                "trade_url": first_ticker.get("trade_url"),
                            }

                        st.markdown(f"""
                            🪙 Coin Details 🪙

                            - Name: `{data.get('name')} ({data.get('symbol', '').upper()})`
                            - Platform: `{data.get('asset_platform_id', 'N/A')}`

                            - Sentiment Upvotes: `{data.get('sentiment_votes_up_percentage', 'N/A')}%`
                            - Sentiment Downvotes: `{data.get('sentiment_votes_down_percentage', 'N/A')}%`
                            - Watchlist Users: `{data.get('watchlist_portfolio_users', 'N/A')}`

                            Description: {truncated_description}

                            Market Information 📊

                            - Current Price (USD): `${data.get('market_data', {}).get('current_price', {}).get('usd', 0):,.4f}`
                            - Total Supply (#): `{data.get('market_data', {}).get('total_supply', 'N/A')}`
                            - Max Supply (#): `{data.get('market_data', {}).get('max_supply', 'N/A')}`
                            - Circulating Supply (#): `{data.get('market_data', {}).get('circulating_supply', 'N/A')}`
                            - Market Cap (USD): `${data.get('market_data', {}).get('market_cap', {}).get('usd', 0):,.2f}`
                            - All-Time High (USD): `${data.get('market_data', {}).get('ath', {}).get('usd', 0):,.8f}`
                            - All-Time Low (USD): `${data.get('market_data', {}).get('atl', {}).get('usd', 0):,.8f}`
                            - 24h Price Change: `{data.get('market_data', {}).get('price_change_percentage_24h', 0):.4f}%`

                            🏛️ Top Exchange Information 🏛️

                            - Exchange Name: `{first_ticker_info.get('market_name', 'N/A')}`
                            - Base - Token Address: `{first_ticker_info.get('base', 'N/A')}`
                            - Target Token Address: `{first_ticker_info.get('target', 'N/A')}`
                            - Last Price (USD): `${first_ticker_info.get('converted_last_usd', 0):,.8f}`
                            - Volume (USD): `${first_ticker_info.get('converted_volume_usd', 0):,.2f}`
                            - Trust Score (Exchange): `{first_ticker_info.get('trust_score', 'N/A')}`
                            {f"- [Trade Now]({first_ticker_info['trade_url']})" if first_ticker_info.get('trade_url') else ""}
                        """)
                    else:
                        st.error(error)
            else:
                st.warning("Please enter a coin name or symbol.")

def display_coin_details_by_address():
    st.header("🪙 Coin Details by Contract Address")
    platform_address = st.selectbox(
        "Select Platform:",
        ("ethereum", "solana"),
        key="platform_address_select"
    )
    contract_address_input = st.text_input("Enter Contract Address (e.g., 0x...)", key="contract_address_input")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Details by Address"):
            if contract_address_input:
                utils.log_command_usage("/coin_details_address", f"{platform_address} {contract_address_input}")
                with st.spinner(f"Fetching details for {contract_address_input} on {platform_address}..."):
                    data, error = api_client.fetch_coin_details_by_address(platform_address, contract_address_input)
                    if data:
                        st.success(f"Details for {contract_address_input} fetched successfully!")
                        description = data.get("description", {}).get("en", "No description available.")
                        truncated_description = description[:500] + "..." if len(description) > 500 else description

                        tickers = data.get("tickers", [])
                        first_ticker_info = {}
                        if tickers:
                            first_ticker = tickers[0]
                            first_ticker_info = {
                                "base": first_ticker.get("base"),
                                "target": first_ticker.get("target"),
                                "market_name": first_ticker.get("market", {}).get("name"),
                                "converted_last_usd": first_ticker.get("converted_last", {}).get("usd"),
                                "converted_volume_usd": first_ticker.get("converted_volume", {}).get("usd"),
                                "trust_score": first_ticker.get("trust_score"),
                                "trade_url": first_ticker.get("trade_url"),
                            }

                        st.markdown(f"""
                            🪙 Coin Details 🪙

                            - Name: `{data.get('name')} ({data.get('symbol', '').upper()})`
                            - Platform: `{data.get('asset_platform_id', 'N/A')}`

                            - Sentiment Upvotes: `{data.get('sentiment_votes_up_percentage', 'N/A')}%`
                            - Sentiment Downvotes: `{data.get('sentiment_votes_down_percentage', 'N/A')}%`
                            - Watchlist Users: `{data.get('watchlist_portfolio_users', 'N/A')}`

                            Description: {truncated_description}

                            Market Information 📊

                            - Current Price (USD): `${data.get('market_data', {}).get('current_price', {}).get('usd', 0):,.4f}`
                            - Total Supply (#): `{data.get('market_data', {}).get('total_supply', 'N/A')}`
                            - Max Supply (#): `{data.get('market_data', {}).get('max_supply', 'N/A')}`
                            - Circulating Supply (#): `{data.get('market_data', {}).get('circulating_supply', 'N/A')}`
                            - Market Cap (USD): `${data.get('market_data', {}).get('market_cap', {}).get('usd', 0):,.2f}`
                            - All-Time High (USD): `${data.get('market_data', {}).get('ath', {}).get('usd', 0):,.8f}`
                            - All-Time Low (USD): `${data.get('market_data', {}).get('atl', {}).get('usd', 0):,.8f}`
                            - 24h Price Change: `{data.get('market_data', {}).get('price_change_percentage_24h', 0):.4f}%`

                            🏛️ Top Exchange Information 🏛️

                            - Exchange Name: `{first_ticker_info.get('market_name', 'N/A')}`
                            - Base - Token Address: `{first_ticker_info.get('base', 'N/A')}`
                            - Target Token Address: `{first_ticker_info.get('target', 'N/A')}`
                            - Last Price (USD): `${first_ticker_info.get('converted_last_usd', 0):,.8f}`
                            - Volume (USD): `${first_ticker_info.get('converted_volume_usd', 0):,.2f}`
                            - Trust Score (Exchange): `{first_ticker_info.get('trust_score', 'N/A')}`
                            {f"- [Trade Now]({first_ticker_info['trade_url']})" if first_ticker_info.get('trade_url') else ""}
                        """)
                    else:
                        st.error(error)
            else:
                st.warning("Please enter a contract address.")

def display_bop():
    st.header("📊 Balance of Power (BOP)")
    bop_coin_symbol = st.text_input("Enter coin symbol (e.g., btc)", key="bop_coin_input")
    bop_days = st.selectbox("Select days:", ("1", "7", "14"), key="bop_days_select")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Calculate BOP"):
            if bop_coin_symbol:
                utils.log_command_usage("/bop", f"{bop_coin_symbol} {bop_days}")
                with st.spinner(f"Calculating BOP for {bop_coin_symbol} over {bop_days} days..."):
                    data, error = api_client.fetch_ohlc_data(bop_coin_symbol, bop_days)
                    if data:
                        st.success(f"BOP for {bop_coin_symbol} calculated successfully!")
                        message = f"📊 Overall Buy/Sell Pressure (BOP) for {data['name']} ({bop_days}-day OHLC):\n\n"
                        for date, avg_bop in sorted(data['bop_data'].items()):
                            pressure = "🔼 Buy Pressure" if avg_bop > 0 else "🔽 Sell Pressure"
                            message += f"- {date}: `{avg_bop:.4f}` {pressure}\n"
                        st.markdown(message)
                    else:
                        st.error(error)
            else:
                st.warning("Please enter a coin symbol.")

def display_rsi():
    st.header("📉 Relative Strength Index (RSI)")
    rsi_coin_symbol = st.text_input("Enter coin symbol (e.g., btc)", key="rsi_coin_input")
    rsi_days = st.slider("Select days (1-14):", 1, 14, 14, key="rsi_days_slider")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Calculate RSI"):
            if rsi_coin_symbol:
                utils.log_command_usage("/rsi", f"{rsi_coin_symbol} {rsi_days}d")
                with st.spinner(f"Calculating RSI for {rsi_coin_symbol} over {rsi_days} days..."):
                    interval_type = 'daily'
                    prices, error = api_client.fetch_market_chart_data(rsi_coin_symbol, rsi_days, interval_type)
                    if prices:
                        total_rsi = utils.calculate_rsi(prices, period=rsi_days)
                        total_rsi_interpretation = utils.interpret_rsi(total_rsi)
                        st.success(f"RSI for {rsi_coin_symbol} calculated successfully!")
                        st.markdown(f"""
                            📉 Relative Strength Index (RSI) for *{rsi_coin_symbol.upper()}* (Last {rsi_days} days):

                            - 🔸 RSI: *{total_rsi:.2f}* {total_rsi_interpretation}

                            *Note: RSI is an indicator used to identify momentum strength, used to evaluate whether an asset is overbought (>70) or oversold (<30).*

                            *🔄 RSI between 30 and 70 indicates neutral market conditions.*
                        """)
                    else:
                        st.error(error)
            else:
                st.warning("Please enter a coin symbol.")

def display_top_boosted_tokens():
    st.header("🔥 Top Boosted Tokens (DexScreener)")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Top Boosted Tokens"):
            utils.log_command_usage("/top_boosted_tokens", "")
            with st.spinner("Fetching top boosted tokens..."):
                data, error = api_client.fetch_top_boosted_tokens()
                if data:
                    st.success("Top boosted tokens fetched successfully!")
                    message = "🔥 Top Boosted Tokens on DexScreener 🔥\n\n"
                    for token in data:
                        links_message = ""
                        for link in token.get("links", []):
                            link_type = link.get("type", link.get("label", "Unknown"))
                            link_url = link.get("url", "N/A")
                            links_message += f"  - {link_type.capitalize()}: [Link]({link_url})\n"

                        message += (
                            f"- Token Address on DexScreener: [Link]({token.get('url', 'N/A')})\n"
                            f"- Platform: `{token.get('chainId', 'N/A')}`\n"
                            f"- Token Address: `{token.get('tokenAddress', 'N/A')}`\n\n"
                            f"Description: {token.get('description', 'No description available')}\n\n"
                            f"Links:\n{links_message}\n"
                            "---------------------------\n"
                        )
                    st.markdown(message)
                else:
                    st.error(error)

def display_latest_boosted_tokens():
    st.header("🔥 Latest Boosted Tokens (DexScreener)")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Latest Boosted Tokens"):
            utils.log_command_usage("/latest_boosted_tokens", "")
            with st.spinner("Fetching latest boosted tokens..."):
                data, error = api_client.fetch_latest_boosted_tokens()
                if data:
                    st.success("Latest boosted tokens fetched successfully!")
                    message = "🔥 Latest Boosted Tokens on DexScreener 🔥\n\n"
                    for token in data:
                        links_message = ""
                        for link in token.get("links", []):
                            link_type = link.get("type", link.get("label", "Unknown"))
                            link_url = link.get("url", "N/A")
                            links_message += f"  - {link_type.capitalize()}: [Link]({link_url})\n"

                        message += (
                            f"- Token Address on DexScreener: [Link]({token.get('url', 'N/A')})\n"
                            f"- Platform: `{token.get('chainId', 'N/A')}`\n"
                            f"- Token Address: `{token.get('tokenAddress', 'N/A')}`\n\n"
                            f"Description: {token.get('description', 'No description available')}\n\n"
                            f"Links:\n{links_message}\n"
                            "---------------------------\n"
                        )
                    st.markdown(message)
                else:
                    st.error(error)

def display_token_orders():
    st.header("📋 Token Orders (DexScreener)")
    token_order_chain_id = st.selectbox(
        "Select Chain ID:",
        ("ethereum", "solana"),
        key="token_order_chain_select"
    )
    token_order_address = st.text_input("Enter Token Address:", key="token_order_address_input")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Token Orders"):
            if token_order_address:
                utils.log_command_usage("/token_orders", f"{token_order_chain_id} {token_order_address}")
                with st.spinner(f"Fetching token orders for {token_order_address} on {token_order_chain_id}..."):
                    data, error = api_client.fetch_token_orders(token_order_chain_id, token_order_address)
                    if data:
                        st.success("Token orders fetched successfully!")
                        message = f"📋 Token Orders on DexScreener\n"
                        message += (
                            f"- Chain: `{token_order_chain_id}`\n"
                            f"- Token Address: `{token_order_address}`\n\n"
                        )
                        type_mapping = {
                            "tokenProfile": "Token Profile added to Dex Screener",
                            "communityTakeover": "Community Takeover",
                            "tokenAd": "Ad on Dex Screener",
                            "trendingBarAd": "Trending Bar Ad on Dex Screener"
                        }
                        for order in data:
                            order_type = order.get("type", "Unknown")
                            status = order.get("status", "Unknown")
                            timestamp = order.get("paymentTimestamp", 0)
                            datetime_str = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")

                            message += (
                                f"- Type: `{type_mapping.get(order_type, order_type)}`\n"
                                f"- Status: `{status.capitalize()}`\n"
                                f"- Date/Time: `{datetime_str}`\n"
                                "------------------------------------\n"
                            )
                        st.markdown(message)
                    else:
                        st.error(error)
            else:
                st.warning("Please enter a token address.")

def display_trade_info():
    st.header("📊 Trade Info (DexScreener)")
    trade_info_token_address = st.text_input("Enter Token Address:", key="trade_info_token_address_input")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Get Trade Info"):
            if trade_info_token_address:
                utils.log_command_usage("/trade_info", trade_info_token_address)
                with st.spinner(f"Fetching trade info for {trade_info_token_address}..."):
                    data, error = api_client.fetch_trade_info(trade_info_token_address)
                    if data:
                        st.success("Trade info fetched successfully!")
                        message = f"📊 Trade History for {trade_info_token_address} 📊\n\n"
                        for pair in data:
                            txns_message = "\n".join(
                                [
                                    f"- {key}: Buys: `{value.get('buys', 0)}`, Sells: `{value.get('sells', 0)}`"
                                    for key, value in pair.get("txns", {}).items()
                                ]
                            )
                            volume_message = "\n".join(
                                [f"- {key}: `${value:,.2f}`" for key, value in pair.get("volume", {}).items()]
                            )
                            price_change_message = "\n".join(
                                [f"- {key}: `{value:.2f}%`" for key, value in pair.get("priceChange", {}).items()]
                            )

                            message += (
                                f"- Dex: `{pair.get('dexId', 'N/A')}`\n"
                                f"- DEX Screener Link: [Link]({pair.get('url', 'N/A')})\n"
                                f"- Pair Address: `{pair.get('pairAddress', 'N/A')}`\n"
                                f"- Base Token - Quote Token: `{pair.get('baseToken', {}).get('symbol', 'N/A')} / {pair.get('quoteToken', {}).get('symbol', 'N/A')}`\n"
                                f"- Price (Native): `{pair.get('priceNative', 'N/A')}`\n"
                                f"- Price (USD): `${pair.get('priceUsd', 'N/A')}`\n\n"
                                f"Transactions:\n{txns_message}\n\n"
                                f"Volume (USD):\n{volume_message}\n\n"
                                f"Price Change (%):\n{price_change_message}\n\n"
                                f"- Liquidity (USD): `${pair.get('liquidity', {}).get('usd', 0):,.2f}`\n"
                                f"- Market Cap: `${pair.get('marketCap', 'N/A')}`\n"
                                f"- FDV: `${pair.get('fdv', 'N/A')}`\n"
                                f"- Active Boosts: `{pair.get('boosts', {}).get('active', 'N/A')}`\n"
                                "---------------------------\n"
                            )
                        st.markdown(message)
                    else:
                        st.error(error)
            else:
                st.warning("Please enter a token address.")
