import pymysql
from db import DB

'''
table_scheme:

1. recipe

id                      BIGINT UNSIGNED
cocktail_title          TINYTEXT

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

insertion           TIMESTAMP
url                 TINYTEXT
html                LONGTEXT

'''

# Create recipe table

def create_reuters_de_article_table(connection):
    sql = "CREATE TABLE `reuters_de_article` (" \
        "`id` bigint UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT, " \
        "`title` longtext," \
        "`header` tinytext," \
        "`sub_header` text," \
        "`article_text` longtext," \
        "`location` tinytext," \
        "`author` tinytext," \
        "`rubricID` smallint(11) UNSIGNED, " \
        "`html` longtext," \
        "`url`text " \
        "`offline_date` INT," \
        "`insertion` timestamp DEFAULT CURRENT_TIMESTAMP," \
        "`modified_date` tinytext," \
        "`creation_date` tinytext," \
        "`last_crawled` timestamp DEFAULT CURRENT_TIMESTAMP," \
        "`tagset` TEXT," \
        " PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ; "
    connection.cursor().execute(sql)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()


def create_REUTERS_DE_outlet_data(connection):
    sql = "INSERT INTO newsoutlets (outlet_name, domain_name, crawling_intervall, url, article_table, parser_class_name) VALUES" \
        " ('REUTERS_DE', 'de.reuters.com', 21200, 'https://de.reuters.com', 'reuters_de_article', 'Parse_REUTERS_DE');"
    connection.cursor().execute(sql)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

def create_REUTERS_DE_rubric_data(connection):
    sql_r = "SELECT id FROM newsoutlets WHERE outlet_name = 'REUTERS_DE'; "
    with connection.cursor() as cursor:
        cursor.execute(sql_r)
        outlet_id = cursor.fetchone()
        id = str(outlet_id['id'])
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Unternehmen', "+id+", 'https://de.reuters.com/news/companies');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Konjunktur', "+id+", 'https://de.reuters.com/news/economics');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Märkte', "+id+", 'https://de.reuters.com/finance/markets');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Marktbericht Deutschland', "+id + \
        ", 'https://de.reuters.com/finance/markets/germany');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Marktbericht USA', "+id+", 'https://de.reuters.com/finance/markets/us');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Marktbericht Asien', "+id + \
        ", 'https://de.reuters.com/finance/markets/asia');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Marktbericht Schweiz', "+id + \
        ", 'https://de.reuters.com/finance/markets/swiss');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Inland', "+id + \
        ", 'https://de.reuters.com/news/domestic');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Ausland', "+id + \
        ", 'https://de.reuters.com/news/world');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Breakingviews', "+id + \
        ", 'https://de.reuters.com/breakingviews');"
    connection.cursor().execute(sql)
    connection.commit()
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! END REUTERS DEUTSCHLAND!!!!!!!!!!!!!!!!!!!!!!!!!!!

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! START REUTERS USA!!!!!!!!!!!!!!!!!!!!!!!!!!!
def create_reuters_us_article_table(connection):
    sql = "CREATE TABLE `reuters_us_article` (" \
        "`id` bigint UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT, " \
        "`title` text," \
        "`header` tinytext," \
        "`sub_header` MEDIUMTEXT," \
        "`article_text` longtext," \
        "`location` tinytext," \
        "`author` tinytext," \
        "`rubricID` smallint(11) UNSIGNED, " \
        "`section` TINYTEXT, " \
        "`html` longtext," \
        "`url` text," \
        "`offline_date` INT," \
        "`insertion` timestamp DEFAULT CURRENT_TIMESTAMP," \
        "`modified_date` tinytext," \
        "`creation_date` tinytext," \
        "`last_crawled` timestamp DEFAULT CURRENT_TIMESTAMP," \
        "`tagset` TEXT," \
        " PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ; "
    connection.cursor().execute(sql)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()


