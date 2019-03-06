from tkinter import *
from tkinter import ttk
import time

import export


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.window_init()
        self.createWidgets()

    def window_init(self):
        self.master.title('Amazon评论获取工具   by 素笺 and 凌寒初见')
        width, height = self.master.maxsize()
        print(width, height)
        # self.master.geometry("{}x{}".format(960, 540))

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

    def start(self):
        site = self.siteBox.get()
        asin = self.asinEntry.get()
        self.write_msg('开始任务...，站点--{}，Asin--{}'.format(site, asin))
        # aa = [{'aa': 3}, {'aa': 4}]
        # path = time.strftime("Amazon_Review_%Y_%m_%d_%H_%M.csv", time.localtime())
        # export.json_2_csv(aa, path)

    def start_download(self):
        pass


if __name__ == '__main__':
    app = Application()
    app.mainloop()
