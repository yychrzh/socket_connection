from number_conversion import Number_conver
from py_tcpsocket import tcpsocket


class Data_transfer(object):
    def __init__(self, conn_type='server', port_num=8088, buffsize=200, host='127.0.0.1', debug_print=True):
        self.number_