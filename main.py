from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import credential
from module import *
import chromedriver_binary
import time

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


def login():
    driver.get(credential.URL)
    driver.find_element_by_name("USERID").send_keys(credential.ID)
    driver.find_element_by_name("USERPASSWD").send_keys(credential.PASS)
    driver.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td/input").click()
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/p/table[2]/tbody/tr[1]/td[2]/form/table/tbody/tr[2]/td[2]/input").click()


def autoReserve(date, row, col):
    if not all((date, row, col)): return "Debug", "予約可能な枠がないよ！"
    try:
        if driver.find_element_by_xpath("/html/body/p/table/tbody/tr[2]/td[5]").text != "0":
            return "Debug", "予約可能な時限数を超えてるよ！"
        cellID = str(row).zfill(2) + str(col - 1).zfill(2)
        cell = driver.find_element_by_xpath(f"//*[@id=\"ID{cellID}\"]")
        if cell.get_attribute("class") != "Have":
            cell.click()
        time.sleep(1)
        nowURL = driver.current_url
        if nowURL != credential.SUCCESS_URL:
            if driver.find_element_by_xpath("/html/body/blockquote").get_attribute("class") == "confirm":
                reserveMessage = f"{date}の{col}限の予約に成功したよ！🌸"
            else:
                reserveMessage = f"{date}の{col}限の予約に失敗しました😭\nおそらく予約重複です。"
    except NoSuchElementException:
        reserveMessage = f"[NoSuchElementException]{date}{col}限"

    return "Success", reserveMessage


def getReserveList():
    tableLists = driver.find_elements_by_xpath("/html/body/table[3]/tbody/tr")
    reservationList = {}

    for i, row in enumerate(tableLists):
        if i == 0: continue
        cells = row.find_elements_by_tag_name("td")
        for cell in cells:
            if cell.get_attribute("class") == "Head":
                date = cell.text
                reservationList[date] = Reservation()
                reservationList[date].addDate(date)
            reservationList[date].appendReservationTypes(cell.get_attribute("class"))

    return reservationList


if __name__ == '__main__':
    try:
        login()
        reservationList = getReserveList()
        oldReservationList = {}
        try:
            oldReservationList = loadCSV("reserve.csv")
        except FileNotFoundError:
            pass
        availableReservations = compareReservation(oldReservationList, reservationList)[0]
        cell = compareReservation(oldReservationList, reservationList)[1]
        reserveMessage = autoReserve(*cell)

        send = Send(credential.CHANNEL_ACCESS_TOKEN, credential.CHENNEL_SECRET, credential.UID)
        send.pushMessage(availableReservations)
        if reserveMessage[0] == "Success":
            send.pushMessage(reserveMessage[1])

        saveCSV("reserve.csv", reservationList)
    finally:
        driver.quit()
