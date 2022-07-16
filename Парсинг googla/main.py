#
# Парсим Google
#

import requests
from bs4 import BeautifulSoup
import json
import time

all_data = []
headers = {'User-Agent': 'Mozilla/4.0 (Linux; Android 5.0; Nexus 3 Build/MRA58N) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.31'}

#запрос что искать
#(слова разделять плюсиками +)
phrase = 'инвестиции'

# Стартовая страница
start_page = 1

# до какой страницы включительно искать
finish_page = 10

def read_file_data():
    # Запись найденных данных в файл JSON
    with open('foundAdress.json', 'a', encoding='utf-8') as file:
        json.dump(all_data, file, indent=4, ensure_ascii=False)

    print(f'Найдено {len(all_data)} записей')

def get_data():
    page_numbers = finish_page - start_page
    count_page = start_page

    for q in range((start_page-1)*10, 10*finish_page, 10):
        url = f'https://www.google.com/search?q={phrase}&start={q}'

        # Записываем страницы в файлы
        req = requests.get(url, headers)
        with open(f'page/page_{count_page}.html', 'w', encoding="utf-8") as file:
            file.write(req.text)

        # Читаем файл
        with open(f'page/page_{count_page}.html', encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        h3 = soup.find_all('h3')
        num = 0
        for i in h3:
            start_time = time.time()
            name_site = i.text.strip()

            try:
                url_adress = i.parent.get('href').split('q=')[1].split('/')[0] + '//' + \
                          i.parent.get('href').split('q=')[1].split('/')[1] + i.parent.get('href').split('q=')[1].split('/')[2]
            except:
                print('Ошибка поиска данных на странице')

            try:
                req = requests.get(url_adress, headers)

                # Проверка на долгий ответ от сайта с последующим пропуском
                if (time.time() - start_time > 3):
                    print(f'Сайт {url_adress} пропущен.')
                    continue

                with open(f'work/site_number_{num}.html', 'w', encoding="utf-8") as file:
                    file.write(req.text)

                with open(f'work/site_number_{num}.html', encoding="utf-8") as file:
                    src1 = file.read()

                soup = BeautifulSoup(src1, 'lxml')

                num +=1
                query_contacts = []

                # Проверка на долгий ответ от сайта с последующим пропуском
                if (time.time() - start_time > 3):
                    print(f'Сайт {url_adress} пропущен.')
                    continue

                #Поиск по тегу <p>
                query_p = soup.find_all('p')
                for i in query_p:
                    if '@' in i.text:
                        all_elements_str = i.text.split(' ')
                        for i2 in all_elements_str:
                            if ('@' in i2 and i2 not in query_contacts):
                                query_contacts.append(i2)

                # Поиск по тегу <a>
                query_a = soup.find_all('a')
                for i in query_a:
                    if '@' in i.text:
                        all_elements_str = i.text.split(' ')
                        for i2 in all_elements_str:
                            if ('@' in i2 and i2 not in query_contacts):
                                query_contacts.append(i2)

                # Поиск по тегу <span>
                query_span = soup.find_all('span')
                for i in query_span:
                    if '@' in i.text:
                        all_elements_str = i.text.split(' ')
                        for i2 in all_elements_str:
                            if ('@' in i2 and i2 not in query_contacts):
                                query_contacts.append(i2)

                # Поиск по тегу <div>
                query_div = soup.find_all('div')
                for i in query_div:
                    if '@' in i.text:
                        all_elements_str = i.text.split(' ')
                        for i2 in all_elements_str:
                            if ('@' in i2 and i2 not in query_contacts):
                                query_contacts.append(i2)


                if(len(query_contacts) == 0):
                    query = 'Контактные данные не найдены'
                    query_contacts.append(query)
                else:
                    data_all_in = {
                        'Название сайта': name_site,
                        'URL адресс': url_adress,
                        'Контактные данные': query_contacts
                    }
                    all_data.append(data_all_in)

                print(f'Анализ сайта {url_adress} завершён!')

                print (time.time() - start_time, "seconds")
                print('----------------------------------------------------------')
            except:
                print(f'Ошибка поиска на сайте {url_adress}')

        print('===================================')
        print(f'Завершен анализ страницы №{count_page}')
        print('===================================')

        count_page +=1

    # Вызываем функцию записи в файл найденных данных
    read_file_data()

# Старт основной функции
get_data()

def start1():
    # headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'}
    url_test = 'https://veles-capital.ru'
    req = requests.get(url_test, headers)
    with open(f'work/test.html', 'w', encoding="utf-8") as file:
        file.write(req.text)
    with open(f'work/test.html', encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    query_contacts = []

    # Поиск по тегу <p>
    query_p = soup.find_all('p')
    for i in query_p:
        if '@' in i.text:
            all_elements_str = i.text.split(' ')
            for i2 in all_elements_str:
                if ('@' in i2 and i2 not in query_contacts):
                    query_contacts.append(i2)

    # Поиск по тегу <a>
    query_a = soup.find_all('a')
    for i in query_a:
        if '@' in i.text:
            all_elements_str = i.text.split(' ')
            for i2 in all_elements_str:
                if ('@' in i2 and i2 not in query_contacts):
                    query_contacts.append(i2)

    # Поиск по тегу <span>
    query_span = soup.find_all('span')
    for i in query_span:
        if '@' in i.text:
            all_elements_str = i.text.split(' ')
            for i2 in all_elements_str:
                if ('@' in i2 and i2 not in query_contacts):
                    query_contacts.append(i2)

    for i in query_contacts:
        print(i)


# start1()