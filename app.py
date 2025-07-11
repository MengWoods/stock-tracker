# app.py

from flask import Flask, render_template, request, redirect, url_for
import json
import os
import subprocess


app = Flask(__name__)

TRACKED_FILE = "tracked_stocks.json"
DATA_FILE = "latest_data.json"

@app.route("/refresh")
def refresh_data():
    subprocess.run(["python", "stock_tracker.py"])
    return redirect(url_for("index"))

def load_tracked_stocks():
    if not os.path.exists(TRACKED_FILE):
        return []
    with open(TRACKED_FILE, "r") as f:
        return json.load(f)

def save_tracked_stocks(stocks):
    with open(TRACKED_FILE, "w") as f:
        json.dump(stocks, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        symbol = request.form.get("symbol", "").strip().upper()
        tracked = load_tracked_stocks()

        if symbol:
            if action == "add" and symbol not in tracked:
                tracked.append(symbol)
            elif action == "remove" and symbol in tracked:
                tracked.remove(symbol)

            save_tracked_stocks(tracked)

            # ⬇️ Automatically update stock data
            subprocess.run(["python", "stock_tracker.py"])

        return redirect(url_for("index"))

    # Load current stock data
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        stocks = data["stocks"]
        last_updated = data["last_updated"]
    except:
        stocks = []
        last_updated = "Unavailable"

    tracked_symbols = load_tracked_stocks()
    return render_template("index.html", stocks=stocks, last_updated=last_updated, tracked=tracked_symbols)


    # Load current stock data
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        stocks = data["stocks"]
        last_updated = data["last_updated"]
    except:
        stocks = []
        last_updated = "Unavailable"

    tracked_symbols = load_tracked_stocks()
    return render_template("index.html", stocks=stocks, last_updated=last_updated, tracked=tracked_symbols)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
