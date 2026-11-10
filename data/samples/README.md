# Samples

Small committed slices of public data, so every chapter and every challenge runs offline. Each
file is named after the book that uses it; its source, licence and retrieval date are listed here.

| File | Book | Source | Licence | Retrieved |
|---|---|---|---|---|
| `ewz_zurich_hourly.csv.gz` | 21 Time Series | ewz, Stadt Zürich: [Viertelstundenwerte des Stromverbrauchs in den Netzebenen 5 und 7](https://opendata.swiss/de/dataset/viertelstundenwerte-zur-stromabgabe-in-den-netzebenen-5-und-7-in-der-stadt-zurich-seit-2010) -- summed to hours (MWh), the interval-end stamps shifted to the interval start, UTC | opendata.swiss `terms_open` | 2026-11-10 |
| `enstat_switzerland_weekly.csv` | 21 Time Series | Bundesamt für Energie: [ENSTAT Wochenstatistik Elektrizitätsbilanz](https://opendata.swiss/de/dataset/enstat-wochenstatistik-elektrizitatsbilanz-erzeugung-und-abgabe-elektrischer-energie-in-der-sch) -- the national consumption column only | opendata.swiss `terms_by` (source: BFE) | 2026-11-10 |
| `rockfall_season.csv` | 3 Probability | **Seeded, not measured**: one 90-day season of `ds_toolbox.rockfall.season()` -- zone 1 fitted to the 68 rows printed in the 2019 FHNW report, zone 2 chosen (see the module) | generated | 2026-11-10 |
