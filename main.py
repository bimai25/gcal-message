from imessage_reader import fetch_data
import os

RECIPIENT_NUMBER = "+17147152590"
MESSAGE = "'Hello world!'"

fd = fetch_data.FetchData()
messages = fd.get_messages()
os.system("osascript sendMessage.applescript {} {}".format(RECIPIENT_NUMBER, MESSAGE))
