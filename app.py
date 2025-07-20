import streamlit as st
import commands
import utils

st.set_page_config(
    page_title="Pumpies Crypto Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0; /* Light text on dark background */
    }
    .main {
        background-color: #1a1a2e; /* Main content area background */
        padding: 20px;
        border-radius: 10px;
    }
    .stApp {
        background-color: #1a1a2e; /* Whole app background */
    }
    .sidebar .sidebar-content {
        background-color: #16213e; /* Sidebar background, slightly different */
        color: #e0e0e0;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #e94560; /* Accent color for titles */
        text-align: left; # Standard left alignment
    }
    .stButton>button {
        background-color: #0f3460; /* Button color */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #533483; /* Button hover effect */
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .stTextInput>div>div>input {
        background-color: #0f3460; /* Input field styling */
        color: #e0e0e0;
        border-radius: 8px;
        border: 1px solid #533483;
        padding: 10px;
    }
    .stSelectbox>div>div>div {
        background-color: #0f3460; /* Selectbox styling */
        color: #e0e0e0;
        border-radius: 8px;
        border: 1px solid #533483;
        padding: 10px;
    }
    .stAlert {
        border-radius: 8px;
    }
    .stCode {
        background-color: #0f3460; /* Code block styling */
        border-radius: 8px;
        padding: 15px;
    }
    .stExpander {
        background-color: #16213e; /* Expander styling */
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stExpander > div > div > p {
        color: #e0e0e0;
    }
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #16213e;
        color: #e0e0e0;
        text-align: center;
        padding: 10px 0;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Main Dashboard Title and Welcome Message ---
st.title("📈 Pumpies Crypto Dashboard")
st.markdown("Welcome to the comprehensive Pumpies Crypto Dashboard! Use the tools below to get real-time market information.")

# --- Sidebar Navigation ---
st.sidebar.header("Commands")
# This is for picking what command to run from the sidebar.
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
    index=0 # Starts on the Introduction page
)

# Small helper for coin names (not a big deal, just for display)
coin_name_translations = {
    "bitcoin": "Bitcoin",
    "ethereum": "Ethereum"
}

# --- Command Logic: What happens when you pick a command ---
# Now calling functions from the 'commands' module for each choice.

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

# --- Footer Section ---
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
