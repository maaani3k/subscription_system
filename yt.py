import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests

def read_api_key(api_key_file):
    try:
        with open(api_key_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: API key file '{api_key_file}' not found.")
        return None

def manual_authentication_url(flow):
    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f"Please go to this URL to authorize the application: {auth_url}")
    authorization_code = input("Enter the authorization code: ")
    return authorization_code

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "/home/pi/secret/yt.web.json"
    api_key_file = "/home/pi/secret/yt.conf"  # Replace with your YouTube API key

    api_key = read_api_key(api_key_file)

    if api_key is not None:
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.readonly"])

        # Use manual_authentication_url to obtain the authorization code
        authorization_code = manual_authentication_url(flow)

        # Fetch the token using the obtained authorization code
        credentials = flow.fetch_token(authorization_response=authorization_code)
        
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        # Modify the request to use API key instead of OAuth credentials
        request = youtube.subscriptions().list(
            part="snippet,contentDetails",
            mine=True,
            key=api_key
        )

        response = request.execute()

        print(response)

if __name__ == "__main__":
    main()
