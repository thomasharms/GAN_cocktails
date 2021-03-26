
import datetime
from db import DB
from parser import Parser


class ContentObject:
    id = None
    spider_object = None

    cocktail_name = None
    glass_name = None
    garnish = None
    image_url = None
    howto = None

    name_ingredient_0 = None
    name_ingredient_1 = None 
    name_ingredient_2 = None
    name_ingredient_3 = None
    name_ingredient_4 = None
    name_ingredient_5 = None
    name_ingredient_6 = None
    name_ingredient_7 = None
    name_ingredient_8 = None
    name_ingredient_9 = None
    name_ingredient_10 = None
    name_ingredient_11 = None
    name_ingredient_12 = None
    name_ingredient_13 = None
    name_ingredient_14 = None
    name_ingredient_15 = None
    
    unit_ingredient_0 = None
    unit_ingredient_1 = None
    unit_ingredient_2 = None
    unit_ingredient_3 = None
    unit_ingredient_4 = None
    unit_ingredient_5 = None
    unit_ingredient_6 = None
    unit_ingredient_7 = None
    unit_ingredient_8 = None
    unit_ingredient_9 = None
    unit_ingredient_10 = None
    unit_ingredient_11 = None
    unit_ingredient_12 = None
    unit_ingredient_13 = None
    unit_ingredient_14 = None
    unit_ingredient_15 = None

    amount_ingredient_0 = None
    amount_ingredient_1 = None
    amount_ingredient_2 = None
    amount_ingredient_3 = None
    amount_ingredient_4 = None
    amount_ingredient_5 = None
    amount_ingredient_6 = None
    amount_ingredient_7 = None
    amount_ingredient_8 = None
    amount_ingredient_9 = None
    amount_ingredient_10 = None
    amount_ingredient_11 = None
    amount_ingredient_12 = None
    amount_ingredient_13 = None
    amount_ingredient_14 = None
    amount_ingredient_15 = None

    html = None
    url = None
    
    name_ingredient_set = []
    unit_ingredient_set = []
    amount_ingredient_set = []

    __parser = None
    parser_error = 0
    # 0 = everything fine
    # 1 = no ingredients found
    # 4 = IO error
    # 5 = Parsing process error

    # auxiliary construct to provide better database handling
    __recipe_attribute_list = ["id", "cocktail_name", "howto", "glass_name", "garnish", "url", "html", "image_url",
                                "name_ingredient_0", 
                                "name_ingredient_1", 
                                "name_ingredient_2",
                                "name_ingredient_3",
                                "name_ingredient_4",
                                "name_ingredient_5",
                                "name_ingredient_6",
                                "name_ingredient_7",
                                "name_ingredient_8",
                                "name_ingredient_9",
                                "name_ingredient_10",
                                "name_ingredient_11",
                                "name_ingredient_12",
                                "name_ingredient_13",
                                "name_ingredient_14",
                                "name_ingredient_15",
                                "unit_ingredient_0",
                                "unit_ingredient_1",
                                "unit_ingredient_2",
                                "unit_ingredient_3",
                                "unit_ingredient_4",
                                "unit_ingredient_5",
                                "unit_ingredient_6",
                                "unit_ingredient_7",
                                "unit_ingredient_8",
                                "unit_ingredient_9",
                                "unit_ingredient_10",
                                "unit_ingredient_11",
                                "unit_ingredient_12",
                                "unit_ingredient_13",
                                "unit_ingredient_14",
                                "unit_ingredient_15",
                                "amount_ingredient_0",
                                "amount_ingredient_1",
                                "amount_ingredient_2",
                                "amount_ingredient_3",
                                "amount_ingredient_4",
                                "amount_ingredient_5",
                                "amount_ingredient_6",
                                "amount_ingredient_7",
                                "amount_ingredient_8",
                                "amount_ingredient_9",
                                "amount_ingredient_10",
                                "amount_ingredient_11",
                                "amount_ingredient_12",
                                "amount_ingredient_13",
                                "amount_ingredient_14",
                                "amount_ingredient_15"]

    __required_attribute_list = ["url", "html", "cocktail_name", "amount_ingredient_0", "unit_ingredient_0", "name_ingredient_0"]
    
    # class dictionary is an auxiliary construct to provide better handling for data base purposes
    # as well as data handling in objects
    __attribute_dict = {}

    def __init__(self, spider):
        self.set_spider(spider)
        self.init_parser_object()
        self.parser_error = self.__parser.get_error()

    def set_spider(self, spider):
        self.spider_object = spider

    def get_url(self):
        return self.__url

    def get_recipe_attribute_list(self):
        return self.__recipe_attribute_list

    def set_parser(self, parser):
        self.parser = parser

    def get_attribute_dict(self):
        return self.__attribute_dict

    def set_attribute_dict_value(self, attribute, value):
        self.__attribute_dict[attribute] = value

    # class dictionary is an auxiliary construct to provide better handling for data base purposes
    # as well as data handling in objects
    def build_recipe_class_dictionary(self):
        for x in self.get_recipe_attribute_list():
            # builds a string to look for in the format: _CLASSNAME.__ATTRIBUTENAME
            #att_ref = '_' + self.__class__.__name__ + '__' + x
            
            # combine attribute name and value in a dictionary to be operated by data base queries and other methods
            if hasattr(self, x):
                self.set_attribute_dict_value(x, getattr(self, x))

    def init_parser_object(self):
        self.__parser = Parser(self.spider_object._source)

    # sets attribute values of recipe object from parsed values out of dictionary 
    def set_parsed_recipe_attributes(self):
        
        # parse recipe data
        recipe_data = self.__parser.parse_recipe_data()
        if recipe_data is not False:

            # assign parsed ingredient_sets to values
            self.__assign_ingredient_values(recipe_data['ingredient_set'])
        
            # set object attribute values
            keys = recipe_data.keys()
            for attribute_reference in keys:
                if hasattr(self, attribute_reference):
                    setattr(self, attribute_reference, recipe_data[attribute_reference])

            # download and save images
            self.__save_cocktail_image()

            return True

        else:
            return False

    # download and save cocktail images
    # the actual process is done by spider
    def __save_cocktail_image(self):

        if self.cocktail_name:
            #print('name is ' +  str(self.cocktail_name))
            self.spider_object.save_cocktail_image(self.cocktail_name, self.image_url)


    #ingredient_set is [ingredient1[name, amount, unit], ingredient2[name, amount, unit],...]
    def __assign_ingredient_values(self, ingredient_set):
        
        for count in range(0, len(ingredient_set)):
            
            name_ingredient_item = 'name_ingredient_'+str(count)
            #print("seting attr " + str(name_ingredient_item) + ' to ' +str(name_ingredient_set[count]))
            if hasattr(self, name_ingredient_item):
                setattr(self, name_ingredient_item, ingredient_set[count][0])

            amount_ingredient_item = 'amount_ingredient_'+str(count)
            if hasattr(self, amount_ingredient_item):
                setattr(self, amount_ingredient_item, ingredient_set[count][1])


            unit_ingredient_item = 'unit_ingredient_'+str(count)
            if hasattr(self, unit_ingredient_item):
                setattr(self, unit_ingredient_item, ingredient_set[count][2])

    # set attributes of recipe object
    # build_data_class_dictionary builds dictionary for db class out of object data
    # save dict
    def save_recipe(self):
        
        #parse recipe data out of source
        empty_check = self.set_parsed_recipe_attributes()

        if empty_check:

            # build dictionary to store recipe
            self.build_recipe_class_dictionary()

            # only save if all important attributes are set
            if self.check_required_attributes_set():

                # save recipe into db
                #print(self.__attribute_dict['name_ingredient_0'])
                db = DB()
                db.save_recipe(self.__attribute_dict)

    def check_required_attributes_set(self):
        all_set = True
        for attribute in self.__required_attribute_list:
            if not self.__attribute_dict[attribute]:
                #print(self.__attribute_dict[attribute])
                all_set = False
        return all_set
