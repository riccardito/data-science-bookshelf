# 22 · Machine Learning Fundamentals

*Shelf VI · Machine Learning · FHNW modules: gml, ml, cml1*

## Why It Matters

Machine learning is where raw data becomes structured knowledge. It's the transition from "what happened" (descriptive) to "what will happen" (predictive) to "what should we do" (prescriptive).

But remember: ML is only as good as the data it's fed. A model fed unstructured or wrong data is an expensive way to be wrong.

## Key Concepts

### The Landscape

```
Machine Learning
├── Supervised Learning (labeled data)
│   ├── Classification (discrete output)
│   │   ├── Logistic Regression
│   │   ├── Decision Trees / Random Forest
│   │   ├── Support Vector Machines
│   │   ├── k-Nearest Neighbors
│   │   └── Gradient Boosting (XGBoost, LightGBM)
│   └── Regression (continuous output)
│       ├── Linear Regression (→ see 19-regression.md)
│       ├── Decision Tree Regression
│       ├── Random Forest Regression
│       └── Gradient Boosting Regression
├── Unsupervised Learning (no labels)
│   ├── Clustering
│   │   ├── k-Means
│   │   ├── DBSCAN
│   │   ├── Hierarchical
│   │   └── Gaussian Mixture Models
│   ├── Dimensionality Reduction
│   │   ├── PCA (→ see 01-linear-algebra.md)
│   │   ├── t-SNE
│   │   └── UMAP
│   └── Anomaly Detection
│       ├── Isolation Forest
│       └── One-Class SVM
└── Reinforcement Learning (→ see 30-reinforcement-learning.md)
```

### The ML Workflow
1. **Problem framing**: What are we predicting? What's the business value?
2. **Data collection**: Where's the data? Is it enough? Is it representative?
3. **EDA**: Explore before you model (→ see [16-eda.md](16-eda.md))
4. **Feature engineering**: The art of ML — domain knowledge meets data
5. **Model selection**: Start simple (baseline), increase complexity only if needed
6. **Training**: Fit the model to training data
7. **Evaluation**: Test on held-out data. Choose the right metric.
8. **Deployment**: The model is useless until it's in production

### Bias-Variance Tradeoff
- **Bias**: Error from oversimplifying (underfitting)
- **Variance**: Error from overcomplicating (overfitting)
- **Sweet spot**: Enough complexity to capture the pattern, not so much that you memorize noise
- Connection to [Statistical Learning](20-statistical-learning.md)

### Evaluation Metrics

| Task | Metrics |
|------|---------|
| Classification | Accuracy, Precision, Recall, F1, AUC-ROC, Confusion Matrix |
| Regression | MSE, RMSE, MAE, R², Adjusted R² |
| Clustering | Silhouette score, Elbow method, Davies-Bouldin |

### Cross-Validation
- k-Fold CV: split data into k folds, train on k-1, test on 1, rotate
- Stratified k-Fold: preserve class distribution in each fold
- Leave-One-Out: k = n (expensive but unbiased)
- Time-series CV: expanding window (never look into the future)

### Feature Engineering
- Encoding categoricals: one-hot, label, target encoding
- Scaling: StandardScaler (z-score), MinMaxScaler, RobustScaler
- Missing values: imputation (mean, median, KNN, MICE)
- Feature selection: mutual information, recursive elimination, L1 regularization
- Domain features: the most valuable ones come from understanding the problem

## The Coffee Factory as ML

The grain size quality control was a classification problem in disguise:
- **Features**: grain size distribution parameters (mean, variance, skewness)
- **Labels**: pass / fail quality check
- **Model**: the expensive machine was essentially a statistical classifier
- **Threshold**: acceptable distribution parameters = decision boundary
- **Cost of error**: false positive (bad coffee passes) vs. false negative (good coffee rejected)

## Tools & Libraries

| Tool | Use Case |
|------|----------|
| `scikit-learn` | The Swiss army knife — classification, regression, clustering, preprocessing |
| `xgboost` | Gradient boosted trees — often wins Kaggle competitions |
| `lightgbm` | Fast gradient boosting, handles large datasets |
| `catboost` | Gradient boosting with built-in categorical handling |
| `pandas` | Data manipulation before/after modeling |
| `joblib` | Model serialization (save/load trained models) |

## Chapters

Read in order: each chapter builds on the one before it.

1. The learning problem
2. K-NN and trees
3. SVMs
4. Ensembles (forests, boosting)
5. Clustering
6. Dimensionality reduction

## Challenge

**one-dataset-ten-models**: ten learners under one honest CV · the ranking, with intervals

## Where it was learned

`FHNW-Projects/MachineLearning`
