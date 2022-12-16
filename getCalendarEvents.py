from __future__ import print_function

import datetime
import os.path
import parseString

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def getEvents():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        events =  []
        message = "Here are your events today: \n \n"

        #build the start and end time 24 hour periods (adjusting for PST and converting to RFC 0339 encoding)
        now = datetime.datetime.now()
        tz = datetime.timezone(datetime.timedelta(hours=-8))
        formatStart = datetime.datetime.combine(now, datetime.time.min, tz).isoformat()
        formatEnd = datetime.datetime.combine(now, datetime.time.max, tz).isoformat()

        # get all the events from the current 24 hour period
        print('Getting events...')
        calendar_list = service.calendarList().list().execute()
        calendar_ids = [calendar['id'] for calendar in calendar_list['items']]

        for calendar_id in calendar_ids:
            calendar_events = service.events().list(calendarId=calendar_id, timeMin=formatStart, timeMax=formatEnd,
                    singleEvents=True, orderBy='startTime').execute()
            events.extend(calendar_events['items'])
        return events #return a list of all the events (unsorted)

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    getEvents()