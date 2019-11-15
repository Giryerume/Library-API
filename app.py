from flask import Flask, jsonify, request, redirect
import json

app = Flask(__name__)

with open('acervo.json','r') as f:
  books = json.load(f)

@app.route('/')
def hello():
    return redirect('/books')

@app.route('/books', methods=['GET'])
def home():
    return jsonify(books), 200

@app.route('/books/author/<string:author>', methods=['GET'])
def books_per_author(author):
    books_per_author = [book for book in books if book['author'] == author]
    if len(books_per_author) > 0:
        return jsonify(books_per_author), 200
    return jsonify({'error':'book not found'}), 404

@app.route('/books/title/<string:title>', methods=['GET'])
def books_per_title(title):
    books_per_title = [book for book in books if book['title'] == title]
    if len(books_per_title) > 0:
        return jsonify(books_per_title), 200
    return jsonify({'error':'book not found'}), 404

@app.route('/books/<int:id>', methods=['GET'])
def books_per_id(id):
    for book in books:
        if book['id'] == id:
            return jsonify(book), 200
    return jsonify({'error':'book not found'}), 404

@app.route('/books/author/<int:id>', methods=['PUT'])
def change_author(id):
    for book in books:
        if book['id'] == id:
            book['author'] = request.get_json().get('author')
            return jsonify(book), 200
    return jsonify({'error': 'book not found'}), 404

@app.route('/books/title/<int:id>', methods=['PUT'])
def change_title(id):
    for book in books:
        if book['id'] == id:
            book['title'] = request.get_json().get('title')
            return jsonify(book), 200
    return jsonify({'error': 'book not found'}), 404

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    books.append(data)
    return jsonify(data), 201

@app.route('/books/<int:id>', methods=['DELETE'])
def remove_book(id):
    index = id - 1
    del books[index]
    return jsonify({'message': 'the book was deleted'}), 200

@app.route('/books/update')
def update():
    with open('acervo.json', 'w') as file:
        json.dump(books, file, indent=2)
    return jsonify({'message': 'the library was updated'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)
