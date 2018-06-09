#include "linux_protocol.h"
#include "time.h"
#define rand_int(x)  (rand() % x)     // 0~x int
#define rand_float(x)  ((2 * rand() / (float)(RAND_MAX) - 1.0) * x)  // -x ~ x float
#define rand_double(x)  ((2 * rand() / (double)(RAND_MAX) - 1.0) * x)  // -x ~ x double


void time_delay(int time_flag);

void remove_new_line(char *str);

int read_from_screen(char *recv_buf, int buffsize);

void float_test(Data_transfer conn);

void tcp_exchange();


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

void float_test(Data_transfer conn)
{
	int MAX_COUNT = 100;
	int count = 0;
	int error_count = 0;
	int total_lens = 0;
	unsigned char data_type = 0;
	int data_lens = 0;
	unsigned char recv_flag;
	double send_array[250];
	
	memset(send_array, '\0', 250);
	double start_time = ((double)clock() / 1000);
	double current_time = 0;
	srand((unsigned)time(NULL)); 
	
	// waiting for connection flag:
	printf("waiting for connection flag...\n");
	conn.recv_data_byte(&recv_flag, &data_type, &data_lens);
	printf("receive recv_flag: %d, data_type: %d, data_lens: %d\n", recv_flag, data_type, data_lens);
	if (CONNECTION_FLAG != recv_flag){
		printf("connect with client error !\n");
		return;
	} 
	else {
	    printf("connect with client success !\n");
	}
	
	while (1){
		data_lens = rand_int(200) + 50;     // 50 ~ 250
		for (int i = 0;i < data_lens;i++){
			send_array[i] = rand_double(10000);
		}
		printf("send double data to client !\n");
		conn.send_data_byte(send_array, data_lens);
		printf("data sent success, waiting for response !\n");
		
		conn.recv_data_byte(&recv_flag, &data_type, &data_lens);
		printf("receive recv_flag: %d, data_type: %d, data_lens: %d\n", recv_flag, data_type, data_lens);
		if (DATA_FLAG == recv_flag){
			if (DATA_FLOAT32 == data_type){
				for (int i = 0;i < data_lens;i++){
					if (conn.recv_float_data[i] != send_array[i]){
						printf("error emerged in %3d's recv, in the %3d's data, expect %.7f, received %.7f\n", 
						       count, i, send_array[i], conn.recv_float_data[i]);
					    error_count++;
					}
				}
		    }
		    else if (DATA_FLOAT64 == data_type){
			    for (int i = 0;i < data_lens;i++){
					if (conn.recv_double_data[i] != send_array[i]){
						printf("error emerged in %3d's recv, in the %3d's data, expect %.15f, received %.15f\n", 
						       count, i, send_array[i], conn.recv_double_data[i]);
					    error_count++;
					}
				}
		    }
		}
		else {
			printf("didn't receive true flag, return !\n");
			break;
		}
		
		current_time = (double)clock() / 1000 - start_time;
		printf(">>>count: %3d, current time: %.3f sec\n", count, current_time);
		count++;
		total_lens += data_lens;
		
		if (MAX_COUNT == count){
			conn.send_flag_byte(TERMINATION_FLAG);
			printf("data transmission end, with %d data transfered error in total %d data\n", error_count, total_lens);
		    break;
		}
	}
	return;
}


// robot: server, agent: server. first recv from robot, and send to agent !
void tcp_exchange()
{
    int r_port_num = 4096;
	int a_port_num = 5096;
	int buffsize = 2048;
	unsigned char recv_flag;
    unsigned char data_type = 0;
	int data_lens = 0;
	
	printf("create agent server, waiting for agent's client...\n");
	Data_transfer conn_agent("server", a_port_num, buffsize, false);  // first connect with agent
	
	// recv connect flag from agent:
	conn_agent.recv_data_byte(&recv_flag, &data_type, &data_lens);
	printf("receive from agent: recv_flag: %d, data_type: %d, data_lens: %d\n", recv_flag, data_type, data_lens);
	if (CONNECTION_FLAG != recv_flag){
		printf("connect with agent's client error !\n");
		return;
	} 
	else {
	    printf("connect with agent's client success !\n");
	}
	
	printf("create robot's server, waiting for robot's client...\n");
	Data_transfer conn_robot("server", r_port_num, buffsize, false);  // then connect with robot
	
	// recv connect flag from robot:
	conn_robot.recv_data_byte(&recv_flag, &data_type, &data_lens);
	printf("receive from robot: recv_flag: %d, data_type: %d, data_lens: %d\n", recv_flag, data_type, data_lens);
	if (CONNECTION_FLAG != recv_flag){
		printf("connect with robot's client error !\n");
		return;
	} 
	else {
	    printf("connect with robot's client success !\n");
	}
    
    // send episode start flag to agent's client and waiting for data:
	conn_agent.send_flag_byte(EPISODE_START_FLAG);
	
	while (1) {
		// recv data from agent:
        conn_agent.recv_data_byte(&recv_flag, &data_type, &data_lens);
	    printf("receive from agent: recv_flag: %d, data_type: %d, data_lens: %d\n", recv_flag, data_type, data_lens);
	    // send the agent's data to robot:
		switch (recv_flag) {
			case DATA_FLAG:
			    printf("receive data from agent\n");
			    switch (data_type) {
					case DATA_FLOAT32:
					    conn_robot.send_data_byte(conn_agent.recv_float_data, data_lens);
					    break;
					case DATA_FLOAT64:
					    conn_robot.send_data_byte(conn_agent.recv_double_data, data_lens);
					    break;
					default:
					    break;
				}
			    break;
			case TERMINATION_FLAG:
			    printf("receive termination flag from agent\n");
				conn_robot.send_flag_byte(TERMINATION_FLAG);
			    break;
			default:
			    printf("receive undefined flag from agent, return !\n");
			    return;
		}
		
		// recv data from robot:
        conn_robot.recv_data_byte(&recv_flag, &data_type, &data_lens);
	    printf("receive from robot: recv_flag: %d, data_type: %d, data_lens: %d\n", recv_flag, data_type, data_lens);
	    // response agent with robot's data:
		switch (recv_flag) {
			case DATA_FLAG:
			    printf("receive data from robot\n");
			    switch (data_type) {
					case DATA_FLOAT32:
					    conn_agent.send_data_byte(conn_robot.recv_float_data, data_lens);
					    break;
					case DATA_FLOAT64:
					    conn_agent.send_data_byte(conn_robot.recv_double_data, data_lens);
					    break;
					default:
					    break;
				}
			    break;
			case TERMINATION_FLAG:
			    printf("receive termination flag from robot\n");
				conn_agent.send_flag_byte(TERMINATION_FLAG);
			    break;
			default:
			    printf("receive undefined flag from robot, return !\n");
			    return;
		}
	}
	return;	

}

int main(int argc, char *argv[])
{	
	tcp_exchange();
	return 0;
}