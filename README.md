# pumpiesstreamlit
A comprehensive Streamlit dashboard for real-time cryptocurrency market data, trending coins, company holdings, and technical analysis.

Ganje Crypto Dashboard 📈
Overview
The Ganje Crypto Dashboard is a powerful and user-friendly Streamlit application designed to provide real-time cryptocurrency market insights. Whether you're a casual enthusiast or a serious trader, this dashboard offers a comprehensive suite of tools to track market trends, analyze coin data, and monitor key indicators without leaving your browser.

Features
Coin Search: Quickly find detailed information about any cryptocurrency by name or symbol.

Trending Coins: Stay updated with the hottest cryptocurrencies gaining traction in the market.

Market Dominance: Visualize the market share of major cryptocurrencies like Bitcoin and Ethereum.

Companies Holdings: Explore which public companies hold significant amounts of Bitcoin or Ethereum in their treasuries.

Coin Categories: Discover top cryptocurrency categories based on market cap changes.

Coin Details (by Name/Address): Get in-depth data for specific coins using their name or contract address (for Ethereum/Solana).

Technical Analysis:

Balance of Power (BOP): Analyze buying and selling pressure over various timeframes.

Relative Strength Index (RSI): Evaluate overbought or oversold conditions.

DexScreener Integration:

Top/Latest Boosted Tokens: Identify tokens receiving significant attention on decentralized exchanges.

Token Orders: View order details for specific tokens on Ethereum or Solana.

Trade Info: Access comprehensive trading data including transactions, volume, and price changes.

Installation
To get this dashboard up and running on your local machine, follow these steps:

Clone the repository:

git clone [https://github.com/your-username/ganje-crypto-dashboard.git](https://github.com/your-username/pumpiesstreamlit.git)
cd ganje-crypto-dashboard

Create a virtual environment (recommended):

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

Install the required Python packages:

pip install -r requirements.txt

(You'll need to create a requirements.txt file if you don't have one. See "Other GitHub Files" below.)

No API Keys Needed: This application uses publicly accessible APIs, so you don't need to set up any API keys or .env files.

Usage
To run the Streamlit application:

streamlit run app.py

This command will open the dashboard in your default web browser.

Project Structure
.
├── app.py              # Main Streamlit application file
├── commands.py         # Modular functions for each dashboard command
├── api_client.py       # Handles all API calls to external services
├── utils.py            # Utility functions (e.g., RSI calculation, logging)
├── requirements.txt    # List of Python dependencies
├── .gitignore          # Specifies intentionally untracked files to ignore
├── LICENSE             # Project license file
└── README.md           # This file

Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes.

Commit your changes (git commit -m 'Add new feature X').

Push to the branch (git push origin feature/your-feature-name).

Open a Pull Request.

License
This project is licensed under the All Rights Reserved policy.

Contact
For any questions or feedback, feel free to reach out:

Developer: Parham Lilian

Instagram: @parhamlilian

LinkedIn: Parham Lilian
