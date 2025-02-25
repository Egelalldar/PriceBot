import secrets
import pymysql.cursors
from secrets import secrets
import datetime

# функция добавить сотрудника в базу
def add_user(user):
    # соединение с базой
    connection = pymysql.connect(host=secrets['host'],
                                 user=secrets['user'],
                                 password=secrets['password'],
                                 database=secrets['database'],
                                 charset=secrets['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            # проверка пользователя на уникальность, пользователь добавляется только один раз
            row_t_user = secrets['row_users_t_user']
            table = secrets['table_users']
            sql_check_unique_t_user = "SELECT " + row_t_user + " FROM " + table + " WHERE " + table + "." + row_t_user + "='" + user + "'"
            cursor.execute(sql_check_unique_t_user)
            result = cursor.fetchall()
            # запросом выше получаем пользователя, если его нет, то добавляем, есть есть, то return False
            try:
                result[0][row_t_user]
            except IndexError:
                sql_add = "INSERT INTO " + table + " (" + row_t_user + ") VALUES (%s)"
                cursor.execute(sql_add, user)
                connection.commit()
                return True
            else:
                return False

# функция получить ссылку от пользователя
def add_url(uid, url):
    connection = pymysql.connect(host=secrets['host'],
                                 user=secrets['user'],
                                 password=secrets['password'],
                                 database=secrets['database'],
                                 charset=secrets['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            row_url = secrets['row_items_url']
            table_users = secrets['table_users']
            table_items = secrets['table_items']
            row_user = secrets['row_users_user']
            row_t_user = secrets['row_users_t_user']
            # проверяем, есть ли пользователь
            sql_search_user = "SELECT " + row_user + " FROM " + table_users + " WHERE " + row_t_user + "=%s"
            cursor.execute(sql_search_user, uid)
            uid = cursor.fetchall()
            try:
                uid[0][row_user]
            except IndexError:
                # если пользователя нет
                return False
            else:
                # если есть, то добавляем ссылку
                uid = uid[0][row_user]
                sql_search_url = "SELECT " + row_url + " FROM " + table_items + " WHERE " + row_url + "=%s"
                # проверка на дублирование ссылки
                cursor.execute(sql_search_url, url)
                url_test = cursor.fetchall()
                try:
                    url_test[0][row_url]
                except IndexError:
                    # если нет такой ссылки
                    sql_add_url = "INSERT INTO " + table_items + " (" + row_user + ", " + row_url + ") VALUES(%s, %s)"
                    values = [uid, url]
                    cursor.execute(sql_add_url, values)
                    connection.commit()
                    return True
                else:
                    # если дублируется
                    return False

# получаем словарь с user_id и url
def take_users_and_urls():
    connection = pymysql.connect(host=secrets['host'],
                                 user=secrets['user'],
                                 password=secrets['password'],
                                 database=secrets['database'],
                                 charset=secrets['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            table_users = secrets['table_users']
            row_users = secrets['row_users_user']
            table_items = secrets['table_items']
            row_url = secrets['row_items_url']

            sql_search_all_users = "select " + row_users + " from " + table_users
            cursor.execute(sql_search_all_users)
            users = cursor.fetchall()
            url_list = []
            # получаем список
            for elem in users:
                sql_search_url_on_users = "SELECT user_id, " + row_url + " FROM " + table_items + " WHERE " + row_users + "=%s"
                cursor.execute(sql_search_url_on_users, str(elem[row_users]))
                urls = cursor.fetchall()
                url_list = url_list + [urls]
            # результат
            # [[{'user_id': 5, 'url': 'http://127.0.0.1'}, {'user_id': 5, 'url': 'http://127.0.0.1/index2.html'}],
            #  [{'user_id': 6, 'url': 'http://127.0.0.1'}, {'user_id': 6, 'url': 'http://127.0.0.1/index3.html'}],
            #  [{'user_id': 7, 'url': 'http://127.0.0.1/index3.html'}]]
            data = []
            temp_dict = {}
            # упрощаем список
            for sublist in url_list:
                for item in sublist:
                    user_id = item[row_users]
                    url = item[row_url]
                    if user_id not in temp_dict:
                        temp_dict[user_id] = []
                    temp_dict[user_id].append(url)
            for user_id, urls in temp_dict.items():
                data.append({row_users: user_id, row_url: urls})
    return data
    # получаем такой словарь
    # [{'user_id': 5, 'urls': ['http://127.0.0.1', 'http://127.0.0.1/index2.html']}, \
    #  {'user_id': 6, 'urls': ['http://127.0.0.1', 'http://127.0.0.1/index3.html']}, \
    #  {'user_id': 7, 'urls': ['http://127.0.0.1/index3.html']}]

# запись цены со страницы
def take_price(price, user_id, url):
    connection = pymysql.connect(host=secrets['host'],
                                 user=secrets['user'],
                                 password=secrets['password'],
                                 database=secrets['database'],
                                 charset=secrets['charset'],
                                 cursorclass=pymysql.cursors.DictCursor)
    with (connection):
        with connection.cursor() as cursor:
            table_price = secrets['table_price']
            table_items = secrets['table_items']
            row_price = secrets['row_price_price']
            row_date = secrets['row_price_date']
            row_items = secrets['row_items_item']
            row_users = secrets['row_users_user']
            row_url = secrets['row_items_url']
            # получаем уникальный item_id из url и user_id
            sql_temp = "select " + row_items + " from " + table_items + " where " + \
                        row_users + "='" + user_id + "' and " + row_url + "='" + url + "'"
            print(sql_temp)
            cursor.execute(sql_temp)
            item = cursor.fetchall()
            item = item[0][row_items]
            # используем item_id для записи цены и даты в таблицу, полученной со страницы
            sql_insert_price = "INSERT INTO " + table_price + " (" + row_items + "," + row_price + \
                              "," + row_date + ") VALUES (%s,%s,%s)"
            date = datetime.date.today().strftime('%Y-%m-%d')
            values = [item, price, date]
            cursor.execute(sql_insert_price, values)
            connection.commit()
