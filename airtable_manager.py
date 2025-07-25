from pyairtable import Api
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

# Initialize Airtable API
api = Api(AIRTABLE_TOKEN)
base = api.base(BASE_ID)

# ----------- CORE FUNCTIONS -----------

def fetch_table_data(table_name, max_records=5):
    """Fetch records from a given Airtable table."""
    try:
        table = base.table(table_name)
        records = table.all(max_records=max_records)
        return [r['fields'] for r in records]
    except Exception as e:
        return f"Error fetching {table_name}: {e}"

def search_by_field(table_name, field_name, value):
    """Search for records in a table by matching a field."""
    try:
        table = base.table(table_name)
        formula = f"{{{field_name}}} = '{value}'"
        records = table.all(formula=formula)
        return [r['fields'] for r in records]
    except Exception as e:
        return f"Error searching {table_name}: {e}"

def get_insurance_expiring(days=30):
    """Find insurance policies that expire within X days."""
    try:
        table = base.table("INSURANCE")
        cutoff_date = datetime.now() + timedelta(days=days)
        records = table.all()
        expiring = []
        for r in records:
            fields = r['fields']
            renew_date = fields.get("RENEW DATE")
            if renew_date:
                try:
                    date_obj = datetime.strptime(renew_date, "%Y-%m-%d")
                    if date_obj <= cutoff_date:
                        expiring.append(fields)
                except ValueError:
                    continue
        return expiring
    except Exception as e:
        return f"Error checking insurance dates: {e}"

def get_loans_due(days=30):
    """Find loans due within X days based on PAYMT DUE/MO."""
    try:
        table = base.table("LOANS")
        cutoff_day = datetime.now().day + days
        records = table.all()
        due = []
        for r in records:
            fields = r['fields']
            due_date = fields.get("PAYMT DUE/MO")
            if due_date:
                try:
                    day_int = int(due_date.replace("th", "").replace("st", "").replace("nd", "").replace("rd", ""))
                    if day_int <= cutoff_day:
                        due.append(fields)
                except ValueError:
                    continue
        return due
    except Exception as e:
        return f"Error checking loan due dates: {e}"

# ----------- TEST RUN -----------

if __name__ == "__main__":
    print("\n✅ Testing Airtable Manager")
    print("Fetching 3 BLDGS records:")
    print(fetch_table_data("BLDGS", max_records=3))

    print("\nSearching for LLC INFO where LLC NAME = 'ETXEA':")
    print(search_by_field("LLC INFO", "LLC NAME", "ETXEA"))

    print("\nInsurance expiring in next 30 days:")
    print(get_insurance_expiring(30))

    print("\nLoans due within next 30 days:")
    print(get_loans_due(30))

