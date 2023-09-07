import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_TAICHI_QUOTE_TABLE = (
    "CREATE TABLE IF NOT EXISTS taichi (id SERIAL PRIMARY KEY, quote TEXT);"
)
INSERT_TAICHI_QUOTE_RETURN_ID = "INSERT INTO taichi (quote) VALUES (%s) RETURNING id;"

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/api/taichi")
def create_taichi_quote():
    data = request.get_json()
    quote = data["quote"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TAICHI_QUOTE_TABLE)
            cursor.execute(INSERT_TAICHI_QUOTE_RETURN_ID, (quote,))
            quote_id = cursor.fetchone()[0]
    return { 
        "id" : quote_id,
        "message": f"Quote ({quote}) was created!"
    }, 201