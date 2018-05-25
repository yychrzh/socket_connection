from py_tcpsocket import tcpsocket


if __name__ == "__main__":
    conn = tcpsocket(conn_type='server', port_num=8088, buffsize=200)
    recv_str = conn.recv_strings()
    print(recv_str)