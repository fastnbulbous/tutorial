__author__ = 'Tom'

import re
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from tutorial.items import BeckettItem

import logging
logging.basicConfig(filename='parsing.log',level=logging.DEBUG)

class BeckettSpider(Spider):
    name = "beckett"
    allowed_domains = ["www.beckett.com"]
    start_urls = [
        "http://www.beckett.com/search/?sport=185226&attr=24470&rowNum=250&page=1&sort=print_run.desc&tmm=extended&term=1998%20van%20horn"
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

            #cache the raw item description as we are going to be parsing it and splicing it up
            originalItemDescription = itemDescription
            print originalItemDescription
            logging.info("Parsing item description: "+originalItemDescription)

            if len(itemDescription) < 2:
               logging.warn("this item was not long enough and is missing info: " + originalItemDescription)
               continue #continue the for loop of elements as this is not enough info to pass

            """Cutting off the year of the product"""

            yearRegEx = re.compile(r'^([\w\-]+)')
            year = yearRegEx.search(itemDescription)

            if year:
                year = year.group()
                print year
                item['year'] = year
            else:
                logging.error("We could not determine the year for the item:"+itemDescription)
                continue #continue the for loop of elements as this is not enough info to pass

            #now we remove the first instance of the year from the item descrption to make further parsing easier
            itemDescription = itemDescription.replace(str(year), "").strip()
            print "Trimmed:"+itemDescription

            """ Cutting off the set name from the item"""

            if "#" in itemDescription:
                hashIndexPosition = itemDescription.index('#');
                if hashIndexPosition >= len(itemDescription):
                    logging.error("There was no hash in this item to help determine the card number:"+itemDescription)
                    continue #continue the for loop of elements as this is not enough info to pass
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
                logging.error("We could not find a card number for this item:"+itemDescription)
                continue #continue the for loop of elements as this is not enough info to pass

            #now we remove the card number from the item descrption to make further parsing easier
            itemDescription = itemDescription.replace(str(cardNumber), "").strip()
            print "Trimmed:"+itemDescription

            errorCount = itemDescription.count("UER")

            if errorCount > 0:
                errorDescriptions = itemDescription.split("UER")
                if errorCount == 1:
                    #the card has error info is on the second one
                    errorDescription = "Error: "+errorDescriptions[1]
                    #remove the error description code and text from the item description
                    itemDescription = itemDescription.replace("UER", "").strip()
                    itemDescription = itemDescription.replace(errorDescription, "").strip()
                    item['errorInformation'] = errorDescription
                    print errorDescription
                    print "Trimmed: " + itemDescription;
                else:
                    logging.error("We had an unecpexted number of UER error stetes for a card"+itemDescription)
                    continue #continue the for loop of elements as this is not enough info to pass

            """Getting the serial number which is in a sepearte column and is listed as a number on becket"""

            item['serialNumber'] = ''.join(tableRow.xpath('./td/text()').re("\d+"))

            try:
                serialNumber = int(item['serialNumber'])
            except:
                 # the serial number is not a number and is empty. mark this item for inverstigation
                logging.warn("There is no serial number listed for this item"+originalItemDescription)

            fileoutput.write(str(item)+"\n")

        fileoutput.close()