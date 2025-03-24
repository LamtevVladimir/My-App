import datetime
import pandas as pd
import random
from faker import Faker
import sqlite3
import time

'''_________________________________________Date_________________________________________'''


class date():
    "некоторая дата"
    __slots__ = ('day', 'month', 'year')

    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
    def __str__(self):
        return(f"{self.day}.{self.month}.{self.year}")
    def __sub__(self, other):
        year = self.year - other.year
        month = 0
        day = 0

        if self.month < other.month:
            year -= 1
            month = 12 - other.month + self.month
        else:
            month = self.month - other.month

        if self.day < other.day:
            if month == 0:
                year -=1
                day = 30 - other.day + self.day
                month = 11
            else:
                day = 30 - other.day + self.day
                month -= 1
        else:
            day = self.day - other.day
        return date(day, month, year)
        #Да, я сначала написал класс "даты", а потом подключил библиотеку, делающую то же самое


'''_________________________________________Person_________________________________________'''


class Person():
    "личные данные одного человека"
    __slots__ = ('__Name', '__Bdate', '__male')

    def __init__(self, Name, Bdate, Male):
        self.__Name = Name
        self.__Bdate = Bdate
        self.__male = Male

    def __str__(self):
        return f"Person: {self.__Name}, {self.__Bdate}, {self.__male}"

    def Age_at(self, today):
        '''принимает две даты и выводит год из итога их разности'''
        age = today - self.__Bdate
        return age.year

    def update(self, list, today):
        a = [self.__Name, self.__Bdate, self.__male, self.Age_at(today)]
        list.append(a)

    def go_to_SQL(self, File_name):
        conn = sqlite3.connect(File_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Users (Name, Bdate, male) VALUES (?, ?, ?)',
                       (self.__Name, str(self.__Bdate), self.__male))
        # Сохраняем изменения
        conn.commit()
        # Закрываем соединение
        conn.close()


    @property
    def Name(self):
        return self.__Name
    @property
    def Bdate(self):
        return self.__Bdate
    @property
    def male(self):
        return self.__male
    ''' при необходимости можно добавить условия в setter (и __init__)'''
    @Name.setter
    def table_size(self, data):
        self.__Name= data
    @Name.deleter
    def table_size(self):
        del self.__Name
    @Bdate.setter
    def table_size(self, data):
        self.__Bdate = data
    @Bdate.deleter
    def table_size(self):
        del self.__Bdate
    @male.setter
    def table_size(self, data):
        self.__male = data
    @male.deleter
    def table_size(self):
        del self.__male


'''_________________________________________Table_________________________________________'''


class Table():
    "локальный справочник"
    __slots__ = ('list_of_Persons', 'today')
    def __init__(self, data = []):
        self.list_of_Persons = data
        current_time = datetime.datetime.now()
        self.today = date(current_time.day, current_time.month, current_time.year)

    def append(self, person):
        self.list_of_Persons.append([person.Name, person.Bdate, person.male, person.Age_at(self.today)])

    def update(self):
        current_time = datetime.datetime.now()
        self.today = date(current_time.day, current_time.month, current_time.year)
        for i in range (len(self.list_of_Persons)):
            self.list_of_Persons[i][3] = self.list_of_Persons[i][1]
        return ()

    def sort(self, what):
        self.list_of_Persons.sort(key=lambda x: x[what])

    def filter(self, key1='', key2=''):
        list = []
        for i in self.list_of_Persons:
            if key1 == '' or i[0].find(key1) == 0:
                if key2 == '' or i[2] == key2:
                    list.append(i)
        return list

    def __str__(self):
        print(pd.DataFrame(self.list_of_Persons, columns = ['ФИО', 'День рождения', 'Пол', 'Возраст']))
        return f"last update: {self.today}"

    def clear(self):
        self.list_of_Persons.clear()

    def generate_Persons(self, num_records, key1 = '', key2 = ''):
        '''добавляет сгенерированных людей, первый ключ - начало фамилии, второй - пол'''
        fake = Faker()
        for i in range(num_records):
            # Генерация ФИО (так как мы используем английский язык,
            last_name = fake.last_name()
            if key1 != '':
                leng = len(key1)
                while last_name[:leng] != key1:
                    last_name = fake.last_name()

            if (key2 == 'male') or (key2 != 'female') and (random.choice([True, False])):
                first_name = fake.first_name_male()
                second_name = fake.first_name_male()
                male = 'male'
            else:
                first_name = fake.first_name_female()
                second_name = fake.first_name_female()
                male = 'female'
            Bdate = fake.date_of_birth(minimum_age=10, maximum_age=69).strftime('%Y-%m-%d')
            Bdate = from_str_to_date(Bdate)
            pers = Person(last_name+' '+first_name+' '+second_name, Bdate, male)
            self.append(pers)

    def go_to_csv(self, name):
        Data = pd.DataFrame(self.list_of_Persons, columns=['ФИО', 'День рождения', 'Пол', 'Возраст'])
        Data.to_csv(name+'.csv')

    def go_to_SQL(self, name, key = 0):
        if key == 0:
            list = []
            for i in self.list_of_Persons:
                list.append((i[0], str(i[1]), i[2]))
            conn = sqlite3.connect(name)
            cursor = conn.cursor()
            with conn:
                cursor.executemany('INSERT INTO Users (Name, Bdate, male) VALUES (?, ?, ?)', list)

            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect(name)
            cursor = conn.cursor()
            with conn:
                cursor.executemany('INSERT INTO Users (Name, Bdate, male, Age) VALUES (?, ?, ?, ?)', self.list_of_Persons)

            conn.commit()
            conn.close()






