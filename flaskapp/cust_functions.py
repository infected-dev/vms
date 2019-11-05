def convert(x):
    sec = ((x.hour*60) + x.minute) *60 + x.second
    return sec 

def minutes (seconds):
    seconds = seconds % (24*3600)
    hour = seconds//3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    formatted = "%d:%02d" %(hour, minutes)
    return formatted

def timeobj(x,y):
    x = convert(x)
    y = convert(y)
    diff = y - x
    diff = minutes(diff)
    return diff
