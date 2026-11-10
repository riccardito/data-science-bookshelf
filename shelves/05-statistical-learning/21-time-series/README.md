# 21 · Time Series

*Shelf V · Statistical Learning & Regression · FHNW modules: spz*

## Why it matters

Most data a business or a city keeps is ordered in time: consumption, sales, admissions, sensor
readings. Order changes the rules. Rows are no longer exchangeable, a shuffled split measures the
wrong task, and the most useful feature is usually the past of the series itself. This book is
about forecasting such a series honestly: knowing what was known at the moment of the forecast,
and proving that a model beats the obvious guess before trusting it.

The whole book works on one real series: the electricity drawn in the city of Zurich, every hour
since 2017.

## Chapters

Read in order: each chapter builds on the one before it.

1. [Time as an index](01-time-as-an-index.ipynb) — parsing, time zones, the 23- and 25-hour days, resampling
2. [Trend and seasonality](02-trend-and-seasonality.ipynb) — the daily, weekly and yearly cycles, decomposition by hand and with STL
3. [Stationarity and autocorrelation](03-stationarity-and-autocorrelation.ipynb) — the ACF by hand, differencing, ADF and KPSS
4. [ARIMA and SARIMA](04-arima-and-sarima.ipynb) — AR and MA simulated and recovered, a seasonal model, residual checks, intervals
5. [Backtesting](05-backtesting.ipynb) — why a shuffled split lies, expanding windows, baselines, skill, bootstrap intervals
6. [Learned forecasters](06-learned-forecasters.ipynb) — the day-ahead framing, gradient boosting on lags, a temporal CNN

## Challenge · [swiss-forecast](challenge/)

**Day-ahead forecast of Zurich's hourly electricity, scored over a full year no model saw.**

| Model | MAE (MW) | vs "the same day last week" |
|---|---|---|
| temporal CNN | 7.29 | −52 % |
| gradient boosting | 7.46 | −51 % |
| SARIMA × last week's shape | 12.82 | −15 % |
| seasonal naive (the baseline) | 15.13 | — |

Test year 9 November 2025 – 8 November 2026. [The notebook](challenge/swiss-forecast.ipynb) ·
[the numbers](challenge/results.json).

## Key concepts

- A time-zone-aware index; UTC for storage, local time for features
- Trend, seasonality and remainder; STL; the strength of seasonality
- Stationarity, autocorrelation, differencing; the ADF and KPSS tests
- AR, MA, ARIMA and seasonal ARIMA; Ljung-Box; prediction intervals
- Backtesting on expanding windows; MAE, MASE, skill against a baseline
- Lead time and leakage; lag features; learning a correction to a baseline

## Tools

| Tool | Used for |
|---|---|
| `pandas` | time indexes, resampling, time zones |
| `statsmodels` | STL, ACF/PACF, ADF/KPSS, SARIMAX, Ljung-Box |
| `scikit-learn` | gradient boosting, permutation importance |
| `torch` | the temporal CNN |
| `ds_toolbox` | `evaluation` (splits, backtest, bootstrap), `baselines`, `features`, `forecasting` |

## Where it was learned

FHNW `spz` (stochastic processes). The book itself was written in November 2026.
