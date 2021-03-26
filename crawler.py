import urllib3
import time
from data_handler import ContentObject

class Crawler:
    _recipe_base_url = 'https://www.diffordsguide.com/cocktails/recipe/'

    _spider_count = 0

    _error = 0
    # 1 - db error
    # 2 - invalid (eg. empty) response

    def __init__(self):
        pass

    def __del__(self):
        pass

    def _decode_url_bytestostring(self, url):
        if type(url) is bytes and url:
            return bytes.decode(url, 'ascii')
        elif type(url) is str and url:
            return url
        else:
            return False

    def crawl_single_site(self):
        site = 'http://www.diffordsguide.com/cocktails/recipe/10/'
        spider = self.sent_spider(site)
        recipe_data_object = ContentObject(spider)
        recipe_data_object.save_recipe()

    def crawl_sites(self):
        
        count = 4766
        
        while count < 9999:
            prefix = str(count)+'/'
            site_to_crawl = self._recipe_base_url + prefix

            print('Crawling Site ' +str(site_to_crawl))

            spider = self.sent_spider(site_to_crawl)
            
            # call data object
            recipe_data_object = ContentObject(spider)
            recipe_data_object.save_recipe()

            print ('Done saving '+str(site_to_crawl))
            time.sleep(5)
            count+=1

    def sent_spider(self, site_to_crawl):
        spider = Spider(site_to_crawl)
        spider = spider.start_spider()
        return spider

    def check_result(self, spider):
        
        valid_Result = True
        
        if spider.get_error != 0:
            valid_Result = False
        
        return valid_Result


class Spider:
    __image_folder = './cocktail_recipe_crawler/images/'
    _url = ""
    _source = ""
    _response = None
    _Pool_Manager = None
    _error = 0
    # error=0 -> OK
    # error=1 -> no source or response
    # error=2 -> no url given
    # error=4 -> site crawled already
    # error=5 -> IO Error
    # error=9 -> other error

    def __init__(self, url):
        self._set_url(url)
        self._set_Pool_Manager()

    def __del__(self):
        pass

    def get_url(self):
        return self._url

    def _set_url(self, url):
        if url:
            self._url = url
        else:
            self._error = 2

    def _set_Pool_Manager(self):
        self._Pool_Manager = urllib3.PoolManager()

    def get_source(self):
        return self._source

    def get_error(self):
        return self._error

    # download the cocktail picture and save it
    def save_cocktail_image(self, cocktail_name, image_url):
        if cocktail_name and image_url:
            response = self._Pool_Manager.request('GET', image_url)

            file_location = self.__image_folder + cocktail_name + '.jpg'
            with open(file_location, "wb") as f:
                f.write(response.data)
            f.close()
            print ('Done saving '+str(cocktail_name))

    # main function usable by the outer world
    # needed variables will be set by init functions or on the way
    # only used by crawler
    def start_spider(self):
        
                #print('url is '+str(self._url))
                self._response = self._Pool_Manager.request('GET', self._url)
                if self._response.status != 200:
                    self._error = 1
                else:
                    self._source = self._response.data
                #print(self._source)
                '''
        except IOError as e:
            self._error = 5
            print(str(e))
        except ValueError as e:
            self._error = 1
            print(str(e))
        except Exception as e:
            self._error = 9
            print(str(e))
            '''
                return self

c = Crawler()
c.crawl_sites()
#c.crawl_single_site()