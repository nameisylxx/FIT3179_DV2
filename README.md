# From farm to café

FIT3179 Data Visualisation 2, Monash University. Author: Liuxiaoxi Yang, October 2026.

An interactive page of 13 figures (14 Vega-Lite and Vega charts) that follows Australian coffee from the café, through trade, to the farms that grow it and the markets that set its price.

Live page: https://nameisylxx.github.io/FIT3179_DV2/ (add `?screenshot` to the address for a version without the scroll animation).

## Files

| Path | What it is |
|---|---|
| `index.html` | The page (structure and text) |
| `css/style.css` | Layout and typography |
| `js/main.js` | Embeds every chart |
| `js/hero.js` | Reveals the opening illustration on scroll |
| `charts/*.vg.json` | One Vega-Lite (or Vega) spec per chart, 14 in total |
| `data/processed/` | Data used by the charts |
| `data/raw/` | Original downloads, the ICO report, and archived UN Comtrade API responses |
| `data/raw/comtrade_import_query_provenance.md` | How the import data was retrieved and checked |
| `data/scripts/build_treemap_data.py` | Builds the treemap hierarchy |
| `data/scripts/build_price_passthrough_data.py` | Builds the price index data for Figure 13 |
| `images/` | Decorative illustrations |
| `sketch/` | Hand-drawn sketch |

## Run locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Data sources

Listed with links in the "About the data" section at the bottom of the page: Australian Bureau of Statistics (business counts, population and Consumer Price Index), UN Comtrade (2025), FAO via Our World in Data, International Coffee Organization (September 2026 report), Roy Morgan, Natural Earth and community map files.

## AI acknowledgement

All illustrations on the page (the mountain engraving, the hand-drawn cup at the end, the café, port, farm and market scenes, and the route and section illustrations) were generated with ChatGPT from text prompts. AI tools (ChatGPT and Claude) were also used to explore the page layout, help with the code, and check the wording of the text. All data come from the sources listed on the page, and every figure was checked against them manually.
