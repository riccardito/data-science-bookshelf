# Challenge · swiss-forecast

**Every night at midnight, forecast the next 24 hours of electricity drawn in the city of Zurich.**

| Model | MAE (MW) | Skill vs last week | Gain per day, 95 % interval | Days better than baseline |
|---|---|---|---|---|
| temporal CNN | **7.29** | 0.52 | 6.6 – 9.1 MW | 80 % |
| gradient boosting | 7.46 | 0.51 | 6.4 – 9.0 MW | 76 % |
| SARIMA × last week's shape | 12.82 | 0.15 | 1.5 – 3.2 MW | 61 % |
| seasonal naive: the same day last week | 15.13 | — | — | — |

- **Data:** ewz, Stadt Zürich, both network levels, hourly, January 2017 – November 2026
  ([`data/samples/`](../../../../data/samples/README.md) names the source and licence).
- **Test year:** 9 November 2025 – 8 November 2026, the last 365 days. Nothing was tuned on it;
  the models and their settings were chosen on the year before (chapter 6).
- **Rules:** fit only on the past; every feature known at the previous midnight; MAE over all
  8 760 forecast hours. The interval is a bootstrap over the 365 daily gains against the baseline.
- **Where the gain comes from:** on public holidays the baseline misses by about 50 MW, because
  last week was a working week; the learned models know the calendar.

## Run it

```
make install install-dl
jupyter nbconvert --to notebook --execute swiss-forecast.ipynb
```

Offline, no key, about a minute on a laptop CPU. It writes [`results.json`](results.json).
