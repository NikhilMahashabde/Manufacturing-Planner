from flask import Flask
import os
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    # connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM mytable;")
    results = cursor.fetchall()
    connection.close()
    return f"{results[0]}"

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
