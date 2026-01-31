from flask import Flask, render_template, request, jsonify, send_file, Response
from modules.mod06_pipeline import run_pipeline
import pandas as pd
import numpy as np
import json
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWITTER_BEARER = os.getenv("TWITTER_BEARER")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

os.makedirs("outputs", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query")

    df = run_pipeline(
        NEWS_API_KEY,
        TWITTER_BEARER,
        YOUTUBE_API_KEY,
        query
    )

    # Convert DataFrame → pure Python
    records = df.head(100).to_dict(orient="records")

    # HARD FIX: remove NaN manually
    clean_records = []
    for row in records:
        clean_row = {}
        for k, v in row.items():
            if isinstance(v, float) and pd.isna(v):
                clean_row[k] = None
            else:
                clean_row[k] = v
        clean_records.append(clean_row)

    file_id = str(uuid.uuid4())
    csv_path = f"outputs/result_{file_id}.csv"
    df.to_csv(csv_path, index=False)

    payload = {
        "results": clean_records,
        "csv_id": file_id
    }

    # STRICT JSON (NaN NOT allowed)
    return Response(
        json.dumps(payload, allow_nan=False),
        mimetype="application/json"
    )

@app.route("/download/<csv_id>")
def download(csv_id):
    path = f"outputs/result_{csv_id}.csv"
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
