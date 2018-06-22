from py_protocol import *
import time
import random


def float_test(conn):
    MAX_COUNT = 100
    count = 0
    error_count = 0
    total_lens = 0

    start_time = time.time()
    while True:
        send_array = []
        data_lens = random.randint(50, 250)
        for i in range(data_lens):
            send_array.append(random.uniform(-1e5, 1e5))  # produce 50 random float numbers

        print("send double data to client: ")
        # print(send_array)
        conn.send_data(send_array, bit=64)

        # time.sleep(0.05)

        print("data sent success, waiting for response !")
        recv_flag, recv_array = conn.recv_data()

        if DATA_FLAG == recv_flag:
            for i in range(data_lens):
                if recv_array[i] != send_array[i]:
                    print("error emerged in %d 's recv in the %d 's data, expect %.15f, but received %.15f"
                          % (count, i, send_array[i], recv_array[i]))
                    error_count += 1
                    break
            if error_count > 0:
                break

        current_time = time.time() - start_time
        print(">>>count: %3d, current_time: %.15f sec" % (count, current_time))
        count += 1
        total_lens += data_lens

        if MAX_COUNT == count:
            conn.send_flag(TERMINATION_FLAG)
            print("data transmission end, with %d data transfered error in total %d data"
                  % (error_count, total_lens))
            break


if __name__ == '__main__':
    print("create socket server, waiting to connect to hexa robot...")
    conn = Data_transfer('client', 4096, 2048, '192.168.123.111', False)
    conn.handshake()
    float_test(conn)