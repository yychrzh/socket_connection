import tkinter as tk
from tkinter import ttk
from auxiliary import *
from py_protocol import *
from HexaInfo import *
import threading as th
import time


# overtime in command function may cause error !
class RemoteGui(tk.Tk):
    def __init__(self, conn=None, title="mind_control", size=None):
        super().__init__()
        # self.wm_title(tk_name)
        # title and size of gui:
        self.title(title)
        if size is not None:
            self.geometry(size)
        # 0: connected or not; 1: ready to connect; 2: ready to send;
        # -1: destroy and return
        self.connect_flag = 0
        # module name and function name dictionary:
        self.module_list = None
        self.func_list = None
        # function's parameters and output information:
        self.params_inout_list = None
        # descriptions of function:
        self.function_description_list = None
        # Entry for conn socket connection's parameters:
        self.conn_entry = []
        # module and function Combobox:
        self.cl_m, self.cl_f = None, None
        # output and input Text:
        self.o_text, self.i_text = None, None
        # master_farme for hold all tk widget
        self.master_frame = None
        # frame and Entry for parameters:
        self.params_frame = None
        self.params_tk = []
        # frame Text for robot's response:
        self.ret_frame = None
        self.ret_tk = []
        # socket from out space:
        self.main_conn = conn
        # module and function's name for current selected:
        self.module_name = ""
        self.func_name = ""
        # parameters input:
        self.params_list = []
        # received data from robot:
        self.ret = None
        # socket parameters:
        self.conn_type = "server"
        self.port_num = 4096
        self.buffsize = 2048
        self.ip = "192.168.123.111"
        self.debug_print = False

    def create_Widgets(self):
        self.master_frame = tk.Frame(self)
        self.master_frame.pack(fill=tk.X)

        # add return menu:
        # <em>create a toplevel menu</em>
        menubar = tk.Menu(self)
        menubar.add_command(label="About!")
        menubar.add_command(label="Quit!", command=self._quit)
        # <em>display the menu</em>
        self.config(menu=menubar)

        # 0. create socket choose menu:
        self.conn_choose()

        # 1. top_frame = tk.Frame(master_frame)
        top_frame = tk.LabelFrame(self.master_frame,
                                  text="please choose a function")
        top_frame.pack(fill="x")

        # choose function
        func = tk.Label(top_frame, text='func_name: ', width=20)
        # func.pack(fill="y", expand=0, side=tk.LEFT)
        func.pack(fill="y", side=tk.LEFT)
        # module comboxlist
        comvalue = tk.StringVar()  # string variable
        self.cl_m = ttk.Combobox(master=top_frame, textvariable=comvalue,
                                 width=20, state='readonly')
        self.cl_m["values"] = self.module_list
        self.cl_m.bind("<<ComboboxSelected>>", self.module_select)
        self.cl_m.pack(fill="y", side=tk.LEFT)
        self.cl_m.current(0)

        # function comboxlist:
        comvalue = tk.StringVar()  # string variable
        self.cl_f = ttk.Combobox(master=top_frame, textvariable=comvalue,
                                 width=25, state='readonly')
        self.cl_f["values"] = self.func_list["Hexa"]
        self.cl_f.bind("<<ComboboxSelected>>", self.func_select)
        self.cl_f.pack(fill="y", side=tk.LEFT)
        self.cl_f.current(0)

        # execute button:
        tk.Button(master=top_frame, text="execute", width=15,
                  command=self.execute_response).pack(fill="y", side=tk.RIGHT)

        # 2. output frame: function description
        # out_frame = tk.Frame(master_frame)
        out_frame = tk.LabelFrame(self.master_frame, text="description "
                                                          "of the function")
        out_frame.pack(fill="x")
        descri = tk.Label(out_frame, text='describe: ', width=20)
        descri.pack(fill="y", side=tk.LEFT)
        self.o_text = tk.Text(out_frame, width=67, height=10)
        self.o_text.pack(side=tk.LEFT)

        # 3. parameters frame:
        self.params_frame = tk.LabelFrame(self.master_frame,
                                          text="parameters for input")
        self.params_frame.pack(fill="x")

        # 4. output frame:
        self.ret_frame = tk.LabelFrame(self.master_frame, text="return data")
        self.ret_frame.pack(fill="x")

    # choose parameters to make a socket connection:
    def conn_choose(self):
        # 0. conn_frame: conn_type, port_num = 4096, buffsize = 2048,
        # host='127.0.0.1', debug_print
        # conn_frame0 hold labels:
        conn_frame0 = tk.LabelFrame(self.master_frame,
                                    text="create socket connection")
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

        # conn_frame1 hold Entry and Combobox
        conn_frame1 = tk.Frame(self.master_frame)
        conn_frame1.pack(fill="x")

        # for conn parameters input:
        # conn_type:
        comvalue = tk.StringVar()  # string variable
        self.conn_entry.append(ttk.Combobox(master=conn_frame1,
                                            textvariable=comvalue, width=12,
                                            state='readonly'))
        self.conn_entry[0]["values"] = ["server", "client"]
        self.conn_entry[0].pack(fill="y", side=tk.LEFT)
        self.conn_entry[0].current(0)

        # port/buffisize/ip
        for i in range(3):
            self.conn_entry.append(tk.Entry(conn_frame1, width=14))
            self.conn_entry[i+1].pack(fill="y", side=tk.LEFT)

        # debug_print_flag
        comvalue = tk.StringVar()  # string variable
        self.conn_entry.append(ttk.Combobox(master=conn_frame1,
                                            textvariable=comvalue, width=12,
                                            state='readonly'))
        self.conn_entry[4]["values"] = ["True", "False"]
        self.conn_entry[4].pack(fill="y", side=tk.LEFT)
        self.conn_entry[4].current(0)

        # connect button:
        tk.Button(master=conn_frame1, text="connect", width=15,
                  command=self.connect_response).pack(fill="y", side=tk.RIGHT)

    # distroy the input Entry and
    def in_listbox_destroy(self):
        for v in self.params_tk:
            for p in v:
                p.destroy()
        self.params_tk = []
        self.params_frame.destroy()

    # create a list of Entry for paramters input:
    def in_listbox(self, module_name, func_name):
        self.in_listbox_destroy()
        # re create:
        self.params_frame = tk.LabelFrame(self.master_frame,
                                          text="parameters for input")
        self.params_frame.pack(fill="x")
        params_str = self.params_inout_list[module_name][func_name][0]
        if 0 == params_str:
            return

        params_lens = len(params_str)
        for i in range(params_lens):
            param_frame = tk.Frame(self.params_frame)
            param_frame.pack(fill="x")
            param_label = tk.Label(param_frame, text=params_str[i] + ": ",
                                   width=30, height=1)
            param_label.pack(fill="y", side=tk.LEFT)
            param_entry = tk.Entry(param_frame, width=40)
            param_entry.pack(fill="y", side=tk.LEFT)
            self.params_tk.append([param_entry, param_label, param_frame])

    # delete the output Text
    def out_listbox_delete(self):
        for v in self.ret_tk:
            v[0].delete(1.0, tk.END)

    # destroy the output Text list
    def out_listbox_destroy(self):
        for v in self.ret_tk:
            for p in v:
                p.destroy()
        self.ret_tk = []
        self.ret_frame.destroy()

    # create a list of Text for robot response:
    def out_listbox(self, module_name, func_name):
        self.out_listbox_destroy()
        # re create:
        self.ret_frame = tk.LabelFrame(self.master_frame, text="return data")
        self.ret_frame.pack(fill="x")
        ret_str = self.params_inout_list[module_name][func_name][1]
        if 0 == ret_str:
            return

        ret_lens = len(ret_str)
        for i in range(ret_lens):
            ret_frame = tk.Frame(self.ret_frame)
            ret_frame.pack(fill="x")
            ret_label = tk.Label(ret_frame, text=ret_str[i] + ": ",
                                 width=30, height=1)
            ret_label.pack(fill="y", side=tk.LEFT)
            ret_text = tk.Text(ret_frame, width=40, height=1)
            ret_text.pack(fill="y", side=tk.LEFT)
            self.ret_tk.append([ret_text, ret_label, ret_frame])

    # response to module comboxlist:
    def module_select(self, value1):
        # empty current output text:
        self.o_text.delete(1.0, tk.END)
        # display current module and function name and description:
        self.module_name = self.cl_m.get()
        self.cl_f["values"] = self.func_list[self.module_name]
        self.cl_f.current(0)

    # response to function comboxlist:
    def func_select(self, value1):
        self.o_text.delete(1.0, tk.END)
        self.module_name = self.cl_m.get()
        self.func_name = self.cl_f.get()
        self.o_text.insert(tk.INSERT, 'module_name: ' + self.module_name + '\n')
        self.o_text.insert(tk.INSERT, 'function_name: ' + self.func_name + '\n')
        describ = self.function_description_list[self.module_name][self.func_name]
        self.o_text.insert(tk.INSERT, 'function_description: ' + '\n    ' +
                           describ + '\n')
        # display paramters list:
        self.in_listbox(self.module_name, self.func_name)
        # display output_data:
        self.out_listbox(self.module_name, self.func_name)

    # response to execute button:
    def execute_response(self):
        self.o_text.delete(1.0, tk.END)
        self.module_name = self.cl_m.get()
        self.func_name = self.cl_f.get()
        self.o_text.insert(tk.INSERT, 'module_name: ' + self.module_name + '\n')
        self.o_text.insert(tk.INSERT, 'function_name: ' + self.func_name + '\n')
        describ = self.function_description_list[self.module_name][self.func_name]
        self.o_text.insert(tk.INSERT, 'function_description: ' + '\n    ' +
                           describ + '\n')
        # extract parameters:
        params_str = []
        for i in range(len(self.params_tk)):
            params_str.append(self.params_tk[i][0].get())  # from Entry read data
        # print(params_str)
        # if len(params_str) > 0:
        #    self.o_text.insert(tk.INSERT, '\nparameters: ' + str(params_str))

        # remote control:
        self.params_list = []
        for i in range(len(params_str)):
            _, params = extract_float_from_str(str(params_str[i]))
            # print(params)
            for v in params:
                self.params_list.append(v)
        # print("params_list: ", self.params_list)
        if len(self.params_list) > 0:
            self.o_text.insert(tk.INSERT,
                               '\nparameters: ' + str(self.params_list))
        self.connect_flag = 2

    # display received data in ret_frame:
    def recv_data_display(self, ret):
        self.out_listbox_delete()
        for i in range(len(ret)):
            self.ret_tk[i][0].insert(tk.INSERT, str(ret[i]))

    # display the received data and state in o_text and ret_frame:
    def ret_display(self, ret):
        if type(ret) == list:
            self.recv_data_display(ret)
            self.o_text.insert(tk.INSERT, "\nrunning success, "
                                          "receive data: " + str(ret))
        elif type(ret) == bool:
            self.o_text.insert(tk.INSERT, "\nreturn error: "
                                          "didn't receive correct response !")
        elif type(ret) == int:
            if 1 == ret:
                self.o_text.insert(tk.INSERT, "\nrunning success !")
            elif -1 == ret:
                self.o_text.insert(tk.INSERT, "\nrunning failed !")
            elif -2 == ret:
                self.o_text.insert(tk.INSERT, "\nparameters input error !")

    # reponse to connect button:
    def connect_response(self):
        conn_type = self.conn_entry[0].get()
        port_num = self.conn_entry[1].get()
        buffsize = self.conn_entry[2].get()
        ip = self.conn_entry[3].get()
        debug_print = self.conn_entry[4].get()

        # default value:
        if conn_type == "":
            conn_type = "server"
        if debug_print == "":
            debug_print = "False"
        if ip == "":
            ip = "192.168.123.111"
        if port_num == "":
            port_num = '4096'
        if buffsize == "":
            buffsize = '2048'
        self.o_text.delete(1.0, tk.END)
        self.o_text.insert(tk.INSERT, "conn_params: " + conn_type + " " +
                           port_num + " " + buffsize + " " + ip + " " +
                           debug_print)

        debug_print = True if debug_print == "True" else False
        if int(port_num) <= 2048:
            port_num = 2048
        # print(conn_type, int(port_num), int(buffsize), ip, debug_print)
        self.conn_type = conn_type
        self.port_num = int(port_num)
        self.buffsize = int(buffsize)
        self.ip = ip
        self.debug_print = debug_print
        # self.o_text.insert(tk.INSERT, "\ncreate socket connection, "
        #                               "waiting to connect to hexa robot...")
        self.connect_flag = 1

    # return and distroy the gui
    def _quit(self):
        self.connect_flag = -1
        self.quit()     # stop mainloop
        self.destroy()  # destroy all widgets


