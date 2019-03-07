RESOURCE = {
    "CN": "https://www.amazon.cn",
    "JP": "https://www.amazon.co.jp",
    "US": "https://www.amazon.com",
    "UK": "https://www.amazon.co.uk",
    "FR": "https://www.amazon.fr",
    "DE": "https://www.amazon.de",
    "ES": "https://www.amazon.es",
    "IT": "https://www.amazon.it",
    "CA": "https://www.amazon.ca",
    "IN": "https://www.amazon.in",
    "AU": "https://www.amazon.com.au",
    "GB": "https://www.amazon.co.uk"
}


def getAmazonDomain(country):
    return RESOURCE[country.upper()]
