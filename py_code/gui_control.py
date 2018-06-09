import numpy as np

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk


class Application(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        # self.wm_title(tk_name)
        self.module_list = ["hexa", "hexabody", "hexahead", "hexaleg", "acce", "distance"]
        self.func_list = ["Available", "Start", "Relax", "Close"]
        self.title(title)
        self.geometry(size)
        self.cl_m, self.cl_f = None, None
        self.o_text, self.i_text = None, None
        self.create_Widgets()

    # response to comboxlist:
    # delete the display text and display the module and function name
    def text_del(self, value1):  # value1 hold the value of comboxlist
        # self.i_text.delete(1.0, tk.END)

        self.o_text.delete(1.0, tk.END)

        module_name = self.cl_m.get()
        self.o_text.insert(tk.INSERT, 'module_name: ' + module_name + '\n')
        func_name = self.cl_f.get()
        self.o_text.insert(tk.INSERT, 'function_name: ' + func_name + '\n')
        self.o_text.insert(tk.INSERT, 'function_desc: ' + '\n')

    # response to execute button:
    def execute_func(self):
        # extract parameters and display in o_text
        input_params = self.i_text.get(1.0, tk.END)
        para_str, para_list = self.extract_float_from_str(input_params)
        dis = ""
        for i in range(len(para_str)):
            dis += " param " + str(i) + ":" + para_str[i]
        self.o_text.insert(tk.INSERT, "params:" + dis)

    # need be more Considerate
    def extract_float_from_str(self, p_str):
        para_list = []
        param = ""
        for i in range(len(p_str)):
            if ((ord(p_str[i]) >= 48) and (ord(p_str[i]) <= 57)) or ord(p_str[i]) == 46:
                param += p_str[i]
            else:
                if param != "":
                    para_list.append(param)
                param = ""
        para_str = para_list
        para_list = [float(v) for v in para_list]
        return para_str, para_list

    def create_Widgets(self):
        master_frame = tk.Frame(self)
        master_frame.pack(fill=tk.X)
        top_frame = tk.Frame(master_frame)
        top_frame.pack(fill="x")

        # choose function
        func = tk.Label(top_frame, text='func_name：', width=20)
        # func.pack(fill="y", expand=0, side=tk.LEFT)
        func.pack(fill="y", side=tk.LEFT)
        # module comboxlist
        comvalue = tk.StringVar()  # string variable
        self.cl_m = ttk.Combobox(master=top_frame, textvariable=comvalue, width=20,
                                 state='readonly')
        self.cl_m["values"] = self.module_list
        self.cl_m.bind("<<ComboboxSelected>>", self.text_del)
        self.cl_m.pack(fill="y", side=tk.LEFT)
        self.cl_m.current(0)

        # function comboxlist:
        comvalue = tk.StringVar()  # string variable
        self.cl_f = ttk.Combobox(master=top_frame, textvariable=comvalue, width=25,
                                 state='readonly')
        self.cl_f["values"] = self.func_list
        self.cl_f.bind("<<ComboboxSelected>>", self.text_del)
        self.cl_f.pack(fill="y", side=tk.LEFT)
        self.cl_f.current(0)

        # execute button:
        tk.Button(master=top_frame, text="execute", width=15,
                  command=self.execute_func).pack(fill="y", side=tk.LEFT)

        # output frame: describe
        out_frame = tk.Frame(master_frame)
        out_frame.pack(fill="x")
        descri = tk.Label(out_frame, text='describe：', width=20)
        descri.pack(fill="y", side=tk.LEFT)
        self.o_text = tk.Text(out_frame, width=67, height=6)
        self.o_text.pack(side=tk.LEFT)

        # input frame:
        in_frame = tk.Frame(master_frame)
        in_frame.pack(fill="x")
        params = tk.Label(in_frame, text='params：', width=20)
        params.pack(fill="y", side=tk.LEFT)
        self.i_text = tk.Text(in_frame, width=67, height=6)
        self.i_text.pack(side=tk.LEFT)

        # return frame
        ret_frame = tk.Frame(master_frame)
        ret_frame.pack(fill="x")
        # add return botton:
        tk.Button(master=ret_frame, text="return", command=self._quit,
                  width=20).pack(fill="y")

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
    def str_comboxlist(self, master, width, value, command=None):
        comvalue = tk.StringVar()            # string variable
        comboxlist = ttk.Combobox(master=master, textvariable=comvalue, width=width,
                                  state='readonly')
        comboxlist["values"] = value
        if command is not None:
            comboxlist.bind("<<ComboboxSelected>>", command)
        comboxlist.current(0)
        return comboxlist

    def Checkbutton(self, master, name, command=None):
        # put checkbutton for choose
        var1 = tk.IntVar()
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
    app = Application("test", '640x230')
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