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

1. [Vectors and spaces](01-vectors-and-spaces.ipynb) — combinations, span, rank, length and angle, cosine similarity
2. [Matrices as maps](02-matrices-as-maps.ipynb) — rotation, scaling, shear, projection; composition; the determinant
3. [Solving systems](03-solving-systems.ipynb) — Gaussian elimination by hand, LU, the condition number
4. [Orthogonality and least squares](04-orthogonality-and-least-squares.ipynb) — projection, Gram-Schmidt, why QR beats the normal equations
5. [Eigenvalues and the SVD](05-eigenvalues-and-svd.ipynb) — power iteration, rotate-stretch-rotate, the best low-rank approximation
6. [PCA](06-pca.ipynb) — principal components from the SVD, on handwritten digits

## Challenge · [photo-compress](challenge/)

**How few singular values does an image need?** Rank for a PSNR of 30 dB: terrain **23**, photograph
**88**, document **101** -- although the document keeps 95 % of its energy at rank 2. Smooth surfaces are
low-rank; text is not. [The notebook](challenge/photo-compress.ipynb) · [the numbers](challenge/results.json).

## Where it was learned

FHNW `gla` `lalg`
