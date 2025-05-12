from edsql_compiler import parser
import pandas as pd
import matplotlib.pyplot as plt
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("students.csv")

def calculate_performance_score(grades, attendance):
    return (grades * 0.7) + (attendance * 0.3)

def convert_to_edsql(nl_query):
    doc = nlp(nl_query.lower())

    if "average" in nl_query and "grades" in nl_query:
        return 'SELECT AVG(grades) FROM students GROUP BY class;'
    elif "performance score" in nl_query:
        return 'SELECT PERFORMANCE_SCORE(grades, attendance) FROM students;'
    elif "plot bar" in nl_query:
        return 'SELECT name, grades FROM students PLOT BAR GRAPH;'
    return None

def execute_query(parsed_query):
    select_list, table, where_clause, group_by_clause, plot_clause = parsed_query[1:]
    result = df.copy()

    if where_clause:
        column, op, value = where_clause[1][1:]
        result = result[result[column] > value] if op == '>' else result[result[column] == value]

    if group_by_clause:
        group_col = group_by_clause[1]
        if isinstance(select_list[0], tuple) and select_list[0][0] == 'AVG':
            result = result.groupby(group_col)[select_list[0][1]].mean().reset_index()

    if isinstance(select_list[0], tuple) and select_list[0][0] == 'CUSTOM_METRIC':
        _, _, col1, col2 = select_list[0]
        result['PERFORMANCE_SCORE'] = calculate_performance_score(result[col1], result[col2])
        select_columns = ['name', 'PERFORMANCE_SCORE']
    else:
        select_columns = [x[1] if isinstance(x, tuple) else x for x in select_list]

    result = result[select_columns]

    if plot_clause:
        plot_type = plot_clause[1]
        if plot_type == 'BAR':
            result.plot(kind='bar', x=select_columns[0], y=select_columns[1])
        elif plot_type == 'LINE':
            result.plot(kind='line', x=select_columns[0], y=select_columns[1])
        elif plot_type == 'PIE':
            result[select_columns[0]].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.show()

    print("Result:")
    print(result)

def main():
    user_input = input("Enter EDSQL or NL query:\n")
    if "select" not in user_input.lower():
        user_input = convert_to_edsql(user_input)
        if not user_input:
            print("Sorry, couldn't understand your natural language query.")
            return
        print("Converted to EDSQL:", user_input)

    parsed = parser.parse(user_input)
    if parsed:
        execute_query(parsed)
    else:
        print("Parsing failed.")

if __name__ == "__main__":
    main()
