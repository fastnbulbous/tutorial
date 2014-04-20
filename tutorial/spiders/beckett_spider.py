__author__ = 'Tom'

import re
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from tutorial.items import BeckettItem

class BeckettSpider(Spider):
    name = "beckett"
    allowed_domains = ["www.beckett.com"]
    start_urls = [
        "http://www.beckett.com/search/?sport=185226&attr=24470&rowNum=100&page=1&sort=print_run.desc&tmm=extended&term=1998"
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]

        fileoutput = open(filename, 'w')

        selector = Selector(response)
        tableRows = selector.xpath("//table[@id='faceted']//tr")
        becketItems = []

        for tableRow in tableRows:
            item = BeckettItem()

            #convert list to string from xpath query
            itemDescription = ''.join(tableRow.xpath('./td/a/text()').re(".*#.*"))
            print itemDescription

            yearRegEx = re.compile(r'^([\w\-]+)')
            year = yearRegEx.search(itemDescription)

            if year:
                year = year.group()

            print year
            item['year'] = year
            item['serialNumber'] = ''.join(tableRow.xpath('./td/text()').re("\d+"))

            fileoutput.write(str(item)+"\n")

        fileoutput.close()