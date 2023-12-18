import datetime

def generate_debtor_file(file_path, phone_amount_mapping):
    with open(file_path, 'w') as file:
        for phone_number, initial_amount in phone_amount_mapping.items():
            # Calculate the amount based on the current day of the month
            current_date = datetime.date.today()
            amount = initial_amount - 11 * max(0, (current_date.day - 17))

            # Format the line as "<phone_number>:<amount>"
            line = f"{phone_number}:{amount:.2f}\n"
            file.write(line)

if __name__ == "__main__":
    debtor_file_path = 'debtor.txt'
    
    # Dictionary mapping phone numbers to initial amounts
    phone_amount_mapping = {
        '+48534181076': 11.00,
        '+48505926878': 21.00
    }

    # Generate debtor.txt for the current month
    generate_debtor_file(debtor_file_path, phone_amount_mapping)
