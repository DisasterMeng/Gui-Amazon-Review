import re
from lxml import etree

STARS = r'(\d+)'
NEED = ('asin', 'date', 'title', 'name', 'stars', 'buyer', 'href', 'content')


class AmazonDispose:
    def __init__(self, AmazonData, ASIN):
        self.ASIN = ASIN
        self.AmazonData = AmazonData

    def dispose(self):
        selector = etree.HTML(self.AmazonData)
        reviewData = selector.xpath('//div[@data-hook="review"]')
        reviewAll = []
        for review in reviewData:
            reviewRow = {}
            reviewDate = review.xpath('div/div/span[@data-hook="review-date"]//text()')
            reviewHref = review.xpath('div/div/div[2]/a[@data-hook="review-title"]/@href')
            reviewTitle = review.xpath('div/div/div[2]/a[@data-hook="review-title"]/span//text()')
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
            reviewContent = review.xpath('div/div/div[4]/span[@data-hook="review-body"]/span//text()')
            reviewRow.asin = self.ASIN
            reviewRow.date = self.getData(reviewDate)
            reviewRow.href = self.getData(reviewHref)
            reviewRow.title = self.getData(reviewTitle)
            reviewRow.buyer = self.getData(reviewBuyer)
            reviewRow.name = self.getData(reviewBuyerName)
            reviewRow.stars = reviewStars
            reviewRow.content = self.getData(reviewContent)
            reviewAll.append(reviewRow)
        return reviewAll

    def getData(self, data):
        if data and len(data) > 0:
            return data[0]
        else:
            return ''
