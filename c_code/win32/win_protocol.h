#ifndef LINUX_PROTOCOL_H_
#define LINUX_PROTOCOL_H_

#include "win_tcpsocket.h"
#include "number_conversion.h"

/*data format: 0: data_flag;1: data_type;2: parity_flag;3: data_length high;4: data_length low;5~: byte data*/
// data bytes format
#define TRANS_FLAG_LENGTH           1                                 // send data flag: 1bits
#define DATA_TYPE_LENGTH            1                                 // data type: float or double
#define PARITY_LENGTH               1                                 // parity check of data: 1bits: 0 or 1
#define DATA_LEN_FLAG_LENGTH        2                                 // max data lens: 65535 bytes, 16383 float or 8191 double data

#define FLAG_LENGTH  TRANS_FLAG_LENGTH + DATA_TYPE_LENGTH + PARITY_LENGTH + DATA_LEN_FLAG_LENGTH  // 5

#define TRANS_FLAG_POSITION         0                                           // 0, the index in send data char array
#define DATA_TYPE_POSITION          1 // TRANS_FLAG_POSITION + TRANS_FLAG_LENGTH     // 1, the index in send data char array
#define PARITY_POSITION             2 // DATA_TYPE_POSITION + DATA_TYPE_LENGTH       // 2, the index in send data char array
#define DATA_LEN_POSITION           3 // PARITY_POSITION + PARITY_LENGTH             // 3
#define DATA_POSITION               5 // DATA_LEN_POSITION + DATA_LEN_FLAG_LENGTH    // 5

// #define TRANS_FLAG_POSITION      0                                               // 0
#define FUNC_NAME_FLAG_POSITION     1    // TRANS_FLAG_POSITION + TRANS_FLAG_LENGTH         // 1
#define PARAM_NUM_FLAG_POSITION     2    // FUNC_NAME_FLAG_POSITION + FUNC_NAME_FLAG_LENGTH // 2
#define DATA_LEN_FLAG_POSITION      3    // PARAM_NUM_FLAG_POSITION + PARAM_NUM_FLAG_LENGTH // 3
#define FUNC_NAME_POSITION          4    // DATA_LEN_FLAG_POSITION + DATA_LEN_FLAG_LENGTH   // 4 


// data type: float, double
#define DATA_FLOAT32                32
#define DATA_FLOAT64                64
#define DATA_CHAR                   8
#define DATA_UCHAR                  9
#define DATA_INT                    32 + 1
#define DATA_LONG                   64 + 1

// send data flag: 0~127
#define CONNECTION_FLAG             1
#define DATA_FLAG                   2
#define EPISODE_START_FLAG          3
#define EPISODE_END_FLAG            4
#define TERMINATION_FLAG            5
#define CONTROL_FLAG                6
#define RESPONSE_FLAG               7

#define EVEN_FLAG                   0
#define ODD_FLAG                    1

#define CHAR_BUFFSIZE               2048    // 2048
#define FLOAT_BUFFSIZE              510     // 510      // (int)((BUFFSIZE - FLAG_LENGTH) / FLOAT32_BYTE)
#define DOUBLE_BUFFSIZE             255     // 255      // (int)((BUFFSIZE - FLAG_LENGTH) / FLOAT64_BYTE)

#define MAX_BUFFSIZE                520 * 520


typedef struct Function_name{
	int module_name_lens;
	unsigned char module_name[30];
	int func_name_lens;
	unsigned char func_name[30];
}Func_name;


typedef struct Parameter_list{
	int params_nums;
	int float_params_nums;
	int double_params_nums;
	unsigned char data_type_list[200];
	float float_params[200];
	double double_params[200];
}Param_list;


// a class for send float data
class Data_transfer : public Tcpsocket, public Number_conver
{
public:
	Data_transfer(const char *s_type, int port_n, int buff_s, const char *s_ip, bool print_flag) :Tcpsocket(s_type, port_n, buff_s, s_ip, print_flag), Number_conver(print_flag) {}
	Data_transfer(const char *s_type, int port_n, int buff_s, bool print_flag) :Tcpsocket(s_type, port_n, buff_s, print_flag), Number_conver(print_flag) {}

	// handshake:
	void handshake();

	float recv_float_data[FLOAT_BUFFSIZE];      // max float data length;
	double recv_double_data[DOUBLE_BUFFSIZE];   // max double data length;
	unsigned char recv_uchar_data[MAX_BUFFSIZE];  
  
	/**********************************send recv byte**************************************/
	// save parmeters
	Func_name func_name;
	Param_list param_list;

	// receive all data if there are data rest:
	void recv_rest_data(int all_lens, int received_lens);

	// recv data flag, parameters: recv data type and data length: processing
	void recv_data_flag(unsigned char *data_type, int *data_lens, int received_lens);

	// recv control flag: processing
	void recv_control_flag(int *data_lens, int received_lens);

	// recv float or double data, parameters: recv data type and data length
	void recv_data(unsigned char *recv_flag, unsigned char *data_type, int *data_lens);
	// send float data:
	void send_data(float *data, int data_lens);
	// send double data:
	void send_data(double *data, int data_lens);
	// send unsigend char data:
	void send_data(unsigned char *data, int data_lens);
	// send flag:
	void send_flag(unsigned char flag);

	/*********************************data copy**************************************/
	//data array copy: from byte array to byte array with data length = lens
	void data_array_copy(unsigned char *output, unsigned char *input, int lens);
	//data array copy: from char array to char array with data length = lens
	void data_array_copy(char *output, char *input, int lens);
	//data array copy: from float array to float array with data length = lens
	void data_array_copy(float *output, float *input, int lens);
	//data array copy: from double array to double array with data length = lens
	void data_array_copy(double *output, double *input, int lens);

private:

	// unsigned char send_byte[CHAR_BUFFSIZE];
	// unsigned char recv_byte[CHAR_BUFFSIZE];
	unsigned char send_byte[MAX_BUFFSIZE];
	unsigned char recv_byte[MAX_BUFFSIZE];

	//data array copy: from byte array to char array with data length = lens
	void data_array_copy(char *output, unsigned char *input, int lens);
	//data array copy: from char array to byte array with data length = lens
	void data_array_copy(unsigned char *output, char *input, int lens);

	/**********************************data trans*************************************/
	// data check parity: 0: even; 1: odd
	unsigned char parity_check(unsigned char *data, int lens);
	unsigned char parity_check(const unsigned char *data, int lens);

	// from a float array to a send byte array []
	void float2send_byte(const float *data, int data_lens);
	// from a double array to a send byte array []
	void double2send_byte(const double *data, int data_lens);
	// from a unsigned char array to a send byte array []
	void uchar2send_byte(const unsigned char *data, int data_lens);

	// trans recv byte array [] to float array: return data length
	void recv_byte2float(int data_lens);
	// trans recv byte array [] to double array: return data length
	void recv_byte2double(int data_lens);
	// trans recv byte array [] to unsigned char array: return data length
	void recv_byte2uchar(int data_lens);
};

#endif