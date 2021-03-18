import pymysql
import time, datetime

'''
table_scheme:

id                      BIGINT UNSIGNED
cocktail_name           TINYTEXT

name_ingeredient_1      TINYTEXT
name_ingeredient_2      TINYTEXT
name_ingeredient_3      TINYTEXT
name_ingeredient_4      TINYTEXT
name_ingeredient_5      TINYTEXT
name_ingeredient_6      TINYTEXT
name_ingeredient_7      TINYTEXT
name_ingeredient_8      TINYTEXT
name_ingeredient_9      TINYTEXT
name_ingeredient_10     TINYTEXT
name_ingeredient_11     TINYTEXT
name_ingeredient_12     TINYTEXT
name_ingeredient_13     TINYTEXT
name_ingeredient_14     TINYTEXT
name_ingeredient_15     TINYTEXT
unit_ingeredient_1      TINYTEXT
unit_ingeredient_2      TINYTEXT
unit_ingeredient_3      TINYTEXT
unit_ingeredient_4      TINYTEXT
unit_ingeredient_5      TINYTEXT
unit_ingeredient_6      TINYTEXT
unit_ingeredient_7      TINYTEXT
unit_ingeredient_8      TINYTEXT
unit_ingeredient_9      TINYTEXT
unit_ingeredient_10     TINYTEXT
unit_ingeredient_11     TINYTEXT
unit_ingeredient_12     TINYTEXT
unit_ingeredient_13     TINYTEXT
unit_ingeredient_14     TINYTEXT
unit_ingeredient_15     TINYTEXT
amount_ingeredient_1    TINYTEXT
amount_ingeredient_2    TINYTEXT
amount_ingeredient_3    TINYTEXT
amount_ingeredient_4    TINYTEXT
amount_ingeredient_5    TINYTEXT
amount_ingeredient_6    TINYTEXT
amount_ingeredient_7    TINYTEXT
amount_ingeredient_8    TINYTEXT
amount_ingeredient_9    TINYTEXT
amount_ingeredient_10   TINYTEXT
amount_ingeredient_11   TINYTEXT
amount_ingeredient_12   TINYTEXT
amount_ingeredient_13   TINYTEXT
amount_ingeredient_14   TINYTEXT
amount_ingeredient_15   TINYTEXT
'''

# !!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!DATA IS FETCHED INTO BYTES FORMAT.... needs to be converted to string!!!!!!!!!!!!!!!!!!!!!!!!

class DB:
    _server_name = "localhost"
    _user_name = "root"
    _pw = "ABcd1234!"

    _db_name = "cocktails"
    _recipe_table_name = "recipe"

    _connection = 0
    # seems like cursor needs to be reassigned after/before every operation
    _cursor = 0
    
    _crawling_intervall = 0
    _url = ""
    _error = 0
    # 0 everything seems to be fine
    # 1 domain does not exist
    # 2 IOERROR
    # 3 no recipe found
    # 9 some other error

    def __init__(self, outlet_name):
        self.establish_connection()

    def __del__(self):
        self.close_connection()

    def get_connection(self):
        return self._connection

    def get_error(self):
        return self._error

    def get_url(self):
        return self._url

    def get_crawling_intervall(self):
        return self._crawling_intervall

    def establish_connection(self):
        self._connection = pymysql.connect(host=self._server_name,
                                            user=self._user_name,
                                            password=self._pw,
                                            db=self._db_name,
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor)

    def set_cursor(self):
        self.__cursor = self._connection.cursor()

    def get_cursor(self):
        return self.__cursor

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    def connection_commit(self):
        self.__connection.commit()

    def close_connection(self):
        self.__connection.close()

    # checks if data returned by database is valid
    def response_error_handle(self, db_response):
        try:
            if db_response is not None or db_response:
                return db_response
            else:
                return False
        except ValueError:
            self.__error = 3
        except IOError:
            self.__error = 2
        except:
            self.__error = 9

    def delete_article(self, recipe_id):
        self.set_cursor()
        try:
            with self.__cursor:
                sql = "DELETE FROM %s where id = %d ;" % (self._recipe_table_name, recipe_id)
                print(sql)
                self._cursor.execute(sql)
                self._connection.commit()
        except Exception as e:
            print(str(e))
        finally:
            return

    def check_recipe_stored_already(self, url):
        self.set_cursor()
        stored = False
        try:
            with self.__cursor:

                sql = "SELECT id FROM " + self.__article_table + " WHERE url = %s;"

                self.__cursor.execute(sql, url)
                idset = self.__cursor.fetchall()
                if len(idset) > 0:
                    stored = True
                return stored
        finally:
            return stored

    def delete_duplicate_entries(self):
        self.set_cursor()
        try:
            with self.__cursor:
                sql = "DELETE t1 FROM " + self._recipe_table + " t1 INNER JOIN " + self.__article_table + " t2 WHERE t1.id < t2.id AND t1.url = t2.url;"
                self._cursor.execute(sql)
                self._connection.commit()
        except Exception as e:
            print(str(e))

            




    # expecting data_dict as dictionary of {attribute_name, value}
    def save_article(self, data_dict):
        self.set_cursor()
        
        count = 0
        attribute_names = data_dict.keys()
        max_count = len(attribute_names) - 1

        sql = "INSERT INTO " + self.__article_table + " ("

        # build the chain of keys
        for key in attribute_names:
            if count == max_count:
                sql = sql + key + ") "
            elif count < max_count:
                sql = sql + key + ", "
                count += 1

        # build intermezzo
        sql = sql + " VALUES ("

        # build the chain of values
        count = 0
        for key in attribute_names:

            if count < max_count:
                sql = sql + " %s, "
                count += 1
            elif count == max_count:
                sql = sql + "%s); "
        
        # execute insertion
        value_tuple = tuple(data_dict.values())
        value_list = []
        value_list.append(value_tuple)
        try:
            with self._cursor:
                self._cursor.execute(sql, *value_list)
                self.connection_commit()
        except Exception as e:
            print(str(e))