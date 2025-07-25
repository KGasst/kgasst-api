from pyairtable import Table
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

def fetch_table_data(table_name, max_records=5):
    """Fetch a limited number of records from a given Airtable table."""
    try:
        table = Table(AIRTABLE_TOKEN, BASE_ID, table_name)
        records = table.all(max_records=max_records)
        return [record['fields'] for record in records]
    except Exception as e:
        return f"Error fetching {table_name}: {e}"

if __name__ == "__main__":
    tables = [
        "LLC INFO", "BLDGS", "UNITS", "LOANS", "INSURANCE",
        "DUE DATES RANDOM", "ETXEA UNITS", "UTILITIES", "CCs", "FIN CEN"
    ]

    for t in tables:
        print(f"\nFetching from {t}...")
        data = fetch_table_data(t)
        print(data)

