#include "linux_tcpsocket.h"
  
#include <signal.h>                          //add signal processing 

// create a connenct server + recv connect_flag:
int create_conn_server()
{
	struct sockaddr_in server_addr;          //save the server's socket address
    struct sockaddr_in client_addr;          //save the client's socket address
	int sock_server, conn;
    int err;                  
  
    /*****************socket()***************/  
    sock_server = socket(AF_INET, SOCK_STREAM, 0);                    
    if (sock_server < 0)  
    {  
#ifdef DEBUG_PRINT
        printf("server : server socket create error\n");
#endif
        return -1;  
    }  
	
	/*
    //register signal
    sighandler_t ret;  
    ret = signal(SIGTSTP, sig_pipe);  
    if (SIG_ERR == ret)  
    {  
#ifdef DEBUG_PRINT
        printf("信号挂接失败\n");  
#endif
        return -1;  
    }  
	else
	{
#ifdef DEBUG_PRINT
		printf("信号挂接成功\n");
#endif
	}
    */
  
    /******************bind()****************/  
    //init the address struct
	memset(&server_addr, 0, sizeof(server_addr));   
    server_addr.sin_family = AF_INET;                   
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);   
    server_addr.sin_port = htons(TCP_PORT);  
  
    err = bind(sock_server, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));  
    if (err < 0)  
    {  
#ifdef DEBUG_PRINT
        printf("server : bind error\n");  
#endif
        return -1;  
    }  
  
    /*****************listen()***************/  
    err = listen(sock_server, BACKLOG);   //start listen from client 
    if (err < 0)  
    {  
#ifdef DEBUG_PRINT
        printf("server : listen error\n");  
#endif
        return -1;  
    }  

	/*****************accept()***************/
	socklen_t addrlen = sizeof(client_addr);
	//accept return the socket of client
	conn = accept(sock_server, (struct sockaddr *)&client_addr, &addrlen);  
	if (conn < 0)    // error
	{
#ifdef DEBUG_PRINT
		printf("failed to accept from client!\n");
#endif
		return -1;
	}
	else
	{
#ifdef DEBUG_PRINT
		printf("server : connected\n");
#endif
		return conn;
	}
}

// create a connenct client with socket:
int create_conn_client()
{
	sockaddr_in server_addr;
	int err, conn;
	sighandler_t ret;

	/********************socket()*********************/
	conn = socket(AF_INET, SOCK_STREAM, 0);
	if (conn < 0)
	{
#ifdef DEBUG_PRINT
		printf("client : create socket error\n");
#endif
		return -1;
	}
	/*
	//信号处理函数  SIGINT 是当用户按一个 Ctrl-C 建时发送的信号  
	ret = signal(SIGTSTP, sig_pipe);
	if (SIG_ERR == ret)
	{
		printf("信号挂接失败\n");
		return -1;
	}
	else
		printf("信号挂接成功\n");
    */

	/*******************connect()*********************/
	//set server address struct 
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(TCP_PORT);
	server_addr.sin_addr.s_addr = htonl(INADDR_ANY); 
	server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // inet_addr(SERVER_IP);

	err = connect(conn, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
	if (err == 0)
	{
#ifdef DEBUG_PRINT
		printf("client : connect to server success\n");
#endif
	}
	else
	{
#ifdef DEBUG_PRINT
		printf("client : connect error\n");
#endif
		return -1;
	}
	return conn;
}

// test to recv data from client and respond:
int test_server(int conn)
{
	int recv_data_lens = 0;
	BYTE recv_buf[BUFFSIZE];
	// unsigned char recv_buf[BUFFSIZE];

	memset(recv_buf, '\0', BUFFSIZE);
	printf("connect with server...");
	recv(conn, (char *)&recv_buf, BUFFSIZE, 0);

	printf("\nASC: ");
	for (int i=0;recv_buf[i] != '\0';i++)
	{
		printf("%c", recv_buf[i]);
		recv_data_lens++;
	}

	printf("\nData: ");
	for (int i = 0; recv_buf[i] != '\0'; i++)
	{
		printf("%d", recv_buf[i]);
	}
	printf("\nrecv data lens: %d", recv_data_lens);

	while (1)
	{
		;
	}
}

//test to send to server and recv respond msg
int test_client(int conn)
{
	int send_data_lens = 0;
    BYTE send_buf[BUFFSIZE];
	// unsigned char send_buf[BUFFSIZE];

	memset(send_buf, '\0', BUFFSIZE);

    // read from standard input
	int size = 0;
	size = read(0, (char*)&send_buf, BUFFSIZE);

	printf("\nsendASC: ");
	for (int i = 0; send_buf[i] != '\0'; i++)
	{
		printf("%c", send_buf[i]);
		send_data_lens++;
	}

	printf("\nsenddata: ");
	for (int i = 0; send_buf[i] != '\0'; i++)
	{
		printf("%d", send_buf[i]);
	}

	send(conn, (char*)&send_buf, send_data_lens, 0);

	while (1)
	{
		;
	}
}

int main(int argc, char *argv[])
{
	int test_flag = 0;
	int conn;
	
	if (0 == test_flag)
	{
		conn = create_conn_server();
		test_server(conn);
	}
	else
	{
		conn = create_conn_client();
		test_client(conn);
	}

}