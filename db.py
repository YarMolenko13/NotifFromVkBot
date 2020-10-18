import psycopg2
from datetime import datetime

class Postgers:
    def __init__(self):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = psycopg2.connect(database="dahgacg8oodfm2", user="bmjtlwlysizldb",
            password="dd75f00eef86bf9ebe96a8d219b7911411d4d79d39314994c2260ac48496b904",
            host="ec2-107-22-241-205.compute-1.amazonaws.com", port=5432)
        self.cursor = self.connection.cursor()


    # методы для работы с statesTable
    def get_current_state(self, user_id):
        """Получаем состояние пользователя"""
        self.cursor.execute('''SELECT state
                                            FROM statesTable
                                            WHERE user_id = {}'''.format(user_id))

        return self.cursor.fetchall()[0][0]

    def set_state(self, user_id, value):
        """Изменяем состояние"""
        def is_exist_func():
            global is_exist
            self.cursor.execute('''SELECT * FROM statesTable WHERE user_id = {}'''.format(user_id))

            if len(self.cursor.fetchall()) == 0:
                is_exist = False
            else:
                is_exist = True

        is_exist_func()

        if is_exist:
            self.cursor.execute('''UPDATE statesTable
        				  SET state = {0}
        				  WHERE user_id = {1}'''.format(value, user_id))
            self.connection.commit()
        else:

            self.cursor.execute('''INSERT INTO statesTable (user_id, state)
            	VALUES ({0}, {1})'''.format(user_id, value))
            self.connection.commit()


    def get_all_users(self):
        """Получаем все id"""
        self.cursor.execute('''SELECT user_id FROM statesTable''')
        return self.cursor.fetchall()


    # методы для работы с notTable

    def subscribe(self, user_id, domain):
        """Подписываемся на уведомления"""
        # def is_exist_func():
        #     global is_exist2

        #     self.cursor.execute('''SELECT * FROM notTable WHERE user_id = {}'''.format(user_id))
        #     if len(self.cursor.fetchall()) == 0:
        #         is_exist2 = False
        #     else:
        #         is_exist2 = True

        # is_exist_func() 

        def is_more_4_func():
            global is_more_4

            self.cursor.execute('''SELECT * FROM notTable WHERE user_id = {}'''.format(user_id))
            if len(self.cursor.fetchall()) > 4:
                is_more_4 = True
            else:
                is_more_4 = False

        is_more_4_func()

        if not is_more_4:
            self.cursor.execute('''INSERT INTO notTable (user_id, domain, is_sub)
                                   VALUES ({0}, '{1}', True)'''.format(user_id, domain))
            self.connection.commit()

        # if is_more_4:
        #     return 'more4pub'

        # if is_exist2:
        #     self.cursor.execute('''UPDATE notTable
        # 				           SET is_sub = True,
        #                            domain = '{0}'
        # 				           WHERE user_id = {1}'''.format(domain, user_id))
        #     self.connection.commit()
        # else:
        # 	self.cursor.execute('''INSERT INTO notTable (user_id, domain, is_sub)
        # 	 	                   VALUES ({0}, '{1}', True)'''.format(user_id, domain))
        # 	self.connection.commit()


    def unsubscribe(self, user_id, domain):
        """Отписываемся от уведомлений"""
        self.cursor.execute('''DELETE FROM nottable WHERE domain = '{}' '''.format(domain))
        self.connection.commit()

        # self.cursor.execute('''UPDATE notTable
        #                        SET id_post = Null,
        #                        date_post = Null,
        #                        is_sub = False,
        #                        WHERE user_id = {}'''.format(user_id))
        # self.connection.commit()
        # self.cursor.execute('''DELETE * FROM notTable WHERE user_id = {} and domain = {}'''.format(user_id, domain))

    def get_count_sub_pub(self, user_id):
        self.cursor.execute('''SELECT domain FROM notTable WHERE user_id = {}'''.format(user_id))
        return len(self.cursor.fetchall())


    def insert_post_data(self, domain, id_post, date_post):
        self.cursor.execute('''UPDATE notTable
                               SET id_post = {0},
                               date_post = '{1}'
                               WHERE domain = '{2}' '''.format(id_post, date_post, domain))
        self.connection.commit()


    def get_sub_users(self):
        """Получение подписанных пользователей"""
        self.cursor.execute('''SELECT user_id
                               FROM notTable
                               WHERE is_sub=True''')
        return self.cursor.fetchall()


    def get_user_domain(self, user_id):
        self.cursor.execute('''SELECT domain
                               FROM notTable
                               WHERE user_id = '{}' '''.format(user_id))
        return self.cursor.fetchall()


    def get_post(self, user_id):
        """Получаем id_post пользователя"""
        self.cursor.execute('''SELECT id_post
                               FROM notTable
                               WHERE user_id = {}'''.format(user_id))
        return self.cursor.fetchall()


    def set_new_post(self, user_id, id_post, domain):
        self.cursor.execute('''UPDATE notTable
                               SET id_post = {0}
                               WHERE user_id = {1} and domain = '{2}' '''.format(id_post, user_id, domain))
        self.connection.commit()


    def get_domains(self, user_id):
        self.cursor.execute('''SELECT domain
                               FROM notTable
                               WHERE user_id = {}'''.format(user_id))
        return self.cursor.fetchall()


    def get_all_rows(self):
        self.cursor.execute('''SELECT * FROM notTable''')
        return self.cursor.fetchall()


db = Postgers()
# db.set_new_post(1365882584, 466665, "eugeneloveyou")
# rows = db.select_all()
# for row in rows:
#     print(row)


# print(db.get_count_sub_pub(1365882584))
# db.subscribe(1456, 8888, '15:04')
# for user in db.get_sub_users():
#     print(user[0])
# print(db.get_post(1365882584))
# lis = [1,2]

# if isinstance(lis, list):
#     print(2)