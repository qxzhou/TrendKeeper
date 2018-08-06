# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy.exceptions import CloseSpider
# import re
#
# from datetime import timedelta
# from MySolution.mysolution import get_end_date
# from MySolution.mysolution import get_start_date
from MySolution.items import MysolutionItem

class MysolutionSpiderSpider(scrapy.Spider):
    name = 'mySolution_spider'

    allowed_domains = ['www.newswire.com']

    start_urls = ['https://www.newswire.com/newsroom']

    def parse(self, response):
        for href in response.xpath("//div[@id='ln-container']/div[@class='news-item col-xs-3']/div[@class='ni-container']/a/@href"):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parseSecond)
        next_link = response.xpath("//a[contains(text(),'Next')]/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://www.newswire.com/" + next_link, callback=self.parse)

    def parseSecond(self, response):

        cur_time = datetime.now()

        item_list = response.xpath("//article[@class='press-release']")
        for i_item in item_list:
            mysolution_item = MysolutionItem()
            #generate the category
            category = i_item.xpath("//strong[contains(text(),'Categories:')]/../a//text()").extract_first()
            #handle corner case when category is empty
            if category:
                i_category = " ".join(category.split())
                mysolution_item["category"] = i_category
            else:
                mysolution_item["category"] = ''


            location = i_item.xpath("//strong[@class='date-line color-pr']//text()").extract_first()
            #generate the location
            i_location = "".join(location.split())
            i_location = i_location.split(',')
            for i in range(2):
                del i_location[-1]
            i_location = ", ".join(i_location)
            mysolution_item["location"] = i_location

            mysolution_item["keyword"] = i_item.xpath("//strong[contains(text(),'Tags:')]/../a//text()").extract_first()

            #generate the date
            date = i_item.xpath("//span[@class='status-true']//text()").extract_first()
            i_date = " ".join(date.split())
            i_date = i_date.split(' ')
            del i_date[0]

            i_date = " ".join(i_date)
            mysolution_item["date"] = i_date


            if i_date == "Aug 2, 2018":
                raise CloseSpider('Termination Condition Met')


            '''
            User input coding part
            '''
            # if get_end_date() & get_end_date():
            #     if datetime.strptime(i_date, '%b %d, %Y') <= datetime.strptime(get_end_date(), '%b %d, %Y'):
            #         if datetime.strptime(i_date, '%b %d, %Y') >= datetime.strptime(get_start_date(), '%b %d, %Y'):
            #             mysolution_item["date"] = i_date
            #         else:
            #             raise CloseSpider('Termination Condition Met')
            #
            #     else:
            #         raise CloseSpider('Termination Condition Met')
            # else:
            #     # get date like 'Aug 3, 2018'
            #
            #     if re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}$', i_date):
            #         print(i_date)
            #         time_diff = cur_time - datetime.strptime(i_date, '%b %d, %Y')
            #         mysolution_item["date"] = i_date
            #         if time_diff > timedelta(days=7):
            #             raise CloseSpider('Termination Condition Met')
            #
            #     # get date like 'Aug 3, 2018 10:00'
            #     elif re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}\s{1}\d{1,2}\W{1}\d{1,2}$', i_date):
            #         print(i_date)
            #         i_date = i_date.split(' ')
            #         del i_date[-1]
            #         i_date = " ".join(i_date)
            #         time_diff = cur_time - datetime.strptime(i_date, '%b %d, %Y')
            #         mysolution_item["date"] = i_date
            #         if time_diff > timedelta(days=7):
            #             raise CloseSpider('Termination Condition Met')
            #
            #     # get date like 'Aug 3, 2018 10:00 PDT'
            #     elif re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}\s{1}\d{1,2}\W{1}\d{1,2}\s{1}\w+$', i_date):
            #         print(i_date)
            #         i_date.split(' ')
            #         for i in range(2):
            #             del i_date[-1]
            #         i_date = " ".join(i_date)
            #         time_diff = cur_time - datetime.strptime(i_date, '%b %d, %Y')
            #         mysolution_item["date"] = i_date
            #         if time_diff > timedelta(days=7):
            #             raise CloseSpider('Termination Condition Met')


            yield mysolution_item

