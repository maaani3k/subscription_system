import datetime

def calculate_amount(decimal_number):
    # Subtract 11 from the decimal number, ensuring it is at least 0
    amount = decimal_number - 11.00

    # If the amount is negative, take its absolute value; otherwise, set it to 0
    amount = abs(amount) if decimal_number - 11.00 < 0 else 0.00

    return amount

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
    
    # Dictionary mapping phone numbers to initial amounts
    phone_amount_mapping = {
        #'+48505926878': 0.00,  #Misialenta
        #'+48534181076': 11.00, #ja
        #'+48880574277': 0.00,  #Srakamai
	#'+48531661191': 0.00,  #Mateusz
	#'+48519718970': 21.12, #Olczi
	'+48660695355': 21.12  #Lysy
    }

    # Generate debtor.txt for the current month
    generate_debtor_file(debtor_file_path, phone_amount_mapping)
