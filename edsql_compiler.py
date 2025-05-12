import ply.lex as lex
import ply.yacc as yacc
import pandas as pd
import matplotlib.pyplot as plt
import spacy

# ------------------ Lexical Analysis ------------------
tokens = (
    'SELECT', 'FROM', 'WHERE', 'PLOT', 'BAR', 'GRAPH', 'LINE', 'PIE', 'CHART',
    'IDENTIFIER', 'NUMBER', 'STRING', 'COMMA', 'GREATER_THAN', 'EQUALS', 'SEMICOLON',
    'LPAREN', 'RPAREN', 'AVG', 'GROUP', 'BY', 'PERFORMANCE_SCORE'
)

reserved = {
    'SELECT': 'SELECT', 'FROM': 'FROM', 'WHERE': 'WHERE',
    'PLOT': 'PLOT', 'BAR': 'BAR', 'GRAPH': 'GRAPH',
    'LINE': 'LINE', 'PIE': 'PIE', 'CHART': 'CHART',
    'AVG': 'AVG', 'GROUP': 'GROUP', 'BY': 'BY',
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
    t.type = reserved.get(t.value.upper(), 'IDENTIFIER')
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# ------------------ Parser ------------------
def p_query(p):
    'query : SELECT select_list FROM IDENTIFIER where_clause group_by_clause plot_clause SEMICOLON'
    p[0] = ('QUERY', p[2], p[4], p[5], p[6], p[7])

def p_select_list(p):
    '''select_list : IDENTIFIER COMMA select_list
                   | IDENTIFIER
                   | AVG LPAREN IDENTIFIER RPAREN
                   | PERFORMANCE_SCORE LPAREN IDENTIFIER COMMA IDENTIFIER RPAREN'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 5:
        p[0] = [('AVG', p[3])]
    elif len(p) == 7:
        p[0] = [('CUSTOM_METRIC', p[1], p[3], p[5])]

def p_where_clause(p):
    '''where_clause : WHERE condition
                    | empty'''
    p[0] = ('WHERE', p[2]) if len(p) == 3 else None

def p_condition(p):
    '''condition : IDENTIFIER GREATER_THAN NUMBER
                 | IDENTIFIER EQUALS STRING'''
    p[0] = ('CONDITION', p[1], p[2], p[3])

def p_group_by_clause(p):
    '''group_by_clause : GROUP BY IDENTIFIER
                       | empty'''
    p[0] = ('GROUP BY', p[3]) if len(p) == 4 else None

def p_plot_clause(p):
    '''plot_clause : PLOT BAR GRAPH
                   | PLOT LINE GRAPH
                   | PLOT PIE CHART
                   | empty'''
    p[0] = ('PLOT', p[2]) if len(p) == 4 else None

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    print(f"Syntax error at token {p.type} ('{p.value}')" if p else "Syntax error at EOF")

parser = yacc.yacc()
