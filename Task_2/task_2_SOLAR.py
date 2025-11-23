import requests
import pandas as pd
import matplotlib.pyplot as plt
import pytz
from datetime import datetime

# ---------------------------
# CONFIG
# ---------------------------
DATE = "2025-11-12"
CEST = pytz.timezone("Europe/Paris")

URL_FORECAST = "https://data.elexon.co.uk/bmrs/api/v1/forecast/generation/wind-and-solar/day-ahead"
URL_ACTUAL   = "https://data.elexon.co.uk/bmrs/api/v1/generation/actual/per-type/wind-and-solar"


# ---------------------------
# SIMPLE JSON EXTRACTION
# ---------------------------
def extract_list(rjson):
    if isinstance(rjson.get("data"), list):
        return rjson["data"]
    if isinstance(rjson.get("data"), dict):
        return rjson["data"].get("data", [])
    return []


# ---------------------------
# FETCH FORECAST SOLAR
# ---------------------------
def fetch_forecast_solar(date):
    params = {
        "from": date,
        "to": date,
        "settlementPeriodFrom": 1,
        "settlementPeriodTo": 48,
        "processType": "all",
        "format": "json",
    }

    r = requests.get(URL_FORECAST, params=params)
    r.raise_for_status()

    data = extract_list(r.json())
    df = pd.DataFrame(data)
    if df.empty:
        return pd.Series(dtype=float)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True).dt.tz_convert(CEST)

    # Filter SOLAR (PV)
    df = df[df["psrType"].str.contains("SOLAR|PV", case=False, na=False)]

    return df.groupby("settlementPeriod")["quantity"].sum()


# ---------------------------
# FETCH ACTUAL SOLAR
# ---------------------------
def fetch_actual_solar(date):
    params = {
        "from": date,
        "to": date,
        "settlementPeriodFrom": 1,
        "settlementPeriodTo": 48,
        "format": "json",
    }

    r = requests.get(URL_ACTUAL, params=params)
    r.raise_for_status()

    data = extract_list(r.json())
    df = pd.DataFrame(data)
    if df.empty:
        return pd.Series(dtype=float)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True).dt.tz_convert(CEST)

    df = df[df["psrType"].str.contains("SOLAR|PV", case=False, na=False)]

    return df.groupby("settlementPeriod")["quantity"].sum()


# ---------------------------
# LOAD DATA
# ---------------------------
forecast = fetch_forecast_solar(DATE)
actual   = fetch_actual_solar(DATE)

# Align indexes
idx = range(1, 49)
forecast = forecast.reindex(idx, fill_value=0)
actual   = actual.reindex(idx, fill_value=0)

difference = actual - forecast

# ---------------------------
# EXPORT CSV
# ---------------------------
df_export = pd.DataFrame({
    "SettlementPeriod": idx,
    "ForecastSolar": forecast.values,
    "ActualSolar": actual.values,
    "Difference": difference.values
})

df_export.to_csv("solar_generation_forecast_vs_actual.csv", index=False)
print("CSV exported: solar_generation_forecast_vs_actual.csv")


# ---------------------------
# PLOT 1 — Forecast vs Actual
# ---------------------------
fig, axs = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={"height_ratios": [3, 1]})

axs[0].plot(idx, forecast, marker="o", color="orange", label="Forecast Solar")
axs[0].plot(idx, actual, marker="o", color="red", label="Actual Solar")

axs[0].set_title(f"SOLAR Generation — Forecast vs Actual — {DATE} (CEST)")
axs[0].set_ylabel("Generation (MW)")
axs[0].grid(True)
axs[0].legend()


# ---------------------------
# PLOT 2 — Difference
# ---------------------------
colors = ["green" if d >= 0 else "red" for d in difference]

axs[1].bar(idx, difference, color=colors)
axs[1].axhline(0, color="black", linewidth=0.7)
axs[1].set_title("Difference (Actual - Forecast)")
axs[1].set_xlabel("Settlement Period (1→48)")
axs[1].set_ylabel("Difference (MW)")
axs[1].grid(True, axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()
