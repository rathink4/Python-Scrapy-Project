import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        # 1. Get all the books on the page by checking the css of the page. Each book is within an <article> tag with an index name = 'product_prod'
        books = response.css('article.product_pod')

        # 2. For each book, we wil explore the book's url and get more details
        for book in books:
            book_page = book.css('h3 a').attrib['href']
            
            if book_page is not None:
                if 'catalogue/' in book_page: 
                    book_page_url = 'http://books.toscrape.com/' + book_page
                else:
                    book_page_url = 'http://books.toscrape.com/catalogue/' + book_page

                yield response.follow(book_page_url, callback=self.parse_book)
        
        # 3. Find the next page button which contains the next page link (eg. catalogue/page2.html)
        next_page = response.css('li.next a').attrib['href']

        # 4. If there is a next_page, then use the follow() method to callback the parse() method in the spider
        if next_page is not None:
            if 'catalogue/' in next_page: 
                next_page_url = 'http://books.toscrape.com/' + next_page
            else:
                next_page_url = 'http://books.toscrape.com/catalogue/' + next_page

            yield response.follow(next_page_url, callback=self.parse)
    
    def parse_book(self, response):
        # We will try to extract the category, description, title, ratings, product type, availability, tax, number of reviews, and price of the book

        # 1. product type and price are in <table> tag so we will get the table rows first
        table_rows = response.css('table tr')

        # 2. return the extracted information
        yield {
            'title': response.css('.product_main h1::text').get(),
            'product_type': table_rows[1].css("td ::text").get(),
            'price_excl_tax': table_rows[2].css("td ::text").get(),
            'price_incl_tax': table_rows[3].css("td ::text").get(),
            'tax': table_rows[4].css("td ::text").get(),
            'availability': table_rows[5].css("td ::text").get(),
            'num_reviews': table_rows[6].css("td ::text").get(),
            'ratings': response.css('p.star-rating').attrib["class"].split(" ")[1],
            'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price': response.css('p.price_color ::text').get()
        }
