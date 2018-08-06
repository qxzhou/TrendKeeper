from scrapy import cmdline


# start_date = input('please input starting date: ')
# end_date = input('please input ending date: ')

cmdline.execute('scrapy crawl mySolution_spider -o test.json -t json'.split())




# def get_start_date():
#     return start_date
#
# def get_end_date():
#     return end_date



