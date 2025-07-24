from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

AIRTABLE_PAT = os.getenv("AIRTABLE_PAT")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_PAT}",
    "Content-Type": "application/json"
}

@app.route("/get-records", methods=["GET"])
def get_records():
    table_name = request.args.get("table")
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}"
    response = requests.get(url, headers=HEADERS)
    return jsonify(response.json())

@app.route("/update-record", methods=["POST"])
def update_record():
    data = request.json
    table_name = data.get("table")
    record_id = data.get("record_id")
    fields = data.get("fields")
    
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_name}/{record_id}"
    response = requests.patch(url, headers=HEADERS, json={"fields": fields})
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)

