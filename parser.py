import re
import time
import html


class Parser():
    __source = ""
    __decoded_source = ""
    __charset = ""
    __site_validation = True

    ingredient_rows = None
    name_ingredient_set = []
    amount_ingredient_set = []
    unit_ingredient_set = []
    
    # result of [ingredient1[name, amount, unit], ingredient2[name, amount, unit],...]
    ingredient_set = []

    # 0 = everything fine
    # 1 = no cocktail name found
    # 2 = no ingredients
    # 3 = error parsing amounts
    # 6 = error parsing units
    # 4 = IO error
    # 5 = Parsing process error
    __error = 0

    __identifier = {"cocktail_name": r"<h1 class=\"strip__heading\">(.*?)<\/h1>",
                    "url": r"<link rel=\"canonical\" href=\"(.*?)\"(?:.)*?>",
                    "image_url": r"<div class=\"product-gallery-static product-gallery-static--cocktails.*\>\s*<img src=\"(.*?)\".*?>",
                    "glass_name": r"<h3>Serve in a<\/h3> <a.*?\">(.*?)<\/a>",
                    "garnish":r"<h3>Garnish:\n|.*?p>(.*?)<\/p>",
                    "howto":r"<h2>How to make:<\/h2>\s*<p>(.*?)<\/p>",
                    
                    "amount_ingredient":r"<td class=\"no-wrap td-min-width td-align-top pad-right\">\s*(\d+)\s*\w+\s*<\/td>|(<sup.*\/sub>)\s*\w+\s*<\/td>|\s*(\d+\s*<sup.*\/sub>)\s*\w+\s*<\/td>",
                    # 3 different capture groups within tuple
                    # "[(single_value, sup/sub, digit), (...)]"
                    # examples:
                    # single value - 1 drop
                    # sup/sub 1/2 shot
                    # digit 1 shot or 1 1/2 shot... digit is 1
                    
                    "unit_ingredient":r"<td class=\"no-wrap td-min-width td-align-top pad-right\">\s*\d+\s*(\w+?)\s*<\/td>|\s*\d*\s*<sup.*\/sub>\s*(\w+?)\s*<\/td>",
                    # 2 different capture groups within tuple
                    # "[(unit of digits, units of numbers with sup/sub), (...)]"
                    # examples:
                    # unit of digit - 1 drop
                    # units of numbers with sup/sub - 1/2 shot or 3 1/8 shot

                    "name_ingredient":r"<td class=\"td-align-top.*\">\s*(.*?)\s*<\/td>|<td class=\"td-align-top.*\">\s*<a.*\s*(.*?)\s*<\/a>",
                    # 2 different capture groups within tuple
                    # "[(name, name), (...)]"
                    # examples: name is either at position 1 or 2

                    "entries_ingredient":r"<tr>((\s|\S)*?)<\/tr>"

                    }    

    def __init__(self, source):
        self.__source = source
        #print('source is'+str(source))
        self.set_charset_definition()
        if self.__site_validation:
            self.convert_source_due_charset()
            self.unescape_html_entities()
            self.flatten_source()

    def set_charset_definition(self):
        result = re.findall(r'<meta.*charset=(.*?)\">', str(self.__source))
        if result:
            self.__charset = str(result[0])
            self.__site_validation = True
        else: 
            self.__site_validation = False

    def get_charset(self):
        return self.__charset

    def get_error(self):
        return self.__error

    def get_source(self):
        return self.__source

    def get_decoded_source(self):
        return str(self.__decoded_source)

    def convert_source_due_charset(self):
        self.__decoded_source = str(self.__source.decode(self.__charset))

    def convert_resultarray_to_string(self, result):
        if self.check_empty_parser_result(result) is True:
            return str(result[0])
        else:
            return False

    def unescape_html_entities(self):
        self.__decoded_source = html.unescape(self.__decoded_source)

    def check_empty_parser_result(self, result):
        if  len(result) < 1:
            return False
        else:
            return True

    # remove non interesting passages in code
    # only content should be stored
    # 1st: delete script tags, js has no meaingful content
    # 2nd: delete svg tags, no content
    def flatten_source(self):
        try:
            self.__decoded_source = re.sub(r'(<script(?:.|\n)*?\/script>)', "", self.__decoded_source)
            self.__decoded_source = re.sub(r'(<svg(?:.|\n)*?\/svg>)', "", self.__decoded_source)
        except Exception as e:
            print(str(e))

    def parse_cocktail_name(self):
        prog = re.compile(self.__identifier["cocktail_name"], re.MULTILINE)
        cocktail_name = prog.findall(self.__decoded_source)
        if not cocktail_name:
            return False
        else:
            return self.sanitize_cocktail_name(cocktail_name)
            

    # certain chars cannot be within the name since they will appear in the filename of the img
    def sanitize_cocktail_name(self, cocktail_name):
        
        name = self.convert_resultarray_to_string(cocktail_name)
        name = name.replace('/', '')
        name = name.replace('.', '')
        return name

    def parse_image_url(self):
        prog = re.compile(self.__identifier["image_url"], re.MULTILINE)
        image_url = prog.findall(self.__decoded_source)
        return self.convert_resultarray_to_string(image_url)

    def parse_glass_name(self):
        prog = re.compile(self.__identifier["glass_name"], re.MULTILINE)
        glass_name = prog.findall(self.__decoded_source)
        return self.convert_resultarray_to_string(glass_name)

    def parse_garnish(self):
        prog = re.compile(self.__identifier["garnish"], re.MULTILINE)
        garnish = prog.findall(self.__decoded_source)
        return self.convert_resultarray_to_string(garnish)

    def parse_howto(self):
        prog = re.compile(self.__identifier["howto"], re.MULTILINE)
        howto = prog.findall(self.__decoded_source)
        return self.convert_resultarray_to_string(howto)

    def parse_amount_ingredient(self, ingredient_row):
        prog = re.compile(self.__identifier["amount_ingredient"], re.MULTILINE)
        amount_ingredient = prog.findall(ingredient_row)
        #print(amount_ingredient)

        # 3 different capture groups within tuple
        # "[(single_value, sup/sub, digit), (...)]"
            
        if amount_ingredient and type(amount_ingredient[0]) is tuple:
            
            # single value - 1 drop
            if amount_ingredient[0][0]:
                return amount_ingredient[0][0]

            # sup/sub 1/2 shot
            # e.g. "<sup>1</sup>⁄<sub>2</sub>"
            elif amount_ingredient[0][1]:
                return self.parse_float_shots(amount_ingredient[0][1])
                
            # e.g. "1 <sup>1</sup>⁄<sub>2</sub>"
            elif amount_ingredient[0][2]:
                return self.parse_float_shots(amount_ingredient[0][2])

            else:
                amount = 0
                return amount
        

    # compute 2nd parse of amount_ingredient
    def parse_float_shots(self, parsed_phrase):
        result = re.findall(r'(\d)', str(parsed_phrase))
        # only extract numbers
        # length of result is important
        # set of 2 digits [x, y] means x/y as in 1/2 shot
        # set of 3 digits [x, y, z] means x y/z as in 1 1/2 shot

        if len(result) == 3:
            return int(result[0]) + (int(result[1]) / int(result[2]))

        elif len(result) == 2:
            return int(result[0]) / int(result[1])

        else:
            self.__error = 3
            return 0

    def parse_unit_ingredient(self, ingredient_row):
        prog = re.compile(self.__identifier["unit_ingredient"], re.MULTILINE)
        unit_ingredient = prog.findall(ingredient_row)
        
        
        # unit_ingredient is set of tuples in either option: [('x', ''), ('', 'y')]
        if unit_ingredient:
            if unit_ingredient[0][0]:
                return unit_ingredient[0][0]
                
            elif unit_ingredient[0][1]:
                return unit_ingredient[0][1]
                
            else:
                self.__error = 6
                return ""
        

    def parse_name_ingredient(self, ingredient_row):
        prog = re.compile(self.__identifier["name_ingredient"], re.MULTILINE)
        name_ingredient = prog.findall(ingredient_row)
        
        # name_ingredient is set of tuples in either option: [('x', ''), ('', 'y')]
        if name_ingredient[0][0]:
            return name_ingredient[0][0]

        elif (name_ingredient[0][1]):
            return name_ingredient[0][1]
            
        else:
            self.__error = 6
            return ""

    # return set of [ingredient1[name, amount, unit], ingredient2[name, amount, unit],...]
    def parse_ingredient_values(self):

        prog = re.compile(self.__identifier["entries_ingredient"], re.MULTILINE)
        self.ingredient_rows = prog.findall(self.__decoded_source)
        
        for ingredient_row in range (0, len(self.ingredient_rows)-1):
            name = self.parse_name_ingredient(self.ingredient_rows[ingredient_row][0])

            amount = self.parse_amount_ingredient(self.ingredient_rows[ingredient_row][0])
            unit = self.parse_unit_ingredient(self.ingredient_rows[ingredient_row][0])

            result = [name, amount, unit]
            self.ingredient_set.append(result)
        
        return self.ingredient_set

    def parse_recipe_url(self):
        prog = re.compile(self.__identifier["url"], re.MULTILINE)
        url = prog.findall(self.__decoded_source)
        return self.convert_resultarray_to_string(url)

    def parse_recipe_data(self):
        recipe_data = {}
        recipe_data['html'] = self.__decoded_source
        '''with open('data.txt', 'w') as f:
            f.write(self.__decoded_source)
            f.close()'''
        
        recipe_data['cocktail_name'] = self.parse_cocktail_name()
        if recipe_data['cocktail_name'] is not False and self.__site_validation:
            recipe_data['url'] = self.parse_recipe_url()
            recipe_data['image_url'] = self.parse_image_url()
            recipe_data['glass_name'] = self.parse_glass_name()
            recipe_data['garnish'] = self.parse_garnish()
            recipe_data['howto'] = self.parse_howto()
            recipe_data['ingredient_set'] = self.parse_ingredient_values()
            return recipe_data
        else:
            return False