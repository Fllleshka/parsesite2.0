# Импорт файла в котором находятся классы
from classes import *

# Импорт библиотек
import time

# Функция определения действия
def switcher(time, data):
    match(time):
        # Время обнуления переменных
        case times.nulltime:
            print(f"Время для обнуления переменных: {times.nulltime}")
            # Обнуляем переменные класса FullDates
            data.exporturls = []
            data.timewithposts = []
            data.importurls = []
            # Выводим данные в лог
            data.printidates()

        # Время для импортирования новостей с сайта
        case times.importtime:
            print("Время для импортирования новостей с сайта: ", times.importtime)
            # Импорт urls для создания статей с новостями
            data.importurlsfrompage()
            # Цикл создания новостей
            for element in data.importurls:
                # Создаём экземпляр новости и работаем с ней
                newnews = News(element)
                data.exporturls.append(newnews.resulturl)
            # Выводим данные в лог
            data.printidates()

        # Время для планирования постов
        case times.planpostingdates:
            print("Время для планирования постинга новостей с сайта: ", times.planpostingdates)
            if len(data.exporturls) == 0:
                print("\tМассив экспортированных новостей пуст")
            else:
                print("\tМассив экспортированных новостей не пуст")
                # Запускаем функцию формирования результирующего списка ссылок для публикации
                data.planpostingdates(times.starttimeposting, times.endtimeposting)
                # Выводим данные в лог
                data.printidates()

        # Время для постанга новости
        case times.timetopost:
            print("Время для постинга новости: ", times.timetopost)
            data.postinchannel()

        # Время для вывода времени
        case _:
            print(f"Время сейчас: {time}")
    # Возвращаем изменившиеся данные
    return data

# Создаём экземпляр класса fulldates
dddates = FullDates()

# Вечный бесконечный цикл
while True:
    try:
        # Время сейчас
        today = datetime.datetime.today()
        todaytime = today.strftime("%H:%M")
        # Запуск функции выбора действия с возвращением занчений в экземпляр класса
        dddates = switcher(todaytime, dddates)
        time.sleep(60)
    except Exception as e:
        print(e)