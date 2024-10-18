import re

def clean_query(custom_query):
    lines = custom_query.splitlines()
    cleaned_lines = []
    for line in lines:
        if not line.strip().startswith('--'):
            cleaned_lines.append(re.sub(r'\s+', ' ', line.strip()))
    return '\n'.join(cleaned_lines)

def extract_with_subqueries(custom_query):
    with_subquery_pattern = r'(\w+)\s+AS\s*\(\s*(SELECT.*?\sFROM\s.*?)(?=\)\s*,|\)\s+SELECT|\))'
    with_subqueries = re.findall(with_subquery_pattern, custom_query, re.IGNORECASE | re.DOTALL)
    return with_subqueries

def resolve_wildcards(columns, alias_to_table, depth=0, max_depth=12):
    if depth > max_depth:
        return columns
    resolved_columns = []
    for col in columns:
        if col == '*':
            for alias, table_columns in alias_to_table.items():
                resolved_columns.extend([f"{alias}.{column}" for column in table_columns])
        elif col.endswith('.*'):
            alias = col.split('.*')[0].strip()
            if alias in alias_to_table:
                expanded_columns = resolve_wildcards(alias_to_table[alias], alias_to_table, depth + 1, max_depth)
                resolved_columns.extend([f"{alias}.{column}" for column in expanded_columns])
            else:
                resolved_columns.append(col)
        else:
            resolved_columns.append(col)
    return resolved_columns

def extract_sql_columns(custom_query):
    alias_to_table = {}
    custom_query = clean_query(custom_query)

    if custom_query.strip().upper().startswith("WITH"):
        with_subqueries = extract_with_subqueries(custom_query)
        for alias, query in with_subqueries:
            columns = extract_columns_from_select(query)
            alias_to_table[alias] = resolve_wildcards(columns, alias_to_table)
        select_pattern = r'\)\s*SELECT\s+(.*?)\s+FROM\s+(.*)'
    else:
        select_pattern = r'SELECT\s+(.*?)\s+FROM\s+(.*)'

    select_match = re.search(select_pattern, custom_query, re.IGNORECASE | re.DOTALL)

    if not select_match:
        return []

    columns_part = select_match.group(1).strip()
    tables_part = select_match.group(2).strip()

    fully_qualified_columns = extract_columns_properly(columns_part)
    tables = re.split(r'\s+(LEFT|RIGHT|INNER|FULL)?\s*JOIN\s+|\s*,\s*', tables_part, flags=re.IGNORECASE)

    for table in tables:
        if not table or table.upper() in ['LEFT', 'RIGHT', 'INNER', 'FULL']:
            continue
        table_parts = re.split(r'\s+ON\s+', table.strip(), flags=re.IGNORECASE, maxsplit=1)[0]

        if re.search(r'[^a-zA-Z0-9_.]', table_parts):
            continue

        table_parts = re.split(r'\s+', table_parts.strip(), maxsplit=1)
        table_name = table_parts[0]
        alias = table_parts[1] if len(table_parts) == 2 else table_name
        alias_to_table[alias] = alias_to_table.get(alias, table_name)

    fully_qualified_columns = resolve_wildcards(fully_qualified_columns, alias_to_table)
    fully_qualified_columns = [remove_extra_dots(column) for column in fully_qualified_columns]
    fully_qualified_columns = list(dict.fromkeys(fully_qualified_columns))

    print("Fully qualified columns:")
    for column in fully_qualified_columns:
        print(column)

    print(f"Total number of fully qualified columns: {len(fully_qualified_columns)}")
    return fully_qualified_columns

def extract_columns_properly(columns_part):
    columns_list = []
    start_idx = 0
    nested_level = 0
    inside_quotes = False

    for i, char in enumerate(columns_part):
        if char == "'":
            inside_quotes = not inside_quotes
        elif char == '(' and not inside_quotes:
            nested_level += 1
        elif char == ')' and not inside_quotes:
            nested_level -= 1
        elif char == ',' and nested_level == 0 and not inside_quotes:
            columns_list.append(columns_part[start_idx:i].strip())
            start_idx = i + 1
    columns_list.append(columns_part[start_idx:].strip())
    return columns_list

def extract_columns_from_select(select_query):
    select_regex = r'SELECT\s+(.*?)\s+FROM\s'
    match = re.search(select_regex, select_query, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    columns_part = match.group(1).strip()
    return extract_columns_properly(columns_part)

def remove_extra_dots(column):
    parts = column.split('.')
    return '.'.join(parts[-2:]) if len(parts) > 2 else column
