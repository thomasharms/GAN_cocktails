import pymysql
import time, datetime

'''
table_scheme:

id                      BIGINT UNSIGNED
cocktail_name           TINYTEXT
glass_name              TINYTEXT
garnish                 TINYTEXT
image_url               TINYTEXT
howto                   MEDIUMTEXT

name_ingredient_0      TINYTEXT
name_ingredient_1      TINYTEXT
name_ingredient_2      TINYTEXT
name_ingredient_3      TINYTEXT
name_ingredient_4      TINYTEXT
name_ingredient_5      TINYTEXT
name_ingredient_6      TINYTEXT
name_ingredient_7      TINYTEXT
name_ingredient_8      TINYTEXT
name_ingredient_9      TINYTEXT
name_ingredient_10     TINYTEXT
name_ingredient_11     TINYTEXT
name_ingredient_12     TINYTEXT
name_ingredient_13     TINYTEXT
name_ingredient_14     TINYTEXT
name_ingredient_15     TINYTEXT
unit_ingredient_0      TINYTEXT
unit_ingredient_1      TINYTEXT
unit_ingredient_2      TINYTEXT
unit_ingredient_3      TINYTEXT
unit_ingredient_4      TINYTEXT
unit_ingredient_5      TINYTEXT
unit_ingredient_6      TINYTEXT
unit_ingredient_7      TINYTEXT
unit_ingredient_8      TINYTEXT
unit_ingredient_9      TINYTEXT
unit_ingredient_10     TINYTEXT
unit_ingredient_11     TINYTEXT
unit_ingredient_12     TINYTEXT
unit_ingredient_13     TINYTEXT
unit_ingredient_14     TINYTEXT
unit_ingredient_15     TINYTEXT
amount_ingredient_0    DECIMAL(5, 3)
amount_ingredient_1    DECIMAL(5, 3)
amount_ingredient_2    DECIMAL(5, 3)
amount_ingredient_2    DECIMAL(5, 3)
amount_ingredient_3    DECIMAL(5, 3)
amount_ingredient_4    DECIMAL(5, 3)
amount_ingredient_5    DECIMAL(5, 3)
amount_ingredient_6    DECIMAL(5, 3)
amount_ingredient_7    DECIMAL(5, 3)
amount_ingredient_8    DECIMAL(5, 3)
amount_ingredient_9    DECIMAL(5, 3)
amount_ingredient_10   DECIMAL(5, 3)
amount_ingredient_11   DECIMAL(5, 3)
amount_ingredient_12   DECIMAL(5, 3)
amount_ingredient_13   DECIMAL(5, 3)
amount_ingredient_14   DECIMAL(5, 3)
amount_ingredient_15   DECIMAL(5, 3)

html                    LONGTEXT
url                     TINYTEXT
'''

# !!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!DATA IS FETCHED INTO BYTES FORMAT.... needs to be converted to string!!!!!!!!!!!!!!!!!!!!!!!!

class DB:
    _server_name = "localhost"
    _user_name = "root"
    _pw = "ABcd1234!"

    _db_name = "cocktails"
    _recipe_table_name = "cocktail_recipes"

    _connection = 0
    # seems like cursor needs to be reassigned after/before every operation
    _cursor = 0
    
    # most likely not relevant, since only done once
    _crawling_intervall = 0

    _error = 0
    # 0 everything seems to be fine
    # 1 domain does not exist
    # 2 IOERROR
    # 3 no recipe found
    # 9 some other error

    def __init__(self):
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
        self._cursor = self._connection.cursor()

    def get_cursor(self):
        return self._cursor

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    def connection_commit(self):
        self._connection.commit()

    def close_connection(self):
        self._connection.close()

    # checks if data returned by database is valid
    def response_error_handle(self, db_response):
        try:
            if db_response is not None or db_response:
                return db_response
            else:
                return False
        except ValueError:
            self._error = 3
        except IOError:
            self._error = 2
        except:
            self._error = 9

    def delete_recipe(self, recipe_id):
        self.set_cursor()
        try:
            with self.__cursor:
                sql = "DELETE FROM %s where id = %d ;" % (self._recipe_table_name, recipe_id)
                
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
            with self._cursor:

                sql = "SELECT id FROM " + self._recipe_table_name + " WHERE url = %s;"

                self._cursor.execute(sql, url)
                idset = self._cursor.fetchall()
                if len(idset) > 0:
                    stored = True
                return stored
        finally:
            return stored

    def delete_duplicate_entries(self):
        self.set_cursor()
        try:
            with self._cursor:
                sql = "DELETE t1 FROM " + self._recipe_table_name + " t1 INNER JOIN " + self._recipe_table_name + " t2 WHERE t1.id < t2.id AND t1.url = t2.url;"
                self._cursor.execute(sql)
                self._connection.commit()
        except Exception as e:
            print(str(e))

    # get a list of recipes without an image
    # write the names of those recipes in a file
    def check_recipe_without_image(self):
        self.set_cursor()

        try:
            with self._cursor:
                sql = "SELECT cocktail_name from cocktail_recipes where image_url not like '%.jpg';";

                self._cursor.execute(sql)
                result_set = self._cursor.fetchall()

                if type(result_set) is list:
                    
                    with open("./cocktail_names_without_image.txt", "wb") as f:
                        
                        for name in result_set:
                            name_as_bytes = str.encode(name['cocktail_name'] + '\n')
                            f.write(name_as_bytes)
                    f.close()
                    
        except Exception as e:
            print(str(e))
        

    # expecting data_dict as dictionary of {attribute_name, value}
    def save_recipe(self, data_dict):
        self.set_cursor()
        
        count = 0
        attribute_names = data_dict.keys()
        max_count = len(attribute_names) - 1

        sql = "INSERT INTO " + self._recipe_table_name + " ("

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