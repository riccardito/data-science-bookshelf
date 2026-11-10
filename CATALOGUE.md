# The catalogue

> To see the whole field, look at the shelf. To understand a topic, take a book down and read it, and
> then the book is what matters, not the shelf.

This file is the shelf's index card: every book that belongs on it, whether it is written yet or not.
Twelve shelves, 48 books. A book has chapters, and each chapter is a Jupyter notebook. Chapter 1 lays
the foundation and the last chapter is the most advanced. Every book closes on a **challenge**, a
small project that measures one number. A book without its challenge is not finished.

**State** in the tables below:

- `built` — chapters and challenge are in the repository
- `being written` — chapters are landing now
- `cover` — the book's README (the topic page) exists, but no chapters yet
- `planned` — catalogued here, not started
- a sibling repository named in the *Challenge* column means that repository *is* the challenge

An empty book is more honest than a padded one. Planned books stay planned until they are written.

## The layout

```
data-science-bookshelf/
├── README.md                 the challenges and their numbers first, then the shelf
├── CATALOGUE.md              this file
├── src/ds_toolbox/           the toolbox every chapter imports
│   ├── io.py                 opendata.swiss and other public sources, cached, sample fallback
│   ├── evaluation.py         metrics, time-series cross-validation, backtesting
│   ├── baselines.py          the naive models every challenge must beat
│   ├── viz.py                one plotting style for the whole shelf
│   └── tracking.py           MLflow runs, local file store
├── shelves/
│   ├── 01-foundations/
│   │   ├── README.md         the shelf: what its books cover, in which order to read them
│   │   ├── 01-linear-algebra/
│   │   │   ├── README.md     the book's cover: concepts, tools, limits, where it was learned
│   │   │   ├── 01-vectors-and-spaces.ipynb
│   │   │   ├── …
│   │   │   └── challenge/    the project, its README with the number, a `make` target
│   │   └── …
│   └── …                     02-programming … 12-cross-cutting
├── data/samples/             small committed slices, so everything runs offline
├── tests/                    the toolbox's tests
└── Makefile                  install · test · lint · notebooks · demo
```

Books keep the knowledge base's global numbers (1–48), so a book is findable by its number from
anywhere.

## How a chapter is written

1. **One notebook, one idea.** About 15 minutes of reading. It opens with *Builds on:* (the earlier
   chapter or book) and *You will:*, and it closes with *Exercises* and *Next:*.
2. **It runs offline.** Data comes from `data/samples/` or is generated in the notebook. No network, no
   key. `ds_toolbox.io` fetches the full series only on request.
3. **It is executed in CI.** Every notebook runs on each push (`nbmake`, Python 3.11, a time limit per
   notebook), and the outputs are committed so GitHub renders the chapter readably.
4. **Shared code lives in `ds_toolbox`**, never pasted from notebook to notebook. If a chapter needs a
   helper twice, the helper moves into the package and gets a test.
5. **Seeds are fixed.** A rerun gives the same numbers as the committed outputs.
6. **From scratch first, then the library.** Where it teaches something (least squares, backprop,
   Metropolis), the chapter writes the 30-line version and then shows that the library agrees.

## The reading path

```
 I Foundations ─► II Programming ─► III Data Engineering ─► IV Exploration
                                                                 │
          VII Deep Learning ◄─ VI Machine Learning ◄─ V Statistical Learning
                 │
                 └─► VIII Specialized Domains

 IX Visualization · X Ethics & Law · XI Applied DS · XII Cross-cutting — read alongside, from the start
```

---

## I · Foundations

