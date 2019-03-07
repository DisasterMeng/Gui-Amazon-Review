import requests
from fake_useragent import UserAgent

from utils import getAmazonDomain

REVIEWSURL = '{domain}/product-reviews/{asin}?reviewerType=all_reviews&pageNumber={page}&sortBy=recent&pageSize=50'


class AmazonRequests:
    def __init__(self, Country, ASIN):
        self.ASIN = ASIN
        self.Country = Country
        self.page = 1
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": UserAgent().random,
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "upgrade-insecure-requests": "1"
        }

    def getURL(self):
        return REVIEWSURL.format(domain=getAmazonDomain(self.Country), asin=self.ASIN, page=self.page)

    def nextPage(self):
        self.page += 1

    def getAmaoznData(self):
        try:
            response = requests.get(self.getURL(), headers=self.headers, timeout=(5, 10))
            response.encoding = 'utf-8'
            return response.text
        except requests.exceptions.RequestException as e:
            print(e)
