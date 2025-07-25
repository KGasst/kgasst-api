from airtable_manager import fetch_table_data, search_by_field, get_insurance_expiring, get_loans_due

def handle_command(command):
    command = command.lower()
    
    if "insurance" in command and "expiring" in command:
        days = extract_days(command)
        return get_insurance_expiring(days)
    
    elif "loans" in command and "due" in command:
        days = extract_days(command)
        return get_loans_due(days)
    
    elif "buildings" in command or "bldgs" in command:
        return fetch_table_data("BLDGS", max_records=10)
    
    elif "llc" in command:
        llc_name = extract_name(command)
        return search_by_field("LLC INFO", "LLC NAME", llc_name)
    
    else:
        return "❌ Command not recognized. Try:\n- insurance expiring in [days]\n- loans due in [days]\n- show buildings\n- show llc [name]"

def extract_days(command):
    for word in command.split():
        if word.isdigit():
            return int(word)
    return 30  # default if no number given

def extract_name(command):
    words = command.split()
    if "llc" in words:
        idx = words.index("llc")
        if idx + 1 < len(words):
            return words[idx + 1].upper()
    return ""

if __name__ == "__main__":
    print("\n✅ Welcome to KGasst CLI!")
    print("Type commands like:\n- insurance expiring in 45 days\n- loans due in 15 days\n- show buildings\n- show llc ETXEA\nType 'quit' to exit.")
    
    while True:
        cmd = input("\nEnter command: ")
        if cmd.lower() == "quit":
            print("Goodbye!")
            break
        result = handle_command(cmd)
        print("\nResult:\n", result)

