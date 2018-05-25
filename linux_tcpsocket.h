#ifndef LINUX_TCPSOCKET_H_
#define LINUX_TCPSOCKET_H_

#include <stdio.h>  
#include <strings.h>
#include <stdlib.h>
#include <unistd.h>  
#include <sys/types.h>  
#include <sys/socket.h>
#include <memory.h>  
#include <arpa/inet.h>  
#include <netinet/in.h>  

#ifndef BYTE
typedef unsigned char BYTE;
#endif

#define BACKLOG               5                   

void debug_print(char *info);
int create_conn_server();
int create_conn_client();
int test_server(int conn);
int test_client(int conn);


// a class for socket communication
class tcpsocket
{
    public:
        tcpsocket(string s_type='server', int port_n=8088, int buff_s=200, char *s_ip='127.0.0.1', bool debug=true);
        void send(char *send_buf, int send_data_lens);
        void recv(char *recv_buf);
        void debug_print(string info);
    private:
	    string socket_type;
	    int port;
	    int buffsize;
	    char server_ip[50];
	    bool debug_print_flag;
	    int create_conn_server();
        int create_conn_client();
};

#endif