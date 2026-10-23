# From farm to café

FIT3179 Data Visualisation 2, Monash University. Author: Liuxiaoxi Yang, October 2026.

An interactive page of 12 Vega-Lite and Vega charts that follows Australian coffee from the café, through trade, to the farms that grow it and the markets that set its price.

## Files

| Path | What it is |
|---|---|
| `index.html` | The page (structure and text) |
| `css/style.css` | Layout and typography |
| `js/main.js` | Embeds every chart |
| `charts/*.vg.json` | One Vega-Lite (or Vega) spec per chart |
| `data/processed/` | Data used by the charts |
| `data/raw/` | Original downloads, the ICO report, and archived UN Comtrade API responses |
| `data/raw/comtrade_import_query_provenance.md` | How the import data was retrieved and checked |
| `data/scripts/build_treemap_data.py` | Builds the treemap hierarchy |
| `images/` | Decorative vector illustrations |
| `sketch/` | Hand-drawn sketch |

## Run locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Data sources

Listed with links in the "About the data" section at the bottom of the page: ABS, UN Comtrade (2025), FAO via Our World in Data, International Coffee Organization (September 2026 report), Roy Morgan, Natural Earth and community map files.

## AI acknowledgement

A first layout idea was generated with ChatGPT and then redrawn by hand as the sketch. Claude (Claude Code) helped write code, check data, draw the decorative illustrations in `images/`, and edit text.
