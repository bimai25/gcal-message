from imessage_reader import fetch_data
from phoneNumber import PHONE_NUMBER

import os
import getCalendarEvents

RECIPIENT_NUMBER = PHONE_NUMBER
MESSAGE = getCalendarEvents.getEvents()

fd = fetch_data.FetchData()
messages = fd.get_messages()
os.system("osascript sendMessage.applescript {} {}".format(RECIPIENT_NUMBER, MESSAGE))
