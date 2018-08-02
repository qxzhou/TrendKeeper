# -*- coding: utf-8 -*-
import scrapy
from MySolution.items import MysolutionItem


class MysolutionSpiderSpider(scrapy.Spider):

    name = 'mySolution_spider'

    allowed_domains = ['www.newswire.com']

    start_urls = ['https://www.newswire.com/newsroom']

    def parse(self, response):
        for href in response.xpath("//div[@id='ln-container']/div[@class='news-item col-xs-3']/div[@class='ni-container']/a/@href"):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parseSecond)
        next_link = response.xpath("//div[class='chunkination chunkination-centered']/ul[3]/li/a/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://www.newswire.com" + next_link, callback=self.parse)


    def parseSecond(self, response):
        item_list = response.xpath("//article[@class='press-release']")
        for i_item in item_list:
            mysolution_item = MysolutionItem()
            mysolution_item["category"] = i_item.xpath("//strong[contains(text(),'Categories:')]/../a//text()").extract()
            location = i_item.xpath("//strong[@class='date-line color-pr']//text()").extract_first()
            #generate the location list
            i_location = "".join(location.split())
            i_location = i_location.split(',')
            for i in range(2):
                del i_location[-1]
            # mysolution_item["location"] = ", ".join(i_location)
            mysolution_item["location"] = i_location

            mysolution_item["keyword"] = i_item.xpath("//strong[contains(text(),'Tags:')]/../a//text()").extract_first()
            yield mysolution_item

