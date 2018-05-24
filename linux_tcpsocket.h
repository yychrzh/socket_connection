#ifndef LINUX_TCPSOCKET_H_
#define LINUX_TCPSOCKET_H_

#include <stdio.h>  
#include <strings.h>  
#include <unistd.h>  
#include <sys/types.h>  
#include <sys/socket.h>  
#include <stdlib.h>  
#include <memory.h>  
#include <arpa/inet.h>  
#include <netinet/in.h>  

#ifndef BYTE
typedef unsigned char BYTE;
#endif

#define TCP_PORT              11910             //define commuicate port
#define BACKLOG               5                   
#define BUFFSIZE              1024  
#define SERVER_IP             "127.0.0.1"
#define DEBUG_PRINT           1

int create_conn_server();
int create_conn_client();
int test_server(int conn);
int test_client(int conn);

#endif