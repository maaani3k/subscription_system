import sys
import requests
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

def get_request_verification_token(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        # Assuming the response is in XML format
        return ET.fromstring(response.content).find('.//token').text
    except requests.exceptions.RequestException as e:
        return f"Error getting token: {e}"

def build_xml_request(phone_numbers, custom_content):
    root = Element('request')
    
    elements = {
        'Index': '-1',
        'Phones': {'Phone': phone_numbers},
        'Sca': '',
        'Content': '''Witaj w systemie powiadomień, dostaniesz info o odnowieniu subskrybcji lub zaległej płatności
serwis: Youtube Premium
status: odnowiona do 17.01.2024r
należność: {}'''.format(custom_content),
        'Length': '-1',
        'Reserved': '1',
        'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    for key, value in elements.items():
        if isinstance(value, dict):
            parent = SubElement(root, key)
            for sub_key, sub_value in value.items():
                if sub_key == 'Phone':
                    for phone in sub_value:
                        SubElement(parent, sub_key).text = str(phone)
                else:
                    SubElement(parent, sub_key).text = str(sub_value)
        else:
            element = SubElement(root, key)
            element.text = str(value)

    return tostring(root, encoding="UTF-8").decode("utf-8")

def send_sms(api_url, xml_data, token):
    headers = {
        '__RequestVerificationToken': token,
        'Content-Type': 'text/xml'
    }

    try:
        response = requests.post(api_url, data=xml_data.encode('utf-8'), headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error sending SMS: {e}"

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py phone_numbers_file.txt 'Custom Content'")
        sys.exit(1)

    token_api_url = 'http://192.168.8.1/api/webserver/token'
    sms_api_url = 'http://192.168.8.1/api/sms/send-sms'

    token = get_request_verification_token(token_api_url)

    if not token:
        print("Failed to obtain the token.")
    else:
        phone_numbers_file = sys.argv[1]
        custom_content = sys.argv[2]

        try:
            with open(phone_numbers_file, 'r') as file:
                # Read phone numbers from the file, assuming one number per line
                phone_numbers = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Error: File '{phone_numbers_file}' not found.")
            sys.exit(1)

        xml_data = build_xml_request(phone_numbers, custom_content)
        result = send_sms(sms_api_url, xml_data, token)
        print("SMS Response:", result)
