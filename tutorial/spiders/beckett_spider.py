__author__ = 'Tom'

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from tutorial.items import BeckettItem

class BeckettSpider(Spider):
    name = "beckett"
    allowed_domains = ["www.beckett.com"]
    start_urls = [
        "http://www.beckett.com/search/?sport=185226&attr=24470&rowNum=10000&page=1&sort=print_run.desc&tmm=extended&term=1998"
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]

        fileoutput = open(filename, 'a+b')


        selector = Selector(response)
        tableRows = selector.xpath("//table[@id='faceted']//tr")
        becketItems = []

        for tableRow in tableRows:
            item = BeckettItem()

            item['title'] = tableRow.xpath('./td/a/text()').re(".*#.*")
            item['serialNumber'] = tableRow.xpath('./td/text()').re("\d+")
            fileoutput.write(str(item)+"\n")
            #print(str(item))

            #print columns[1]
            #print columns[2]
            #print columns[3]

            #item['title'] = tableRow.xpath('./td[2]/p/span[2]/text()').extract()
            #item['link'] = tableRow.xpath('./td[3]/p/span[2]/text()').extract()
            #item['description'] = tableRow.xpath('./td[4]/p/text()').extract()
            #item['serialNumber'] = tableRow.xpath('./td[4]/p/text()').extract()
            #print str(item)
        fileoutput.close()