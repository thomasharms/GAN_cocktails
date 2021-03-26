import urllib3
from parser import Parser
import re
'''
import os
path =r'/Users/t/projects/GAN_cocktails/cocktail_recipe_crawler/images'
for root, directories, file in os.walk(path):
	for file in file:
		if not (file.endswith(".jpg")):
			print(os.path.join(root,file))
'''


http = urllib3.PoolManager()
r = http.request('GET', 'https://www.diffordsguide.com/cocktails/recipe/7951/blitz')
with open("./sample_test.txt", "wb") as f:
    f.write(r.data)
f.close()
#print(r.data)

'''
r2 = http.request('GET', 'https://cdn.diffords.com/contrib/stock-images/2021/03/6051d41fb76ae.jpg')
im = r2.data
with open("./images/sample.jpg", "wb") as f:
    f.write(r2.data)
f.close()
#source = r.data
#result = re.findall(r'<meta.*charset=(.*?)\">', str(source))
#print(result)
parser = Parser(r.data)
data = parser.parse_recipe_data()

#print(data['html'])
print(data['cocktail_name'])
print(data['glass_name'])
print(data['garnish'])
print(data['howto'])
print(data['amount_ingredient'])
print(data['unit_ingredient'])
print(data['name_ingredient'])


result = re.findall(r'\d', str('<sup>1</sup>⁄<sub>2</sub>'))
print(result)
'''