| # | Book | Chapters (foundation → advanced) | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 1 | Linear Algebra | vectors and spaces · matrices as maps · solving systems (LU) · orthogonality and least squares (QR) · eigenvalues and SVD · PCA | **photo-compress**: rank-k SVD compression of a photo, a terrain and a document · the rank for 95 % energy and for 30 dB | FHNW `gla` `lalg` | **built** · [read it](shelves/01-foundations/01-linear-algebra/) · 30 dB at rank 23-101 |
| 2 | Analysis | limits and continuity · derivatives and the chain rule · Taylor series · integrals · gradients in many variables · automatic differentiation | **tiny-autodiff**: reverse-mode autodiff in ~100 lines · the largest gradient error against finite differences | FHNW `gan` `an1` `an2` | planned |
| 3 | Probability | counting and axioms · random variables · the common distributions · joint, conditional, Bayes · law of large numbers and CLT by simulation · Monte Carlo | **rockfall**: the Steinschlag challenge redone with the toolbox · the yearly breach probability with its interval | `FHNW-Projects/Probabilities` | **being written** |
| 4 | Statistics | descriptive statistics · sampling distributions · confidence intervals · hypothesis tests · the bootstrap · multiple testing | **coverage-check**: bootstrap against t-intervals by simulation · the empirical coverage of a 95 % interval | FHNW `stagl` `wst` | planned |
| 5 | Numerics | floating point · root finding · interpolation · numerical integration · ODE solvers · conditioning | **ode-race**: Euler, RK4 and `scipy` on an SIR model · the measured order of convergence | FHNW `num` | planned |

