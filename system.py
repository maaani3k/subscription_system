import requests
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

def get_request_verification_token(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        # Assuming the response is in XML format
        root = ET.fromstring(response.content)
        token = root.find('.//token').text

        return token
    except requests.exceptions.RequestException as e:
        return f"Error getting token: {e}"

def build_xml_request():
    root = Element('request')
    
    index = SubElement(root, 'Index')
    index.text = '-1'
    
    phones = SubElement(root, 'Phones')
    phone = SubElement(phones, 'Phone')
    phone.text = '+48534181076'
    
    sca = SubElement(root, 'Sca')
    
    content = SubElement(root, 'Content')
    content.text = '''
        Witaj w systemie powiadomień, dostaniesz info o odnowieniu subskrybcji lub zaległej płatności
        serwis: Youtube Premium
        status: odnowiona do 17.01.2024r
        należność: 0zł
    '''
    
    length = SubElement(root, 'Length')
    length.text = '-1'
    
    reserved = SubElement(root, 'Reserved')
    reserved.text = '1'
    
    date = SubElement(root, 'Date')
    date.text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    # Replace 'http://192.168.8.1/api/webserver/token' with the actual API URL to obtain the token
    token_api_url = 'http://192.168.8.1/api/webserver/token'

    # Replace 'http://192.168.8.1/api/sms/send-sms' with the actual API URL for sending SMS
    sms_api_url = 'http://192.168.8.1/api/sms/send-sms'

    # Get the RequestVerificationToken
    token = get_request_verification_token(token_api_url)

    if not token:
        print("Failed to obtain the token.")
    else:
        # Build the XML request
        xml_data = build_xml_request()

        # Send the SMS
        result = send_sms(sms_api_url, xml_data, token)

        print("SMS Response:", result)
