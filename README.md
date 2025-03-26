# BRAND-Platform-Quant-Trading-Demo
A demo project leveraging the BRAND platform’s low‑latency capabilities for quantitative trading. It simulates intraday data from multiple exchanges, computes momentum signals using z‑scores, and executes rapid trading decisions.

## Overview

This repo shows off a cool trading strategy using the BRAND platform. The idea is to fetch simulated data from several exchanges in parallel, calculate momentum signals using simple z‑scores, and then make fast buy/sell decisions. It's a rough-and-ready demo to highlight low-latency processing for quant trading.

## Repo Structure

```
brand-platform-quant-trading-demo/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── brand_demo.py
└── momentum_burst_demo.py
```

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/brand-platform-quant-trading-demo.git
   cd brand-platform-quant-trading-demo
   ```

2. **Optional: Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   This project uses only Python’s standard library. If you add any external dependencies, update `requirements.txt` and install them with:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

- **Brand Demo:**  
  Simulates fetching stock data, computes a moving average signal, and makes a basic trading decision.
  ```bash
  python brand_demo.py
  ```

- **Momentum Burst Demo:**  
  Simulates intraday data fetching from multiple exchanges, computes momentum signals using z‑scores, and makes rapid trading decisions.
  ```bash
  python momentum_burst_demo.py
  ```

## Final Thoughts

This is a demo to show off the BRAND platform’s low‑latency data processing for quant trading. It demonstrates real-time signal computation and automated trading decisions in a simple, modular format. Enjoy exploring and feel free to build on it!
