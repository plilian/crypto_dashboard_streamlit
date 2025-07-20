import streamlit as st
import commands
import utils

# --- Initial Page Config ---
st.set_page_config(
    page_title="Pumpies Crypto Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Theme Settings in Sidebar ---
st.sidebar.header("Theme Customization")

# Initialize default colors in session_state if not already set
# The sidebar background is set to black as per your request
if 'main_bg' not in st.session_state:
    st.session_state.main_bg = "#1a1a2e" # Dark blue/purple
if 'sidebar_bg' not in st.session_state:
    st.session_state.sidebar_bg = "#000000" # Black for sidebar background
if 'accent_color' not in st.session_state:
    st.session_state.accent_color = "#e94560" # Accent red/pink for titles
if 'button_bg' not in st.session_state:
    st.session_state.button_bg = "#0f3460" # Dark blue for buttons
if 'text_color' not in st.session_state:
    st.session_state.text_color = "#e0e0e0" # Light grey for main text
if 'button_hover_color' not in st.session_state:
    st.session_state.button_hover_color = "#533483" # Purple for button hover

# Allow user to pick colors using st.color_picker
st.session_state.main_bg = st.sidebar.color_picker("Main Background", st.session_state.main_bg, key="main_bg_picker")
st.session_state.sidebar_bg = st.sidebar.color_picker("Sidebar Background", st.session_state.sidebar_bg, key="sidebar_bg_picker")
st.session_state.accent_color = st.sidebar.color_picker("Title/Accent Color", st.session_state.accent_color, key="accent_color_picker")
st.session_state.button_bg = st.sidebar.color_picker("Button Background", st.session_state.button_bg, key="button_bg_picker")
st.session_state.button_hover_color = st.sidebar.color_picker("Button Hover Color", st.session_state.button_hover_color, key="button_hover_color_picker")
st.session_state.text_color = st.sidebar.color_picker("Text Color", st.session_state.text_color, key="text_color_picker")


# --- Dynamic CSS Generation ---
# This section generates the CSS using the colors chosen by the user or default values.
custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="st-"] {{
        font-family: 'Inter', sans-serif;
        color: {st.session_state.text_color}; /* Dynamic Light text on dark background */
    }}
    .main {{
        background-color: {st.session_state.main_bg}; /* Dynamic Main content area background */
        padding: 20px;
        border-radius: 10px;
    }}
    .stApp {{
        background-color: {st.session_state.main_bg}; /* Dynamic Whole app background */
    }}
    .sidebar .sidebar-content {{
        background-color: {st.session_state.sidebar_bg}; /* Dynamic Sidebar background */
        color: {st.session_state.text_color};
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {st.session_state.accent_color}; /* Dynamic Accent color for titles */
        text-align: left;
    }}
    .stButton>button {{
        background-color: {st.session_state.button_bg}; /* Dynamic Button color */
        color: white; /* Keep button text white for contrast */
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stButton>button:hover {{
        background-color: {st.session_state.button_hover_color}; /* Dynamic Button hover effect */
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }}
    .stTextInput>div>div>input {{
        background-color: {st.session_state.sidebar_bg}; /* Input field styling, using sidebar bg for consistency */
        color: {st.session_state.text_color};
        border-radius: 8px;
        border: 1px solid {st.session_state.accent_color}; /* Using accent color for border */
        padding: 10px;
    }}
    .stSelectbox>div>div>div {{
        background-color: {st.session_state.sidebar_bg}; /* Selectbox styling */
        color: {st.session_state.text_color};
        border-radius: 8px;
        border: 1px solid {st.session_state.accent_color}; /* Using accent color for border */
        padding: 10px;
    }}
    .stAlert {{
        border-radius: 8px;
    }}
    .stCode {{
        background-color: {st.session_state.sidebar_bg}; /* Code block styling */
        border-radius: 8px;
        padding: 15px;
    }}
    .stExpander {{
        background-color: {st.session_state.sidebar_bg}; /* Expander styling */
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }}
    .stExpander > div > div > p {{
        color: {st.session_state.text_color};
    }}
    /* Footer styling */
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: {st.session_state.sidebar_bg}; /* Footer uses sidebar bg */
        color: {st.session_state.text_color};
        text-align: center;
        padding: 10px 0;
        font-size: 0.9em;
    }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

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
