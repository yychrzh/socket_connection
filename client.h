#ifndef CLIENT_H_
#define CLIENT_H_

#include <Winsock2.h>  
#pragma comment(lib,"ws2_32.lib")
#include "math.h"

#define PORT_NUM                 6888

#define DATA_WIDTH               4  // 2 BYTE: range: 

#define MIN_ONE_BIT_NUM          1
#define MAX_ONE_BIT_NUM          127
#define DATA_ONE_BIT_RANGE       127
#define DATA_LOW_RANGE           1
#define DATA_HIGH_RANGE          pow(DATA_ONE_BIT_RANGE, DATA_WIDTH)//(int)(DATA_ONE_BIT_RANGE * (1 - pow(DATA_ONE_BIT_RANGE, DATA_WIDTH)) / (1 - DATA_ONE_BIT_RANGE))

#define MAX_SEND_DATA            127
#define BUFSIZE                  200

#define FLAG_LENGTH              7
#define PARITY_LENGTH            1
#define DATA_LEN_FLAG_LENGTH     1
#define PARITY_POSITION          FLAG_LENGTH
#define DATA_LEN_POSITION        PARITY_POSITION + PARITY_LENGTH
#define DATA_POSITION            DATA_LEN_POSITION + DATA_LEN_FLAG_LENGTH 

#define TOTAL_FLAG_LENGTH        FLAG_LENGTH + PARITY_LENGTH + DATA_LEN_FLAG_LENGTH

#define FLAG_NUM                 5
#define CONNECT_FLAG             1
#define DATA_FLAG                2
#define EPISODE_START_FLAG       3
#define EPISODE_END_FLAG         4
#define TRAIN_END_FLAG           5

//#define DEBUG_PRINT            1

//byte data vector copy
void byte_data_copy(BYTE *output, BYTE *input, int lens);

void byte_data_trans(BYTE *input, float *output, int output_lens);

void float_data_trans(float *input, BYTE *output, int input_lens);

int conn_send_flag(SOCKET sockClient, BYTE *flag);

void conn_recv(SOCKET sockClient, float *output, int *output_lens, int *recv_flag);

void conn_recv_flag(BYTE *recv_data, int *recv_flag);

int conn_send_data(SOCKET sockClient, float *input, int input_lens);

SOCKET create_conn_client();

SOCKET create_conn_server();

void conn_test(SOCKET sockClient);

void conn_close(SOCKET sockClient);

int byte_data_check(BYTE *data, int lens);

void print_byte_data(char *name, BYTE *data, int lens);

void print_float_data(char *name, float *data, int lens);

int parity_check(BYTE *data, int lens);

#endif