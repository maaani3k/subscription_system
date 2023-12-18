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

def build_xml_request():
    root = Element('request')
    
    elements = {
        'Index': '-1',
        'Phones': {'Phone': '+48534181076'},
        'Sca': '',
        'Content': '''
            Witaj w systemie powiadomień, dostaniesz info o odnowieniu subskrybcji lub zaległej płatności
            serwis: Youtube Premium
            status: odnowiona do 17.01.2024r
            należność: 0zł
        ''',
        'Length': '-1',
        'Reserved': '1',
        'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    for key, value in elements.items():
        if isinstance(value, dict):
            parent = SubElement(root, key)
            for sub_key, sub_value in value.items():
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
        print("SMS Request Headers:", headers)
        print("SMS Request XML Data:", xml_data)
        print("SMS Response Status Code:", response.status_code)
        print("SMS Response Content:", response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error sending SMS: {e}"

# Example usage
if __name__ == "__main__":
    token_api_url = 'http://192.168.8.1/api/webserver/token'
    sms_api_url = 'http://192.168.8.1/api/sms/send-sms'

    token = get_request_verification_token(token_api_url)

    if not token:
        print("Failed to obtain the token.")
    else:
        xml_data = build_xml_request()
        result = send_sms(sms_api_url, xml_data, token)
        print("SMS Response:", result)
