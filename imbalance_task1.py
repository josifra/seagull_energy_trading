import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
import time

plt.ion()   # Interactive mode: window updates without freezing

API_URL = "https://data.elexon.co.uk/bmrs/api/v1/forecast/indicated/day-ahead/evolution"

def fetch_day(date_str, periods):
    params = {
        "settlementDate": date_str,
        "settlementPeriod": periods,
        "format": "json"
    }
    r = requests.get(API_URL, params=params)
    r.raise_for_status()
    return r.json()["data"]

def load_full_day(date_str):
    d = datetime.strptime(date_str, "%Y-%m-%d")
    prev = (d - timedelta(days=1)).strftime("%Y-%m-%d")

    # SP47–48 from previous day + SP1–46 for current day
    data_prev = fetch_day(prev, [47, 48])
    data_day = fetch_day(date_str, list(range(1, 47)))

    df = pd.DataFrame(data_prev + data_day)
    df = df.rename(columns={"indicatedImbalance": "imbalance"})
    return df.groupby("settlementPeriod")["imbalance"].mean()

# Reference day (example day)
day_ref = "2025-11-12"

# Create figure only once
fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(14, 8), sharex=True,
    gridspec_kw={'height_ratios': [3, 1]}
)

while True:
    day_today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    curve_ref = load_full_day(day_ref)
    curve_today = load_full_day(day_today)

    diff = curve_today.values - curve_ref.values
    colors = ["green" if d > 0 else "red" for d in diff]

    # ----------------------------
    # Export CSV table
    # ----------------------------
    df_table = pd.DataFrame({
        "SettlementPeriod": curve_today.index,
        "Imbalance_Ref": curve_ref.values,
        "Imbalance_Today": curve_today.values,
        "Delta": diff
    })
    df_table.to_csv("imbalance_table.csv", index=False)

    # Clear old plots
    ax1.clear()
    ax2.clear()

    # ----------------------------
    # Main line chart
    # ----------------------------
    ax1.plot(curve_ref.index, curve_ref.values, marker="o", color="blue",
             label=f"Example {day_ref}")
    ax1.plot(curve_today.index, curve_today.values, marker="o", color="red",
             label=f"Today {day_today}")

    ax1.set_ylabel("Imbalance")
    ax1.set_title("Imbalance — comparison + visual indicator")
    ax1.grid()
    ax1.legend()

    # ----------------------------
    # Update timestamps
    # ----------------------------
    current_time = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
    next_time = (datetime.now(timezone.utc) + timedelta(minutes=30)).strftime("%H:%M UTC")

    ax1.text(
        0.99, 0.98,
        f"Last update: {current_time}\nNext refresh: {next_time}",
        transform=ax1.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.7, edgecolor="none")
    )

    # ----------------------------
    # Bar chart of differences
    # ----------------------------
    ax2.bar(curve_today.index, diff, color=colors)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.set_ylabel("Forecast Change vs Reference Day")
    ax2.set_xlabel("Settlement Period (1 → 48)")

    # Fix margins AFTER all drawing is done
    plt.tight_layout()

    fig.canvas.draw()
    fig.canvas.flush_events()

    print(f"Updated at {current_time}")
    plt.pause(30 * 60)   # 30 min non-blocking pause

    # STOP the loop if the window is closed
    if not plt.fignum_exists(fig.number):
        print("Figure closed. Stopping loop.")
    break