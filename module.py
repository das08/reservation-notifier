import csv
import requests
import datetime
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, PostbackEvent
)

now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
PERIOD = ["9:40", "10:40", "11:40", "13:30", "14:30", "15:30", "16:30", "17:40", "18:40", "19:40"]
MAX_DAYS = 5
WISHLISTS = ["09/01@1"]


class Reservation:
    def __init__(self):
        self.types = []
        self.date = ""

    def appendReservationTypes(self, types):
        self.types.append(types)

    def addDate(self, date):
        self.date = date


class Send:
    def __init__(self, CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, UID):
        self.line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        self.handler = WebhookHandler(CHANNEL_SECRET)
        self.UID = UID

    def pushMessage(self, message):
        if message == "": return
        self.line_bot_api.push_message(
            self.UID,
            TextSendMessage(text=message),
        )


def saveCSV(filename, reservationList):
    with open(filename, 'w') as f:
        write = csv.writer(f, lineterminator='\n')
        for row in reservationList:
            writeEntry = [row]
            writeEntry.extend(reservationList[row].types)
            write.writerow(writeEntry)
    return print(f"{now}")


def loadCSV(filename):
    with open(filename, 'r') as f:
        readfile = csv.reader(f)
        entry = [row for row in readfile]
        oldReservationList = {}
        for e in entry:
            oldReservationList[e[0]] = Reservation()
            oldReservationList[e[0]].types = e[1:]

    return oldReservationList


def compareReservation(oldReservationList, latestReservationList):
    message = "\n" + now.strftime('%Y/%m/%d %H:%M:%S')
    message_cnt = 0
    cell = (None, None, None)  # (date, row , col)
    isNewSlot = False

    for cnt, date in enumerate(latestReservationList):
        if date not in oldReservationList: continue
        if cnt > MAX_DAYS: break
        latestEntryList = latestReservationList[date].types
        oldEntryList = oldReservationList[date].types

        # Looking through period 1 to 10
        for i, (o, l) in enumerate(zip(oldEntryList, latestEntryList)):
            if l == "Free":
                if o == "Empty":
                    message += "\n" + f"🟧{date}: {i}組目 {PERIOD[i - 1]}"
                    isNewSlot = True
                if o == "Free":
                    message += "\n" + f"🟩{date}: {i}組目 {PERIOD[i - 1]}"
                if not all(cell):
                    for wish in WISHLISTS:
                        wishDate = wish.split("@")[0]
                        wishPeriod = wish.split("@")[1]
                        if date.split("(")[0] == wishDate and i == int(wishPeriod):
                            cell = (date, cnt, i)
                message_cnt += 1

    if message_cnt == 0: message = ""
    if isNewSlot: message = "🔴" + message
    return message, cell
