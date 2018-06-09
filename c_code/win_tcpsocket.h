#ifndef WIN_TCPSOCKET_H_
#define WIN_TCPSOCKET_H_

#include <Winsock2.h>  
#pragma comment(lib,"ws2_32.lib")
#include "math.h"
#include "stdio.h"
#include "string.h"

#ifndef BYTE
typedef unsigned char BYTE;
#endif

#define PORT_NUM                 6888


SOCKET create_conn_client();

SOCKET create_conn_server();

void conn_test(SOCKET sockClient);

void conn_close(SOCKET sockClient);

#endif
