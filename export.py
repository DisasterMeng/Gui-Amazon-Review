import os, time, csv

from utils import getDesktopPath

NEED = ('asin', 'name', 'vp', 'date', 'stars', 'title', 'content', 'href', 'buyer')
NEEDDOC = ('ASIN', '评价人', '是否vp', '日期', '星级', '标题', '内容', '评论链接', '买家链接')
FILENAME = "Amazon_{asin}_Review_%Y_%m_%d_%H_%M.csv"


class JsonCsv:
    def __init__(self, ASIN):
        self.ASIN = ASIN
        self.csvFile = open(self.getPath(), 'w', newline='', encoding='utf-8-sig')
        self.writer = csv.writer(self.csvFile)
        self.writer.writerow(NEEDDOC)

    def getPath(self):
        name = time.strftime(FILENAME.format(asin=self.disposeASIN()), time.localtime())
        return os.path.join(getDesktopPath(), name)

    def writerCsv(self, dicData):
        for dic in dicData:
            row = []
            for item in NEED:
               row.append(dic[item])
            self.writer.writerow(row)

    def closeCsv(self):
        self.csvFile.close()

    def disposeASIN(self):
        return self.ASIN.replace(' ', '').strip('\n')