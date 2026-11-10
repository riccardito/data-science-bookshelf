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

1. Counting and axioms
2. Random variables
3. The common distributions
4. Joint, conditional, Bayes
5. Law of large numbers and CLT by simulation
6. Monte Carlo

*The chapters are being written now; each becomes a notebook in this folder.*

## Challenge

**rockfall**: the Steinschlag challenge redone with the toolbox · the yearly breach probability with its interval

## Where it was learned

`FHNW-Projects/Probabilities`
