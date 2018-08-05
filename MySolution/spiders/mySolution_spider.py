# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy.exceptions import CloseSpider
import pytz
import re

# from datetime import timedelta
# from pytz import timezone
# from MySolution.mysolution import start_date
# from MySolution.mysolution import end_date

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

        # month = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6',
        #          'Jul': '7', 'Aug': '8', 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

        # fmt = "%b %d, %Y %H:%M %Z"

        cur_time = datetime.now()
        cur_utc = datetime.now(pytz.utc)

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
            #Change month from characters to numbers
            # i_date[0] = month[i_date[0]]
            # #formatting date
            # i_date[1] = i_date[1].strip(',')
            i_date = " ".join(i_date)
            mysolution_item["date"] = i_date


            if i_date == "Aug 1, 2018":
            # if i_date[:3] == ['8','2', '2018']:
                raise CloseSpider('Termination Condition Met')

            # if re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}$', start_date):
            #     if re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}$', end_date):
            #
            #         if datetime.strptime(i_date, '%b %d, %Y') <= datetime.strptime(end_date(), '%b %d, %Y'):
            #             if datetime.strptime(i_date, '%b %d, %Y') >= datetime.strptime(start_date(), '%b %d, %Y'):
            #                mysolution_item["date"] = i_date
            #             else:
            #                 raise CloseSpider('Termination Condition Met')
            #
            #         else:
            #             raise CloseSpider('Termination Condition Met')




            # # get date like 'Aug 3, 2018'
            #
            # if re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}$', i_date):
            #     print(i_date)
            #     time_diff = cur_time - datetime.strptime(i_date, '%b %d, %Y')
            #     if time_diff > timedelta(days=7):
            #         raise CloseSpider('Termination Condition Met')
            #
            # # get date like 'Aug 3, 2018 10:00'
            # elif re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}\s{1}\d{1,2}\W{1}\d{1,2}$', i_date):
            #     print(i_date)
            #     time_diff = cur_time - datetime.strptime(i_date, '%b %d, %Y %H:%M')
            #     if time_diff > timedelta(days=7):
            #         raise CloseSpider('Termination Condition Met')
            #
            # # get date like 'Aug 3, 2018 10:00 PDT'
            # elif re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}\s{1}\d{1,2}\W{1}\d{1,2}\s{1}\w+$', i_date):
            #     print(i_date)
            #
            #     time = datetime.strptime(i_date, '%b %d, %Y %H:%M %Z')
            #     eastern_time = time.astimezone(timezone('US/Eastern'))
            #     time_diff = cur_utc - eastern_time
            #     if time_diff > timedelta(days=7):
            #         raise CloseSpider('Termination Condition Met')

            yield mysolution_item

