#ifndef LINUX_PROTOCOL_H_
#define LINUX_PROTOCOL_H_

#include "linux_tcpsocket.h"
#include "number_conversion.h"

/*data format: 0: data_flag;1: data_type;2: parity_flag;3: data_length high;4: data_length low;5~: byte data*/

// bytes
#define TRANS_FLAG_LENGTH        1                                 // send data flag: 1bits
#define DATA_TYPE_LENGTH         1                                 // data type: float or double
#define PARITY_LENGTH            1                                 // parity check of data: 1bits: 0 or 1
#define DATA_LEN_FLAG_LENGTH     2                                 // max data lens: 65535 bytes, 16383 float or 8191 double data

#define FLAG_LENGTH  TRANS_FLAG_LENGTH + DATA_TYPE_LENGTH + PARITY_LENGTH + DATA_LEN_FLAG_LENGTH  // 5

#define TRANS_FLAG_POSITION      0                                           // 0, the index in send data char array
#define DATA_TYPE_POSITION       TRANS_FLAG_POSITION + TRANS_FLAG_LENGTH     // 1, the index in send data char array
#define PARITY_POSITION          DATA_TYPE_POSITION + DATA_TYPE_LENGTH       // 2, the index in send data char array
#define DATA_LEN_POSITION        PARITY_POSITION + PARITY_LENGTH             // 3
#define DATA_POSITION            DATA_LEN_POSITION + DATA_LEN_FLAG_LENGTH    // 5


// data type: float, double
#define DATA_FLOAT32             32
#define DATA_FLOAT64             64

// send data flag: 0~127
#define CONNECTION_FLAG          1
#define DATA_FLAG                2
#define EPISODE_START_FLAG       3
#define EPISODE_END_FLAG         4
#define TERMINATION_FLAG         5

#define EVEN_FLAG                0
#define ODD_FLAG                 1

#define CHAR_BUFFSIZE            2048    // 2048
#define FLOAT_BUFFSIZE           510    // 510      // (int)((BUFFSIZE - FLAG_LENGTH) / FLOAT32_BYTE)
#define DOUBLE_BUFFSIZE          255     // 255      // (int)((BUFFSIZE - FLAG_LENGTH) / FLOAT64_BYTE)


// a class for send float data
class Data_transfer: public Tcpsocket, public Number_conver 
{
    public:
		Data_transfer(const char *s_type, int port_n, int buff_s, const char *s_ip, bool print_flag):Tcpsocket(s_type, port_n, buff_s, s_ip, print_flag), Number_conver(print_flag) {}
        Data_transfer(const char *s_type, int port_n, int buff_s, bool print_flag):Tcpsocket(s_type, port_n, buff_s, print_flag), Number_conver(print_flag) {}
       
	    float recv_float_data[FLOAT_BUFFSIZE];   // max float data length;
		double recv_double_data[DOUBLE_BUFFSIZE]; // max double data length;
	   
	    /**********************************send recv**************************************/
		// recv float or double data, parameters: recv data type and data length
		void recv_data(unsigned char *recv_flag, unsigned char *data_type, int *data_lens);
		// send float data
		void send_data(float *data, int data_lens);
		// send double data
		void send_data(double *data, int data_lens);
		// send flag:
		void send_flag(unsigned char flag);
		
		// recv all data
		// void recv_loop(unsigned char *recv_flag, unsigned char *data_type, int *data_lens);
		
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
	    char send_char[CHAR_BUFFSIZE];
	    char recv_char[CHAR_BUFFSIZE];
		
	    //data array copy: from byte array to char array with data length = lens
        void data_array_copy(char *output, unsigned char *input, int lens);
		//data array copy: from char array to byte array with data length = lens
        void data_array_copy(unsigned char *output, char *input, int lens);
	
		/**********************************data trans*************************************/
	    // data check parity: 0: even; 1: odd
        unsigned char parity_check(unsigned char *data, int lens);
		
	    // from a float array to a send char array []
        void float2send_char(const float *data, int data_lens);
        // from a double array to a send char array []
        void double2send_char(const double *data, int data_lens);
		
		// trans recv char array [] to float array: return data length
        void recv_char2float(int data_lens);
        // trans recv char array [] to double array: return data length
        void recv_char2double(int data_lens);
};

#endif