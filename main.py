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
    login()
    reservationList = getReserveList()
    oldReservationList = {}

    try:
        oldReservationList = loadCSV("reserve.csv")
    except FileNotFoundError:
        pass

    message = compareReservation(oldReservationList, reservationList)
    sendNotification(token=credential.LINE_TOKEN, message=message)
    saveCSV("reserve.csv", reservationList)

    driver.quit()
