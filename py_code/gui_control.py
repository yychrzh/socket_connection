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


class Gui(tk.Tk):
    def __init__(self, title, size=None):
        super().__init__()
        # self.wm_title(tk_name)
        self.connect_flag = 0
        self.module_list = None # ["hexa", "hexabody", "hexahead", "hexaleg", "acce", "distance"]
        self.func_list = None # ["Available", "Start", "Relax", "Close"]
        self.params_inout_list = None
        self.function_description_list = None
        self.title(title)
        if size is not None:
            self.geometry(size)
        self.conn_entry = []
        self.cl_m, self.cl_f = None, None
        self.o_text, self.i_text = None, None
        self.params_frame = None
        self.ret_frame = None
        self.params_tk = []
        self.ret_tk = []
        # self.create_Widgets()

    # response to module comboxlist:
    def module_select(self, value1):
        pass

    # response to module comboxlist:
    def func_select(self, value1):
        pass

    # response to execute button:
    def execute_func(self):
        pass

    # reponse to connect button:
    def connect_conn(self):
        pass

    # need be more Considerate
    def extract_float_from_str(self, p_str):
        p_list = []
        param = ""
        # 0~9, -, .
        for i in range(len(p_str)):
            if ((ord(p_str[i]) >= 48) and (ord(
                    p_str[i]) <= 57)) or ord(p_str[i]) == 45 or ord(p_str[i]) == 46:
                param += p_str[i]
            else:
                if param != "":
                    p_list.append(param)
                param = ""
        if param != "" and param != "." and param != "-":
            p_list.append(param)

        para_str = p_list
        para_list = [float(v) for v in p_list]
        return para_str, para_list

    def create_Widgets(self):
        master_frame = tk.Frame(self)
        master_frame.pack(fill=tk.X)

        # 0. conn_frame: conn_type, port_num = 4096, buffsize = 2048, host='127.0.0.1', debug_print
        conn_frame0 = tk.LabelFrame(master_frame, text="create socket connection")
        conn_frame0.pack(fill="x")
        # conn type/Port_num/Buffsize/Ip/debug
        tk.Label(conn_frame0, text="Type(S:0/C:1)",
                 width=14).pack(fill="y", side=tk.LEFT)
        tk.Label(conn_frame0, text="Port(>2048)",
                 width=14).pack(fill="y", side=tk.LEFT)
        tk.Label(conn_frame0, text="Buffsize(2048)",
                 width=14).pack(fill="y", side=tk.LEFT)
        tk.Label(conn_frame0, text='Ip(for C)',
                 width=14).pack(fill="y", side=tk.LEFT)
        tk.Label(conn_frame0, text="debug_print(T/F)",
                 width=14).pack(fill="y", side=tk.LEFT)
        conn_frame1 = tk.Frame(master_frame)
        conn_frame1.pack(fill="x")
        # entry for conn parameters input:
        for i in range(5):
            self.conn_entry.append(tk.Entry(conn_frame1, width=14))
            self.conn_entry[i].pack(fill="y", side=tk.LEFT)
        # connect button:
        tk.Button(master=conn_frame1, text="connect", width=15,
                  command=self.connect_conn).pack(fill="y", side=tk.LEFT)

        # 1. top_frame = tk.Frame(master_frame)
        top_frame = tk.LabelFrame(master_frame, text="please choose a function")
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
        self.cl_m.bind("<<ComboboxSelected>>", self.module_select)
        self.cl_m.pack(fill="y", side=tk.LEFT)
        self.cl_m.current(0)

        # function comboxlist:
        comvalue = tk.StringVar()  # string variable
        self.cl_f = ttk.Combobox(master=top_frame, textvariable=comvalue, width=25,
                                 state='readonly')
        self.cl_f["values"] = self.func_list["Hexa"]
        self.cl_f.bind("<<ComboboxSelected>>", self.func_select)
        self.cl_f.pack(fill="y", side=tk.LEFT)
        self.cl_f.current(0)

        # execute button:
        tk.Button(master=top_frame, text="execute", width=15,
                  command=self.execute_func).pack(fill="y", side=tk.LEFT)

        # 2. output frame: function description
        # out_frame = tk.Frame(master_frame)
        out_frame = tk.LabelFrame(master_frame, text="description of the function")
        out_frame.pack(fill="x")
        descri = tk.Label(out_frame, text='describe：', width=20)
        descri.pack(fill="y", side=tk.LEFT)
        self.o_text = tk.Text(out_frame, width=67, height=10)
        self.o_text.pack(side=tk.LEFT)

        # 3. parameters frame:
        self.params_frame = tk.LabelFrame(master_frame, text="parameters for input")
        self.params_frame.pack(fill="x")

        # 4. output frame:
        self.ret_frame = tk.LabelFrame(master_frame, text="return data")
        self.ret_frame.pack(fill="x")

        # 5. return frame
        # return_frame = tk.LabelFrame(master_frame, text="press to return")
        return_frame = tk.Frame(master_frame)
        return_frame.pack(fill="x")
        # add return botton:
        tk.Button(master=return_frame, text="return", command=self._quit,
                  width=20).pack(fill="y")

    def in_listbox_destroy(self):
        for v in self.params_tk:
            for p in v:
                p.destroy()
        self.params_tk = []

    def in_listbox(self, master, module_name, func_name):
        self.in_listbox_destroy()
        params_str = self.params_inout_list[module_name][func_name][0]
        if 0 == params_str:
            return

        params_lens = len(params_str)
        for i in range(params_lens):
            param_frame = tk.Frame(master)
            param_frame.pack(fill="x")
            param_label = tk.Label(param_frame, text=params_str[i] + ": ",
                                   width=30)
            param_label.pack(fill="y", side=tk.LEFT)
            param_entry = tk.Entry(param_frame, width=30)
            param_entry.pack(fill="y")
            self.params_tk.append([param_entry, param_label, param_frame])

    def out_listbox_delete(self):
        for v in self.ret_tk:
            v[0].delete(1.0, tk.END)

    def out_listbox_destroy(self):
        for v in self.ret_tk:
            for p in v:
                p.destroy()
        self.ret_tk = []

    def out_listbox(self, master, module_name, func_name):
        self.out_listbox_destroy()
        ret_str = self.params_inout_list[module_name][func_name][1]
        if 0 == ret_str:
            return

        ret_lens = len(ret_str)
        for i in range(ret_lens):
            ret_frame = tk.Frame(master)
            ret_frame.pack(fill="x")
            ret_label = tk.Label(ret_frame, text=ret_str[i] + ": ",
                                 width=30)
            ret_label.pack(fill="y", side=tk.LEFT)
            ret_text = tk.Text(ret_frame, width=30, height=1)
            ret_text.pack(fill="y")
            self.ret_tk.append([ret_text, ret_label, ret_frame])

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
        self.connect_flag = -1
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