## II · Programming & Algorithms

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 6 | Python | the data model · iteration and generators · typing and dataclasses · packaging · testing with pytest · vectorising with NumPy | **this repository's toolbox**: `ds_toolbox` itself · its test coverage, held in CI | `tardoc-validator` | **being written** (the package) |
| 7 | R | vectors and data frames · the tidyverse · ggplot2 · models in R · Quarto | **r-analysis**: one regression in R and in Python · the largest coefficient difference (should be 0) | FHNW `prr` | planned |
| 8 | Algorithms & Data Structures | complexity · sorting and searching · hashing · trees and heaps · graphs (BFS, Dijkstra) · dynamic programming | **rail-routes**: shortest paths on the SBB timetable (GTFS) · nodes expanded by A* against Dijkstra | FHNW `algd1` `algd2` | planned |
| 9 | Software Engineering | version control · testing · design and architecture · CI/CD · documentation | → [`agora-method`](https://github.com/riccardito/agora-method) | FHNW `swa` `devops` | cover via sibling |
| 10 | OOP & Functional Programming | objects and protocols · composition over inheritance · pure functions · higher-order functions · choosing a paradigm | **two-pipelines**: one feature pipeline as an estimator class and as composed functions · the same output, and which is shorter to test | FHNW `ofp` | planned |

## III · Data Engineering

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 11 | Databases | the relational model and SQL · normalisation · indexes and query plans · transactions · document stores · choosing a store | **index-or-not**: one query set on DuckDB and MongoDB over a Swiss open dataset · query time with and without the index | FHNW `gdb` `edbs` | cover |
| 12 | Data Wrangling | tidy data · pandas · missing values · joins · reshaping · validating a frame | → [`tardoc-validator`](https://github.com/riccardito/tardoc-validator) | `FHNW-Projects/DataWrangling` | planned |
| 13 | Data Acquisition | HTTP and APIs · scraping politely · streams and IoT · sensor data | **collector**: a cached, retrying collector for a MeteoSwiss or opendata.swiss feed · the share of requests served from cache | `FHNW-Projects/internetOfThings` | planned |
| 14 | Cloud & Infrastructure | containers · cloud storage and compute · distributed computing (DuckDB, Dask) · cost | **sbb-punctuality**: a year of SBB actual times · rows per second, and cost per run | FHNW `cic` `hpc` | planned |
| 15 | Information Systems | networks · operating systems · system design · the architecture of a data platform | **small-stack**: a reproducible compose stack with health checks · time from clone to green | FHNW `insy` | planned |

## IV · Exploratory Data Analysis

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 16 | Exploratory Data Analysis | one variable · two variables · outliers · patterns of missingness · from a pattern to a hypothesis | **municipalities**: an EDA of the BFS municipal portraits, ending in three written hypotheses · the hypotheses, handed to book 17 | FHNW `eda` | planned |
| 17 | Data Analysis | tests in practice · effect sizes · power · a reproducible analysis · p-hacking | **pre-registered**: book 16's hypotheses tested as registered · three effect sizes with intervals | FHNW `dan` | planned |
| 18 | Bayesian Data Analysis | Bayes on a grid · conjugate priors · Metropolis by hand · PyMC · hierarchical models · model checking | **cantons**: a hierarchical model of a cantonal rate · held-out log-likelihood against the raw rates | FHNW `bda` | planned |

## V · Statistical Learning & Regression

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 19 | Linear & Logistic Regression | least squares from scratch · diagnostics · ridge and lasso · logistic regression · GLMs (Poisson) · reading coefficients | **rents**: Swiss rent prices from public data · held-out RMSE and the coefficients that carry it | `FHNW-Projects/MachineLearning` | planned |
| 20 | Statistical Learning | bias and variance · resampling and cross-validation · model selection · trees and splines · a first ensemble | **cv-honesty**: k-fold and leave-one-out against the true test error, by simulation · the bias of each estimate | FHNW `stl` | planned |
| 21 | Time Series | time as an index · trend and seasonality · stationarity and autocorrelation · ARIMA and SARIMA · backtesting and time-series CV · learned forecasters (boosting on lags, a small temporal CNN) | **swiss-forecast**: Zurich's hourly electricity, day ahead · MAE of three models against the seasonal baseline | FHNW `spz` | **built** · [read it](shelves/05-statistical-learning/21-time-series/) · MAE 7.29 MW against 15.13 |

## VI · Machine Learning

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 22 | Machine Learning Fundamentals | the learning problem · k-NN and trees · SVMs · ensembles (forests, boosting) · clustering · dimensionality reduction | **one-dataset-ten-models**: ten learners under one honest CV · the ranking, with intervals | `FHNW-Projects/MachineLearning` | cover |
| 23 | Applied Machine Learning | feature engineering · pipelines · leakage · imbalanced data · tracking and a model registry · serving | **served**: one model from notebook to an HTTP endpoint, tracked in MLflow · its metric and p95 latency | FHNW `aml` | planned |
| 24 | Efficient ML Algorithms | the cost of a learner · approximate nearest neighbours · online learning · sketches | **ann-or-exact**: exact search against an ANN index · recall@10 against queries per second | FHNW `eml` | planned |
| 25 | Optimization | convexity · gradient descent and its family · linear and integer programs · metaheuristics · hyperparameter search | **ward-rostering**: a rostering problem as a MILP · constraint violations and the optimality gap | FHNW `oml` | planned |

## VII · Deep Learning

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 26 | Deep Learning Fundamentals | the perceptron · an MLP in NumPy · backpropagation · training (optimisers, regularisation) · CNNs · RNNs and LSTMs | **from-scratch**: the NumPy MLP against the same net in PyTorch · the accuracy gap (should be ~0) | `FHNW-Projects/DeepLearning` | planned |
| 27 | DL on Images & Signals | images as arrays · classical image processing · geometry and distortion (what a phone photo does) · detection · CNNs on images (and when transfer learning pays) · OCR and documents | **qr-bill-reader**: synthetic Swiss QR bills photographed badly · fields read correctly, per image quality | FHNW `dlbs` `bver` | **built** · [read it](shelves/07-deep-learning/27-dl-vision-signals/) · 83 % of fields from a blurred photo |
| 28 | Advanced Deep Learning | attention · transformers · pretrained models and fine-tuning · embeddings and retrieval · generative models | → [`fedlex-rag`](https://github.com/riccardito/fedlex-rag) | FHNW `vdl` | planned |

## VIII · Specialized Domains

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 29 | Natural Language Processing | text as data · tokenisation · embeddings · classification · LLMs and prompting · evaluating text systems | → [`fedlex-rag`](https://github.com/riccardito/fedlex-rag) | `FHNW-Projects/nlp` | cover |
| 30 | Reinforcement Learning | bandits · Markov decision processes · dynamic programming · Q-learning · policy gradients | **gridworld**: tabular Q-learning against a random and a greedy agent · reward per episode | FHNW `rle` | planned |
| 31 | Recommender Systems | collaborative filtering · content-based · matrix factorisation · hybrids · offline evaluation | **recommend**: the Mini-Challenge 2 redone · NDCG@10 against the popularity baseline | `FHNW-Projects/Recommendersystems` | planned |
| 32 | Graph Machine Learning | graphs and centrality · communities · node embeddings · graph neural networks | **transit-communities**: communities in the Swiss transit graph · modularity | FHNW `cgml` `sna` | planned |
| 33 | Explainable AI | global and local explanations · permutation importance · SHAP · LIME · counterfactuals · limits | **explain-the-rents**: book 19's model explained two ways · rank agreement of SHAP and permutation importance | FHNW `eai` | planned |

## IX · Data Visualization & Communication

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 34 | Data Visualization | perception · choosing a chart · matplotlib · plotly · colour and accessibility | **redesign**: three published charts redrawn, before and after · how many lookups a reader needs, before and after | FHNW `gdv` | cover |
| 35 | Visual Analytics | interactive exploration · dashboards · linked views | **forecast-board**: a dashboard over `swiss-forecast`'s backtests · runs from the committed results alone | FHNW `van` | planned |
| 36 | Storytelling with Data | the narrative · one finding, one page · writing for a reader | **one-pager**: a challenge's result as a one-page brief | FHNW `std` | planned |

## X · Ethics, Law & Society

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 37 | Data Ethics | where bias comes from · fairness metrics · transparency · responsible AI | **fairness-audit**: a public credit-style dataset audited and mitigated · the parity gap before and after | FHNW `eim` | planned |
| 38 | Data Law | the DSG and the GDPR · anonymous against pseudonymous · data licences · the AI Act | **k-anonymity**: a public microdata sample made k-anonymous · re-identification risk before and after | FHNW `dre` | planned |
| 39 | Sustainable Data Science | the energy of training · measuring it · greener choices | **joules**: books 26 and 27's trainings measured · kWh and CO₂ per run | FHNW `ngs` | planned |

## XI · Applied Data Science & Business

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 40 | Data Science Process | CRISP-DM · framing a problem · scoping · delivering | → [`tardoc-validator`](https://github.com/riccardito/tardoc-validator), the process written down | FHNW `gds` | planned |
| 41 | Design Thinking for DS | user research · requirements · prototyping | none yet, catalogued for completeness | FHNW `dtds` | planned |
| 42 | Data-Driven Business Models | where data creates value · business models · strategy | none yet, catalogued for completeness | FHNW `dgm` | planned |
| 43 | System Modeling & Simulation | system dynamics · agent-based models · discrete-event simulation · validating a simulation | **counter-queue**: a discrete-event model of a service counter · waiting time against staffing | FHNW `mss` | planned |
| 44 | Scientific Methods | research design · reproducibility · scientific writing | **this shelf reruns**: every notebook re-executed in CI · the share that reproduces its committed numbers | FHNW `wisa` | planned |

## XII · Cross-Cutting Skills

| # | Book | Chapters | Challenge · the number | Evidence | State |
|---|---|---|---|---|---|
| 45 | Knowledge Management | personal knowledge systems · information literacy · this shelf as a system | → [`agora-method`](https://github.com/riccardito/agora-method) and this repository | FHNW `pwm` | planned |
| 46 | AI-Assisted Programming | prompting · agents and tools · evaluating agent work · the risks | → [`agora-method`](https://github.com/riccardito/agora-method) | FHNW `kip` | cover |
| 47 | Security | threat modelling · application security · secrets · cryptography basics | **scan-the-shelf**: the secrets scan in this repository's CI · findings (must be 0) | FHNW `infsec` | planned |
| 48 | Web Technologies | HTTP · HTML, CSS, JS · Flask and FastAPI · APIs | → book 23's endpoint | FHNW `wet` `webpr` | planned |

---

**Counts:** 48 books · about 250 chapters planned · 4 books being written first (1, 3, 21, 27)
plus the toolbox -- 21 and 27 built, 1 and 3 next · 7 sibling-repository challenges · 5 covers carried over from the knowledge base.
