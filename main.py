from tkinter import *
from tkinter import ttk
import random
import time
import threading

from export import JsonCsv
from request import AmazonRequests
from dispose import AmazonDispose
from utils import is_number


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.window_init()
        self.createWidgets()
        self.data = []
        self.requests = ''
        self.csv = ''

    def window_init(self):
        self.master.title('Amazon评论获取工具   by 素笺 and 凌寒初见')
        self.master.resizable(width=FALSE,height=FALSE)

    def createWidgets(self):
        # fm2
        self.fm2 = Frame(self)
        self.fm2_left = Frame(self.fm2)
        self.fm2_right = Frame(self.fm2)
        self.fm2_left_top = Frame(self.fm2_left)
        self.fm2_left_bottom = Frame(self.fm2_left)

        self.siteLabel = Label(self.fm2_left_top, text='站点')
        self.siteLabel.pack(side=LEFT, padx=10)

        self.siteBox = ttk.Combobox(self.fm2_left_top, state='readonly',width=17)
        self.siteBox.pack(side=LEFT)
        self.siteBox['value'] = ('US', 'JP', 'FR', 'ES', 'IT', 'MX', 'GB', 'UK', 'CA', 'DE', 'IN')
        self.siteBox.current(0)
        self.fm2_left_top.pack(side=TOP, pady=5)

        self.asinLabel = Label(self.fm2_left_bottom, text='asin')
        self.asinLabel.pack(side=LEFT, padx=10)

        self.asinEntry = Entry(self.fm2_left_bottom)
        self.asinEntry.pack(side=LEFT)
        self.fm2_left_bottom.pack(side=TOP, pady=5)
        self.fm2_left.pack(side=LEFT)

        self.startButton = Button(self.fm2_right, text='开始获取', command=self.start)
        self.startButton.pack()
        self.fm2_right.pack(side=LEFT, padx=10)

        self.fm2.pack(side=TOP, pady=10)

        # fm3
        self.fm3 = Frame(self)
        self.msg = Text(self.fm3)
        self.msg.pack()
        self.msg.config(state=DISABLED)
        self.fm3.pack(side=TOP, fill=X)

    def write_msg(self, msg):
        self.msg.config(state=NORMAL)
        self.msg.insert(END, '\n' + msg)
        self.msg.config(state=DISABLED)
        self.msg.see(END)

    def delete_msg(self):
        self.msg.config(state=NORMAL)
        self.msg.delete(0.0, END)
        self.msg.config(state=DISABLED)

    def start(self):
        self.delete_msg()
        self.startButton.config(state=DISABLED)
        site = self.siteBox.get()
        asin = self.asinEntry.get()
        if not asin:
            self.write_msg('asin 为空，请先输入asin')
            self.startButton.config(state=NORMAL)
            return
        self.write_msg('开始任务...，站点--{}，Asin--{}'.format(site, asin))
        #初始化请求类
        self.requests = AmazonRequests(site, asin)
        self.csv = JsonCsv(asin)
        t = threading.Thread(target=self.start_download)
        t.setDaemon(True)
        t.start()

    def start_download(self, is_lang=False):
        # 解析数据 并存储数据
        # 判断asin是否存在
        amazon_data = self.requests.getAmaoznData(is_lang)
        self.write_msg('正在获取第{}页'.format(self.requests.getPage()))
        if amazon_data and is_number(amazon_data):
            if amazon_data == 404:
                self.write_msg('asin不存在，请查看是否输入有误')
            if amazon_data == 2:
                self.write_msg('请求失败')
            self.startButton.config(state=NORMAL)
            return
        self.write_msg('正在解析数据')
        dispose = AmazonDispose(amazon_data, self.siteBox.get(), self.asinEntry.get())
        if dispose.is_robot():
            self.write_msg('机器人验证')
            self.startButton.config(state=NORMAL)
            return
        if dispose.is_lang():
            self.write_msg('语言不符合, 重新请求')
            self.wait('重新请求')
            self.start_download(True)
            return
        dic_data = dispose.dispose()
        # self.write_msg(str(dic_data))
        if dic_data:
            self.write_msg('写入数据')
            self.csv.writerCsv(dic_data)
        else:
            self.write_msg('没有数据可以写入')
        if dispose.isNextPage():
            self.wait('请求下一页')
            self.requests.nextPage()
            self.start_download()
        else:
            self.csv.closeCsv()
            self.write_msg('评论获取完毕')
            self.startButton.config(state=NORMAL)

    def wait(self, msg):
        random_time = random.randint(5, 10)
        self.write_msg('等待%s秒,%s' % (random_time, msg))
        time.sleep(random_time)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
