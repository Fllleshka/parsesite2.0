# Импорт библиотек
import datetime
import math
import shutil
import requests
import os
import telebot
from telegraph import Telegraph
from bs4 import BeautifulSoup

# Импорт данных по сайту, боту
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

        # Получаем данные со страницы
        try:
           page = requests.get(urlpage, headers=headers, timeout=5)
        except requests.exceptions.HTTPError as error:
            print(error)

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

        # Формируем массив с ссылками на новости которые надо распарсить
        result = []
        i = 0
        for element in dates:
            # Ограничение на максимальное количество новостей на странице
            if i == 20:
                break
            # Обрезаем дату поста новости, для сравнения с текущей датой
            date_post = str(element.text)[:-8]
            # Если дата поста совпадает с сегодняшней датой, то
            if date_post == today:
                # Формируем итоговый массив с ссылками
                result.append(str(pathlist[i]))
            i = i + 1
        # Записываем результат в лист экспортированных url
        self.importurls = result

    # Функция открытия статьи и импорта названия
    def insertnamepage(self, url):
        page = requests.get(url, headers=headers)
        # Разбираем страницу с помощью BeautifulSoup
        html = BeautifulSoup(page.content, 'html.parser')
        postdates = html.select("title")
        title = str(postdates)[8:-21]
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
            self.timewithposts.append(str(timetopost))
            self.timewithposts.append(str(element))
            self.timewithposts.append(str(namepage))
            #self.timewithposts.append(str([timetopost, element, namepage]))
            timetopost += nextstep

    # Функция постинга новости
    def postinchannel(self):
        # Токен для связи с ботом
        bot = telebot.TeleBot(botkey)
        # Выбираем данные для отправки публикации новости в канал
        mass = [self.timewithposts[0], self.timewithposts[1], self.timewithposts[2]]
        # Удаляем ненужные данные из списка
        for element in range(0, 3):
            self.timewithposts.pop(0)
        # Генерируем новое время публикации
        times.timetopost = datetime.time(int(mass[0]), 00).strftime("%H:%M")
        print("Время для постинга следующей новости: ", times.timetopost)
        # Формируем сообщение для отправки
        print(f"{type(mass[2])} {mass[2]}")
        print(f"{type(mass[1])} {mass[1]}")
        message = "[" + str(mass[2]) + "](" + str(mass[1]) + ")"
        print(message)
        status = bot.send_message(channel_id, message, parse_mode='MarkdownV2')
        print(f"Публикация: {mass[2]}\nЗавершилась со статусом: {status}")

