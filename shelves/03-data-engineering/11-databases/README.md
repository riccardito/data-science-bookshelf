# 11 · Databases

*Shelf III · Data Engineering · FHNW modules: gdb, edbs, ddi*

## Why It Matters

The database is the foundation of any data system. If the data model is wrong, everything built on top is wrong. If it's right, you can build anything.

## Key Concepts

### Relational (SQL)
- Tables, rows, columns, schemas
- Primary keys, foreign keys, relationships (1:1, 1:N, N:M)
- Normalization (1NF → 3NF → BCNF)
- Joins: INNER, LEFT, RIGHT, FULL OUTER
- Indexes: B-tree, hash, composite
- ACID properties: Atomicity, Consistency, Isolation, Durability
- PostgreSQL, MySQL, SQLite

### Document-Oriented (NoSQL)
- Collections, documents, embedded documents
- Schema-flexible: documents in same collection can differ
- MongoDB: BSON format, ObjectId, PyMongo
- When to embed vs. reference
- Aggregation pipeline
- Indexes in MongoDB: compound, text, TTL

### Data Modeling Decisions
- SQL vs. NoSQL: when to use which
- Denormalization for read performance
- Soft delete (`status: 'deleted'`) vs. hard delete
- Audit trails: append-only logs
- Schema migration strategies

## Tools & Libraries

| Tool | Use Case |
|------|----------|
| `pymongo` | MongoDB driver for Python |
| `motor` | Async MongoDB driver |
| `sqlalchemy` | SQL ORM for Python |
| `elasticsearch-py` | Elasticsearch client |
| `redis-py` | Redis client |
| `mongosh` | MongoDB shell |

## Chapters

Read in order: each chapter builds on the one before it.

1. The relational model and SQL
2. Normalisation
3. Indexes and query plans
4. Transactions
5. Document stores
6. Choosing a store

## Challenge

**index-or-not**: one query set on DuckDB and MongoDB over a Swiss open dataset · query time with and without the index

## Where it was learned

FHNW `gdb` `edbs`
