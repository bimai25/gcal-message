from imessage_reader import fetch_data
from phoneNumber import PHONE_NUMBER

import os
import getCalendarEvents
import message

RECIPIENT_NUMBER = PHONE_NUMBER
MESSAGE = '\'' + message.buildMessage(message.parseEvents(getCalendarEvents.getEvents())) + '\''

os.system("osascript sendMessage.applescript {} {}".format(RECIPIENT_NUMBER, MESSAGE))
