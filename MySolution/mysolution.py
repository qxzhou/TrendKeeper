import re
from scrapy import cmdline

start_date = input('please input the starting date(Month dd, yyyy): ')
end_date = input('please input the ending date(Month dd, yyyy): ')
# print(start_date)
# print(end_date)

if re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}$', start_date):
    if re.match(r'^\w{3}\s{1}\d{1,2}\W{1}\s{1}\d{4}$', end_date):
        print(1)
        cmdline.execute('scrapy crawl mySolution_spider'.split())






# def get_start_date():
#     return start_date
#
# def get_end_date():
#     return end_date



# cmdline.execute('scrapy crawl mySolution_spider - o test.json'.split())
