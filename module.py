import csv
import requests
import datetime

now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
PERIOD = ["9:40", "10:40", "11:40", "13:30", "14:30", "15:30", "16:30", "17:40", "18:40", "19:40"]
MAX_DAYS = 7


class Reservation:
    def __init__(self):
        self.types = []
        self.date = ""

    def appendReservationTypes(self, types):
        self.types.append(types)

    def addDate(self, date):
        self.date = date

    def showAllDailyReservation(self, dates):
        print(dates, self.types)


def saveCSV(filename, reservationList):
    with open(filename, 'w') as f:
        write = csv.writer(f, lineterminator='\n')
        for row in reservationList:
            writeEntry = [row]
            writeEntry.extend(reservationList[row].types)
            write.writerow(writeEntry)


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
    isNewSlot = False
    for cnt, date in enumerate(latestReservationList):
        if date not in oldReservationList: continue
        if cnt > MAX_DAYS: break
        latestEntryList = latestReservationList[date].types
        oldEntryList = oldReservationList[date].types

        # Looking through period 1 to 10
        for i, (o, l) in enumerate(zip(oldEntryList, latestEntryList)):
            if o == "Empty" and l == "Free":
                message += "\n" + f"🟧{date}: {i}組目 {PERIOD[i - 1]}"
                message_cnt += 1
                isNewSlot = True
            if o == "Free" and l == "Free":
                message += "\n" + f"🟩{date}: {i}組目 {PERIOD[i - 1]}"
                message_cnt += 1

    if message_cnt == 0: message = ""
    if isNewSlot: message = "🔴" + message

    return message


def sendNotification(token, message):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': f'{message}'}
    requests.post(line_notify_api, headers=headers, data=data)
