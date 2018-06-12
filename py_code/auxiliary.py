# coding: utf-8


# need be more Considerate: extract float data from a string
def extract_float_from_str(p_str):
    p_str_lens = len(p_str)
    p_list = []
    param = ""
    # 0~9: 48~57, -: 45, .: 46
    for i in range(len(p_str)):
        # case: 0, eg: *0*, .0, -0., *0.999, *099
        # remove: *0999, *0009,
        if 48 == ord(p_str[i]):
            if param == "":  # 0 in the first:
                if i < (p_str_lens - 1) and ord(p_str[i + 1]) == 46:
                    # the next of 0 is .
                    param += p_str[i]  # add 0
                elif i == (p_str_lens - 1):
                    param += p_str[i]  # add 0
            else:  # ord(param[-1]) != 48:  # last of param != 0
                param += p_str[i]  # add 0
        # case: 1~9:
        elif (ord(p_str[i]) > 48) and (ord(p_str[i]) <= 57):
            param += p_str[i]
        # case: -, only in the first:
        elif ord(p_str[i]) == 45:
            if param == "":
                param += p_str[i]
            else:
                if param != '.' and param != '-' and param != '-.':
                    p_list.append(param)  # save last
                param = ""
                param += p_str[i]
        # case: ., only one in data:
        elif ord(p_str[i]) == 46 and -1 == param.find('.'):
            param += p_str[i]
        else:
            if param != "" and param != '.' and param != '-' and param != '-.':
                p_list.append(param)
            param = ""
    if param != "" and param != '.' and param != '-' and param != '-.':
        p_list.append(param)

    para_str = p_list
    para_list = [float(v) for v in p_list]
    return para_str, para_list


import threading as th


class ConnThread():
    def __init__(self):
        self.lock = th.Lock()
        self.th = []
        pass

    def add(self, name, target, args, daemon=True):
        self.th.append([name, th.Thread(target=target,
                                        args=args, daemon=daemon)])

    def start_one(self, name):
        for v in self.th:
            if v[0] == name:
                v[1].start()

    def start_all(self):
        for v in self.th:
            v[1].start()


import threading
import time


class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            print(time.time())
            time.sleep(1)

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False