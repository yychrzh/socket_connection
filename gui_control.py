import numpy as np

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title("Embed matplotlib in tkinter")
        self.create_Widgets()

    def test_command(self):
        tx_str = self.tx1.get(1.0, 10.0)
        print(type(tx_str))
        print(len(tx_str))
        for i in range(len(tx_str)):
            print(i, tx_str[i])

    def create_Widgets(self):
        self.title('python test GUI')
        self.geometry('640x360')

        master = self
        func_list = ["Available", "Start", "Relax", "Close"]
        # choose function
        func = tk.Label(master, text='func_name：')
        func.grid(row=0, sticky=tk.W)
        # comboxlist:
        self.cl1 = self.comboxlist(master, "cl1", func_list)
        self.cl1.grid(row=0, column=1)  # , sticky=tk.E)

        # output:
        self.tx1 = tk.Text(master)
        self.tx1.grid(row=1)

        # execute button:
        tk.Button(master=master, text="execute",
                  command=self.test_command).grid(row=0, column=2, sticky=tk.E)
        # add return botton:
        tk.Button(master=self, text="return", command=self._quit).grid(row=4)

    def test_s(self, num):
        print("scale: ", num)

    def Button(self, master, name, command=None):
        button = tk.Button(master=master, text=name, command=command)
        return button

    def Scale(self, master, name, from_=0, to=50,
              orient=tk.HORIZONTAL, length=500, showvalue=0, tickinterval=5,
              resolution=1, command=None):
        # put scale for choose filter num
        if command is not None:
            scale = tk.Scale(master=master, label=name, from_=from_, to=to,
                             orient=orient, length=length, showvalue=showvalue,
                             tickinterval=tickinterval, resolution=resolution,
                             command=command)
        else:
            scale = tk.Scale(master=master, label=name, from_=from_, to=to,
                             orient=orient, length=length, showvalue=showvalue,
                             tickinterval=tickinterval, resolution=resolution)
        return scale

    # string choose
    def comboxlist(self, master, name, value, command=None):
        # def select(*args):
        #    print("label " + name + ": ", comboxlist.get())

        # ttk.Label(master=master, text=" " * 5 + name + ":").pack()

        comvalue = tk.StringVar()            # string variable
        comboxlist = ttk.Combobox(master=master, textvariable=comvalue,
                                  state='readonly')
        comboxlist["values"] = value
        if command is not None:
            comboxlist.bind("<<ComboboxSelected>>", command)
        comboxlist.current(0)
        return comboxlist

    def Checkbutton(self, master, name, command=None):
        # put checkbutton for choose
        var1 = tk.IntVar()

        # def check():
        #    print("check " + name + ": ", var1.get())
        #    # print("check %d: " % data_num, extend.get())
        if command is not None:
            c1 = tk.Checkbutton(master=master, text=name,
                                variable=var1, onvalue=1, offvalue=0, command=command)
        else:
            c1 = tk.Checkbutton(master=master, text=name,
                                variable=var1, onvalue=1, offvalue=0)
        return c1

    def _quit(self):
        self.quit()     # stop mainloop
        self.destroy()  # destroy all widgets


def main():
    root = Tkinter.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry('640x360')  # 设置了主窗口的初始大小960x540 800x450 640x360

    main_frame = MainFrame(root)
    main_frame.mainloop()

import time
from py_protocol import Data_transfer
from remote_robot import Hexa, HexaBody, HexaHead, HexaLeg

"""
class Gui_control(Application):
    def __init__(self, hexa, hexabody, hexahead, hexaleg):
        Application.__init__(self)
        self.hexa = hexa
        self.hexabody = hexabody
        self.hexahead = hexahead
        self.hexaleg = hexaleg
        self.wm_title("Gui_control")

    def create_Widgets(self):
        footframe = self

        # put return button
        self.Button(master=footframe, name="return",
                    command=self._quit)
"""


robot_ip = '192.168.123.111'  # '10.20.4.113'
hexa_port_num = 4096

if __name__ == '__main__':
    # initialize Application
    app = Application()
    # main loop:
    app.mainloop()

    """
    conn = Data_transfer('server', hexa_port_num, buffsize=2048,
                         debug_print=False)
    conn.handshake()
    hexa = Hexa(conn)
    hexabody = HexaBody(conn)
    hexahead = HexaHead(conn)
    hexaleg = HexaLeg(conn)
    app = Gui_control(hexa, hexabody, hexahead, hexaleg)
    app.create_Widgets()
    app.mainloop()
    """