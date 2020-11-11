import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email.mime.text import MIMEText
import base64

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# You'll need create a project with Google's API interfaces through their website.
# Next you'll need to enable the GMAIL API for your app.
# Create credentials and then download those creds, save it as credentials.json.

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']


def create_message(sender, to, subject, msg):
    """
    Creates an e-mail message based on sender, recipient, subject and content information.
    """
    message = MIMEText(msg)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Base 64 encode
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw': b64_string}
    # return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, msg):
    """
    Sends the e-mail message.
    """
    # try:
    message = (service.users().messages().send(userId=user_id, body=msg).execute())
    print(f"Message Id: {message['id']}")
    return message
    # except errors.HttpError, error:print( 'An error occurred: %s' % error )


def create_credentials():
    """
    Creates credentials and saves them in 'token.pickle' file.
    In case 'token.pickle' already exists it tries to loads the credentials from this file first.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def create_and_send_email(sender, recipient, subject, text):
    """
    Triggers functions to create credentials, create the e-mail message and finally send it over the network.
    """
    creds = create_credentials()
    service = build('gmail', 'v1', credentials=creds)
    msg = create_message(sender, recipient, subject, text)
    send_message(service, 'me', msg)
