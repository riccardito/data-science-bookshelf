"""The toolbox on the data-science bookshelf.

Every chapter of every book imports from here instead of pasting helpers from notebook to
notebook. Five modules:

- ``io`` -- public data (opendata.swiss and plain URLs), cached on disk, with the committed
  samples as the offline fallback
- ``evaluation`` -- error metrics, time-series cross-validation and backtesting
- ``baselines`` -- the naive models a real model has to beat before it counts
- ``viz`` -- one plotting style for the whole shelf
- ``tracking`` -- a run log that uses MLflow when it is installed and plain JSON when it is not
"""

__version__ = "0.1.0"
