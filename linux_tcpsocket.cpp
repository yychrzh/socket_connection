#include "linux_tcpsocket.h"

void debug_print(char *info)
{
#ifdef DEBUG_PRINT
    printf("(debug)");
    printf(info);
#endif
}

// create a connenct server + recv connect_flag:
int create_conn_server()
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
    server_addr.sin_port = htons(TCP_PORT);  
  
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
        debug_print("server : connected\n");
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
	if (conn < 0){
        debug_print("client : create socket error\n");
		return -1;
	}

	/*******************connect()*********************/
	//set server address struct 
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(TCP_PORT);
	server_addr.sin_addr.s_addr = htonl(INADDR_ANY); 
	server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); // inet_addr(SERVER_IP);

	err = connect(conn, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
	if (err == 0){
        debug_print("client : connect to server success\n");
        return conn;
	}
	else{
        debug_print("client : connect error\n");
		return -1;
	}
}