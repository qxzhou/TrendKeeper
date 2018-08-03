from scrapy import cmdline


cmdline.execute('scrapy crawl mySolution_spider'.split())
cmdline.excute('scrapy crawl mySolution_spider - o test.json')