"""# default:
conn_type = "server"
hexa_port_num = 4096
buffsize = 2048
robot_ip = '192.168.123.111'  # '10.20.4.113'
debug_print = False
"""


# send the function to remote robot:
def remote_run(conn, module_name, func_name, params):
    expect_params_list = function_in_out_list[module_name][func_name][0]
    # params list check:
    params_lens = 0 if expect_params_list == 0 else len(expect_params_list)
    if len(params) != params_lens:
        if (func_name == "MoveLegs_Coordinates") or (
                func_name == "MoveLegs_JointDegrees"):
            if len(params) != (1 + params[0] * 4):
                print("parammeters input error, please input twice !")
                return int(-2)
        else:
            if len(params) != (1 + params[0] * 4):
                print("parammeters input error, please input twice !")
                return int(-2)

    param_list = [[DATA_FLOAT64, v] for v in params]
    print("send params: ", param_list)
    if param_list is None:
        conn.send_control_instruction(module_name, func_name, [])
    else:
        conn.send_control_instruction(module_name, func_name, param_list)
    print("control instructions send success, waiting for response...")
    # waiting for response !
    recv_flag, recv_array = conn.recv_data()  # 1 float (bool)
    print("recv from robot: ", recv_flag, recv_array)
    if DATA_FLAG == recv_flag:
        return recv_array  # list
    elif SUCCESS_RESPONSE_FLAG == recv_flag:
        return int(1)  # int
    elif ERROR_RESPONSE_FLAG == recv_flag:
        return int(-1)  # int
    else:
        print("didn't receive correct response when run %s func !" % func_name)
        return bool(False)  # bool


