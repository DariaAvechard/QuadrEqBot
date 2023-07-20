# -*- coding: utf-8 -*-
import telebot
import time
import numpy as np
from telebot import types
import emoji
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')

bot = telebot.TeleBot('6209127648:AAH-XZlUE8yj4YtfgK0prk4blRXPwm7RC4g')

wc_dict = {
            'Парк культуры': f"{emoji.emojize(':red_circle:')} *Парк культуры:* 2 МТК (1 – на выходе в город на улицу Остоженка, 1 – в переходе на Кольцевую линию)",
            'Кропоткинская': f"{emoji.emojize(':red_circle:')} *Кропоткинская:* 1 МТК на выходе в город на Гоголевский бульвар",
            'Библиотека имени Ленина': f"{emoji.emojize(':red_circle:')} *Библиотека им. Ленина:* 3 МТК (2 – в переходе на Александровский сад и 1 угловой – в переходе на Боровицкую",
            'Сокольники': f"{emoji.emojize(':red_circle:')} *Сокольники:* 1 МТК на выходе в город, около поста полиции",
            'Парк Победы': f"{emoji.emojize(':blue_circle:')} *Парк Победы*",
            'Площадь революции': f"{emoji.emojize(':blue_circle:')} *Площадь революции*",
            'Семёновская': f"{emoji.emojize(':blue_circle:')} *Семёновская:* 2 МТК на платформе",
            'Чкаловская': f"{emoji.emojize(':green_circle:')} *Чкаловская:* 1 МТК на платформе, возле перехода на Курскую Арбатско-Покровской линии",
            'Трубная': f"{emoji.emojize(':green_circle:')} *Трубная*",
            'Комсомольская': f"{emoji.emojize(':brown_circle:')} *Комсомольская:* 1 МТК в переходе с Кольцевой на Сокольническую линию",
            'Таганская': f"{emoji.emojize(':brown_circle:')} *Таганская*",
            'Краснопресненская': f"{emoji.emojize(':brown_circle:')} *Краснопресненская*",
            'Проспект Мира': f"{emoji.emojize(':brown_circle:')}{emoji.emojize(':orange_circle:')} *Проспект Мира:* 1 МТК в переходе с Калужско-Рижской на Кольцевую линию",
            'ВДНХ': f"{emoji.emojize(':orange_circle:')} *ВДНХ:* 1 МТК на выходе к гостинице Космос",
            'Третьяковская': f"{emoji.emojize(':orange_circle:')} *Третьяковская*",
            'Китай-город': f"{emoji.emojize(':orange_circle:')}{emoji.emojize(':purple_circle:')} *Китай-город*",
            'Пушкинская': f"{emoji.emojize(':purple_circle:')} *Пушкинская:* 2 МТК в переходе на Чеховскую",
            'Александровский сад': f"{emoji.emojize(':blue_circle:')} *Александровский сад*",
            'Маяковская': f"{emoji.emojize(':green_circle:')} *Маяковская*",
            'Цветной бульвар': f"{emoji.emojize(':white_circle:')} *Цветной бульвар:* 2 МТК (1 – в переходе на Трубную, 1 – на выходе в город на Цветной бульвар)",
            'Боровицкая': f"{emoji.emojize(':white_circle:')} *Боровицкая:* 2 МТК в переходе на Библиотеку им. Ленина",
            'Чеховская': f"{emoji.emojize(':white_circle:')} *Чеховская*",
            'Менделеевская': f"{emoji.emojize(':white_circle:')} *Менделеевская*"}

