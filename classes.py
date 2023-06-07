# Импорт библиотек
import datetime
import math

import requests
from bs4 import BeautifulSoup

# Импорт данных по сайту
from dates import *

# Класс общих данных
class FullDates:
    # Метод-конструктор с переменными экземпляра класса
    def __init__(self):
        # Список экспортированных url
        self.exporturls = []
        # Список запланированных постов с временем
        self.timewithposts = []
        # Список импортированных новостей
        self.importurls = []

    # Функция печати данных
    def printidates(self):
        print("\t=Start===Class FullDates==========")
        print("\t===========ExportUrls=============")
        for element in self.exporturls:
            print("\t\t" + element)
        print("\t=========TimeWithPosts===========")
        for element in self.timewithposts:
            print("\t\t" + element)
        print("\t==========ImportUrls=============")
        for element in self.importurls:
            print("\t\t" + element)
        print("\t=End=====Class FullDates=========")

    # Функция импорта данных
    def importurlsfrompage(self):

        # Получаем сегодняшнее число
        today = datetime.datetime.today()
        day = today.strftime("%d")
        intday = int(day)
        month = today.strftime("%m")
        months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
        year = today.strftime("%Y")
        today = str(intday) + " " + months[int(month) - 1] + " " + year
        #print(f"\t{today}")

        # Получем данные со страницы
        try:
           page = requests.get(urlpage, headers=headers, timeout=5)
        except requests.exceptions.HTTPError as error:
            print(error)
        #print(f"\t{page}")

        # Разбираем страницу с помощью BeautifulSoup
        html = BeautifulSoup(page.content, 'html.parser')
        postdates = html.select(".gbnews-listShort > td > a")

        # Попытка решить проблему с вылетом скрипта
        s = requests.session()
        s.keep_alive = False

        # Формируем список ссылок на новости
        pathlist = []
        i = 0
        for element in postdates:
            if i % 2 == 0:
                pathlist.append(element["href"])
            i = i + 1
        dates = html.select(".sub")
        #pprint.pprint(dates)

        # Формируем массив с ссылками на новости которые надо распарсить
        result = []
        i = 0
        for element in dates:
            # Ограничение на максимальное количество новостей на странице
            if i == 20:
                break
            # Обрезаем дату поста новости, для сравнения с текущей датой
            date_post = str(element.text)[:-8]
            #print(f"\t\t{date_post}")
            # Если дата поста совпадает с сегодняшней датой, то
            #if date_post == today:
            if date_post == "6 июня 2023":
                # Формируем итоговый массив с ссылками
                result.append(str(pathlist[i]))
            i = i + 1
        # Записываем результат в лист экспортированных url
        self.exporturls = result

    # Функция открытия статьи и импорта названия
    def insertnamepage(self, url):
        page = requests.get(url, headers=headers)
        # Разбираем страницу с помощью BeautifulSoup
        html = BeautifulSoup(page.content, 'html.parser')
        postdates = html.select("title")
        title = str(postdates)[8:-23]
        return title

    # Функция планирования постанга новостей
    def planpostingdates(self, starttime, endtime):
        # Расчитываем время ожидания (для формирования времени следующего поста)
        delta = int(endtime) - int(starttime)
        nextstep = math.floor(delta / len(self.exporturls))
        # Создаём массив названий статей
        mass = []
        timetopost = int(starttime)
        for element in self.exporturls:
            namepage = self.insertnamepage(element)
            #mass.append([timetopost, element, namepage])
            self.timewithposts.append(str(timetopost))
            self.timewithposts.append(element)
            self.timewithposts.append(namepage)
            timetopost += nextstep

# Класс времён
class times:

    # Время импорта новостей
    importtime = datetime.datetime.today().strftime("%H:%M")
    #importtime = datetime.time(23, 55).strftime("%H:%M")

    # Время подготовки плана постинга
    #planpostingdates = datetime.time(23, 58).strftime("%H:%M")
    planpostingdates = (datetime.datetime.today() + datetime.timedelta(minutes=1)).strftime("%H:%M")
    # Время начала постинга
    starttimeposting = datetime.time(9,00).strftime("%H")
    # Время конца постинга
    endtimeposting = datetime.time(23, 00).strftime("%H")

    # Время первого поста
    #timetopost = datetime.time(8, 00).strftime("%H:%M")
    timetopost = (datetime.datetime.today() + datetime.timedelta(minutes=3)).strftime("%H:%M")

    # Время обнуления переменных
    #nulltime = datetime.time(23, 0).strftime("%H:%M")
    nulltime = (datetime.datetime.today() + datetime.timedelta(minutes=5)).strftime("%H:%M")

    #nulltime = (datetime.datetime.today() + datetime.timedelta(minutes=1)).strftime("%H:%M")
