import pymysql
from db import DB

'''
table_scheme:

1. recipe

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

# Create recipe table

def create_recipe_table(connection):
    sql = "CREATE TABLE `cocktail_recipes` (" \
        "`id` bigint UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT, " \
        "`cocktail_name` tinytext," \
        "`glass_name` tinytext," \
        "`garnish` tinytext," \
        "`image_url` tinytext," \
        "`howto` mediumtext," \
        "`name_ingredient_0` tinytext," \
        "`name_ingredient_1` tinytext," \
        "`name_ingredient_2` tinytext," \
        "`name_ingredient_3` tinytext," \
        "`name_ingredient_4` tinytext," \
        "`name_ingredient_5` tinytext," \
        "`name_ingredient_6` tinytext," \
        "`name_ingredient_7` tinytext," \
        "`name_ingredient_8` tinytext," \
        "`name_ingredient_9` tinytext," \
        "`name_ingredient_10` tinytext," \
        "`name_ingredient_11` tinytext," \
        "`name_ingredient_12` tinytext," \
        "`name_ingredient_13` tinytext," \
        "`name_ingredient_14` tinytext," \
        "`name_ingredient_15` tinytext," \
        "`unit_ingredient_0` tinytext," \
        "`unit_ingredient_1` tinytext," \
        "`unit_ingredient_2` tinytext," \
        "`unit_ingredient_3` tinytext," \
        "`unit_ingredient_4` tinytext," \
        "`unit_ingredient_5` tinytext," \
        "`unit_ingredient_6` tinytext," \
        "`unit_ingredient_7` tinytext," \
        "`unit_ingredient_8` tinytext," \
        "`unit_ingredient_9` tinytext," \
        "`unit_ingredient_10` tinytext," \
        "`unit_ingredient_11` tinytext," \
        "`unit_ingredient_12` tinytext," \
        "`unit_ingredient_13` tinytext," \
        "`unit_ingredient_14` tinytext," \
        "`unit_ingredient_15` tinytext," \
        "`amount_ingredient_0` decimal(5,3)," \
        "`amount_ingredient_1` decimal(5,3)," \
        "`amount_ingredient_2` decimal(5,3)," \
        "`amount_ingredient_3` decimal(5,3)," \
        "`amount_ingredient_4` decimal(5,3)," \
        "`amount_ingredient_5` decimal(5,3)," \
        "`amount_ingredient_6` decimal(5,3)," \
        "`amount_ingredient_7` decimal(5,3)," \
        "`amount_ingredient_8` decimal(5,3)," \
        "`amount_ingredient_9` decimal(5,3)," \
        "`amount_ingredient_10` decimal(5,3)," \
        "`amount_ingredient_11` decimal(5,3)," \
        "`amount_ingredient_12` decimal(5,3)," \
        "`amount_ingredient_13` decimal(5,3)," \
        "`amount_ingredient_14` decimal(5,3)," \
        "`amount_ingredient_15` decimal(5,3)," \
        "`html` longtext," \
        "`url` tinytext," \
        " PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ; "
    connection.cursor().execute(sql)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()



# establish connection
db = DB()
connection = db.get_connection()

#create_recipe_table(connection)

# write all cocktail_names without image into file
db.check_recipe_without_image()