#include "linux_tcpsocket.h"


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