from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_note', methods=['POST'])
def add_note():

    data = request.get_json()
    note = data['note']

    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes(content) VALUES(?)",
        (note,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note Saved Successfully"})

@app.route('/notes')
def get_notes():

    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM notes ORDER BY id DESC"
    )

    notes = cur.fetchall()
    print(notes)

    conn.close()

    return jsonify(notes)

@app.route('/delete_note/<int:id>', methods=['DELETE'])
def delete_note(id):

    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM notes WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted Successfully"})

if __name__ == '__main__':
    app.run(debug=True)