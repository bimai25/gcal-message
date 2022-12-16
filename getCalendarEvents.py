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
        all_calendars = list()
        message = "Here are your events today: \n \n"

        #build the start and end time 24 hour periods
        current_date = datetime.date.today()
        startTime = datetime.datetime.combine(current_date,datetime.time(hour=0))
        endTime = datetime.datetime.combine(current_date, datetime.time(hour=23, minute=59, second=59))
        #convert to RFC 3339 format
        formatStart = startTime.strftime("%Y-%m-%dT%H:%M:%SZ")
        formatEnd = endTime.strftime("%Y-%m-%dT%H:%M:%SZ")

        # print a list of all currently displayed calendars
        print('Getting events...')
        calendar_list = service.calendarList().list().execute()
        for calendar_list_entry in calendar_list['items']:
            id = calendar_list_entry['id']
            # gets the calendar using the ids from calendar list
            calendar = service.calendars().get(calendarId=id).execute()
            all_calendars.append(calendar)
        for calendar in all_calendars:
            event_list = service.events().list(calendarId=calendar['id'],maxResults=1, singleEvents=True,orderBy='startTime', timeMin=formatStart, timeMax = formatEnd).execute()
            daily_events = event_list.get('items',[])
            for event in daily_events:
                start = event['start'].get('dateTime',event['start'].get('date'))
                end = event['end'].get('dateTime',event['end'].get('date'))

                start_string = parseString.parseTime(start)
                if start_string[0:2] == 12: #catch case if the start time is midnight
                    start_string.replace("pm","am")
                end_string = parseString.parseTime(end)

                message += str(event['summary']) + " - " + start_string + " to " + end_string + "\n"
        message += "\nHave a great day!"
        print(message)
        return

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    getEvents()