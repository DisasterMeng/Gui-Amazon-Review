import os, time, csv

from utils import getDesktopPath

NEED = ('asin', 'name', 'date', 'stars', 'title', 'content', 'href', 'buyer')


class JsonCsv:
    def __init__(self):
        self.csvFile = open(self.getPath(), 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csvFile)
        self.writer.writerow(['ASIN', '评价人', '日期', '星级', '标题', '内容', '评论链接', '买家链接'])

    def getPath(self):
        return os.path.join(getDesktopPath(), time.strftime("Amazon_Review_%Y_%m_%d_%H_%M.csv", time.localtime()))

    def writerCsv(self, dicData):
        for dic in dicData:
            row = []
            for item in NEED:
               row.append(dic[item])
            self.writer.writerow(row)

    def closeCsv(self):
        self.csvFile.close()
