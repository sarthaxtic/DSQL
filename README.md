# 📊 Domain-Specific Query Language (DSQL) Compiler

A compiler that processes a custom query language (EDSQL) designed for educational data analysis. It allows querying and visualizing student data such as grades, attendance, and performance using both structured queries and natural language input.

---

## ✨ Features

- 🔤 **Lexical and Syntax Analysis** using PLY (`lex` and `yacc`)
- 📥 **Natural Language Query Translation** using spaCy
- 🧠 Support for:
  - `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`, `LIMIT`
  - Aggregates like `AVG`
  - `CUSTOM_METRIC` functions (e.g., Performance Score)
- 📈 Graphical Visualizations:
  - `BAR`, `LINE`, `PIE` graphs
- 📊 Input via structured EDSQL or natural language queries
- 📁 Input data from CSV files (`student_data.csv`)

---


---

## 🛠 Technologies Used

- Python 🐍
- [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/) for lexing and parsing
- [spaCy](https://spacy.io/) for NLP
- [pandas](https://pandas.pydata.org/) for data manipulation
- [matplotlib](https://matplotlib.org/) for data visualization

---

## 📌 Example Queries

### ✅ EDSQL Query:
```sql
SELECT Name, AVG(Grade)
FROM student_data
WHERE Attendance > 75
GROUP BY Class
ORDER BY AVG(Grade) DESC
PLOT BAR GRAPH;
