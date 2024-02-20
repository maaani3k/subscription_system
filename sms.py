import time
import sys
import requests
import xml.dom.minidom
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

# ANSI escape codes for color
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def get_request_verification_token(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        # Assuming the response is in XML format
        return ET.fromstring(response.content).find('.//token').text
    except requests.exceptions.RequestException as e:
        print(f"Error getting token: {e}")
        return None

def build_xml_request(phone_number, amount):
    root = Element('request')

    # Add Index element
    index_element = SubElement(root, 'Index')
    index_element.text = '-1'

    phones_element = SubElement(root, 'Phones')

    # Add Phone element inside Phones
    phone_element = SubElement(phones_element, 'Phone')
    phone_element.text = phone_number

    # Add Sca element
    sca_element = SubElement(root, 'Sca')
    sca_element.text = ''

    # Format the Content as "Witaj w systemie ... należność: *number*zł"
    content_template = '''Witaj w systemie powiadomień, dostaniesz info o odnowieniu subskrybcji lub zaległej płatności
serwis: Youtube Premium
status: odnowiona do 17.03.2024r
należność: {}zł'''
    content = content_template.format(amount)

    # Add Content element
    content_element = SubElement(root, 'Content')
    content_element.text = content

    # Add Length element
    length_element = SubElement(root, 'Length')
    length_element.text = '-1'

    # Add Reserved element
    reserved_element = SubElement(root, 'Reserved')
    reserved_element.text = '1'

    # Add Date element
    date_element = SubElement(root, 'Date')
    date_element.text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert the XML tree to a string
    xml_data = tostring(root, encoding="UTF-8").decode("utf-8")

    # Replace <Sca /> with <Sca></Sca>
    xml_data = xml_data.replace('<Sca />', '<Sca></Sca>')

    return xml_data

def send_sms(api_url, xml_data, token):
    headers = {
        '__RequestVerificationToken': token,
        'Content-Type': 'text/xml'
    }

    print("POST Request Headers:")
    for header, value in headers.items():
        print(f"{header}: {value}")

    print(f"POST Request XML Data:\n{xml_data}")

    try:
        response = requests.post(api_url, data=xml_data.encode('utf-8'), headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return None

def read_debtor_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read phone numbers and amounts from the file
            phone_amount_mapping = {}
            for line_number, line in enumerate(file, start=1):
                try:
                    phone, amount_str = line.strip().split(':')
                    amount = float(amount_str)
                    phone_amount_mapping[phone] = amount
                except ValueError as ve:
                    print(f"Error parsing line {line_number}: {line.strip()}. {ve}")
                    continue
            return phone_amount_mapping
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py debtor.txt")
        sys.exit(1)

    token_api_url = 'http://192.168.8.1/api/webserver/token'
    sms_api_url = 'http://192.168.8.1/api/sms/send-sms'

    print("Fetching token...")
    token = get_request_verification_token(token_api_url)

    if not token:
        print("Failed to obtain the token. Exiting.")
        sys.exit(1)

    print(f"Token obtained successfully: {token}")
    
    debtor_file_path = sys.argv[1]
    print(f"Reading phone numbers and amounts from {debtor_file_path}...")

    # Read phone numbers and amounts from debtor.txt
    phone_amount_mapping = read_debtor_file(debtor_file_path)

    if not phone_amount_mapping:
        print("No valid phone numbers and amounts found in debtor.txt. Exiting.")
        sys.exit(1)

    print(f"Phone numbers and amounts: {phone_amount_mapping}")

    print("Sending SMS for each entry in debtor.txt...")
    for phone_number, amount in phone_amount_mapping.items():
        print(f"Sending SMS for {phone_number} with amount {amount}...")
        
        # Generate XML request based on the data from debtor.txt
        xml_data = build_xml_request(phone_number, amount)

        # Send SMS with the generated XML data
        result = send_sms(sms_api_url, xml_data, token)

        if result is not None:
            if "<response>OK</response>" in result:
                print(f"{GREEN}SMS Response for {phone_number}: {result}{RESET}")
            elif "<error>" in result:
                print(f"{RED}SMS Response for {phone_number}: {result}{RESET}")
            else:
                print(f"Unknown response for {phone_number}: {result}")
        else:
            print(f"{RED}Failed to send SMS for {phone_number}. Check debug messages for details.{RESET}")

        time.sleep(10)  # Introduce a 10-second delay between SMS sends
