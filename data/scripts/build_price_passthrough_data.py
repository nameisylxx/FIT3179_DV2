"""Builds data/processed/au_coffee_price_passthrough.csv for the price pass-through chart.

Input : data/processed/coffee_price_by_variety_monthly.csv
            ICO Coffee Market Report, September 2026, Table 1 (I-CIP composite, US cents per pound).
        data/raw/abs_cpi/640103_cpi_aug2026_table3.xlsx
            ABS Consumer Price Index, Australia, August 2026 release, Table 3
            (expenditure class index numbers, weighted average of eight capital cities).
            Column 30 = "Coffee, tea and cocoa", column 32 = "Meals out and take away foods".
Output: one row per month per series, with each series rebased to 100 at the first shared month
        so a world commodity price in US cents can be compared with two Australian CPI indexes.

The window is the overlap of the two sources: October 2025 to August 2026.
The ABS class is "Coffee, tea and cocoa", not coffee on its own, and "Meals out and take away
foods" is not a cup of coffee on its own. Both limits are stated on the page.
"""
import csv, datetime, os
import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABS_XLSX = f"{ROOT}/data/raw/abs_cpi/640103_cpi_aug2026_table3.xlsx"
ICO_CSV = f"{ROOT}/data/processed/coffee_price_by_variety_monthly.csv"
OUT = f"{ROOT}/data/processed/au_coffee_price_passthrough.csv"

COL_COFFEE, COL_MEALS = 30, 32
SERIES = [
    ("World coffee bean price", "world", "US cents per pound (ICO composite)"),
    ("Australian coffee, tea and cocoa prices", "shop", "CPI index, coffee tea and cocoa"),
    ("Australian meals out and takeaway prices", "meals", "CPI index, meals out and take away foods"),
]

wb = openpyxl.load_workbook(ABS_XLSX, read_only=True, data_only=True)
rows = list(wb["Data1"].iter_rows(min_row=1, values_only=True))
header = rows[0]
assert "Coffee, tea and cocoa" in str(header[COL_COFFEE]), header[COL_COFFEE]
assert "Meals out and take away foods" in str(header[COL_MEALS]), header[COL_MEALS]

abs_data = {}
for r in rows:
    if isinstance(r[0], (datetime.datetime, datetime.date)) and r[COL_COFFEE] is not None and r[COL_MEALS] is not None:
        abs_data[r[0].strftime("%Y-%m")] = (float(r[COL_COFFEE]), float(r[COL_MEALS]))

ico = {r["month"]: float(r["ico_composite_cents_per_lb"])
       for r in csv.DictReader(open(ICO_CSV, encoding="utf-8"))}

months = sorted(set(abs_data) & set(ico))
base = months[0]
raw = {
    "world": {m: ico[m] for m in months},
    "shop": {m: abs_data[m][0] for m in months},
    "meals": {m: abs_data[m][1] for m in months},
}

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["month", "series", "series_key", "raw_value", "unit", "index_base_oct_2025"])
    for label, key, unit in SERIES:
        for m in months:
            w.writerow([m, label, key, round(raw[key][m], 2), unit,
                        round(100 * raw[key][m] / raw[key][base], 2)])

print(f"{OUT}: {len(months)} months x {len(SERIES)} series, base {base}")
for label, key, _ in SERIES:
    print(f"  {label:36s} {raw[key][months[0]]:8.2f} -> {raw[key][months[-1]]:8.2f}"
          f"  ({100*(raw[key][months[-1]]/raw[key][months[0]]-1):+.1f}%)")
