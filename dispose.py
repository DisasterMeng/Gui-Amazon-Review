import re
from lxml import etree

from utils import getAmazonDomain

STARS = r'(\d+)'


class AmazonDispose:
    def __init__(self, AmazonData, Country, ASIN):
        self.Country = Country
        self.ASIN = ASIN
        self.selector = etree.HTML(AmazonData)

    def dispose(self):
        reviewAll = []
        reviewData = self.selector.xpath('//div[@data-hook="review"]')
        if len(reviewData) <= 0:
            return None
        for review in reviewData:
            reviewRow = {}
            reviewDate = review.xpath('div/div/span[@data-hook="review-date"]//text()')
            reviewHref = review.xpath('div/div/div[2]/a[@data-hook="review-title"]/@href')
            reviewTitle = review.xpath('div/div/div[2]/a[@data-hook="review-title"]/span//text()')
            reviewVP = review.xpath('div/div/div[3]/span/a/span[@data-hook="avp-badge"]')
            if reviewVP and len(reviewVP) > 0:
                reviewVP = 'vp'
            else:
                reviewVP = '非vp'
            reviewBuyer = review.xpath('div/div/div[@data-hook="genome-widget"]/a/@href')
            reviewBuyerName = \
                review.xpath('div/div/div[@data-hook="genome-widget"]/a/div[@class="a-profile-content"]/span//text()')
            reviewStars = \
                review.xpath('div/div/div[2]/a[@class="a-link-normal"]/i[@data-hook="review-star-rating"]/@class')
            reviewStars = re.search(STARS, self.getData(reviewStars))
            if reviewStars:
                reviewStars = reviewStars.group(1)
            else:
                reviewStars = ''
            reviewContent = review.xpath('div/div/div[4]/span[@data-hook="review-body"]//text()')
            reviewRow['asin'] = self.ASIN
            reviewRow['date'] = self.getData(reviewDate)
            reviewRow['href'] = self.getURLData(reviewHref)
            reviewRow['title'] = self.getData(reviewTitle)
            reviewRow['vp'] = reviewVP
            reviewRow['buyer'] = self.getURLData(reviewBuyer)
            reviewRow['name'] = self.getData(reviewBuyerName)
            reviewRow['stars'] = reviewStars
            reviewRow['content'] = self.getData(reviewContent)
            reviewAll.append(reviewRow)
        return reviewAll

    def isNextPage(self):
        nextPage = self.selector.xpath('//li[contains(@class, "a-last")]/@class')
        if nextPage and len(nextPage) > 0:
            if 'a-disabled' in nextPage:
                return False
            else:
                return True
        else:
            return False

    def getData(self, data):
        if data and len(data) > 0:
            return data[0]
        else:
            return ''

    def getURLData(self, data):
        if data and len(data) >0:
            return '%s%s' % (getAmazonDomain(self.Country), data[0])
        else:
            return ''
