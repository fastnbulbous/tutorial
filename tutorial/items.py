# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BeckettItem(Item):
    setName = Field()
    becketLink = Field()
    imageLink = Field()
    description = Field()
    cardNumber = Field()
    serialNumber = Field()
    year = Field()
    errorInformation = Field()
    subsetName = Field()
    team = Field()
    playerNames = Field()
    autograph = Field()
    memorabilia = Field()
    rookieCard = Field()

def __repr__(self):
    return self.__str__()

def __str__(self):
    stringList = ("Set Name:", str(self.setName), " Link:", self.link, " Description:", self.description, " Serial Number:", self.serialNumber, "\n")
    return str("".join(stringList))