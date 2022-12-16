import parseString
import getCalendarEvents

def buildMessage(events):
    message = "Here are your events today: \n\n"
    for event in events:
        start = event['start'].get('dateTime',event['start'].get('date'))
        end = event['end'].get('dateTime',event['end'].get('date'))

        start_string = parseString.parseTime(start)
        if start_string[0:2] == 12: #catch case if the start time is midnight
            start_string.replace("pm","am")
        end_string = parseString.parseTime(end)

        message += str(event['summary']) + " - " + start_string + " to " + end_string + "\n"
    message += "\nHave a great day!"
    print(message)
    return message

def test():
    buildMessage(getCalendarEvents.getEvents())

if __name__ == '__main__':
    test()