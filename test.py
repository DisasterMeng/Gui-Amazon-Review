import requests
from lxml import etree
from dispose import AmazonDispose
from request import AmazonRequests


def test():
    with open('amazon.txt', 'rb') as f:
        data = f.read()
        selector = etree.HTML(data)
        s = selector.xpath('//div[@data-asin]')
        print(s)
        # dispose = AmazonDispose(data, 'US', 'B076MP43X5')
        # print(dispose.dispose())
    # request = AmazonRequests('US', 'B01N2K4U7')
    # print(request.getAmaoznData())
    pass


def test2():
    url = "https://www.amazon.com/product-reviews/B01GW2GH4M/ref=cm_cr_dp_d_show_all_btm"
    querystring = {"ie": "UTF8", "reviewerType": "all_reviews"}
    headers = {
          'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
          'accept-encoding': "gzip, deflate, br",
          'accept-language': "zh-CN,zh;q=0.9",
          'upgrade-insecure-requests': "1",
          'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
          'Host': "www.amazon.com",
          'Cookie': 'session-id=139-9990947-0054464; session-id-time=2082787201l; ubid-main=130-4498879-2446230;'
                    ' x-wl-uid=1DK2hCjGRanOF9SqtLU+cG2jpVaZc8RqqWI0RsdSziAnlhPKPXh9+G6McB8O39ouF0g+rZAAZaHQ=;'
                    ' session-token=4OknvgrkZrGafAYRbufkHpNtHcsN2vzxvk3WsD+LDtMoDH2RvLqahHkcm8H+'
                    'zrZGHqG9J3CX8pWjr5zsQqK0Mymb6tIKy6/JzD4PJCk17uqw5EUQPVnRoB5yyeoLDJbDUNJfx/c4XZVUNqKEqdd4JlvdOOCjTeEfxKqFBjKT4iJlGA+'
                    'TNi7ySJj8oD5Y3lqD; skin=noskin; i18n-prefs=USD; lc-main=zh_CN; sp-cdn="L5Z9: CN"',
        'Connection': "keep-alive"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)


if __name__ == '__main__':
    test2()
