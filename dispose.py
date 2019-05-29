import re
import time
from lxml import etree

from utils import getAmazonDomain, LANG_CODE, TIME_CODE, STANDARD_TIME

STARS = r'(\d+)'
HELPFUL = r'(\d+)'


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
            reviewStrip = review.xpath('div/div/div[3]/a[@data-hook="format-strip"]//text()')
            reviewVP = review.xpath('div/div/div[3]/span/a/span[@data-hook="avp-badge"]')
            if reviewVP:
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
            reviewHelpful = review.xpath('div/div/div[5]/div/span[@data-hook="review-voting-widget"]'
                                         '/div/span[@data-hook="helpful-vote-statement"]//text()')
            reviewHelpful = re.search(HELPFUL, self.getData(reviewHelpful))
            if reviewHelpful:
                reviewHelpful = reviewHelpful.group(1)
            else:
                reviewHelpful = 0
            reviewContent = review.xpath('div/div/div[4]/span[@data-hook="review-body"]//text()')
            #print(self.get_date(reviewDate))
            reviewRow['asin'] = self.ASIN
            reviewRow['date'] = self.get_date(reviewDate)
            reviewRow['href'] = self.getURLData(reviewHref)
            reviewRow['title'] = self.getData(reviewTitle)
            reviewRow['format'] = self.getData(reviewStrip)
            reviewRow['vp'] = reviewVP
            reviewRow['buyer'] = self.getURLData(reviewBuyer)
            reviewRow['name'] = self.getData(reviewBuyerName)
            reviewRow['stars'] = reviewStars
            reviewRow['content'] = self.getData(reviewContent)
            reviewRow['helpful'] = reviewHelpful
            reviewAll.append(reviewRow)
        return reviewAll

    def isNextPage(self):
        next_page = self.selector.xpath('//li[contains(@class, "a-last")]/@class')
        if next_page:
            if 'a-disabled' in next_page:
                return False
            else:
                return True
        else:
            return False

    def getData(self, data):
        if data:
            return ''.join(data).strip().replace('\n', '')
        else:
            return ''

    def getURLData(self, data):
        if data:
            return '%s%s' % (getAmazonDomain(self.Country), self.getData(data))
        else:
            return ''

    def get_date(self, data):
        date = self.getData(data)
        try:
            date = date.replace(' ', '')
            time_format = TIME_CODE[self.Country]
            if type(time_format) == dict:
                if 'replace' in time_format:
                    date = date.replace(time_format['replace'], '')
                for item in time_format['MapMonth']:
                    date = date.replace(item, time_format['MapMonth'][item])
                time_format = time_format['format']
            time_struct = time.strptime(date, time_format)
            return time.strftime(STANDARD_TIME, time_struct)
        except (TypeError, ValueError, SyntaxError) as e:
            print(e)
            return date

    def is_robot(self):
        robot = self.selector.xpath('//form[@action="/errors/validateCaptcha"]')
        if robot:
            return True
        return False

    def is_lang(self):
        lang = self.selector.xpath('//select[@id="language-type-dropdown"]')
        if not lang:
            return False
        for item in lang:
            param = item.xpath('option[@selected]/@value')
        for (key, value) in LANG_CODE.items():
            if value == self.getData(param) and key == 'CN':
                return True
        return False
