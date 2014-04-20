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
        "http://www.beckett.com/search/?sport=185226&attr=24470&rowNum=10000&page=1&sort=print_run.desc&tmm=extended&term=1997"
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]

        fileoutput = open(filename, 'w')

        selector = Selector(response)
        tableRows = selector.xpath("//table[@id='faceted']//tr")
        becketItems = []

        for tableRow in tableRows:
            print "Parsing Row"
            item = BeckettItem()

            """ Getting the whole item description, which we need to cut up, it is a text element which contains a hash"""

            #convert list to string from xpath query and clean any white space off the edges, strip
            itemDescription = ''.join(tableRow.xpath('./td/a/text()').re(".*#.*"))
            print itemDescription

            """Cutting off the year of the product"""

            yearRegEx = re.compile(r'^([\w\-]+)')
            year = yearRegEx.search(itemDescription)

            if year:
                year = year.group()
                print year
                item['year'] = year
            else:
                print "Group was not found for year item:"+itemDescription

            #now we remove the first instance of the year from the item descrption to make further parsing easier
            itemDescription = itemDescription.replace(str(year), "").strip()
            print "Trimmed:"+itemDescription

            """ Cutting off the set name from the item"""

            if "#" in itemDescription:
                hashIndexPosition = itemDescription.index('#');
                if hashIndexPosition >= len(itemDescription):
                    print "we couldn't find th hash!"
                else:
                    #the setname is the first part of the string, without the has
                    setName = itemDescription[0:hashIndexPosition].strip()
                    item['setName'] = setName
                    itemDescription = itemDescription.replace(str(setName), "").strip()
                    print setName
                    print "Trimmed:"+itemDescription
            else:
                print "The hash is not in"+itemDescription

            cardNumberRegEx = re.compile(r'^(#\S+)')
            cardNumber = cardNumberRegEx.search(itemDescription)

            if cardNumber:
                cardNumber = cardNumber.group()
                print cardNumber
                item['cardNumber'] = cardNumber
            else:
                print "Group was not found for card number item:"+itemDescription

            #now we remove the card number from the item descrption to make further parsing easier
            itemDescription = itemDescription.replace(str(cardNumber), "").strip()
            print "Trimmed:"+itemDescription

            """Getting the serial number which is in a sepearte column and is listed as a number on becket"""

            item['serialNumber'] = ''.join(tableRow.xpath('./td/text()').re("\d+"))
            print item['serialNumber']

            fileoutput.write(str(item)+"\n")

        fileoutput.close()