# Options Contract Toolkit 🧮📈

A Python-powered tool for evaluating single and multi-leg option strategies. This toolkit supports:

- 💰 **P&L calculation** for basic option contracts and advanced strategies (e.g. straddles, collars, spreads)
- 🧠 **Black-Scholes pricing** for both calls and puts
- 🔥 **Interactive heatmaps** showing how volatility and stock prices impact option premiums
- ✅ Realistic user prompts and alias recognition for intuitive input

---

## 💼 Strategies Supported

- Basic Contracts: Buy Call, Sell Call, Buy Put, Sell Put
- Protective Put
- Covered Call
- Straddle
- Collar
- Bull Call Spread / Bear Call Spread
- Bull Put Spread / Bear Put Spread
- Long Butterfly / Short Butterfly

---

## 📊 Features

- Built-in calculator using Black-Scholes formula (supports call and put)
- Heatmap visualizations using Seaborn and Matplotlib
- Modular structure for strategy reuse
- Alias system lets users type shorthand like `bc`, `sc`, `straddle`, or `lbf`

---

## 🚀 How to Use

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/ryanmkah/Option-Contract-Toolkit.git
   ```

2. Navigate to the project folder:
   ```
   cd Option-Contract-Toolkit
   ```

3. Install the required Python libraries:
   ```
   pip install pandas numpy matplotlib seaborn scipy yfinance requests
   ```

4. Run the program:
   ```
   python options_toolkit.py
   ```

5. Follow the interactive prompts to:
   - Choose between basic contracts, multi-leg strategies, or Black-Scholes pricing
   - Enter option details (strike price, premium, time, etc.)
   - View your contract's payoff and profit
   - Generate a visual Black-Scholes heatmap for calls or puts





## 🛠 Tech Stack

- Python
- NumPy
- Pandas
- Seaborn
- Matplotlib
- SciPy
- Yahoo Finance or Alpha Vantage (optional APIs)

---

## 📦 Future Plans

- Wrap in a class or package
- Add Streamlit GUI for web deployment
- Add portfolio-level tracking and export

---

## 🧠 Author

**Ryan Kahrimanian**  
Finance + AI @ Fordham University | Baruch Mathematics  
GitHub: [ryanmkah](https://github.com/ryanmkah)


---

## ⚠️ Disclaimer

This is an educational tool. Not investment advice.