def create_REUTERS_US_outlet_data(connection):
    sql = "INSERT INTO newsoutlets (outlet_name, domain_name, crawling_intervall, url, article_table, parser_class_name) VALUES" \
        " ('REUTERS_US', 'www.reuters.com', 21200, 'https://www.reuters.com', 'reuters_us_article', 'Parse_REUTERS_US');"
    connection.cursor().execute(sql)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

def create_REUTERS_US_rubric_data(connection):
    sql_r = "SELECT id FROM newsoutlets WHERE outlet_name = 'REUTERS_US'; "
    with connection.cursor() as cursor:
        cursor.execute(sql_r)
        outlet_id = cursor.fetchone()
        id = str(outlet_id['id'])
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Business', "+id+", 'https://www.reuters.com/finance');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Legal', "+id+", 'https://www.reuters.com/legal');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Deals', "+id+", 'https://www.reuters.com/finance/deals');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Aerospace Defense', "+id +", 'https://www.reuters.com/subjects/aerospace-and-defense');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Finance', "+id+", 'https://www.reuters.com/subjects/banks');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Autos', "+id +", 'https://www.reuters.com/subjects/autos');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Sustainable Business', "+id +", 'https://www.reuters.com/subjects/sustainable-business');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Markets', "+id +", 'https://www.reuters.com/finance/markets');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('U.S. Markets', "+id +", 'https://www.reuters.com/finance/markets/us');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('European Markets', "+id +", 'https://www.reuters.com/finance/markets/europe');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Asian Markets', "+id +", 'https://www.reuters.com/finance/markets/asia');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('World News', "+id +", 'https://www.reuters.com/news/world');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('U.S. News', "+id +", 'https://www.reuters.com/news/us');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Special Reports', "+id +", 'https://www.reuters.com/subjects/specialReports');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Euro Zone', "+id +", 'https://www.reuters.com/subjects/euro-zone');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Middle East and North Africa', "+id +", 'https://www.reuters.com/subjects/middle-east');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('China', "+id +", 'https://www.reuters.com/places/china');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Japan', "+id +", 'https://www.reuters.com/places/japan');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Mexico', "+id +", 'https://www.reuters.com/places/mexico');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Brazil', "+id +", 'https://www.reuters.com/places/brazil');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Africa', "+id +", 'https://www.reuters.com/places/africa');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Russia', "+id +", 'https://www.reuters.com/places/russia');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('India', "+id +", 'https://www.reuters.com/places/india');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Germany', "+id +", 'https://www.reuters.com/places/germany');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('France', "+id +", 'https://www.reuters.com/places/france');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Italy', "+id +", 'https://www.reuters.com/places/italy');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Iran', "+id +", 'https://www.reuters.com/places/iran');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Greece', "+id +", 'https://www.reuters.com/places/greece');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Turkey', "+id +", 'https://www.reuters.com/places/turkey');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Syria', "+id +", 'https://www.reuters.com/places/syria');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Spain', "+id +", 'https://www.reuters.com/places/spain');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Israel', "+id +", 'https://www.reuters.com/places/israel');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Australia', "+id +", 'https://www.reuters.com/places/australia');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Politics', "+id +", 'https://www.reuters.com/politics');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Supreme Court', "+id +", 'https://www.reuters.com/subjects/supreme-court');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Science', "+id +", 'https://www.reuters.com/news/science');"
    connection.cursor().execute(sql)
    connection.commit()
    sql = "INSERT INTO rubrics (rubric_name, outletID, url) VALUES" \
        " ('Media', "+id +", 'https://www.reuters.com/news/media');"
    connection.cursor().execute(sql)
    connection.commit()
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! END REUTERS USA!!!!!!!!!!!!!!!!!!!!!!!!!!!

# establish connection
outlet_name = "REUTERS_US"
db = DB(outlet_name)
connection = db.get_connection()

#create_rubric_table(connection)
create_outlet_table(connection)

#create_reuters_de_article_table(connection)
create_REUTERS_DE_outlet_data(connection)
create_REUTERS_DE_rubric_data(connection)

#create_reuters_us_article_table(connection)
create_REUTERS_US_outlet_data(connection)
create_REUTERS_US_rubric_data(connection)