'''abba_date = date(12, 12, 2001)
current_time = datetime.datetime.now()
today = date(current_time.day, current_time.month, current_time.year)
abba = Person('213', abba_date, '213')
A = Table()
A.append(abba)
print(type(A))
print(abba)
print (today - abba_date)
print(abba.Age_at(today))
print(A)'''

'''_________________________________________Functions_________________________________________'''


def file_name(request, a):
    return (request[request.find(a) + len(a):])

def from_str_to_date(Bdate):
    if '-' in Bdate:
         Bmonth = int(Bdate[Bdate.find('-') + 1:Bdate.rfind('-')])
         Bday = int(Bdate[Bdate.rfind('-') + 1:])
         Byear = int(Bdate[:Bdate.find('-')])
         Answer = date(Bday, Bmonth, Byear)
    elif '.' in Bdate:
        Bmonth = int(Bdate[Bdate.find('.') + 1:Bdate.rfind('.')])
        Byear = int(Bdate[Bdate.rfind('.') + 1:])
        Bday = int(Bdate[:Bdate.find('.')])
        Answer = date(Bday, Bmonth, Byear)
    return Answer


'''_________________________________________Main_________________________________________'''

while True:
    print("What's your request")
    request = input()
    Main_Table = Table()
    if 'my App 1' in request:
        Main_Table.clear()

    elif 'my App 2' in request:
        # my App 2
        # #Example "Name" 11.11.2011 male
        Name = request[request.find('"') + 1:request.rfind('"')]
        print(Name)
        Male = request[request.rfind(' ') + 1:]
        print(Male)
        Bdate = request[request.rfind('"')+2:request.rfind(' ')]
        Bdate = from_str_to_date(Bdate)
        print(Bdate)
        Pers = Person(Name, Bdate, Male)
        if 'my App 2x' in request:
            print('Where?')
            File = input()
            Pers.go_to_SQL(File)
        else:
            Main_Table.append(Pers)

    elif 'my App 3' in request:
        print(Main_Table)
    elif 'my App k4' in request:
        Main_Table.generate_Persons(100, 'F', 'male')
    elif 'my App 4' in request:
        Main_Table.generate_Persons(int(request[request.rfind(' '):]))
    elif request == 'stop':
        break
    elif 'my App 5 ' in request:
        #выводит значения по 2 фильтрам: начало фамилии и пол
        #my App 5 F|male
        keys = file_name(request, 'my App 5 ')

        start_time = time.time()  # Запоминаем время начала
        Filtered = Main_Table.filter(keys[: keys.find('|')], keys[keys.find('|') + 1:])
        end_time = time.time()

        print(pd.DataFrame(Filtered, columns = ['ФИО', 'День рождения', 'Пол', 'Возраст']))
        print(end_time - start_time)
    elif 'my App CopySQL: ' in request:
        #копирует базу в локальный список Main_Table
        #Example my App CopySQL: test_data.db
        conn = sqlite3.connect(file_name(request, 'my App CopySQL: '))
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Users
        ''')
        users = cursor.fetchall()
        Main_Table.clear()
        for i in users:
            Pers = Person(i[0], from_str_to_date(i[1]), i[2])
            Main_Table.append(Pers)

        conn.commit()
        conn.close()

    elif 'my App WriteSQL: ' in request:
        #добавляет пакет данных к подключённой базе данных
        #  Example my App WriteSQL: test_data.db
        name = file_name(request, 'my App WriteSQL: ')
        Main_Table.go_to_SQL(name)


    elif 'my App AddCSV: ' in request:
        #добавляет из базы CSV в локальный список Main_Table
        File = file_name(request, 'my App CopyCSV: ')
        original = pd.read_csv(File)
        Head = original.columns.tolist()
        '''print(original.columns.tolist())
        print(original.ФИО)
        print(original.to_dict()['ФИО'][1])'''
        for i in range(len(original[Head[0]])):
            Pers = Person(original[Head[1]][i], from_str_to_date(original[Head[2]][i]), original[Head[3]][i])
            Main_Table.append(Pers)
        print(Main_Table)
    elif 'my App WriteСSV: ' in request:
        # сохраняет локальный список Main_Table или пользователя в csv базу
        Main_Table.go_to_csv(file_name(request, 'my App Write: '))
    elif 'my App AddCSV: ' in request:
        #добавляет из базы CSV в локальный список Main_Table
        File = file_name(request, 'my App CopyCSV: ')
        original = pd.read_csv(File)
        Head = original.columns.tolist()
        '''print(original.columns.tolist())
        print(original.ФИО)
        print(original.to_dict()['ФИО'][1])'''
        for i in range(len(original[Head[0]])):
            Pers = Person(original[Head[1]][i], from_str_to_date(original[Head[2]][i]), original[Head[3]][i])
            Main_Table.append(Pers)
        print(Main_Table)
    else:
        print('Not correct request')
print('Thanks for using my App')




