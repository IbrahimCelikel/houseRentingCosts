import scrapy

class HepsiemlakspiderSpider(scrapy.Spider):
    name = "hepsiemlakspider"
    allowed_domains = ["www.hepsiemlak.com"]
    # Generate urls with the function
    # Change the "antalya" part of the url to ankara and bursa after Antalya finishes
    start_urls = [f"https://www.hepsiemlak.com/antalya-kiralik/daire?page={str(x)}" for x in range(1,115)]

    # Get the apartment links for each results pages
    def parse(self, response):
        apartments = response.xpath("//a[@class='card-link']/@href").getall()
        for apartment in apartments:
            apartment_url = "https://www.hepsiemlak.com" + apartment
            yield response.follow(apartment_url, callback=self.parse_apartment_url)
    
    # Collecte the required information from the apartment pages
    def parse_apartment_url(self, response):
        # Specs, properties, and description will be taken completely and will be cleaned later (no direct selection)
        specs = []
        for x in range(1, len(response.xpath('//div[@class="spec-groups"]/ul/li').getall())):
            spec_name_xpath = (f'(//div[@class="spec-groups"]/ul/li)[{x}]/span[1]/text()')
            spec_name = response.xpath(spec_name_xpath).get()

            spec_name_result_xpath = (f'(//div[@class="spec-groups"]/ul/li)[{x}]/span/text()')
            spec_name_result = response.xpath(spec_name_result_xpath).getall()[1:]

            specs.append(spec_name)
            specs.append("|??|")
            specs.append(spec_name_result)
            specs.append("|??|")

        properties = []
        for y in range(0, len(response.xpath('//div[@class="properties-column"]/ul/li/text()').getall())-1):
            properties.append(response.xpath('//div[@class="properties-column"]/ul/li/text()').getall()[y])
            properties.append("|??|")

        yield{
            "title" : response.xpath("//div[@class='det-title-upper']//h1/text()").get(),
            "price" : response.xpath("//div[@class='det-title-upper']/div[@class='right']//p[contains(@class,'price')]/text()").get(),
            "city" : response.xpath('//ul[@class="short-property"]//text()').getall()[0],
            "region" : response.xpath('//ul[@class="short-property"]//text()').getall()[2],
            "district" : response.xpath('//ul[@class="short-property"]//text()').getall()[4],
            "specs" : specs,
            "description" : response.xpath('//div[@class="inner-html description"]//text()').getall(),
            "properties" : properties
        }