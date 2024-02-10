import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        # 1. Get all the books on the page by checking the css of the page. Each book is within an <article> tag with an index name = 'product_prod'
        books = response.css('article.product_pod')

        # 2. For each book, get the name, price, and the link of the book
        for book in books:
            yield {
                'name': book.css('h3 a').attrib['title'],
                'price': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href']
            }
        
        # 3. Find the next page button which contains the next page link (eg. catalogue/page2.html)
        next_page = response.css('li.next a').attrib['href']

        # 4. If there is a next_page, then use the follow() method to callback the parse() method in the spider
        if next_page is not None:
            if 'catalogue/' in next_page: 
                next_page_url = 'http://books.toscrape.com/' + next_page
            else:
                next_page_url = 'http://books.toscrape.com/catalogue/' + next_page
                
            yield response.follow(next_page_url, callback=self.parse)
