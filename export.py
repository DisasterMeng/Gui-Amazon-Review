import os, time, csv

from utils import getDesktopPath

NEED = ('asin', 'name', 'date', 'stars', 'title', 'content', 'href', 'buyer')


class JsonCsv:
    def __init__(self):
        self.csvFile = open(self.getPath(),'w', newline='')
        self.writer = csv.writer(self.csvFile)
        self.writer.writerow(['ASIN', '评价人', '日期', '星级', '标题', '内容', '评论链接', '买家链接'])

    def getPath(self):
        return os.path.join(getDesktopPath(), time.strftime("Amazon_Review_%Y_%m_%d_%H_%M.csv", time.localtime()))

    def writerCsv(self, dicData):
        row = []
        for dic in dicData:
            for item in NEED:
               row.append(dic[item])
        self.writer.writerow(row)

    def closeCsv(self):
        self.csvFile.close()

# def json_2_csv(dic_data, csv_path):
#     csv_file = open(csv_path, 'w', newline='')
#     keys = []
#     writer = csv.writer(csv_file)
#
#     # dic_data = json.loads(json_data, encoding='utf8')
#
#     for dic in dic_data:
#         keys = dic.keys()
#         # 写入列名
#         writer.writerow(keys)
#         break
#
#     for dic in dic_data:
#         for key in keys:
#             if key not in dic:
#                 dic[key] = ''
#         writer.writerow(dic.values())
#     csv_file.close()
