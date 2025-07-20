# utils.py (English Version)
import csv
from datetime import datetime
import os
import streamlit as st
import uuid

def get_session_id():
    """
    Generates or retrieves a unique session ID for the current Streamlit session.
    """
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def log_command_usage(command: str, query: str):
    """
    Logs the usage of a command to a CSV file, including a unique session ID.
    """
    session_id = get_session_id() # Get the unique session ID
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(script_dir, 'command_usage_log_streamlit_en.csv')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Use session_id instead of a generic user ID
    log_entry = [session_id, 'N/A', command, query, timestamp] # 'N/A' for username as it's not available

    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Check if file exists to write header
    file_exists = os.path.exists(log_file_path)

    with open(log_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Session ID', 'Username', 'Command', 'Query', 'Timestamp']) # Updated Header
        writer.writerow(log_entry)

def calculate_rsi(prices: list[float], period: int = 14) -> float:
    """
    Calculates the Relative Strength Index (RSI) for a list of prices.

    Args:
        prices (list[float]): A list of closing prices.
        period (int): The period for RSI calculation (default is 14).

    Returns:
        float: The calculated RSI value.
    """
    if len(prices) < period + 1: # Need at least period + 1 prices to calculate 'period' changes
        return 0.0 # Not enough data for RSI calculation

    # Calculate price changes
    price_changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]

    gains = [change if change > 0 else 0 for change in price_changes]
    losses = [abs(change) if change < 0 else 0 for change in price_changes]

    # Calculate initial average gain and loss over the first 'period' changes
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    # Apply smoothing for the rest of the data
    for i in range(period, len(gains)): # Iterate over the rest of the 'gains'/'losses' list
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0 # Avoid division by zero, handle edge cases

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def interpret_rsi(rsi: float) -> str:
    """
    Interprets the RSI value.

    Args:
        rsi (float): The RSI value.

    Returns:
        str: The interpretation of the RSI.
    """
    if rsi > 70:
        return "Overbought - The asset may be overvalued and could be due for a correction."
    elif rsi < 30:
        return "Oversold - The asset may be undervalued and could be due for a rally."
    else:
        return "Neutral - The asset is in a balanced state."
