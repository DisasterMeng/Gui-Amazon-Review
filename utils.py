import winreg

RESOURCE = {
    'US': 'https://www.amazon.com',
    'AE': 'https://www.amazon.ae',
    'CN': 'https://www.amazon.cn',
    'JP': 'https://www.amazon.co.jp',
    'UK': 'https://www.amazon.co.uk',
    'FR': 'https://www.amazon.fr',
    'DE': 'https://www.amazon.de',
    'ES': 'https://www.amazon.es',
    'IT': 'https://www.amazon.it',
    'CA': 'https://www.amazon.ca',
    'IN': 'https://www.amazon.in',
    'AU': 'https://www.amazon.com.au',
    'GB': 'https://www.amazon.co.uk',
    'MX': 'https://www.amazon.com.mx'
    # 'SG': 'https://www.amazon.com.sg'
}

LANG_CODE = {
    'CN': 'zh_CN',
    'US': 'en_US'
}

FR_MONTH = {
    "janvier": "January",
    "février": "February",
    "mars": "March",
    "avril": "April",
    "mai": "May",
    "juin": "June",
    "juillet": "July",
    "août": "August",
    "septembre": "September",
    "octobre": "October",
    "novembre": "November",
    "décembre": "December"
}

MX_MONTH = ES_MONTH = {
    "enero": "January",
    "febrero": "February",
    "marzo": "March",
    "abril": "April",
    "mayo": "May",
    "junio": "June",
    "julio": "July",
    "agosto": "August",
    "septiembre": "September",
    "octubre": "October",
    "noviembre": "November",
    "diciembre": "December"
}

IT_MONTH = {
    "gennaio": "January",
    "febbraio": "February",
    "marzo": "March",
    "aprile": "April",
    "maggio": "May",
    "giugno": "June",
    "luglio": "July",
    "agosto": "August",
    "settembre": "September",
    "ottobre": "October",
    "novembre": "November",
    "dicembre": "December"
}

DE_MONTH = {
    "Januar": "January",
    "Februar": "February",
    "März": "March",
    "April": "April",
    "Mai": "May",
    "Juni": "June",
    "Juli": "July",
    "August": "August",
    "September": "September",
    "Oktober": "October",
    "November": "November",
    "Dezember": "December"
}

TIME_CODE = {
    'US': '%B%d,%Y',
    'AE': '%B%d,%Y',
    'CN': '%Y年%m月%d日',
    'JP': '%Y年%m月%d日',
    'UK': '%d%B%Y',
    'FR': {'MapMonth': FR_MONTH, 'format': '%d%B%Y'},
    'DE': '%d.%B%Y',
    'ES': {'MapMonth': ES_MONTH, 'format': '%d%B%Y', 'replace': 'de'},
    'IT': {'MapMonth': IT_MONTH, 'format': '%d%B%Y'},
    'CA': '%B%d,%Y',
    'IN': '%d%B%Y',
    'AU': '%d%B%Y',
    'GB': '%d%B%Y',
    'MX': {'MapMonth': MX_MONTH, 'format': '%d%B%Y', 'replace': 'de'}
    # 'SG': 'https://www.amazon.com.sg'
}

STANDARD_TIME = '%d-%b-%y'


def getAmazonDomain(country):
    return RESOURCE[country.upper()]


def getDesktopPath():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
