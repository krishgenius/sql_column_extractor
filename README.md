# SQL Column Extractor

`sql_column_extractor` is a Python library designed to extract fully qualified column names from SQL queries, including complex queries with `WITH` clauses, joins, and nested subqueries. The library efficiently processes SQL queries and returns a list of all the columns used, ensuring accurate handling of wildcards, alias resolution, and multi-line expressions.

## Features

- **Handle WITH Clauses**: Extract columns from SQL queries that use `WITH` clauses (Common Table Expressions).
- **Resolve Wildcards**: Automatically expand wildcard (`*`) columns and resolve them based on table aliases.
- **Support Complex Queries**: Handle nested subqueries, join conditions, and complex column expressions (e.g., functions with multiple parentheses and nested clauses).
- **Case Insensitive Parsing**: Query parsing is case-insensitive for flexibility.
- **Deduplicate Columns**: Avoid duplicate column names in the output.
- **Multi-line Support**: Handle multi-line SQL expressions gracefully.

## Installation

You can install `sql_column_extractor` using `pip`:

```bash
pip install sql_column_extractor
