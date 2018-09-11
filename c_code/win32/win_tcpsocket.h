#ifndef WIN_TCPSOCKET_H_
#define WIN_TCPSOCKET_H_

#include <stdio.h> 
#include <string.h>
#include <stdlib.h>
#include <memory.h>  
#include <Winsock2.h>  
#pragma comment(lib,"ws2_32.lib")
#include "math.h"
 

using namespace std;

#define BACKLOG          5                


// a class for socket communication
class Tcpsocket
{
public:
	Tcpsocket(const char *s_type, int port_n, int buff_s, const char *s_ip, bool debug);
	Tcpsocket(const char *s_type, int port_n, int buff_s, bool debug);
	void debug_print(const char* fmt, ...);
	int buffsize;
	char socket_type[10];
    // send and receive char data:
	int send_strings(const void *send_buf, int send_data_lens);
	int recv_strings(void *recv_buf);
	int recv_strings(void *recv_buf, int recv_lens);
	void close_socket();
private:
	void copy_str(char *t_str, const char *str);
	int port_num;
	SOCKET conn;
	char server_ip[50];
	bool debug_print_flag;
	int create_conn_server();
	int create_conn_client();
};

#endif