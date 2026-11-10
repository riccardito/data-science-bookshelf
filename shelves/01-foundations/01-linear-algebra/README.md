# 1 · Linear Algebra

*Shelf I · Foundations · FHNW modules: gla, ala, lalg1, lag*

## Why It Matters

Linear algebra is the language of data. Every dataset is a matrix. Every transformation is a matrix operation. Every ML algorithm — from linear regression to neural networks — is linear algebra under the hood.

- A patient record with 20 features is a vector in R^20
- A dataset of 1000 patients is a 1000 x 20 matrix
- PCA finds the directions of maximum variance via eigendecomposition
- Neural network layers are matrix multiplications + nonlinear activation

## Key Concepts

### Vectors & Matrices
- Vector spaces, basis, dimension
- Matrix operations: multiplication, transpose, inverse
- Rank, null space, column space

### Systems of Linear Equations
- Gaussian elimination
- LU decomposition
- Solving Ax = b

### Eigenvalues & Eigenvectors
- Characteristic polynomial
- Diagonalization
- Spectral decomposition
- Connection to PCA (principal components = eigenvectors of covariance matrix)

### Matrix Decompositions
- SVD (Singular Value Decomposition) — the Swiss army knife
- QR decomposition
- Cholesky decomposition (for positive definite matrices)

### Norms & Distances
- L1 (Manhattan), L2 (Euclidean), L-infinity norms
- Cosine similarity (used in NLP, recommender systems)
- Frobenius norm for matrices

## Tools & Libraries

| Tool | Use Case |
|------|----------|
| `numpy` | Core matrix operations, broadcasting |
| `scipy.linalg` | Decompositions, solvers |
| `numpy.linalg` | Eigenvalues, SVD, norms |

## Chapters

Read in order: each chapter builds on the one before it.

1. Vectors and spaces
2. Matrices as maps
3. Solving systems (LU)
4. Orthogonality and least squares (QR)
5. Eigenvalues and SVD
6. PCA

*The chapters are being written now; each becomes a notebook in this folder.*

## Challenge

**photo-compress**: rank-k SVD compression of photos · the rank that keeps 95 % of the energy, and PSNR against rank

## Where it was learned

FHNW `gla` `lalg`
