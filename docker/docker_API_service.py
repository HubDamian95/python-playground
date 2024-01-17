from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/books', methods=['GET'])
def get_books():
    books = [
        {"id": 1, "title": "Book One"},
        {"id": 2, "title": "Book Two"}
        # Add more books or fetch from a database
    ]
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)