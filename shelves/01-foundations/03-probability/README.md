# 3 · Probability

*Shelf I · Foundations · FHNW modules: wer, wst, dist*

## Why It Matters

Probability is how we reason under uncertainty — which is always. Every measurement has noise. Every prediction has confidence. Every clinical decision balances risk.

> "Correlations are not always Causalities." — Dr. Norma Graf

This one sentence is the entire reason probability theory matters in data science: understanding the difference between "these things happen together" and "this thing causes that thing."

## Key Concepts

### Foundations
- Sample space, events, axioms of probability
- Conditional probability: P(A|B)
- Independence vs. conditional independence
- Law of total probability

### Bayes' Theorem
- P(H|D) = P(D|H) · P(H) / P(D)
- Prior → Evidence → Posterior
- The foundation of Bayesian thinking (see [Bayesian Data Analysis](18-bayesian.md))

### Random Variables & Distributions
- Discrete: Bernoulli, Binomial, Poisson, Geometric
- Continuous: Uniform, Normal/Gaussian, Exponential, Gamma, Beta
- Expectation, variance, moments
- Joint, marginal, conditional distributions

### Key Theorems
- Law of Large Numbers (sample mean → population mean)
- Central Limit Theorem (sums of random variables → Normal)
- Why CLT matters: it's why so many things in nature look Gaussian

### Correlation vs. Causation
- Pearson correlation coefficient ρ
- Spurious correlations (ice cream sales and drowning)
- Confounding variables
- Simpson's paradox
- Causal inference: do-calculus, DAGs, interventions

## The Coffee Factory Connection

The grain size inspection at the coffee factory was probability in action:
- Grain sizes follow a distribution (approximately log-normal)
- The expensive machine measured the probability distribution of grain sizes
- Quality control = checking if the distribution parameters fell within acceptable bounds
- 50kg of coffee per day, measured against a probabilistic standard

This is the same pattern as clinical data:
- Lab values follow distributions (reference ranges are percentiles)
- "Abnormal" means "outside the expected distribution for healthy population"
- Drug interaction risk is a conditional probability: P(adverse event | drug A AND drug B)

## Tools & Libraries

| Tool | Use Case |
|------|----------|
| `scipy.stats` | Distributions, tests, PDF/CDF |
| `numpy.random` | Random number generation, sampling |
| `statsmodels` | Statistical models, hypothesis testing |

## Chapters

Read in order: each chapter builds on the one before it.

1. [Counting and axioms](01-counting-and-axioms.ipynb) — permutations and combinations, Swiss Lotto, the birthday problem, every count checked by simulation
2. [Random variables](02-random-variables.ipynb) — pmf, pdf, cdf, expectation, linearity, and why E[g(X)] is not g(E[X])
3. [The common distributions](03-the-common-distributions.ipynb) — where each distribution comes from; four families fitted to one dataset that agree on the data and not on the tail
4. [Joint, conditional, Bayes](04-joint-conditional-bayes.ipynb) — conditioning, independence, Bayes' theorem and the base-rate fallacy
5. [The law of large numbers and the CLT](05-law-of-large-numbers-and-clt.ipynb) — averages, sigma over root n, the cost of a rare event, heavy tails
6. [Monte Carlo](06-monte-carlo.ipynb) — estimating by sampling, importance sampling for a rare event, validating a model two ways

## Challenge · [rockfall](challenge/)

**From one season of 90 rocks, how well can you estimate how often a rock breaks through a net?** The
seeded truth is 0.0165 a year. Over 100 seasons, even the true distribution family lands within a factor
of two only a third of the time, and the lognormal -- the family the 2019 analysis chose -- is a median
50 times too high. [The notebook](challenge/rockfall.ipynb) · [the numbers](challenge/results.json).

## Where it was learned

[`FHNW-Projects/Probabilities`](https://github.com/riccardito/FHNW-Projects) -- the 2019 Steinschlag challenge, redone here
