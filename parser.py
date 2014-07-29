from lxml import etree
from itertools import izip_longest

from config import MONGO_STORAGE_INPUT_DICT
from models import insert

class FParser(object):
    def __init__(self, page, pformat='html'):
        self.data = page.replace('<b>','').replace('</b>','')
        self.data_format = pformat
        self.dom = etree.HTML(self.data)
        self.products_xpath = '//div[@id="products"]'
        self.product_col_xpath = '//div[@class="gd-col gu3"]'
        self.title_path = '//a[@data-tracking-id="prd_title"]/text()'
        self.ratings_path = '//div[@class="pu-rating"]/text()'
        self.price_path = '//span[@class="fk-font-17 fk-bold"]/text()'
        self.product_url = '//a[@data-tracking-id="prd_title"]/@href'

    def __parse(self):
        pass

    def get_all_cols(self, xp):
        prod = self.dom.xpath(self.products_xpath)
        if prod:
            prod = prod[0]
            return prod.xpath(xp) 

    def items(self):
      
        pitems = self.get_all_cols(self.product_col_xpath)
        if pitems:
            titles = [_.strip() for _ in pitems[0].xpath(self.title_path)]
            ratings = pitems[0].xpath(self.ratings_path)
            prices = pitems[0].xpath(self.price_path)
            landing_page_url = pitems[0].xpath(self.product_url)
            #print "name list:",titles
            #print "rating list:",ratings
            #print "price list:",prices
            for i in izip_longest(titles,ratings,prices,landing_page_url):
                yield i
        
        #return products


data = open('out.html','rb').read()
fp = FParser(data)
for i in fp.items():
    if i:
        data_layer = MONGO_STORAGE_INPUT_DICT
        data_layer['name'],data_layer['price'],data_layer['rating'],data_layer['url'] = i
        insert(data_layer)