from datetime import datetime

gi = "18 giờ trước"
ph = "36 phút trước"
ng = "1 ngay truoc"
na = "2 nam truoc"

def convertUpdateTimeToSec(updated_at):

    now = datetime.now()
    currentTimeStamp = int(now.timestamp())
    timeInSec = 0
    timePublish = 0

    text = updated_at.split()
    time = text[0]
    timeLetter = text[1][:2]

    if (timeLetter == "gi"):
        timeInSec = int(time)*60*60
    elif(timeLetter == "ph"):
        timeInSec = int(time)*60
    elif(timeLetter == "ng"):
        timeInSec = int(time)*24*60*60
    else:
        timeInSec = int(time)*365*24*60*60
    
    timePublish = currentTimeStamp - timeInSec
    date_time_publish = datetime.fromtimestamp(timePublish)
    # print(date_time_publish)
    # print(timeLetter)
    return timeInSec
