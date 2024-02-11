# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

''' 
    - Pipelines.py file is mainly used to process and clean the data which you scraped
    - Anything from removing white spaces, changing prices from pound to dollar, sentence striping, etc.
    - You can also use Pipelines.py to store the data in a database (relational or non-relational way)
'''
class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()

        # 1. Cleaning up white spaces in the propeties except book_item['description']
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        # 2. Changing the category and product type from upper-case to lower-case
        fields_to_lowercase = ['category', 'product_type']
        for field in fields_to_lowercase:
            value = adapter.get(field)
            adapter[field] = value.lower()

        # 3. Changing all the prices to float
        fields_to_float = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for field in fields_to_float:
            value = adapter.get(field)
            value = value.replace('£', '')
            if value != '':
                adapter[field] = float(value)
            else:
                adapter[field] = float(0)
        
        # 4. Extracting the availability as a number rather than a string
        availability_str = adapter.get('availability')
        split_string = availability_str.split("(")
        if len(split_string) < 2:
            adapter['availability'] = 0
        else:
            availability_split = split_string[1].split(' ')
            adapter['availability'] = int(availability_split[0])

        # 5. Reviews should be in number (changing from string)
        num_reviews_str = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_str)

        # 6. Convert star-rating string to number
        star_rating_str = adapter.get('ratings').lower()
        if star_rating_str == 'zero':
            adapter['ratings'] = 0
        elif star_rating_str == 'one':
            adapter['ratings'] = 1
        elif star_rating_str == 'two':
            adapter['ratings'] = 2
        elif star_rating_str == 'three':
            adapter['ratings'] = 3
        elif star_rating_str == 'four':
            adapter['ratings'] = 4
        else:
            adapter['ratings'] = 5



        return item
