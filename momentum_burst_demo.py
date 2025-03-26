"""
BRAND Platform Demo: Short-Term Momentum Burst (Intraday Momentum Strategy)

Purpose:
    This script demonstrates a quantitative trading strategy that captures short-term momentum bursts.
    Using the BRAND platform’s low-latency capabilities, it simulates rapid data fetching from multiple
    exchanges (e.g., NYSE, NASDAQ, BATS) in parallel, calculates a price-volume spike indicator, and
    makes an immediate trading decision based on the computed momentum score.

Strategy Overview:
    1. Data Gathering (Parallel Nodes):
       - Simulate low-latency fetching of key data streams: price (bid/ask) and trade volume.
       - Each simulated exchange produces 60 data points representing 1 minute of intraday activity.
       - For demonstration, one exchange (e.g., NASDAQ) is set to exhibit a forced momentum burst.

    2. Signal Quantification:
       - Compute the z-score of the latest price and volume data relative to the historical data from that minute.
       - Calculate the Momentum Score as:
             Momentum Score = (Price Z-Score) × (Volume Z-Score)
       - A high positive score indicates strong bullish momentum; a high negative score indicates strong bearish momentum.
       - A threshold of |2.5| for individual z-scores is used conceptually, while the final decision thresholds are set at ±5.

    3. Decision-Making Logic:
       - If Momentum Score > +5: Immediately execute a BUY order.
       - If Momentum Score < -5: Immediately execute a SELL (short) order.
       - Otherwise: HOLD the position.
       - This low-latency decision-making process mimics the need for millisecond-level responsiveness.

    4. Risk Management (Conceptual):
       - Suggested exit conditions: exit after a ±0.2% price movement or after holding for 10 minutes.
       - These are noted for realism, though not fully implemented in this demo.

Usage:
    Run the script from the command line:
        python momentum_burst_demo.py
"""

import concurrent.futures
import random
import statistics

# ----------------------------------
# Data Simulation & Parallel Fetching
# ----------------------------------
def simulate_exchange_data(exchange, num_points=60, base_price=150.0, base_volume=1000):
    """
    Simulates intraday price and volume data for a given exchange.
    
    Parameters:
        exchange (str): Exchange name (e.g., "NYSE", "NASDAQ", "BATS").
        num_points (int): Number of data points (e.g., one per second for 60 seconds).
        base_price (float): Starting stock price.
        base_volume (int): Starting trade volume.
    
    Returns:
        dict: Contains lists for 'prices' and 'volumes'.
    """
    prices = []
    volumes = []
    
    for i in range(num_points):
        # Simulate normal random fluctuations: ±0.5% for price; ±20% for volume.
        price_fluctuation = random.uniform(-0.005, 0.005)
        volume_fluctuation = random.uniform(0.8, 1.2)
        price = base_price * (1 + price_fluctuation)
        volume = int(base_volume * volume_fluctuation)
        prices.append(round(price, 2))
        volumes.append(volume)
    
    # Force a momentum burst on one exchange (e.g., NASDAQ) by injecting a spike in the last data point.
    if exchange.upper() == "NASDAQ":
        burst_price = base_price * (1 + random.uniform(0.01, 0.02))
        burst_volume = int(base_volume * random.uniform(2.0, 3.0))
        prices[-1] = round(burst_price, 2)
        volumes[-1] = burst_volume

    return {"prices": prices, "volumes": volumes}

def fetch_all_exchanges(exchanges, num_points=60, base_price=150.0, base_volume=1000):
    """
    Simulates parallel data fetching from multiple exchanges using concurrent futures.
    
    Parameters:
        exchanges (list): List of exchange names.
        num_points (int): Data points per exchange.
        base_price (float): Base price for simulation.
        base_volume (int): Base volume for simulation.
    
    Returns:
        dict: Mapping of exchange name to its simulated data.
    """
    exchange_data = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(exchanges)) as executor:
        future_to_exchange = {
            executor.submit(simulate_exchange_data, ex, num_points, base_price, base_volume): ex
            for ex in exchanges
        }
        for future in concurrent.futures.as_completed(future_to_exchange):
            ex = future_to_exchange[future]
            try:
                exchange_data[ex] = future.result()
            except Exception as exc:
                print(f"Error fetching data from {ex}: {exc}")
    return exchange_data

