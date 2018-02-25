import scrapy

class MainScraper(scrapy.Spider):
    name = "MainScraper"
    start_urls = [
        "https://www.disclosurequest.com/results?sortColumn=&sortDirection=&searchBox=&amountToBeRaisedMin=&amountToBeRaisedMax=&filingDateMin=&filingDateMax=&cikNumber=&page=1"]

    def parse(self, response):
        urls = response.xpath("//tr[@class='detail']/td/div[4]/span[2]/a/@href").extract()
        company_names = response.xpath("//tr[@class='summary']/td[1]/text()").extract()

        for url, company_name in zip(urls, company_names):
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.getURL1, meta={"Company Name": company_name})

        # follow pagination link
        next_page_url = response.css("a.next-page.middle::attr(href)").extract_first()
        # if next_page_url:
        #     next_page_url = response.urljoin(next_page_url)
        #     yield scrapy.Request(url=next_page_url, callback=self.parse)

    def getURL1(self, response):
        company_name = response.meta["Company Name"]
        # url = response.css('iframe#formFrame::attr(src)').extract_first()
        url = response.urljoin(response.xpath("//div[@class='sec-form-page']/label/select/option[2]/@value").extract_first())
        yield scrapy.Request(url=url, callback=self.getURL2, meta={"Company Name": company_name})

    def getURL2(self, response):
        company_name = response.meta["Company Name"]
        url = response.css('iframe#formFrame::attr(src)').extract_first()
        yield scrapy.Request(url=url, callback=self.parse_iframe, meta={"Company Name": company_name})

    def parse_iframe(self, response):
        company_name = response.meta["Company Name"]

        xmlTxt = response.text.split("<TEXT>")[1].split("</TEXT>")[0]


        # cik = response.xpath("//table[@summary='Issuer Identity Information']/tbody/tr[2]/td[1]/a/text()").extract_first()
        # name_of_issuer = response.xpath("//table[@summary='Issuer Identity Information']/tbody/tr[4]/td[1]/text()").extract_first()
        # jurisdiction = response.xpath("//table[@summary='Issuer Identity Information']/tbody/tr[6]/td[1]/text()").extract_first()
        # entity_type = response.xpath("//table[@summary='Table with Multiple boxes']/tr/td[1]/span[text()='X']/../../td[2]/text()").extract_first()



        yield {
            "Entity Type": response.xpath(
                "//table[@summary='Table with Multiple boxes']/tr/td[1]/span[text()='X']/../../td[2]/text()").extract_first(),

            "Company Name": company_name,

            "CIK (Filer ID Number)": response.xpath(
                "//table[@summary='Issuer Identity Information']/tbody/tr[2]/td[1]/a/text()").extract_first(),

            "Name of Issuer": response.xpath(
                "//table[@summary='Issuer Identity Information']/tbody/tr[4]/td[1]/text()").extract_first(),

            "Jurisdiction of Incorporation/Organization": response.xpath(
                "//table[@summary='Issuer Identity Information']/tbody/tr[6]/td[1]/text()").extract_first(),

            "Name of Issuer": response.xpath(
                "//table[@summary='Principal Place of Business and Contact Information']/tbody/tr[2]/td[1]/text()").extract_first(),

            "Street Address 1": response.xpath(
                "//table[@summary='Principal Place of Business and Contact Information']/tbody/tr[4]/td[1]/text()").extract_first(),

            "Street Address 2": response.xpath(
                "//table[@summary='Principal Place of Business and Contact Information']/tbody/tr[4]/td[2]/text()").extract_first(),

            "City": response.xpath(
                "//table[@summary='Principal Place of Business and Contact Information']/tbody/tr[6]/td[1]/text()").extract_first(),

            "State/Province/Country": response.xpath(
                "//table[@summary='Principal Place of Business and Contact Information']/tbody/tr[6]/td[2]/text()").extract_first(),

            "ZIP/PostalCode": response.xpath(
                "//table[@summary='Principal Place of Business and Contact Information']/tbody/tr[6]/td[3]/text()").extract_first(),

            "Phone Number of Issuer": response.xpath(
                "//table[@summary='Principal Place of Business and Contact Information']/tbody/tr[6]/td[4]/text()").extract_first(),

            "Last Name": response.xpath("//table[@summary='Related Persons']/tbody/tr[2]/td[1]/text()").extract(),

            "First Name": response.xpath("//table[@summary='Related Persons']/tbody/tr[2]/td[2]/text()").extract(),

            "Street Address 1": response.xpath(
                "//table[@summary='Related Persons']/tbody/tr[4]/td[1]/text()").extract(),

            "Street Address 2": response.xpath(
                "//table[@summary='Related Persons']/tbody/tr[4]/td[2]/text()").extract(),

            "City": response.xpath("//table[@summary='Related Persons']/tbody/tr[6]/td[1]/text()").extract(),

            "State/Province/Country": response.xpath(
                "//table[@summary='Related Persons']/tbody/tr[6]/td[2]/text()").extract(),

            "ZIP/PostalCode": response.xpath("//table[@summary='Related Persons']/tbody/tr[6]/td[3]/text()").extract(),

            "Revenue Range": response.xpath(
                "//table[@summary='Issuer Size']/tr/td[1]/span[text()='X']/../../td[2]/text()").extract_first(),

            "Aggregate Net Asset Value Range": response.xpath(
                "//table[@summary='Issuer Size']/tr/td[3]/span[text()='X']/../../td[4]/text()").extract_first(),
        }

if __name__ == '__main__':
    app = MainScraper()

"""
scrapy runspider main.py
scrapy runspider main.py -o items.json
more items.json

"""
