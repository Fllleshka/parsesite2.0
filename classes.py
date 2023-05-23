# Класс общих данных
class FullDates:
    # Метод-конструктор с переменными экземпляра класса
    def __init__(self):
        # Список экспортированных url
        self.exporturls = []
        # Список запланированных постов с временем
        self.timewithposts = []

    # Функция печати данных
    def printidates(self):
        print("=Start===Class FullDates==========")
        print("===========ExportUrls=============\n")
        for element in self.exporturls:
            print("\t" + element)
        print("=========TimeWithPosts===========\n")
        for element in self.timewithposts:
            print("\t" + element)
        print("=End=====Class FullDates==========")