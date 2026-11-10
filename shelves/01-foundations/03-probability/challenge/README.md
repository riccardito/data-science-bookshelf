# Challenge · rockfall

**From one season of rockfalls -- three months, about 90 rocks -- how well can you estimate how often a
rock breaks through a protection net in a year?**

The slope is seeded, so the answer is known: **0.0165 breaches a year**, one in about 60 years.

| Mass distribution fitted | the observed season | 100 seasons: median | 90 % range | within 2x of the truth |
|---|---|---|---|---|
| lognormal | 85x | 50x | 12-165x | 0 % |
| gamma (the true family) | 0.85x | 0.51x | 0.002-5.8x | 33 % |
| Weibull | 0.78x | 0.58x | 0.0002-6.0x | 35 % |
| exponential | 1.7x | 0.81x | 0.05-4.6x | 43 % |
| whichever AIC picks | 1.7x (exponential) | 0.80x | 0.001-6.2x | 38 % |

- **One season does not contain the tail.** No observed rock comes near 500 kJ; every predicted breach
  comes from the fitted distribution beyond the data, and even the true family misses by more than a
  factor of two in two seasons out of three.
- **The one-parameter exponential, a wrong family, behaves best** -- in the tail, the variance of an
  extra parameter costs more than the bias of the wrong shape.
- **The lognormal is always far too high.** The family choice alone can multiply the answer fifty-fold.

**The model** follows the FHNW probability challenge "Steinschlag" (2019, report in
[`FHNW-Projects/Probabilities`](https://github.com/riccardito/FHNW-Projects)): two zones, one net
emptied daily at 08:00, a break at 1000 kJ, or at 500-1000 kJ into a net holding 2000 kg. Zone 1 is
fitted to the 68 rocks the report prints; zone 2's masses and speeds are chosen so the model
reproduces the report's 0.016 a year (`ds_toolbox.rockfall`). The observed season is
[`data/samples/rockfall_season.csv`](../../../../data/samples/rockfall_season.csv) -- seeded, not measured.

Run it: `jupyter nbconvert --to notebook --execute rockfall.ipynb` -- offline, about two minutes.
The numbers go to [`results.json`](results.json).
