# products/utils.py
from datetime import datetime

def read_product_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract the product data
    name = lines[0].split(":")[1].strip().strip('"')
    price = lines[1].split(":")[1].strip()
    market_value = lines[2].split(":")[1].strip()

    # Extract logs (everything after the third line)
    logs = lines[3:] if len(lines) > 3 else []

    return name, price, market_value, logs


def write_product_data(file_path, market_value, user):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        # Update the market value line
        lines[2] = f"market value: {market_value}\n"

        # Create the new log entry
        log_entry = f"Updated by {user} to ${market_value} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        # Insert the log entry after the product details
        lines.insert(3, log_entry)

        # Write the updated content back to the file
        file.seek(0)
        file.writelines(lines)
        file.truncate()

