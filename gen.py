import datetime
import json
from phone_data import phone_amount_mapping_update

def calculate_amount(decimal_number):
    # Subtract 7.80 from the decimal number, ensuring it is at least 0
    amount = decimal_number - 7.80

    # If the amount is negative, take its absolute value; otherwise, set it to 0
    amount = abs(amount) if decimal_number - 7.80 < 0 else 0.00

    return amount

def read_phone_amount_mapping(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_phone_amount_mapping(file_path, phone_amount_mapping):
    with open(file_path, 'w') as file:
        json.dump(phone_amount_mapping, file)

def generate_debtor_file(file_path, phone_amount_mapping):
    with open(file_path, 'w') as file:
        for phone_number, initial_amount in phone_amount_mapping.items():
            # Check if the current date is at the 17th day of the month or later
            current_date = datetime.date.today()
            if current_date.day >= 19:
                # Perform the calculation based on the specified logic
                amount = calculate_amount(initial_amount)

                # Format the line as "<phone_number>:<amount>"
                line = f"{phone_number}:{amount:.2f}\n"
                file.write(line)

if __name__ == "__main__":
    debtor_file_path = 'debtor.txt'
    phone_mapping_file = 'phone_mapping.json'

    # Read phone amount mapping from file
    phone_amount_mapping = read_phone_amount_mapping(phone_mapping_file)

    # Add or update phone numbers and initial amounts
    phone_amount_mapping.update(phone_amount_mapping_update)

    # Write phone amount mapping back to file
    write_phone_amount_mapping(phone_mapping_file, phone_amount_mapping)

    # Generate debtor.txt for the current month
    generate_debtor_file(debtor_file_path, phone_amount_mapping)
