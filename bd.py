import sqlite3 as sql
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.wait import WebDriverWait
import requests

def iphone():
    data_cbr = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

    driver = webdriver.Chrome()
    driver.get('https://cdek.shopping/p/16093/smartfon-apple-iphone-14-pro-1-tb-glubokii-fioletovyi')
    price_out = WebDriverWait(driver, 10).until(expect.visibility_of_element_located((By.CLASS_NAME, 'actual-price'))).text
    price = int(price_out.split('\n')[1].replace(' ', '').replace('₽', ''))
    driver.quit()

    connect = sql.connect('iphone14pro.db')

    with connect:
        cursor = connect.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS `iphone14pro` (`date` DATETIME, `price` MONEY)")
        #cursor.execute("INSERT INTO `iphone14pro` VALUES ('2023-07-18', '158892')")
        #cursor.execute(f"INSERT INTO `iphone14pro` VALUES ('2023-07-19', '{price}')")
        cursor.execute(f"INSERT INTO `iphone14pro` VALUES ('{datetime.today().strftime('%Y-%m-%d')}', '{price}')")
        cursor.execute("SELECT * FROM `iphone14pro`")
        rows = cursor.fetchall()
        x = []
        y = []
        for row in rows:
            print(date.fromisoformat(row[0]).strftime("%d.%m.%Y"), row[1])
            x.append(date.fromisoformat(row[0]).strftime("%d.%m.%Y"))
            y.append(row[1])

        cursor.execute("CREATE TABLE IF NOT EXISTS `dollar` (`date` DATETIME, `exchange` MONEY)")
        #cursor.execute("INSERT INTO `dollar` VALUES ('2023-07-18', '91')")
        #cursor.execute(f"INSERT INTO `dollar` VALUES ('2023-07-19', '{round(float(data_cbr['Valute']['USD']['Value']), 2)}')")
        cursor.execute(f"INSERT INTO `dollar` VALUES ('{datetime.today().strftime('%Y-%m-%d')}', '{round(float(data_cbr['Valute']['USD']['Value']), 2)}')")
        cursor.execute("SELECT * FROM `dollar`")
        rows2 = cursor.fetchall()
        x2 = []
        y2 = []
        for row2 in rows2:
            print(date.fromisoformat(row2[0]).strftime("%d.%m.%Y"), row2[1])
            y2.append(row2[1])

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax2.plot(x, y2, label = 'Курс', color = 'r', marker = 'o')
        ax1.plot(x, y, label = 'Цена', color = 'b', linewidth = 3)
        ax1.legend(loc = 2)
        ax2.legend(loc = 4)
        plt.xlabel('Дата')
        plt.ylabel('RUB')
        plt.show()

        connect.commit()
        cursor.close()