@bot.message_handler(commands = ['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = 'Решить уравнение'))
    keyboard.add(types.KeyboardButton(text = 'Показать список Т'))
    keyboard.add(types.KeyboardButton(text = 'Найти ближайший Т'))
    sent = bot.send_message(message.chat.id, 'Привет! Меня зовут Квадрик, и я могу помочь тебе решить квадратное уравнение, показать список туалетов в метро или найти ближайший из них к тебе.', reply_markup = keyboard)
    bot.register_next_step_handler(sent, task)

def task(message):
    if (message.text == 'Решить уравнение'):
        global a0
        a0 = bot.send_message(message.chat.id, 'Введите a')
        bot.register_next_step_handler(a0, q1)
    elif (message.text == 'Показать список Т'):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        keyboard.add(types.KeyboardButton(text = 'Спасибо!'))
        sent = bot.send_message(message.chat.id, '\n'.join(wc_dict.values()), parse_mode = 'Markdown', reply_markup=keyboard)
        bot.register_next_step_handler(sent, question)
    elif (message.text == 'Найти ближайший Т'):
        sent = bot.send_message(message.chat.id, 'Введите Вашу станцию')
        bot.register_next_step_handler(sent, neares_wc)

@bot.message_handler(content_types=['text'])
def question(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(types.KeyboardButton(text = 'Решить уравнение'))
    keyboard.add(types.KeyboardButton(text = 'Показать список Т'))
    keyboard.add(types.KeyboardButton(text = 'Найти ближайший Т'))
    sent = bot.send_message(message.chat.id, 'Чем еще я могу Вам помочь?', reply_markup = keyboard)
    bot.register_next_step_handler(sent, task)

def neares_wc(message):
    if (message.text in wc_dict.keys()):
        bot.send_message(message.chat.id, 'Есть туалет')
        res = f'*На этой станции есть туалет*\n{wc_dict[message.text]}'
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get('https://yandex.ru/metro/')
        bot.send_message(message.chat.id, 'Сейчас найдем')
        input1 = WebDriverWait(driver, 10).until(expect.visibility_of_element_located((By.XPATH, "//input[@placeholder = 'Откуда']")))
        input1.send_keys(Keys.CONTROL, 'a')
        input1.send_keys(Keys.DELETE)
        input1.send_keys(message.text)
        input1.send_keys(Keys.ENTER)
        input2 = WebDriverWait(driver, 10).until(expect.visibility_of_element_located((By.XPATH, "//input[@placeholder = 'Куда']")))
        input2.send_keys('Парк культуры')
        input2.send_keys(Keys.ENTER)
        try:
            if WebDriverWait(driver, 10).until(expect.visibility_of_element_located((By.CLASS_NAME, 'metro-input-form__route-input-error'))).text == 'Вы не задали точку маршрута':
                res = f'Некорректный ввод'
                driver.quit()
        except TimeoutException:
            min_time = 500
            for station in wc_dict.keys():
                input2 = WebDriverWait(driver, 10).until(expect.visibility_of_element_located((By.XPATH, "//input[@placeholder = 'Куда']")))
                input2.send_keys(Keys.CONTROL, 'a')
                input2.send_keys(Keys.DELETE)
                input2.send_keys(station)
                input2.send_keys(Keys.ENTER)

                output = WebDriverWait(driver, 10).until(expect.visibility_of_element_located((By.CLASS_NAME, 'masstransit-route-snippet-view__route-duration'))).text
                if int(output.split(' ')[0]) < min_time:
                    min_time = int(output.split(' ')[0])
                    min_station = station
            res = f'*Минут до ближайшей станции: {min_time}*\n{wc_dict[min_station]}'
            driver.quit()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Спасибо!'))
    sent = bot.send_message(message.chat.id, res, parse_mode='Markdown', reply_markup=keyboard)
    bot.register_next_step_handler(sent, question)

def isNotEmpty(s):
    return bool(s and s.strip())

def q0(message):
    global a0
    a0 = bot.send_message(message.chat.id, 'Введите a')
    bot.register_next_step_handler(a0, q1)

def q1(message):
    global a
    a = message.text
    if (isNotEmpty(a) == True and a.lstrip('-').isdigit() == True):
        global b0
        b0 = bot.send_message(message.chat.id, 'Введите b')
        bot.register_next_step_handler(b0, q2)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        keyboard.add(types.KeyboardButton(text='Повторить ввод'))
        sent = bot.send_message(message.chat.id, 'Не числовое значение', reply_markup = keyboard)
        bot.register_next_step_handler(sent, q0)

def q2(message):
    global b
    b = message.text
    if (isNotEmpty(b) == True and b.lstrip('-').isdigit() == True):
        global c0
        c0 = bot.send_message(message.chat.id, 'Введите c')
        bot.register_next_step_handler(c0, q3)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        keyboard.add(types.KeyboardButton(text='Повторить ввод'))
        sent = bot.send_message(message.chat.id, 'Не числовое значение', reply_markup = keyboard)
        bot.register_next_step_handler(sent, q0)
def q3(message):
    c = message.text
    if (isNotEmpty(c) == True and c.lstrip('-').isdigit() == True):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        keyboard.add(types.KeyboardButton(text='Спасибо!'))
        if int(a) == 0:
            sent = bot.send_message(message.chat.id, 'Не квадратное уравнение', reply_markup = keyboard)
        else:
            res = quadr_eq(int(a), int(b), int(c))
            if (res[0].imag == 0 and res[1].imag == 0):
                s11 = str(np.round(res[0].real, 4))
                s12 = str(np.round(res[1].real, 4))
                sent = bot.send_message(message.chat.id, 'x1 = {s11}, '.format(s11 = str(s11)) + 'x2 = {s12}'.format(s12 = str(s12)), reply_markup = keyboard)
            else:
                s21 = str(np.round(res[0], 4))
                s22 = str(np.round(res[1], 4))
                sent = bot.send_message(message.chat.id, 'x1 = {s21}, '.format(s21 = str(s21)) + 'x2 = {s22}'.format(s22 = str(s22)), reply_markup = keyboard)
        bot.register_next_step_handler(sent, question)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
        keyboard.add(types.KeyboardButton(text='Повторить ввод'))
        sent = bot.send_message(message.chat.id, 'Не числовое значение', reply_markup = keyboard)
        bot.register_next_step_handler(sent, q0)

def quadr_eq(a1, b1, c1):
    if a1 == 0:
        return 0
    else:
        D = b1 ** 2 - 4 * a1 * c1
        x1 = (-b1 - np.sqrt(complex(D))) / (2 * a1)
        x2 = (-b1 + np.sqrt(complex(D))) / (2 * a1)
        return x1, x2

while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(10)
