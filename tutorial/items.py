# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BeckettItem(Item):
    title = Field()
    link = Field()
    description = Field()
    serialNumber = Field()

def __repr__(self):
    stringList = ("Title:", str(self.title), " Link:", self.link, " Description:", self.description, " Serial Number:", self.serialNumber, "\n")
    return "".join(stringList)