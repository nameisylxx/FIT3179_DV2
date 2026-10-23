// One container for every chart: each .vg.json spec is embedded into its element.
const embedOptions = { actions: false, renderer: 'svg' };

const charts = [
  ['#chart_cafe_density', 'charts/au_cafe_choropleth.vg.json'],
  ['#chart_cafe_change', 'charts/au_cafe_slopegraph.vg.json'],
  ['#chart_cafe_size', 'charts/au_cafe_business_size_stacked_bar.vg.json'],
  ['#chart_import_flows', 'charts/au_coffee_import_flow_map.vg.json'],
  ['#chart_suppliers', 'charts/au_coffee_supplier_ranked_bar.vg.json'],
  ['#chart_treemap', 'charts/world_production_treemap.vg.json'],
  ['#chart_production_map', 'charts/world_production_symbol_map.vg.json'],
  ['#chart_bump', 'charts/world_production_bump_chart.vg.json'],
  ['#chart_yield', 'charts/world_yield_heatmap.vg.json'],
  ['#chart_prices', 'charts/coffee_price_line_chart.vg.json'],
  ['#chart_species', 'charts/coffee_robusta_share_line_chart.vg.json'],
  ['#chart_balance', 'charts/coffee_supply_demand_waterfall.vg.json'],
];

// Wait for the web fonts so Vega measures text with the final typeface.
const fontsReady = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();

fontsReady.then(() => {
  charts.forEach(([selector, spec]) => {
    vegaEmbed(selector, spec, embedOptions).catch((error) => {
      console.error('Could not draw ' + spec, error);
    });
  });
});
