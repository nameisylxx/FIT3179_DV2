"""Builds data/processed/coffee_production_2024_treemap.csv for the treemap chart.

Input : data/processed/coffee_production_latest_with_coordinates.csv  (FAO via Our World in Data, 2024)
        data/raw/country_centroids_dr5hn.csv                          (UN region / subregion per country)
Output: one row per tree node (root, 4 regions, country tiles + one "Other" tile per region).

All countries are kept as FAO publishes them. (The Central African Republic and Guinea rise sharply
after 2015; the page notes this rather than dropping them.)
Countries below MIN_TONNES are combined into an "Other" tile inside their region.
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MIN_TONNES = 300_000
EXCLUDE = set()   # all FAO countries are shown as published

centroids = {r["iso3"]: r for r in csv.DictReader(open(f"{ROOT}/data/raw/country_centroids_dr5hn.csv", encoding="utf-8"))}

def ico_region(row):
    if row["region"] == "Africa":
        return "Africa"
    if row["region"] in ("Asia", "Oceania"):
        return "Asia & Oceania"
    if row["subregion"] == "South America":
        return "South America"
    return "Central America & Mexico"   # Central America, Northern America (Mexico) and the Caribbean

regions = ["South America", "Central America & Mexico", "Africa", "Asia & Oceania"]
production = [r for r in csv.DictReader(open(f"{ROOT}/data/processed/coffee_production_latest_with_coordinates.csv"))
              if r["iso3"] not in EXCLUDE and r["production_tonnes"]]

nodes = [{"id": 0, "parent": "", "name": "World", "region": "", "production_tonnes": ""}]
region_id = {name: i + 1 for i, name in enumerate(regions)}
for name, rid in region_id.items():
    nodes.append({"id": rid, "parent": 0, "name": name, "region": name, "production_tonnes": ""})

next_id = len(regions) + 1
other = {name: 0.0 for name in regions}
for r in production:
    region = ico_region(centroids[r["iso3"]])
    tonnes = float(r["production_tonnes"])
    if tonnes >= MIN_TONNES:
        nodes.append({"id": next_id, "parent": region_id[region], "name": r["country_name"], "region": region,
                      "production_tonnes": round(tonnes, 1)})
        next_id += 1
    else:
        other[region] += tonnes
for region, tonnes in other.items():
    nodes.append({"id": next_id, "parent": region_id[region], "name": "Other", "region": region,
                  "production_tonnes": round(tonnes, 1)})
    next_id += 1

out = f"{ROOT}/data/processed/coffee_production_2024_treemap.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["id", "parent", "name", "region", "production_tonnes"])
    w.writeheader()
    w.writerows(nodes)

total = sum(float(n["production_tonnes"]) for n in nodes if n["production_tonnes"] != "")
print(f"wrote {out}: {len(nodes)} nodes, total {total:,.0f} t")
for region in regions:
    t = sum(float(n["production_tonnes"]) for n in nodes if n["region"] == region and n["production_tonnes"] != "")
    print(f"  {region:26s} {t:>12,.0f} t  {t/total*100:4.1f}%")
