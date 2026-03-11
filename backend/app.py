from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Database
conn = sqlite3.connect("alerts.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    camera TEXT,
    event TEXT,
    time TEXT
)
""")
conn.commit()

@app.route("/alert", methods=["POST"])
def receive_alert():
    data = request.json
    c.execute(
        "INSERT INTO alerts (camera, event, time) VALUES (?, ?, ?)",
        (data["camera"], data["event"], datetime.now().strftime("%H:%M:%S"))
    )
    conn.commit()
    return jsonify({"status": "saved"})

@app.route("/alerts", methods=["GET"])
def get_alerts():
    rows = c.execute("SELECT * FROM alerts ORDER BY id DESC").fetchall()
    return jsonify(rows)

app.run(debug=True)

