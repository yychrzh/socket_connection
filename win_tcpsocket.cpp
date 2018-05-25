#include "win_tcpsocket.h"

//create socket connection as client
SOCKET create_conn_client()
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

	printf("\ncreate socket");
	SOCKET sockClient = socket(AF_INET, SOCK_STREAM, 0);

	printf("\ncreate address");
	SOCKADDR_IN addrSrv;
	addrSrv.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");  //host
	//addrSrv.sin_addr.S_un.S_addr = inet_addr("219.231.146.160");  //server
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(PORT_NUM);

	printf("\nconnecting...");
	connect(sockClient, (SOCKADDR*)&addrSrv, sizeof(SOCKADDR));
	printf("\nconnect success");

	//send connect flag
	printf("\nsend connect flag...");

	int send_check_flag = conn_send_flag(sockClient, connect_flag);

	if (send_check_flag != 1)
	{
		printf("\ncreate socket connection error!");
		while (1)
		{
			;
		}
	}

	//test the connection
	//conn_test();
	return sockClient;
}

//create socket connection as server
SOCKET create_conn_server()
{
	WSADATA wsaData;
	SOCKET sockServer;
	SOCKADDR_IN addrServer;
	SOCKET conn;
	SOCKADDR_IN addr;

	WSAStartup(MAKEWORD(2, 2), &wsaData);
	//create Socket  
	sockServer = socket(AF_INET, SOCK_STREAM, 0);
	//create address 
	addrServer.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
	addrServer.sin_family = AF_INET;
	addrServer.sin_port = htons(PORT_NUM);

	printf("\nsocket bind");
	//bind
	bind(sockServer, (SOCKADDR*)&addrServer, sizeof(SOCKADDR));
	printf("\nsocket bind success");
	printf("\nsocket listen");
	//listen 
	listen(sockServer, 5);

	int len = sizeof(SOCKADDR);

	printf("\nconn accept");
	//accept
	conn = accept(sockServer, (SOCKADDR*)&addr, &len);

	//recv connect flag:
	int recv_flag = 0;
	int recv_data_lens = 0;
	BYTE recv_data[BUFSIZE];

	//while (1){
	printf("connect with server...");
	conn_recv(conn, recv_data, recv_data_lens, recv_flag);
	if (recv_flag == CONNECT_FLAG)
	{
		printf("connect with server success");
		//break;
	}

	//delay:
	int n = 0;
	for (int i = 0; i < 500; i++)
	{
		for (int j = 0; j < 1000; j++)
		{
			n = i - j;
		}
	}

	//send connect flag
	printf("\nsend connect flag...");

	int send_check_flag = conn_send_flag(conn, connect_flag);

	if (send_check_flag != 1)
	{
		printf("create socket connection error!");
		while (1)
		{
			;
		}
	}

	//test the connection
	//conn_test();
	return conn;
}

void conn_test(SOCKET sockClient)
{
	//recv data from server
	float recv_data[30];
	int recv_flag = 0;
	int recv_data_lens = 0;

	printf("\ntest the socket connection...");

	//recv data from server:
	conn_recv(sockClient, recv_data, &recv_data_lens, &recv_flag);
	printf("\nrecv_flag: %d", recv_flag);
	printf("\nfloat data: ");
	for (int i = 0; i < recv_data_lens; i++)
	{
		printf("%f ", recv_data[i]);
	}

	//send data to server: 
	printf("\nsend data to server...");
	float a[5] = { -1, -0.125, 0, 0.37, 1 };
	int data_lens = sizeof(a) / sizeof(float);
	conn_send_data(sockClient, a, data_lens);
}

void conn_close(SOCKET sockClient)
{
	closesocket(sockClient);
	WSACleanup();
}