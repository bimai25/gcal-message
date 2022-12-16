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

        print(formatStart,formatEnd)

        # print a list of all currently displayed calendars
        print('Getting events...')
        calendar_list = service.calendarList().list().execute()
        calendar_ids = [calendar['id'] for calendar in calendar_list['items']]

        for calendar_id in calendar_ids:
            calendar_events = service.events().list(calendarId=calendar_id, timeMin=formatStart, timeMax=formatEnd,
                    singleEvents=True, orderBy='startTime').execute()
            events.extend(calendar_events['items'])
        for event in events:
                start = event['start'].get('dateTime',event['start'].get('date'))
                end = event['end'].get('dateTime',event['end'].get('date'))

                start_string = parseString.parseTime(start)
                if start_string[0:2] == 12: #catch case if the start time is midnight
                    start_string.replace("pm","am")
                end_string = parseString.parseTime(end)

                message += str(event['summary']) + " - " + start_string + " to " + end_string + "\n"
        #for calendar in calendar_ids:
            #event_list = service.events().list(calendarId=calendar, maxResults=10,singleEvents=True,orderBy='startTime', timeMin=formatStart, timeMax = formatEnd).execute()
            #daily_events = event_list.get('items',[])

        message += "\nHave a great day!"
        toReturn = '\'' + message + '\''
        print(message)
        return toReturn

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    getEvents()