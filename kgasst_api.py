from flask import Flask, request, jsonify
from airtable_manager import get_insurance_expiring, get_loans_due, search_by_field, fetch_table_data

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "KGasst API is running!"})

@app.route("/insurance-expiring", methods=["GET"])
def insurance_expiring():
    days = request.args.get("days", default=30, type=int)
    result = get_insurance_expiring(days)
    return jsonify(result)

@app.route("/loans-due", methods=["GET"])
def loans_due():
    days = request.args.get("days", default=30, type=int)
    result = get_loans_due(days)
    return jsonify(result)

@app.route("/search-llc", methods=["GET"])
def search_llc():
    name = request.args.get("name", default="", type=str)
    if not name:
        return jsonify({"error": "Missing LLC name"}), 400
    result = search_by_field("LLC INFO", "LLC NAME", name.upper())
    return jsonify(result)

@app.route("/buildings", methods=["GET"])
def buildings():
    result = fetch_table_data("BLDGS", max_records=10)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
