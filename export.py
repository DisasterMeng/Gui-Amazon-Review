import csv
import json


def json_2_csv(dic_data, csv_path):
    csv_file = open(csv_path, 'w', newline='')
    keys = []
    writer = csv.writer(csv_file)

    # dic_data = json.loads(json_data, encoding='utf8')

    for dic in dic_data:
        keys = dic.keys()
        # 写入列名
        writer.writerow(keys)
        break

    for dic in dic_data:
        for key in keys:
            if key not in dic:
                dic[key] = ''
        writer.writerow(dic.values())
    csv_file.close()
