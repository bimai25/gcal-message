from dataclasses import dataclass

import parseString
import getCalendarEvents
import datetime

@dataclass
class Event:
    startTime: datetime
    endTime: datetime
    summary: str

def sort_chronologically(event):
    return event.startTime

def parseEvents(events):
    allEvents = list()
    for event in events:
        startTime = event['start'].get('dateTime',event['start'].get('date'))
        endTime = event['end'].get('dateTime',event['end'].get('date'))
        summary = str(event['summary'])
        allEvents.append(Event(startTime,endTime,summary))
    allEvents.sort(key = sort_chronologically)
    return allEvents

def buildMessage(events):
    message = "Here are your events today: \n\n"
    for event in events:
        start = event.startTime
        end = event.endTime

        start_string = parseString.parseTime(start)
        if start_string[0:2] == 12: #catch case if the start time is midnight
            start_string.replace("pm","am")
        end_string = parseString.parseTime(end)

        message += event.summary + " - " + start_string + " to " + end_string + "\n"
    message += "\nHave a great day!"
    print(message)
    return message

def test():
    events = parseEvents(getCalendarEvents.getEvents())
    buildMessage(events)

if __name__ == '__main__':
    test()