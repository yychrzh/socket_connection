#include "win_tcpsocket.h"

Tcpsocket::Tcpsocket(const char *s_type, int port_n, int buff_s, const char *s_ip, bool debug)
{
	// copy parameters
	// strcpy(socket_type, s_type);
	copy_str(socket_type, s_type);
	port_num = port_n;
	buffsize = buff_s;
	// strcpy(server_ip, s_ip);
	copy_str(server_ip, s_ip);
	debug_print_flag = debug;

	if (0 == strcmp(socket_type, "client")){
		conn = create_conn_client();
	}
	else{
		debug_print("socket type input error!\n");
	}
	return;
}

Tcpsocket::Tcpsocket(const char *s_type, int port_n, int buff_s, bool debug)
{
	// copy parameters
	strcpy_s(socket_type, s_type);
	port_num = port_n;
	buffsize = buff_s;
	debug_print_flag = debug;

	if (0 == strcmp(socket_type, "server")){
		conn = create_conn_server();
	}
	else{
		debug_print("socket type input error!\n");
	}
	return;
}

// copy rotation_motor's name:
void Tcpsocket::copy_str(char *t_str, const char *str)
{
	int i = 0;
	for (i = 0; str[i] != '\0' && i < 20; i++) {
		t_str[i] = str[i];
	}
	t_str[i] = '\0';
}

void Tcpsocket::debug_print(const char* fmt, ...)
{
	if (debug_print_flag){
		printf("[DEBUG]");
		va_list ap;
		va_start(ap, fmt);   // point ap to the last parameters after fmt
		vfprintf(stderr, fmt, ap);
		va_end(ap);          // set ap NULL
	}
	return;
}

int Tcpsocket::create_conn_server()
{
	WSADATA wsaData;
	SOCKET sockServer;
	SOCKADDR_IN addrServer;
	SOCKET conn;
	SOCKADDR_IN addrClient;

	WSAStartup(MAKEWORD(2, 2), &wsaData);
	//create Socket  
	sockServer = socket(AF_INET, SOCK_STREAM, 0);
	//create address 
	addrServer.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
	addrServer.sin_family = AF_INET;
	addrServer.sin_port = htons(port_num);

	debug_print("socket bind...\n");
	//bind
	bind(sockServer, (SOCKADDR*)&addrServer, sizeof(SOCKADDR));
	debug_print("socket bind success...\n");
	debug_print("socket listen...\n");
	//listen 
	listen(sockServer, BACKLOG);

	int len = sizeof(SOCKADDR);

	debug_print("conn accept\n");
	//accept
	conn = accept(sockServer, (SOCKADDR*)&addrClient, &len);

	char msg[200] = "\0";
	char port_str[10];
	sprintf_s(port_str, "%d", ntohs(addrClient.sin_port));
	strcpy_s(msg, "accept from client ");
	strcat_s(msg, inet_ntoa(addrClient.sin_addr));
	strcat_s(msg, ":");
	strcat_s(msg, port_str);
	strcat_s(msg, " success !\n");
	debug_print(msg);
	return conn;
}

int Tcpsocket::create_conn_client()
{
	WORD wVersionRequested;
	WSADATA wsaData;
	int err;

	wVersionRequested = MAKEWORD(1, 1);

	err = WSAStartup(wVersionRequested, &wsaData);
	if (err != 0) {
		return -1;
	}

	if (LOBYTE(wsaData.wVersion) != 1 ||
		HIBYTE(wsaData.wVersion) != 1) {
		WSACleanup();
		return -1;
	}

	debug_print("create socket...\n");
	SOCKET sockClient = socket(AF_INET, SOCK_STREAM, 0);

	debug_print("create address...\n");
	SOCKADDR_IN addrSrv;
	addrSrv.sin_addr.S_un.S_addr = inet_addr(server_ip);  //host
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(port_num);

	debug_print("connecting with server...\n");
	err == connect(sockClient, (SOCKADDR*)&addrSrv, sizeof(SOCKADDR));

	if (err == 0){
		char msg[200] = "\0";
		char port_str[10];
		sprintf_s(port_str, "%d", port_num);
		strcpy_s(msg, "connect to server ");
		strcat_s(msg, server_ip);
		strcat_s(msg, ":");
		strcat_s(msg, port_str);
		strcat_s(msg, " success !\n");
		debug_print(msg);
		return sockClient;
	}
	else{
		debug_print("client : connect error !\n");
		return -1;
	}
}

// recv_buf: char pointer that stores the received strings
int Tcpsocket::recv_strings(void *recv_buf)
{
	int recv_data_lens = 0;
	recv_data_lens = recv(conn, (char*)recv_buf, buffsize, 0);
	if (recv_data_lens <= 0){
		debug_print("the connection might have broken !\n");
	}
	return recv_data_lens;
}

// recv data with length: recv_lens bytes:
int Tcpsocket::recv_strings(void *recv_buf, int recv_lens)
{
	int recv_data_lens = 0;
	recv_data_lens = recv(conn, (char*)recv_buf, recv_lens, 0);
	if (recv_data_lens <= 0){
		debug_print("the connection might have broken !\n");
	}
	return recv_data_lens;
}

// send_buf: char pointer that stores the strings will be sent
int Tcpsocket::send_strings(const void *send_buf, int send_data_lens)
{
	int real_send_lens = 0;
	real_send_lens = send(conn, (const char *)send_buf, send_data_lens, 0);
	if (real_send_lens < send_data_lens){
		debug_print("not all data has been sent\n");
	}
	return real_send_lens;
}

void Tcpsocket::close_socket()
{
	if (0 == strcmp(socket_type, "client")){
		printf("shutdown and close socket connection !\n");
		shutdown(conn, 2);
		closesocket(conn);
	}
	return;
}