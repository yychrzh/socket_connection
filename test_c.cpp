#include "linux_tcpsocket.h"

void time_delay(int time_flag);

void remove_new_line(char *str, int lens);

int read_from_screen(char *recv_buf, int buffsize);

void char_test();

void server_test(Tcpsocket conn);

void client_test(Tcpsocket conn);


void time_delay(int time_flag)  // delay 1000 * time_flag
{
	int k = 0;
	for (int i = 0; i < time_flag; i++)
	{
		k = 0;
		for (int j = 0; j < 1000; j++)
		{
	        k++;
		}
	}
}

//remove '\n'
void remove_new_line(char *str)
{
	for (int i = 0;str[i] != '\0';i++){
		if ('\n' == str[i]){
			str[i] = '\0';   //remove '\n'
		}
	}
}

// read data from screen without newline:
int read_from_screen(char *recv_buf, int buffsize)
{
	int read_data_lens = 0;
	read_data_lens = read(0, recv_buf, buffsize);
	remove_new_line(recv_buf);
	return read_data_lens;
}

// test in client mode:
void char_test(Tcpsocket conn)
{
    char recv_buf[conn.buffsize];
	int data_bytes_size = 0;
    char data[5] = {-128, -64, 0, 64, 127};
	
	printf("send five typical char data to server: \n");
	conn.send_strings(data, 5);

	data_bytes_size = conn.recv_strings(recv_buf);
	if (data_bytes_size <= 0){
		printf("connection might have broken !\n");
	}
	printf("receive from client:\n");
	for (int i = 0;i < 5;i++){
		printf("%d ", recv_buf[i]);
	}
    printf("\n");

	return;
}
	
// test send and receive data with or from clent
void server_test(Tcpsocket conn)
{
	char recv_buf[conn.buffsize];
	int data_bytes_size = 0;
	int recv_lens = 0;

	memset(recv_buf, '\0', conn.buffsize);
	
	while (true)
	{
		data_bytes_size = conn.recv_strings(recv_buf);
		if (data_bytes_size <= 0){
				break;
		}
		recv_lens = strlen(recv_buf) + 1;
		printf("receive from client：%s\n", recv_buf);
		printf("receive data lens: %d\n", recv_lens);
		time_delay(50);
		conn.send_strings(recv_buf, recv_lens);
	}
}

// test send and receive data with or from server
void client_test(Tcpsocket conn)
{
	char recv_buf[conn.buffsize];
	int data_bytes_size = 0;
	int input_lens = 0;
	int test_times = 0;

	memset(recv_buf, '\0', conn.buffsize);
	
	while (true)
	{
		test_times++;
	    printf("please input one line data:\n");
		data_bytes_size = read_from_screen(recv_buf, conn.buffsize); 
		input_lens = strlen(recv_buf) + 1;
		if (data_bytes_size > 0){
		    conn.send_strings(recv_buf, input_lens);
			printf("send data lens: %d\n", input_lens);
            data_bytes_size = conn.recv_strings(recv_buf);
			if (data_bytes_size <= 0){
				break;
			}
		    printf("receive from server: %s\n", recv_buf);
		    time_delay(50);					
		}
		if (test_times > 1){
			conn.close_socket();
			break;
		}
	}
}

int main(int argc, char *argv[])
{
	char socket_type[10];
	char socket_port_num[10];
	char server_ip[50];
	int port_num = 8088;
	int buffsize = 200;
	int read_lens = 0;
	
	memset(socket_port_num, '\0', 10);
	printf("please input socket port_num(default:8088, >2048):\n");
	read_lens = read_from_screen(socket_port_num, 10); // read a line from screen
	if (read_lens > 0)
	{
		if (socket_port_num[0] != '\0'){
			int num = atoi(socket_port_num);  
			if (num > 2048){
				port_num = num;
			}
		}
	}
	
	memset(socket_type, '\0', 10);
	printf("please input socket type(server or client):\n");
	read_lens = read_from_screen(socket_type, 10); // read a line from screen
	
	if (read_lens > 0){
		if (0 == strcmp(socket_type, "server")){
			printf("create socket server, waiting for client:\n");
			Tcpsocket conn("server", port_num, buffsize, true);
			server_test(conn);
		}
		else if (0 == strcmp(socket_type, "client")){
			printf("create socket client, please input server ip(default: '127.0.0.1'):\n");
			memset(server_ip, '\0', 10);
	        read_lens = read_from_screen(server_ip, 50); // read a line from screen
			if (read_lens > 0){
				if (server_ip[0] == '\0'){
					strcpy(server_ip, "127.0.0.1");
				}
				Tcpsocket conn("client", port_num, buffsize, server_ip, true);
				// client_test(conn);
				char_test(conn);
			}
			else{
				printf("inpput server ip wrong !\n");
			}
		}
		else{
			printf("company with server: %d\n", strcmp(socket_type, "server"));
			printf("company with client: %d\n", strcmp(socket_type, "client"));
			printf("%s\n", socket_type);
		}
	}
	else{
		printf("input socket_type wrong !\n");
	}

	return 0;
}