# running in a independent threading:
def remote_conn(pc_tk):
    conn = None
    lock = th.Lock()
    while True:
        # time.sleep(0.05)
        # ready to connect with robot:
        if pc_tk.connect_flag == 1:
            pc_tk.connect_flag = 0
            print("create socket server, waiting to connect to hexa robot...")
            lock.acquire()
            pc_tk.o_text.insert(tk.INSERT, "\ncreate socket connection, "
                                           "waiting to connect to hexa robot...")
            lock.release()
            conn = Data_transfer(pc_tk.conn_type, pc_tk.port_num,
                                 pc_tk.buffsize, pc_tk.ip, pc_tk.debug_print)
            conn.handshake()
            lock.acquire()
            pc_tk.o_text.insert(tk.INSERT, "\nconnect with robot success !")
            lock.release()
        # send one control instruction to robot:
        elif pc_tk.connect_flag == 2:
            pc_tk.connect_flag = 0
            # remote run:
            if conn is not None:
                ret = remote_run(conn, pc_tk.module_name,
                                 pc_tk.func_name, pc_tk.params_list)
                lock.acquire()
                pc_tk.ret = ret
                pc_tk.ret_display(ret)
                lock.release()
        # close and return:
        elif pc_tk.connect_flag == -1:
            pc_tk.connect_flag = 0
            if conn is not None:
                conn.close_socket()
            break


# creat a gui and a socket connection threading:
def th_test():
    pc_gui = RemoteGui(title="Hexapod_Robot")  # , size="640x640")
    pc_gui.module_list = module_list  # load module name list
    pc_gui.func_list = function_list  # load function name list
    pc_gui.params_inout_list = function_in_out_list
    pc_gui.function_description_list = function_description_list
    pc_gui.create_Widgets()  # create frame
    t = th.Thread(target=remote_conn, args=(pc_gui, ), daemon=True)
    t.start()
    pc_gui.mainloop()
    t.join()


if __name__ == '__main__':
    th_test()