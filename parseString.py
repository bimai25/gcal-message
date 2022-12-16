def parseTime(string):
    t_index = string.find('T')
    toReturn = ""
    am = False
    if int(string[t_index+1])== 0:
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
