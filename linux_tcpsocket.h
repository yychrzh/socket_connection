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

using namespace std;

#define BACKLOG          5                


// a class for socket communication
class Tcpsocket
{
    public:
        Tcpsocket(const char *s_type, int port_n, int buff_s, const char *s_ip, bool debug);
		Tcpsocket(const char *s_type, int port_n, int buff_s, bool debug);
        void debug_print(const char *info);
		int buffsize;
		char socket_type[10];
		void send_strings(const void *send_buf, int send_data_lens);
        int recv_strings(void *recv_buf);
		int recv_strings(void *recv_buf, int recv_lens);
		void close_socket();
    private:
	    int port_num;
		int conn;
	    char server_ip[50];
	    bool debug_print_flag;
	    int create_conn_server();
        int create_conn_client();
};

#endif