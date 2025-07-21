import streamlit as st
import commands
import utils

st.set_page_config(
    page_title="Pumpies Crypto Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="st-"] {{
        font-family: 'Inter', sans-serif;
        color: #000000;
    }}

    .main {{
        background-color: #e0f2f7;
        padding: 20px;
        border-radius: 10px;
    }}
    .stApp {{
        background-color: #1a1a2e;
    }}

    /* Layout and Padding Fixes */
    .block-container {{
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }}

    div[data-testid^="st"] {{
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    [data-testid="stHorizontalBlock"],
    [data-testid="stVerticalBlock"],
    [data-testid="stColumn"],
    [data-testid="stForm"],
    [data-testid="stContainer"]
    {{
        width: 100% !important;
        max-width: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    [data-testid="stMarkdownContainer"],
    [data-testid="stText"] {{
        width: 100% !important;
        max-width: none !important;
        padding: 0 !important;
        margin: 0 !important;
        word-break: break-word;
        overflow-wrap: break-word;
    }}

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stText"] p,
    p {{
        max-width: none !important;
        width: 100% !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        padding: 0 !important;
    }}

    .stAlert {{
        border-radius: 8px;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        width: 100% !important;
        max-width: none !important;
    }}
    /* End Layout and Padding Fixes */

    .sidebar .sidebar-content {{
        background-color: #000000;
        color: #000000;
    }}
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {{
        color: #000000;
    }}
    .stRadio > label {{
        color: #000000;
    }}
    .stRadio [data-testid="stRadio"] > div > label {{
        color: #000000;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: #e94560;
        text-align: left;
    }}

    .stButton>button {{
        background-color: #a7d9e8;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stButton>button:hover {{
        background-color: #7bc6e0;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }}

    .stTextInput>div>div>input,
    .stSelectbox>div>div>div {{
        background-color: #16213e;
        color: #e0e0e0;
        border-radius: 8px;
        border: 1px solid #533483;
        padding: 10px;
    }}
    .stSelectbox > div[data-baseweb="select"] ul {{
        background-color: #16213e;
        color: #e0e0e0;
    }}
    .stSelectbox > div[data-baseweb="select"] li:hover {{
        background-color: #0f3460;
    }}

    .stCode {{
        background-color: #16213e;
        border-radius: 8px;
        padding: 15px;
    }}
    .stExpander {{
        background-color: #16213e;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }}
    .stExpander > div > div > p {{
        color: #e0e0e0;
    }}

    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #16213e;
        color: #e0e0e0;
        text-align: center;
        padding: 10px 0;
        font-size: 0.9em;
    }}
    .footer a {{
        color: #e94560;
        text-decoration: none;
    }}
    .footer a:hover {{
        text-decoration: underline;
    }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("📈 Pumpies Crypto Dashboard")
st.markdown("Welcome to the comprehensive Pumpies Crypto Dashboard! Use the tools below to get real-time market information.")

st.sidebar.header("Commands")
command_choice = st.sidebar.radio(
    "Choose a command:",
    (
        "Introduction",
        "Search Coin",
        "Trending Coins",
        "Market Dominance",
        "Companies Holdings",
        "Coin Categories",
        "Coin Details (by Name)",
        "Coin Details (by Address)",
        "Balance of Power (BOP)",
        "Relative Strength Index (RSI)",
        "Top Boosted Tokens",
        "Latest Boosted Tokens",
        "Token Orders",
        "Trade Info"
    ),
    index=0
)

coin_name_translations = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum"
}

if command_choice == "Introduction":
    commands.display_introduction()

elif command_choice == "Search Coin":
    commands.display_search_coin()

elif command_choice == "Trending Coins":
    commands.display_trending_coins()

elif command_choice == "Market Dominance":
    commands.display_market_dominance()

elif command_choice == "Companies Holdings":
    commands.display_companies_holdings(coin_name_translations)

elif command_choice == "Coin Categories":
    commands.display_coin_categories()

elif command_choice == "Coin Details (by Name)":
    commands.display_coin_details_by_name()

elif command_choice == "Coin Details (by Address)":
    commands.display_coin_details_by_address()

elif command_choice == "Balance of Power (BOP)":
    commands.display_bop()

elif command_choice == "Relative Strength Index (RSI)":
    commands.display_rsi()

elif command_choice == "Top Boosted Tokens":
    commands.display_top_boosted_tokens()

elif command_choice == "Latest Boosted Tokens":
    commands.display_latest_boosted_tokens()

elif command_choice == "Token Orders":
    commands.display_token_orders()

elif command_choice == "Trade Info":
    commands.display_trade_info()

st.markdown(
    """
    <div class='footer'>
        Developer: Parham Lilian
        <br>
        Instagram: <a href='https://instagram.com/parhamlilian' target='_blank' style='color: #e94560;'>@parhamlilian</a>
        <br>
        LinkedIn: <a href='https://www.linkedin.com/in/parhamlilian' target='_blank' style='color: #e94560;'>linkedin.com/in/parhamlilian</a>
    </div>
    """, unsafe_allow_html=True
)
