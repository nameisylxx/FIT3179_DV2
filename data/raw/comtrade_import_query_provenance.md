# Provenance: `data/processed/au_coffee_imports_by_origin.csv`

## Method

Figures were retrieved directly from the free **UN Comtrade public preview API**
(`https://comtradeapi.un.org/public/v1/preview/...`), which does not require a paid
subscription for small, targeted queries like this one (bulk/large-scale extraction is
the part that requires a subscription; this project never needed that). The raw JSON
responses are archived in `data/raw/comtrade/` so every number in the CSV can be traced
back to an exact API response field.

- **Reporter:** Australia (UN M49/Comtrade code 36) — Australia's own customs
  import declarations.
- **Product code:** HS 0901 — "Coffee, whether or not roasted or decaffeinated;
  coffee husks and skins; coffee substitutes containing coffee in any proportion."
- **Flow:** Imports (M).
- **Period:** 2025 (calendar year; the 2025 annual data had been published by October 2026). The 2024 pull is kept in the raw folder for reference.
- **Mode-of-transport handling:** Comtrade returns one row per mode of transport
  (sea, air, etc.) *plus* a `motCode: 0` row that is already the sum across all modes.
  Only `motCode == 0` rows are used. An earlier pass summed all rows including the
  `motCode: 0` total, which double-counted every country by roughly 2x — that bug was
  caught and fixed; the archived JSON plus this note is the record of the fix.
- **Raw files:**
  - `data/raw/comtrade/comtrade_australia_imports_hs0901_2025.json` — **the file the chart uses**:
    one batched query for 24 candidate coffee-growing countries (22 returned trade), reporter =
    Australia, 2025, India queried with the correct code 699. This response contains only the
    all-modes row (`motCode: 0`) per partner, so no double-counting is possible.
  - `data/raw/comtrade/comtrade_australia_imports_hs0901_2024.json` and
    `comtrade_india_correct_code_check.json` — the earlier 2024 pull, kept for reference.
  - `data/raw/comtrade/comtrade_partner_areas_reference.json` — Comtrade's official
    partner-code reference table, used to validate every country code below.
- **Precision:** The decimal figures in the CSV (e.g. Brazil's 30,351,955.1 kg for 2025) are
  copied directly from the `netWgt` / `cifvalue` fields of the archived JSON responses
  above — not read off a rounded webpage table. A rounded display value seen elsewhere
  (e.g. "28,842,800") is just that page's own rounding of the same underlying figure.

## Country selection — final decision

The 22 countries in the CSV (the same 22 as the 2024 pull) are **known coffee-growing origin countries** (cross-referenced
against the OWID/FAO production list used elsewhere in this project), not a strict "top-22
trading partners by volume" ranking. Under the broader HS 0901 code, a few non-producing
countries (e.g. Switzerland, Germany) show meaningful trade value because they act as
coffee trading/logistics hubs for roasted coffee, not because they grow it — these are
deliberately excluded. The chart is titled and captioned accordingly: "Coffee imports
(HS 0901) **from selected coffee-growing origins**", not "top trading partners." No
attempt was made to verify why Switzerland specifically ranks where it does (that would
need its own sourced explanation), so no claim about "soluble coffee" or re-exports is
made anywhere in the chart or this note.

## India — code bug found and fixed (2026-09-15)

India was originally queried using partner code **356**, taken from the ISO 3166-1
numeric code in this project's country-centroids lookup file. That query returned zero
rows. The initial (wrong) conclusion was that Australia had a genuine reporting gap for
India, and the CSV was patched with India's own mirrored export-to-Australia figure
instead.

That conclusion was wrong. Comtrade's own partner-code reference table
(`comtrade_partner_areas_reference.json`) shows that **356 is not India** in Comtrade's
system — it is `"India (...1974)"`, a deprecated entity code for pre-1975 India
(excluding Sikkim), which naturally has no 2024 trade data. Comtrade's current, active
code for India is **699**. All 21 other countries in this project's list were
cross-checked against the same reference table (filtering out expired entries) and all
matched correctly; India was the only mismatch.

Re-querying Australia's imports with the correct code (`comtrade_india_correct_code_check.json`)
shows Australia **did** report India-origin HS 0901 imports for 2024 directly:
4,984,945.3 kg in 2024 (5,446,807 kg in 2025), on the same reporter-declared basis as every other
country in the CSV. The CSV now uses this figure. The earlier "mirrored data" caveat has
been removed from the chart subtitle because it no longer applies — every row in the CSV
is now Australia-reporter-declared, HS 0901, `motCode: 0`, 2024.

## Not yet done

- The full-partner ranking (`partnerCode=all`) was not obtained — Comtrade's preview API
  rejects `partnerCode=all` as an invalid value; a true "all partners" cross-check would
  need either a manual list of every partner code or the paid bulk endpoint. The 22-country
  list above was cross-checked against the WITS web interface's all-partner view in an
  earlier session instead (see prior conversation), not against a locally archived file.
