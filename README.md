# data-science-bookshelf

[![CI](https://github.com/riccardito/data-science-bookshelf/actions/workflows/ci.yml/badge.svg)](https://github.com/riccardito/data-science-bookshelf/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Data science as a bookshelf: twelve shelves, 48 books, chapters as notebooks that build on each
other, and a measured challenge closing every book.**

To see the whole field, look at the shelf. To understand a topic, take a book down and read it.

- [`CATALOGUE.md`](CATALOGUE.md) — every book, its chapters, its challenge, its state
- [`shelves/`](shelves/) — the books, one folder each
- [`src/ds_toolbox/`](src/ds_toolbox/) — the toolbox every chapter imports

```
make install     # the toolbox and the chapters' libraries (Python 3.11)
make check       # lint, tests, every notebook re-executed offline, the private-term scan
```

*Work in progress: the shelf is catalogued whole; the books are being written.*