# Класс новости
class News:

    # Метод-конструктор с переменными экземпляра класса
    def __init__(self, url):
        self.url = url
        self.header_title = ""
        self.autor = ""
        self.first_photo = ""
        self.massive_text = []
        self.massive_photos = []
        self.resulturl = ""
        self.importdates(url)

    # Функция печати данных
    def printimportdates(self):
        print("========================")
        print("URL:")
        print("\t" + self.url)
        print("\t" + self.header_title)
        print("\t" + self.autor)
        print("\t" + self.first_photo)
        for element in self.massive_text:
            print("\t" + element)
        for element in self.massive_photos:
            print("\t" + element)
        print("\t" + self.resulturl)
        print("========================")

    # Функция импорта данных с сайта
    def importdates(self, urlpage):
        print("Запускаем импорт данных с: ", urlpage)
        # Получаем страницу
        page = requests.get(urlpage, headers=headers)
        # Разбираем страницу с помощью BeautifulSoup
        html = BeautifulSoup(page.content, 'html.parser')
        # Достаём название статьи
        self.header_title = html.select(".container-header > h1")[0].text
        # Достаём автора статьи
        self.autor = html.select(".gbusers-login > span")[0].text
        # Достаём адрес главной картинки
        self.first_photo = "https://gamebomb.ru/" + html.select(".img > a")[0]['href']
        # Достаём текстовую информацию и формируем из неё массив
        maintext = html.select(".content > div > p")
        for element in maintext:
            if element.text == "":
                continue
            else:
                self.massive_text.append(element.text)
        # Достаём URL картинкок
        mainphotos = html.select(".content > div > p > a")
        # Пробегаемся по массиву и исключаем из него данные которые не подходят
        for element in mainphotos:
            substring = str(str(element)[10:])[:5]
            if substring != "files":
                mainphotos.remove(element)
        # Проверка полученных ссылок на картинки
        for element in mainphotos:
            substring = str(str(element)[9:])[:5]
            if substring == "/file":
                if ("https:" in element['href']) == True:
                    continue
                else:
                    self.massive_photos.append("https://gamebomb.ru" + element['href'])
            else:
                continue
        # Выполняем выгрузку данных
        self.downloadfiles()

    # Функция скачивания файлов
    def downloadfiles(self):
        # Скачиваем главную картинку
        page = requests.get(self.first_photo)
        url = "main_photo.jpg"
        outputpage = open(url, "wb")
        outputpage.write(page.content)
        outputpage.close()

        # Создаём временную папку TEMP
        urltemp = "TEMP"
        # Если есть такая папка, то удаляем и создаём заного (Обработка [WinError 183])
        try:
            os.mkdir(urltemp)
        except OSError:
            os.rmdir(urltemp)
            os.mkdir(urltemp)

        # Скачиваем картинки из massive_photos
        i = 0
        for element in self.massive_photos:
            page = requests.get(element)
            urlphotos = "TEMP/" + str(i) + ".jpg"
            outputpage = open(urlphotos, "wb")
            outputpage.write(page.content)
            outputpage.close()
            i = i + 1

        # Выполняем загрузку файлов в Telegram
        self.uploadfiles(url)

    # Функция загрузки фаилов на сервера telegram
    def uploadfiles(self,urlmainphoto):

        # Закачиваем на сервер главную картинку
        with open(urlmainphoto, 'rb') as f:
            path = requests.post(
                'https://telegra.ph/upload',
                files={'file': ('file', f, 'image/jpg')}).json()[0]['src']
            self.first_photo = path

        # Подчищаем главную картинку
        os.remove(urlmainphoto)

        # Путь до папки с TEMP
        pathtemp = './TEMP/'

        # Получаем список фаилов папки TEMP
        directory_list = os.listdir(pathtemp)

        # Обнуляем massive_photos
        self.massive_photos = []

        # Загружаем картинки в Telegram и переопределяем массив со ссылками
        for element in directory_list:
            waytoimage = "./TEMP/" + element
            with open(waytoimage, 'rb') as f:
                path = requests.post(
                    'https://telegra.ph/upload',
                    files={'file': ('file', f, 'image/jpg')}).json()[0]['src']
            self.massive_photos.append(path)

        # Подчищаем папку
        shutil.rmtree(str(pathtemp)[2:-1])

        # Создаём пост
        self.createpost()

    # Функция создания ссылки на страницу новости
    def createpost(self):
        # Создаём аккаунт
        telegraph = Telegraph()
        telegraph.create_account(short_name = self.autor)
        # Начинаем формировать контент нашей страницы
        # Загружаем главное фото
        content = "<img src = {}/>".format(self.first_photo)
        # Формируем первые 2 текста
        content += "<p>{}</p>".format(str(self.massive_text[0]))
        content += "<p>{}</p>".format(str(self.massive_text[1]))
        # Удаляем данные из списка
        self.massive_text.pop(0)
        self.massive_text.pop(0)
        # Формируем первые 1 картинку
        content += "<img src = {}/>".format(self.massive_photos[0])
        # Удаляем данные из списка
        self.massive_photos.pop(0)
        # Дописываем всё в фаил
        for element in self.massive_text:
            content += "<p>{}</p>".format(str(element))
        # Если есть ещё картинки, то дописываем в фаил
        for element in self.massive_photos:
            content += "<img src = {}/>".format(element)
        # Создаём страницу
        response = telegraph.create_page(self.header_title, html_content = content)
        # Записываем данные в переменную resulturl
        self.resulturl = response['url']

# Класс времён
class times:

    # Время импорта новостей
    #importtime = datetime.datetime.today().strftime("%H:%M")
    importtime = datetime.time(23, 50).strftime("%H:%M")

    # Время подготовки плана постинга
    planpostingdates = datetime.time(23, 54).strftime("%H:%M")
    #planpostingdates = (datetime.datetime.today() + datetime.timedelta(minutes=2)).strftime("%H:%M")
    # Время начала постинга
    starttimeposting = datetime.time(9,00).strftime("%H")
    # Время конца постинга
    endtimeposting = datetime.time(23, 00).strftime("%H")

    # Время первого поста
    timetopost = datetime.time(9, 00).strftime("%H:%M")
    #timetopost = (datetime.datetime.today() + datetime.timedelta(minutes=3)).strftime("%H:%M")

    # Время обнуления переменных
    nulltime = datetime.time(23, 30).strftime("%H:%M")
    #nulltime = (datetime.datetime.today() + datetime.timedelta(minutes=10)).strftime("%H:%M")