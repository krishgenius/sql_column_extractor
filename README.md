SQL Column Extractor
sql_column_extractor is a Python library that parses SQL queries and extracts the fully qualified column names from SELECT statements. It handles both queries with and without WITH clauses and resolves wildcards (*) in the columns. This library is helpful for SQL query analysis, column lineage tracing, and ensuring completeness of column extraction in large queries.

Features
1.Extracts fully qualified column names from SQL queries.
2.Handles nested SQL queries, including subqueries within WITH clauses.
3.Supports SQL functions, expressions, and complex column calculations.
4.Resolves wildcard (*) columns into specific column names from tables.
5.Works for both simple SELECT queries and more complex queries involving multiple joins and subqueries.


Installation:
Install the package from PyPi:

pip install sql_column_extractor

Usage:
After installing the package, you can use it in your Python code to extract fully qualified columns from SQL queries:

Sample python code:
from sql_column_extractor import extract_sql_columns

query = """
WITH A as (
    SELECT  
     a1,a2,a3,a4, trunc(a5) as a5 from table_a
)
SELECT *
FROM A
"""

columns = extract_sql_columns(query)
print("Extracted columns:", columns)
Example Output
For the above SQL query, the sql_column_extractor will return the following output:
 
Extracted columns: ['A.a1', 'A.a2', 'A.a3', 'A.a4', 'A.trunc(a5) as a5']
How it Works
The library uses regex patterns to parse SQL queries and identify column names.
It also resolves aliases and expands wildcards (*) to list the actual columns in the output.
The output is a list of fully qualified column names in the form table_name.column_name.
Sample Code
Here is another sample that demonstrates how the library handles queries without a WITH clause:

python
Copy code
query = """
SELECT a.a1, a.a2, b.b2
FROM (SELECT a1, a2, a3 FROM table_a) a
JOIN (SELECT b2, b3 FROM table_b) b ON a.a1 = b.b2
"""

columns = extract_sql_columns(query)
print("Extracted columns:", columns)
Example Output
 
Extracted columns: ['a.a1', 'a.a2', 'b.b2']
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contributing
If you would like to contribute, please submit an issue or a pull request on the GitHub repository.
