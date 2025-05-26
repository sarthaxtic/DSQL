from matcher_utils import extract_entities

def convert_entities_to_edsql(nl_query):
    entities = extract_entities(nl_query)

    column = entities.get("column")
    operator = entities.get("operator")
    value = entities.get("value")
    agg = entities.get("aggregation")
    group_by = entities.get("group_by")
    plot = entities.get("plot")
    x = entities.get("x")
    y = entities.get("y")
    order = entities.get("order")
    limit = entities.get("limit")
    custom = entities.get("custom_metric")

    if operator: operator = operator.upper()
    if order: order = order.upper()

    # Case: Plot (with x, y and optionally aggregation)
    if plot and x and y:
        return f"SELECT {x}, {y} FROM students PLOT {plot} GRAPH;"

    # Case: Aggregation with grouping
    if agg and column and group_by:
        return f"SELECT {agg}({column}) FROM students GROUP BY {group_by};"

    # Case: Custom metric with WHERE filter
    if custom and operator and value is not None:
        return f"SELECT name, CUSTOM_METRIC({custom}, grades, attendance) FROM students WHERE {custom} {operator} {value};"

    # Case: Custom metric with order and limit
    if custom and order and limit is not None:
        return f"SELECT CUSTOM_METRIC({custom}, grades, attendance) FROM students ORDER BY {custom} {order} LIMIT {limit};"

    # Case: Simple custom metric without ordering
    if custom:
        return f"SELECT CUSTOM_METRIC({custom}, grades, attendance) FROM students;"

    # Case: Filtered WHERE clause
    if column and operator and value is not None:
        return f"SELECT name, {column} FROM students WHERE {column} {operator} {value};"

    # Case: Order by column
    if column and order and limit is not None:
        return f"SELECT name, {column} FROM students ORDER BY {column} {order} LIMIT {limit};"

    return None



