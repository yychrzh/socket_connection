#include "client.h"
#include "stdio.h"
#include "string.h"

BYTE connect_flag[FLAG_LENGTH] =       "CONNECT";
BYTE data_flag[FLAG_LENGTH] =          "DATA   ";
BYTE episode_start_flag[FLAG_LENGTH] = "E_START";
BYTE episode_end_flag[FLAG_LENGTH] =   "E_END  ";
BYTE train_end_flag[FLAG_LENGTH] =     "T_END  ";

// flag pointer 
BYTE *conn_flag[FLAG_NUM] = { connect_flag, data_flag, episode_start_flag, 
                                          episode_end_flag, train_end_flag};

//print data vector: name:"name\0", data:data pointer, lens: data length
void print_byte_data(char *name, BYTE *data, int lens)
{
	printf("\n%s: [ ", name);
	for (int i = 0; i < lens; i++)
	{
		printf("%d ", data[i]);
	}
	printf("]");
}

//print data vector: name:"name\0", data:data pointer, lens: data length
void print_float_data(char *name, float *data, int lens)
{
	printf("\n%s: [ ", name);
	for (int i = 0; i < lens; i++)
	{
		printf("%f ", data[i]);
	}
	printf("]");
}

//parity check of the data
int parity_check(BYTE *data, int lens)
{
	int parity_num = 0;
	for (int i = 0; i < lens; i++)
	{
		parity_num += (data[i] % 2);
	}

#ifdef DEBUG_PRINT
	printf("\nparity_num: %d", parity_num);
#endif

	if (parity_num % 2)
	{
		return 1;     //odd
	}
    
	return 0;        //even
}

int byte_data_check(BYTE *data, int lens)
{
	for (int i = 0; i < lens; i++)
	{
		if (data[i] < 1 || data[i] > 127)
		{
			printf("\nerror: the %dth num in the data is not in range[1, 127]");
			return 0;
		}
	}
	return 1;
}

//byte data vector copy
void byte_data_copy(BYTE *output, BYTE *input, int lens)
{
	for (int i = 0; i < lens; i++)
	{
		output[i] = input[i];
	}
}

//transfer byte data in range [1, DATA_HIGH_RANGE] to float data in range [-1, 1] 
void byte_data_trans(BYTE *input, float *output, int output_lens)
{
	float temp = 0;
	int i = 0;
	int j = 0;

#ifdef DEBUG_PRINT
	printf("\ntrans byte data to float:");
	print_byte_data("input\0", input, output_lens * DATA_WIDTH);
#endif

	for (i = 0; i < output_lens; i++)
	{
		temp = 1;
		for (j = 0; j < DATA_WIDTH; j++)
		{
			temp += (input[i*DATA_WIDTH + j] - 1) * pow(DATA_ONE_BIT_RANGE, j);
		}

		temp = (temp - 1) / (DATA_HIGH_RANGE - 1) * 2 - 1;
		output[i] = temp;
	}

#ifdef DEBUG_PRINT
	print_float_data("output\0", output, output_lens);
#endif
}

//transfer float data in range [-1, 1] to byte data in range [1, DATA_HIGH_RANGE] 
void float_data_trans(float *input, BYTE *output, int input_lens)
{
	int temp = 0;
	int div = 0;
	int rem = 0;
	int i = 0;
	int j = 0;
	BYTE data[DATA_WIDTH];
	int output_lens = 0;

#ifdef DEBUG_PRINT
	printf("\ntrans float data to byte:");
	print_float_data("input\0", input, input_lens);
	printf("\ninput_lens: %d", input_lens);
	printf("\n");
#endif

	for (i = 0; i < input_lens; i++)
	{
		temp = ((float)(input[i] + 1) / 2 * (DATA_HIGH_RANGE - 1) + 1);  // [-1, 1] to [1, DATA_HIGH_RANGE]
#ifdef DEBUG_PRINT
		printf("|%d: %d ", i, temp);
#endif

		for (j = 0; j < DATA_WIDTH; j++)
		{
			div = (temp-1) / DATA_ONE_BIT_RANGE;
			rem = (temp-1) % DATA_ONE_BIT_RANGE;
			data[j] = rem+1;
			temp = div+1;
#ifdef DEBUG_PRINT
			printf("%d ", data[j]);
#endif
		}

		byte_data_copy(&output[i*DATA_WIDTH], data, DATA_WIDTH);
		output_lens += DATA_WIDTH;
	}

#ifdef DEBUG_PRINT
	print_byte_data("output\0", output, output_lens);
	printf("\noutput_lens: %d", output_lens);
	printf("\ntrans success");
#endif
}

