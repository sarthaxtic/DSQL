from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

@app.route('/execute_query', methods=['POST'])
def execute_query():
    data = request.get_json()
    query = data.get('query', '').lower()

    try:
        with open('students.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

        if 'select' in query:
            headers = rows[0].keys() if rows else []
            selected_rows = [[row[header] for header in headers] for row in rows]
            return jsonify({
                "type": "table",
                "data": {
                    "headers": list(headers),
                    "rows": selected_rows
                }
            })
        elif 'update' in query:
            # Update logic (not implemented for simplicity)
            return jsonify({
                "type": "text",
                "data": "Update successful!"
            })
        else:
            return jsonify({
                "type": "text",
                "data": "Invalid query or syntax error"
            }), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