# ----------------------------------
# Signal Quantification Functions
# ----------------------------------
def compute_z_score(data_list):
    """
    Computes the z-score of the last data point compared to historical data.
    
    Parameters:
        data_list (list): List of numeric values.
    
    Returns:
        float: z-score of the last value.
    
    Raises:
        ValueError: If data is insufficient or standard deviation is zero.
    """
    if len(data_list) < 2:
        raise ValueError("Not enough data to compute z-score.")
    
    mean_val = statistics.mean(data_list)
    stdev_val = statistics.stdev(data_list)
    if stdev_val == 0:
        raise ValueError("Standard deviation is zero; cannot compute z-score.")
    
    return (data_list[-1] - mean_val) / stdev_val

def compute_momentum_score(prices, volumes):
    """
    Computes the momentum score as the product of the price and volume z-scores.
    
    Parameters:
        prices (list): List of price data.
        volumes (list): List of volume data.
    
    Returns:
        float: Calculated momentum score.
    """
    try:
        price_z = compute_z_score(prices)
        volume_z = compute_z_score(volumes)
        return price_z * volume_z
    except ValueError as e:
        print(f"Error in momentum score computation: {e}")
        return 0

# ----------------------------------
# Decision-Making Function
# ----------------------------------
def determine_order(momentum_score, threshold=5.0):
    """
    Determines the trading decision based on the momentum score.
    
    Parameters:
        momentum_score (float): The computed momentum score.
        threshold (float): Decision threshold (default is 5).
    
    Returns:
        str: Trading decision: "BUY", "SELL", or "HOLD".
    """
    if momentum_score > threshold:
        return "BUY"
    elif momentum_score < -threshold:
        return "SELL"
    else:
        return "HOLD"

# ----------------------------------
# Main Execution Function
# ----------------------------------
def main():
    exchanges = ["NYSE", "NASDAQ", "BATS"]
    num_points = 60         # Simulate 60 seconds (1 minute) of data
    base_price = 150.0      # Base stock price
    base_volume = 1000      # Base trade volume

    print("Fetching intraday data from multiple exchanges in parallel...\n")
    
    data_by_exchange = fetch_all_exchanges(exchanges, num_points, base_price, base_volume)
    
    momentum_results = {}
    
    for exchange, data in data_by_exchange.items():
        prices = data["prices"]
        volumes = data["volumes"]
        momentum = compute_momentum_score(prices, volumes)
        momentum_results[exchange] = momentum
        
        try:
            price_z = compute_z_score(prices)
            volume_z = compute_z_score(volumes)
        except ValueError:
            price_z = volume_z = 0
        
        print(f"Exchange: {exchange}")
        print(f"  Latest Price: {prices[-1]} | Mean Price: {round(statistics.mean(prices), 2)} | Price Z-Score: {round(price_z, 2)}")
        print(f"  Latest Volume: {volumes[-1]} | Mean Volume: {round(statistics.mean(volumes), 2)} | Volume Z-Score: {round(volume_z, 2)}")
        print(f"  Computed Momentum Score: {round(momentum, 2)}\n")
    
    extreme_exchange, extreme_score = max(momentum_results.items(), key=lambda x: abs(x[1]))
    decision = determine_order(extreme_score)
    
    print("==============================================")
    print(f"Most Extreme Signal from {extreme_exchange}: Momentum Score = {round(extreme_score, 2)}")
    print(f"Trading Decision: {decision}")
    print("==============================================\n")
    
    print("Risk Management Note: Exit trade after ±0.2% price movement or after 10 minutes (not actively implemented in this demo).")

if __name__ == "__main__":
    main()

"""
Final Documentation:
---------------------
How to Run the Script:
    - Save the script as 'momentum_burst_demo.py'.
    - Run from the command line using: python momentum_burst_demo.py

Code Sections:
    1. Data Gathering:
         - simulate_exchange_data(): Simulates 1 minute of intraday price and volume data for an exchange.
         - fetch_all_exchanges(): Uses concurrent.futures to fetch data from multiple exchanges in parallel.
    2. Signal Quantification:
         - compute_z_score(): Calculates the z-score of the latest data point.
         - compute_momentum_score(): Computes the momentum score as (Price Z-Score × Volume Z-Score).
    3. Decision-Making:
         - determine_order(): Implements the trading logic to decide BUY, SELL, or HOLD based on the momentum score.
    4. Main Execution:
         - main(): Coordinates data fetching, signal computation, decision-making, and prints out detailed logs.

Reflection on the BRAND Platform:
    This demo leverages low‑latency, parallel processing to rapidly identify short‑term momentum bursts,
    highlighting the BRAND platform’s ability to make millisecond‑level trading decisions. The script
    demonstrates both the technical design and real‑world applicability of the strategy in a clear, modular fashion.
"""
