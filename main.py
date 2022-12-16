from imessage_reader import fetch_data

import os
import getCalendarEvents

RECIPIENT_NUMBER = "+17145884969"
MESSAGE = getCalendarEvents.getEvents()

fd = fetch_data.FetchData()
messages = fd.get_messages()
os.system("osascript sendMessage.applescript {} {}".format(RECIPIENT_NUMBER, MESSAGE))