//recv data from server and judge the recv flag
void conn_recv(SOCKET sockClient, float *output, int *output_lens, int *recv_flag)
{
	int data_lens = 0;
	int parity_flag = 0;

	BYTE recv_data[BUFSIZE];
	BYTE recv_buf[BUFSIZE];

	recv(sockClient, recv_buf, BUFSIZE, 0);              //recv data from server

    //get the recv_flag:
	conn_recv_flag(recv_buf, recv_flag);
	//printf("\nrecv_flag_num: %d ", *recv_flag);

	if (DATA_FLAG == *recv_flag)
	{
		//get data lens
		for (int i = 0; i < DATA_LEN_FLAG_LENGTH; i++)
		{
			data_lens += recv_buf[DATA_LEN_POSITION + i] * pow(DATA_ONE_BIT_RANGE, i);
		}
		//get parity flag;
		for (int i = 0; i < PARITY_LENGTH; i++)
		{
			parity_flag += recv_buf[PARITY_POSITION + i] * pow(DATA_ONE_BIT_RANGE, i);
		}
		//check the parity
		if ((parity_flag - 1) != parity_check(&recv_buf[DATA_POSITION], data_lens*DATA_WIDTH))
		{
			printf("\nerror: parity error, data is wrong, praity_flag: %d, true_flag: %d", parity_flag, parity_check(&recv_buf[DATA_POSITION], data_lens*DATA_WIDTH));
		}

		*output_lens = data_lens;

#ifdef DEBUG_PRINT
		print_byte_data("recv_buf\0", recv_buf, TOTAL_FLAG_LENGTH + data_lens*DATA_WIDTH);
#endif

		byte_data_copy(recv_data, &recv_buf[DATA_POSITION], data_lens*DATA_WIDTH);  //remove flag
		byte_data_trans(recv_data, output, data_lens);  //trans BYTE data to output float data
	}
}

//get the recv_flag
void conn_recv_flag(BYTE *recv_data, int *recv_flag)
{
	int i, j;
	BYTE flag[FLAG_LENGTH];
	byte_data_copy(flag, recv_data, FLAG_LENGTH);

	for (i = 0; i < FLAG_NUM; i++)
	{
		for (j = 0; j < FLAG_LENGTH; j++)
		{
			if (flag[j] != conn_flag[i][j])
				break;
		}
		if (j == FLAG_LENGTH)
		{
			*recv_flag = i+1;
			break;
		}
	}
}

// send flag to server
int conn_send_flag(SOCKET sockClient, BYTE *flag)
{
	BYTE flag_buf[FLAG_LENGTH];
	byte_data_copy(flag_buf, flag, FLAG_LENGTH);

#ifdef DEBUG_PRINT
	print_byte_data("send_buf\0", flag_buf, FLAG_LENGTH);
#endif

	int byte_check_flag = byte_data_check(flag_buf, FLAG_LENGTH);
	if (byte_check_flag != 1)
	{
		return 0;
	}

	send(sockClient, (char *)&flag_buf, FLAG_LENGTH, 0);
	return 1;
}

//send data to the client
int conn_send_data(SOCKET sockClient, float *input, int input_lens)
{
	int data_lens = input_lens;
	int parity_flag = 0;
	BYTE send_buf[BUFSIZE];           
	BYTE send_data[BUFSIZE];
	BYTE *flag = data_flag;

	if (input_lens > MAX_SEND_DATA)
	{
		printf("\nerror: send too much data!");
	}

	float_data_trans(input, send_data, data_lens);                                    //trans input float data to BYTE data

	parity_flag = parity_check(send_data, data_lens * DATA_WIDTH) + 1;                //cal parity_flag

	byte_data_copy(send_buf, flag, FLAG_LENGTH);                                      //add data_flag
#ifdef DEBUG_PRINT
	print_byte_data("add flag to send_buf\0", send_buf, FLAG_LENGTH);
#endif

	byte_data_copy(&send_buf[PARITY_POSITION], &parity_flag, PARITY_LENGTH);           //add parity_flag
#ifdef DEBUG_PRINT
	print_byte_data("add parity to send_buf\0", send_buf, FLAG_LENGTH + PARITY_LENGTH);
#endif

	byte_data_copy(&send_buf[DATA_LEN_POSITION], &data_lens, DATA_LEN_FLAG_LENGTH);    //add data_lens_flag
#ifdef DEBUG_PRINT
	print_byte_data("add data_len_flag to send_buf\0", send_buf, FLAG_LENGTH + PARITY_LENGTH + DATA_LEN_FLAG_LENGTH);
#endif

	byte_data_copy(&send_buf[DATA_POSITION], send_data, data_lens * DATA_WIDTH);      //add data

	int send_data_lens = FLAG_LENGTH + PARITY_LENGTH + DATA_LEN_FLAG_LENGTH + data_lens * DATA_WIDTH;

#ifdef DEBUG_PRINT
	print_byte_data("send_buf\0", send_buf, send_data_lens);
	printf("\nsend_buf_lens: %d", send_data_lens);
#endif

	int byte_check_flag = byte_data_check(send_buf, send_data_lens);
	if (byte_check_flag != 1)
	{
		return 0;
	}

	send(sockClient, (char*)&send_buf, send_data_lens, 0);
	return 1;
}

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

	printf("\conn accept");
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
