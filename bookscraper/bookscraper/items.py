# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# You can clean the data this way in the Items.py file but it is better to clean it in the Pipelines.py file
def price_serializer(value):
    return f'$ {str(value)}'


class BookItem(scrapy.Item):
    title = scrapy.Field()
    product_type =  scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    ratings = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()