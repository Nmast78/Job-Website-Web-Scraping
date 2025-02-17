import scrapy

class LinkedinscraperItem(scrapy.Item):
    tableName = scrapy.Field()
    jobID = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    fullAddress = scrapy.Field()
    extUrl = scrapy.Field()
    fullDescription = scrapy.Field()
