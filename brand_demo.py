"""
BRAND System Demonstration Script

Purpose:
    This script demonstrates early work using the BRAND system by simulating a low‑latency parallel nodes model to evaluate a stock.
    It simulates fetching stock market data for a specific ticker (e.g., "AAPL") using parallel processing, quantifies a signal from that data,
    and makes an investment judgment ("Buy", "Hold", or "Sell") based on the computed signal.

Data Simulation:
    - Simulates stock market data for "AAPL" using random number generation to mimic real stock prices.
    - Divides the data-fetching process into multiple parallel tasks using Python's concurrent.futures module to simulate low‑latency processing.

Signal Quantification:
    - Computes a simple moving average over the last 10 data points as the signal.

Investment Judgment:
    - Implements a decision rule:
        * If the moving average is above a defined upper threshold, the decision is "Buy".
        * If below a lower threshold, the decision is "Sell".
        * Otherwise, the decision is "Hold".

Usage:
    Run the script from the command line:
        python brand_demo.py
"""

import concurrent.futures
import random

def simulate_stock_fetch(segment_index, num_points, base_price):
    """
    Simulates fetching stock data for a segment.

    Parameters:
        segment_index (int): Index of the segment (for debugging purposes).
        num_points (int): Number of data points to simulate.
        base_price (float): Base price around which to simulate stock data.

    Returns:
        list: Simulated stock prices as floats.
    """
    simulated_data = []
    for _ in range(num_points):
        # Simulate a small percentage price fluctuation between -0.5% and 0.5%
        fluctuation = random.uniform(-0.005, 0.005)
        price = base_price * (1 + fluctuation)
        simulated_data.append(round(price, 2))
    return simulated_data

def fetch_stock_data(ticker, total_points=100, segments=4, base_price=150.0):
    """
    Simulates fetching stock data in parallel for a given ticker.

    Parameters:
        ticker (str): Stock ticker symbol.
        total_points (int): Total number of data points to simulate.
        segments (int): Number of parallel segments to split the data fetching.
        base_price (float): Base price for simulation.

    Returns:
        list: Combined list of simulated stock prices.
    """
    data = []
    points_per_segment = total_points // segments

    # Using ThreadPoolExecutor to simulate low‑latency parallel data fetching
    with concurrent.futures.ThreadPoolExecutor(max_workers=segments) as executor:
        future_to_segment = {
            executor.submit(simulate_stock_fetch, i, points_per_segment, base_price): i
            for i in range(segments)
        }
        for future in concurrent.futures.as_completed(future_to_segment):
            segment_index = future_to_segment[future]
            try:
                segment_data = future.result()
                data.extend(segment_data)
            except Exception as exc:
                print(f"Segment {segment_index} generated an exception: {exc}")
    return data

def compute_signal(stock_data, window_size=10):
    """
    Computes a simple moving average signal from the stock data.

    Parameters:
        stock_data (list): List of stock prices.
        window_size (int): Number of recent data points to calculate the moving average.

    Returns:
        float: The computed moving average signal.
    """
    if len(stock_data) < window_size:
        raise ValueError("Not enough data points to compute the moving average.")

    window = stock_data[-window_size:]
    moving_average = sum(window) / window_size
    return moving_average

def determine_investment_decision(signal, base_price, upper_multiplier=1.005, lower_multiplier=0.995):
    """
    Determines an investment decision based on the computed signal.

    Decision criteria:
        - If signal is above base_price * upper_multiplier: "Buy"
        - If signal is below base_price * lower_multiplier: "Sell"
        - Otherwise: "Hold"

    Parameters:
        signal (float): The computed moving average signal.
        base_price (float): The base price used in simulation.
        upper_multiplier (float): Multiplier for the upper threshold.
        lower_multiplier (float): Multiplier for the lower threshold.

    Returns:
        str: Investment decision ("Buy", "Sell", or "Hold").
    """
    upper_threshold = base_price * upper_multiplier
    lower_threshold = base_price * lower_multiplier

    if signal > upper_threshold:
        return "Buy"
    elif signal < lower_threshold:
        return "Sell"
    else:
        return "Hold"

def main():
    ticker = "AAPL"
    base_price = 150.0
    total_points = 100

    print(f"Simulating stock data for {ticker}...\n")

    stock_data = fetch_stock_data(ticker, total_points=total_points, segments=4, base_price=base_price)

    print("Simulated Stock Data:")
    print(stock_data)
    print("\n")

    try:
        signal = compute_signal(stock_data, window_size=10)
        print(f"Computed Signal (Moving Average over last 10 data points): {signal:.2f}")
    except ValueError as ve:
        print(f"Error computing signal: {ve}")
        return

    decision = determine_investment_decision(signal, base_price)
    print(f"Final Investment Decision: {decision}")

if __name__ == "__main__":
    main()

"""
Final Documentation:
---------------------
How to Run the Script:
    - Save the script as 'brand_demo.py'.
    - Run from the command line using: python brand_demo.py

Code Sections:
    - simulate_stock_fetch: Simulates a segment of stock data with random fluctuations.
    - fetch_stock_data: Uses parallel processing to simulate low‑latency data fetching.
    - compute_signal: Calculates a moving average as the signal.
    - determine_investment_decision: Implements the decision logic to output "Buy", "Sell", or "Hold".
    - main: Coordinates the simulation, signal computation, and decision output.

Reflection on the BRAND System:
    This demo highlights the BRAND platform’s ability to perform low‑latency data processing and immediate decision-making,
    showcasing modular design and clear technical execution.
"""
