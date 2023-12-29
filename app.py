import sqlite3
import imdb
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize the IMDb instance
ia = imdb.IMDb()

def fetch_movie_data(code):
    try:
        series = ia.get_movie(code)
        title = series['title']
        year = series['year']
        rating = series['rating']
        return title, year, rating
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

@app.route('/')
def index():
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM movie")
    movies = cur.fetchall()
    con.close()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        imdb_id = request.form['imdb_id']
        movie_data = fetch_movie_data(imdb_id)
        if movie_data:
            con = sqlite3.connect("tutorial.db")
            cur = con.cursor()
            cur.execute("INSERT INTO movie VALUES(?, ?, ?)", movie_data)
            con.commit()
            con.close()
            return redirect(url_for('index'))
    return render_template('add_movie.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete_movie():
    if request.method == 'POST':
        title_to_delete = request.form['title']
        con = sqlite3.connect("tutorial.db")
        cur = con.cursor()
        cur.execute("DELETE FROM movie WHERE title=?", (title_to_delete,))
        con.commit()
        con.close()
        return redirect(url_for('index'))
    return render_template('delete_movie.html')

if __name__ == '__main__':
    # Ensure the database table exists
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS movie(title TEXT, year INT, score REAL)")
    con.commit()
    con.close()

    app.run(debug=True)
