from datetime import datetime
import math
import sys

from Strategy_2_FuturePayOff_definition import get_future_payoff
from app_helper import get_session_token, load_options_request_json

def calendar_arbitrage(spot, F1, F2, T1_days, T2_days, 
                       risk_free_rate=0.07, dividend_yield=0.01, 
                       margin_rate=0.15, trade_cost=1, lot_size=150):
    """
    spot: Spot price of stock/index
    F1: Near-month futures price
    F2: Next-month futures price
    T1_days: Days to expiry for near-month future
    T2_days: Days to expiry for next-month future
    risk_free_rate: Annual risk-free rate (default 7%)
    dividend_yield: Expected annual dividend yield (default 1%)
    margin_rate: % margin required (default 15%)
    trade_cost: per side cost (default Rs.22)
    lot_size: number of units per lot
    """
    
    # Convert days to years
    T1 = T1_days / 365
    T2 = T2_days / 365
    
    # Implied cost of carry from F1 and F2
    implied_carry = (1 / (T2 - T1)) * math.log(F2 / F1)
    
    # Actual expected cost of carry
    expected_carry = risk_free_rate - dividend_yield
    
    # Actual spread
    spread_actual = F2 - F1
    
    # Fair spread under expected carry model
    fair_F2 = F1 * math.exp(expected_carry * (T2 - T1))
    spread_fair = fair_F2 - F1
    
    # Transaction cost = 2 trades (Buy & Sell)
    total_cost = 2 * trade_cost * lot_size
    
    # Initial margin required (approximate, per lot)
    margin_required = margin_rate * max(F1, F2) * lot_size
    
    # Arbitrage logic
    if implied_carry > expected_carry:
        suggestion = "Spread too wide → Sell F2, Buy F1 (expect narrowing)"
        # At F1 expiry, F1 = Spot
        F2_new = spot * math.exp(expected_carry * (T2 - T1))
        print(F2_new, spot, F1, F2)
        pnl = ((F2 - F2_new) + (spot - F1))  * lot_size
    elif implied_carry < expected_carry:
        suggestion = "Spread too narrow → Buy F2, Sell F1 (expect widening)"
        F2_new = spot * math.exp(expected_carry * (T2 - T1))
        print(F2_new, spot, F1, F2)
   
        pnl = ((F2_new - F2) + (F1 - spot)) * lot_size 
    else:
        suggestion = "No clear arbitrage"
        pnl = -total_cost
    
    # Return on capital (%)
    return_pct = (pnl / margin_required) * 100 if margin_required > 0 else 0
    
    return {
        "Spot": spot,
        "Near Future (F1)": F1,
        "Far Future (F2)": F2,
        "Implied Carry (annualized)": round(implied_carry * 100, 2),
        "Expected Carry (annualized)": round(expected_carry * 100, 2),
        "Actual Spread": round(spread_actual, 2),
        "Fair Spread": round(spread_fair, 2),
        "Arbitrage Suggestion": suggestion,
        "Expected PnL at F1 Expiry (Rs)": round(pnl, 2),
        "Margin Required (Rs)": round(margin_required, 2),
        "Return on Capital (%)": round(return_pct, 2)
    }

# Example usage
# Read and parse the file
stock_data = []
op_request = load_options_request_json()
session_key = op_request['session_key']
secret_key= sys.argv[2]
appkey= sys.argv[1]

for line in op_request["optionchain_method"]:
    # Remove whitespace/newlines and split by space
    stock_data.append({
                "stockcode": line["payload"]["stock_code"],
                "lotsize": line["lot_size"],
                "current_expiry": line["payload"]["expiry_date"],
                "nearfuture_expiry": line["payload"]["nearfuture_expiry"]
            })
    print(stock_data)
    
# Example: print parsed data
for record in stock_data:
    today = datetime.today()

    # Calculate difference
    t1_days = ( datetime.strptime(record.get("current_expiry"), "%Y-%m-%dT%H:%M:%S.%fZ") - today).days
    t2_days = ( datetime.strptime(record.get("nearfuture_expiry"), "%Y-%m-%dT%H:%M:%S.%fZ") - today).days
    lotsize =record.get("lotsize")
    stock_code = record.get("stockcode")
    expiry_date = record.get("nearfuture_expiry")
    expiry_date_current = record.get("current_expiry")
    print(f"Stock: {stock_code}, expiry: {expiry_date}, expiryCurrent: {expiry_date_current}")
    result_current = get_future_payoff(stock_code, expiry_date_current, appkey, secret_key, session_key)
    #print(result_current)
    spot_price = result_current.get("spot_price")
    future_value_1 = result_current.get("future_value")
    result_future = get_future_payoff(stock_code, expiry_date, appkey, secret_key, session_key)
    future_value_2 = result_future.get("future_value")

    print(f"Spot Price: {spot_price}, Future Value 1: {future_value_1}, Future Value 2: {future_value_2}, T1 Days: {t1_days}, T2 Days: {t2_days}, Lot Size: {lotsize}") 

    # Convert to float before calculation
    if None in (spot_price, future_value_1, future_value_2):
        print("Error: One or more required values are None. Skipping calculation for this record.")
        continue

    result = calendar_arbitrage(
        spot=float(spot_price),
        F1=float(future_value_1),
        F2=float(future_value_2),
        T1_days=t1_days,
        T2_days=t2_days,
        lot_size=lotsize
    )
    for k, v in result.items():
        print(f"{k}: {v}")
