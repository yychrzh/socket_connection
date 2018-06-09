#include "linux_tcpsocket.h"


Tcpsocket::Tcpsocket(const char *s_type, int port_n, int buff_s, const char *s_ip, bool debug)
{
    // copy parameters
	strcpy(socket_type, s_type);
    port_num = port_n;
    buffsize = buff_s;
    strcpy(server_ip, s_ip);
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
	strcpy(socket_type, s_type);
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

void Tcpsocket::debug_print(const char *info)
{
    if (debug_print_flag){
		printf("(tcp %s)", socket_type);
        printf("%s", info);
    }
	return;
}

int Tcpsocket::create_conn_server()
{
	struct sockaddr_in server_addr;          //save the server's socket address
    struct sockaddr_in client_addr;          //save the client's socket address
	int sock_server, conn, err;

    /*****************socket()***************/
    sock_server = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_server < 0){
        debug_print("server : server socket create error\n");
        return -1;
    }

    /******************bind()****************/
    //init the address struct
	memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port_num);

    err = bind(sock_server, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
    if (err < 0){
        debug_print("server : bind error\n");
        return -1;
    }

    /*****************listen()***************/
    err = listen(sock_server, BACKLOG);   //start listen from client
    if (err < 0){
        debug_print("server : listen error\n");
        return -1;
    }

	/*****************accept()***************/
	socklen_t addrlen = sizeof(client_addr);
	// accept return the socket of client
	conn = accept(sock_server, (struct sockaddr *)&client_addr, &addrlen);
	if (conn < 0){
        debug_print("failed to accept from client!\n");
		return -1;
	}
	else{
		char msg[200] = "\0";
		char port_str[10];
		// test: printf("h: %d; n: %d\n", htons(ntohs(9999)), ntohs(htons(9999)));
		sprintf(port_str, "%d", ntohs(client_addr.sin_port));
		strcpy(msg, "accept from client ");
		strcat(msg, inet_ntoa(client_addr.sin_addr));
		strcat(msg, ":");
		strcat(msg, port_str);
		strcat(msg, " success !\n");
        debug_print(msg);
		return conn;
	}
}

int Tcpsocket::create_conn_client()
{
    sockaddr_in server_addr;
	int err, conn;

	/********************socket()*********************/
	conn = socket(AF_INET, SOCK_STREAM, 0);
	if (conn < 0){
        debug_print("client : create socket error\n");
		return -1;
	}

	/*******************connect()*********************/
	//set server address struct 
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(port_num);
	server_addr.sin_addr.s_addr = inet_addr(server_ip); 

	err = connect(conn, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
	if (err == 0){
		char msg[200] = "\0";
		char port_str[10];
		sprintf(port_str, "%d", port_num);
		strcpy(msg, "connect to server ");
		strcat(msg, server_ip);
		strcat(msg, ":");
		strcat(msg, port_str);
		strcat(msg, " success !\n");
        debug_print(msg);
        return conn;
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
	recv_data_lens = recv(conn, recv_buf, buffsize, 0);
	if (recv_data_lens <= 0){
		debug_print("the connection might have broken !\n");
	}
	return recv_data_lens;
}

// recv data with length: recv_lens bytes:
int Tcpsocket::recv_strings(void *recv_buf, int recv_lens)
{
	int recv_data_lens = 0;
	recv_data_lens = recv(conn, recv_buf, recv_lens, 0);
	if (recv_data_lens <= 0){
		debug_print("the connection might have broken !\n");
	}
	return recv_data_lens;
}

// send_buf: char pointer that stores the strings will be sent
void Tcpsocket::send_strings(const void *send_buf, int send_data_lens)
{
	int real_send_lens = 0;
	real_send_lens = send(conn, send_buf, send_data_lens, 0);
	if (real_send_lens < send_data_lens){
		debug_print("not all data has been sent\n");
	}
	return;
}

void Tcpsocket::close_socket()
{
	if (0 == strcmp(socket_type, "client")){
		printf("shutdown and close socket connection !\n");
		shutdown(conn, 2);
	    close(conn);
	}
	return;
}
