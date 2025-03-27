# edsql_compiler.py
import ply.lex as lex
import ply.yacc as yacc
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------- Lexical Analysis -------------------------
tokens = (
    'SELECT', 'FROM', 'WHERE', 'PLOT', 'BAR', 'GRAPH', 'LINE', 'PIE', 'CHART',
    'IDENTIFIER', 'NUMBER', 'STRING', 'COMMA', 'GREATER_THAN', 'EQUALS', 'SEMICOLON',
    'LPAREN', 'RPAREN', 'AVG', 'GROUP', 'BY', 'PERFORMANCE_SCORE'
)

reserved = {
    'SELECT': 'SELECT',
    'FROM': 'FROM',
    'WHERE': 'WHERE',
    'PLOT': 'PLOT',
    'BAR': 'BAR',
    'GRAPH': 'GRAPH',
    'LINE': 'LINE',
    'PIE': 'PIE',
    'CHART': 'CHART',
    'AVG': 'AVG',
    'GROUP': 'GROUP',
    'BY': 'BY',
    'PERFORMANCE_SCORE': 'PERFORMANCE_SCORE'
}

t_SELECT = r'SELECT'
t_FROM = r'FROM'
t_WHERE = r'WHERE'
t_PLOT = r'PLOT'
t_BAR = r'BAR'
t_GRAPH = r'GRAPH'
t_LINE = r'LINE'
t_PIE = r'PIE'
t_CHART = r'CHART'
t_AVG = r'AVG'
t_GROUP = r'GROUP'
t_BY = r'BY'
t_PERFORMANCE_SCORE = r'PERFORMANCE_SCORE'
t_COMMA = r','
t_GREATER_THAN = r'>'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ------------------------- Parsing -------------------------
def p_query(p):
    '''
    query : SELECT select_list FROM IDENTIFIER where_clause group_by_clause plot_clause SEMICOLON
    '''
    p[0] = ('QUERY', p[2], p[4], p[5], p[6], p[7])

def p_select_list(p):
    '''
    select_list : IDENTIFIER COMMA select_list
                | IDENTIFIER
                | AVG LPAREN IDENTIFIER RPAREN
                | PERFORMANCE_SCORE LPAREN IDENTIFIER COMMA IDENTIFIER RPAREN
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 5:
        p[0] = ('AVG', p[3])
    elif len(p) == 7:
        p[0] = ('CUSTOM_METRIC', p[1], p[3], p[5])

def p_where_clause(p):
    '''
    where_clause : WHERE condition
                 | empty
    '''
    if len(p) == 3:
        p[0] = ('WHERE', p[2])
    else:
        p[0] = None

def p_condition(p):
    '''
    condition : IDENTIFIER GREATER_THAN NUMBER
              | IDENTIFIER EQUALS STRING
    '''
    p[0] = ('CONDITION', p[1], p[2], p[3])

def p_group_by_clause(p):
    '''
    group_by_clause : GROUP BY IDENTIFIER
                    | empty
    '''
    if len(p) == 4:
        p[0] = ('GROUP BY', p[3])
    else:
        p[0] = None

def p_plot_clause(p):
    '''
    plot_clause : PLOT BAR GRAPH
                | PLOT LINE GRAPH
                | PLOT PIE CHART
                | empty
    '''
    if len(p) == 4:
        p[0] = ('PLOT', p[2])
    else:
        p[0] = None

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}')")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# ------------------------- Query Execution -------------------------
df = pd.read_csv('students.csv')

def calculate_performance_score(grades, attendance):
    return (grades * 0.7) + (attendance * 0.3)

def execute_query(query):
    select_list, table, where_clause, group_by_clause, plot_clause = query[1], query[2], query[3], query[4], query[5]
    
    if table != 'students':
        raise ValueError("Only 'students' table is supported.")
    
    result = df.copy()
    
    # Apply WHERE clause
    if where_clause:
        condition = where_clause[1]
        column, operator, value = condition[1], condition[2], condition[3]
        if operator == '>':
            result = result[result[column] > value]
        elif operator == '=':
            result = result[result[column] == value]
    
    # Apply GROUP BY clause
    if group_by_clause:
        group_by_column = group_by_clause[1]
        if isinstance(select_list[0], tuple) and select_list[0][0] == 'AVG':
            result = result.groupby(group_by_column)[select_list[0][1]].mean().reset_index()
    
    # Apply custom metrics
    if isinstance(select_list[0], tuple) and select_list[0][0] == 'CUSTOM_METRIC':
        metric_name, col1, col2 = select_list[0][1], select_list[0][2], select_list[0][3]
        if metric_name == 'PERFORMANCE_SCORE':
            result['PERFORMANCE_SCORE'] = calculate_performance_score(result[col1], result[col2])
            select_columns = ['name', 'PERFORMANCE_SCORE']
        else:
            raise ValueError(f"Unknown metric: {metric_name}")
    else:
        select_columns = select_list
    
    # Select columns
    result = result[select_columns]
    
    # Apply PLOT clause
    if plot_clause:
        plot_type = plot_clause[1]
        if plot_type == 'BAR':
            result.plot(kind='bar', x=select_columns[0], y=select_columns[1])
            plt.show()
        elif plot_type == 'LINE':
            result.plot(kind='line', x=select_columns[0], y=select_columns[1])
            plt.show()
        elif plot_type == 'PIE':
            result[select_columns[0]].value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.show()
    
    return result

# ------------------------- Main Function -------------------------
def main():
    query = input("Enter your EDSQL query: ")
    lexer.input(query)
    tokens = list(lexer)
    print("Tokens:", tokens)
    
    parsed_query = parser.parse(query)
    print("Parsed Query:", parsed_query)
    
    if parsed_query:
        result = execute_query(parsed_query)
        print("Query Result:")
        print(result)
    else:
        print("Failed to parse the query.")

if __name__ == "__main__":
    main()