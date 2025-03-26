from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("comments.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          comment TEXT NOT NULL)''')
        conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        comment = request.form["comment"]
        
        with sqlite3.connect("comments.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO comments (name, comment) VALUES (?, ?)", (name, comment))
            conn.commit()
        
        return redirect("/")
    
    with sqlite3.connect("comments.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, comment FROM comments ORDER BY id DESC")
        comments = cursor.fetchall()
    
    return render_template("index.html", comments=comments)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)