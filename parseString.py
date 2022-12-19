# parameters: string - datetime object
# return: string - formatted time in xx:xx am/pm format
# description: datetime objects are formatted in the following manner:
# date(YYYY-MM_DD)T(HH:MM:SS), the parseTime functions works by getting substrings
# relative to the T, and then checking the HH to see what its value is. Datetime objects
# use military time, so that's why the hour value must be checked to see how to convert to am/pm format
def parseTime(string):
    t_index = string.find('T')
    toReturn = ""
    am = False
    if int(string[t_index+1]) == 0 and int(string[t_index+2]) == 0:
        toReturn += "12"
        am = True
    elif int(string[t_index+1])== 0:
        toReturn +=string[t_index+2]
        am = True
    elif int(string[t_index+1:t_index+3]) < 12:
        toReturn+= string[t_index+1:t_index+3]
        am = True
    elif int(string[t_index+1:t_index+3]) == 12:
        toReturn += string[t_index+1:t_index+3]
        am = False
    elif int(string[t_index+1:t_index+3]) > 12:
        adjustTime = int(string[t_index+1:t_index+3]) - 12
        toReturn += str(adjustTime)
        am = False
    minuteStart = string.find(':')
    toReturn += ":" + string[minuteStart+1:minuteStart+3]
    if am == True:
        toReturn += " am"
    else:
        toReturn += " pm"
    return toReturn
