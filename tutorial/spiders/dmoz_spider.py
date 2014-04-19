__author__ = 'Tom'

from scrapy.spider import Spider
from scrapy.selector import Selector

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.beckett.com/search/?sport=185226&attr=24470&rowNum=1000&page=1&sort=print_run.desc&tmm=extended&term=1992",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]

        sel = Selector(response)
        sites = sel.xpath('//ul/li')
        fileoutput = open(filename, 'a+b')
        for site in sites:
            title = site.xpath('a/text()').extract()
            link = site.xpath('a/@href').extract()
            desc = site.xpath('text()').extract()
            print title, link, desc
            output = (title.__str__(), link.__str__(), desc.__str__(), "\n")
            fileoutput.write("items:".join(output))
        fileoutput.close()