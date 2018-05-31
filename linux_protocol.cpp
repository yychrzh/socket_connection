#include "linux_protocol.h"


/*************************************************data_copy**************************************************/
//data array copy: from byte array to byte array with data length = lens
void Data_transfer::data_array_copy(unsigned char *output, unsigned char *input, int lens)
{
	for (int i = 0; i < lens; i++)
	{
		output[i] = input[i];
	}    	
}

//data array copy: from byte array to char array with data length = lens
void Data_transfer::data_array_copy(char *output, unsigned char *input, int lens)
{
    for (int i = 0; i < lens; i++)
	{
		output[i] = byte2char(input[i]);
	}
}

//data array copy: from char array to byte array with data length = lens
void Data_transfer::data_array_copy(unsigned char *output, char *input, int lens)
{
	for (int i = 0; i < lens; i++)
	{
		output[i] = char2byte(input[i]);
	}
}

//data array copy: from char array to char array with data length = lens
void Data_transfer::data_array_copy(char *output, char *input, int lens)
{
	for (int i = 0; i < lens; i++)
	{
		output[i] = input[i];
	}	
}
		
//data array copy: from float array to float array with data length = lens
void Data_transfer::data_array_copy(float *output, float *input, int lens)
{
    for (int i = 0; i < lens; i++)
	{
		output[i] = input[i];
	}
}

//data array copy: from double array to double array with data length = lens
void Data_transfer::data_array_copy(double *output, double *input, int lens)
{
	for (int i = 0; i < lens; i++)
	{
		output[i] = input[i];
	}
}

/*************************************************data_trans**************************************************/
//parity check of the data
unsigned char Data_transfer::parity_check(unsigned char *data, int lens)
{
	int parity_num = 0;
	for (int i = 0; i < lens; i++)
	{
		parity_num += (data[i] % 2);
	}

	if (parity_num % 2)
	{
		return ODD_FLAG;     //odd
	}
    
	return EVEN_FLAG;        //even
}

// trans a float array to a send char array []: len(send_char) = data_lens + 5, data_lens < 65535 
void Data_transfer::float2send_char(const float *data, int data_lens)
{
	unsigned char float_bytes[FLOAT32_BYTE * data_lens]; // bytes
	
	memset(float_bytes, '\0', FLOAT32_BYTE * data_lens);
	
	// trans float data array to byte data array:
	float_array2bys(data, float_bytes, data_lens); 

    Number_conver::debug_print("float_bytes", float_bytes, data_lens * FLOAT32_BYTE);	
	
	// add send flag:
	send_char[TRANS_FLAG_POSITION] = byte2char(DATA_FLAG);   // data
	// add data type:
	send_char[DATA_TYPE_POSITION] = byte2char(DATA_FLOAT32);
	// add parity flag:
    send_char[PARITY_POSITION] = byte2char(parity_check(float_bytes, FLOAT32_BYTE * data_lens));
	// add data length's high byte:
    send_char[DATA_LEN_POSITION] = byte2char((unsigned char)(data_lens / 256));
	// add data length's low byte:
    send_char[DATA_LEN_POSITION + 1] = byte2char((unsigned char)(data_lens % 256));
	
    // add data:
	data_array_copy(&send_char[DATA_POSITION], float_bytes, FLOAT32_BYTE * data_lens);
	return;
}

// trans a double array to a send char array []: len(send_char) = data_lens + 5, data_lens < 65535
void Data_transfer::double2send_char(const double *data, int data_lens)
{
	unsigned char double_bytes[FLOAT64_BYTE * data_lens]; // bytes
	
	memset(double_bytes, '\0', FLOAT64_BYTE * data_lens);
	
	// trans float data array to byte data array:
	double_array2bys(data, double_bytes, data_lens);  
	
	// printf("check point 1\n");
	
	Number_conver::debug_print("double_bytes", double_bytes, data_lens * FLOAT64_BYTE);
	
	// add send flag:
	send_char[TRANS_FLAG_POSITION] = byte2char(DATA_FLAG);   // data
	// add data type:
	send_char[DATA_TYPE_POSITION] = byte2char(DATA_FLOAT64);
	// add parity flag:
    send_char[PARITY_POSITION] = byte2char(parity_check(double_bytes, FLOAT64_BYTE * data_lens));
	// add data length's high byte:
    send_char[DATA_LEN_POSITION] = byte2char((unsigned char)(data_lens / 256));
	// add data length's low byte:
    send_char[DATA_LEN_POSITION + 1] = byte2char((unsigned char)(data_lens % 256));
	
	printf("check point 2\n");
    // add data:
	data_array_copy(&send_char[DATA_POSITION], double_bytes, FLOAT64_BYTE * data_lens);
	printf("check point 3\n");
	return;
} 

// trans recv char array [] to float array:
int Data_transfer::recv_char2float()
{
	unsigned int data_lens = 0;
	unsigned char parity_flag = 0;
	
	// get data_lens of float data:
	data_lens = char2byte(recv_char[DATA_LEN_POSITION]) * 256 + char2byte(recv_char[DATA_LEN_POSITION + 1]);
	
	// get byte data:
	unsigned char float_bytes[FLOAT32_BYTE * data_lens]; // bytes
	data_array_copy(float_bytes, &recv_char[DATA_POSITION], FLOAT32_BYTE * data_lens);
		
	// get parity flag:
	parity_flag = parity_check(float_bytes, FLOAT32_BYTE * data_lens);
	
	if (parity_flag == char2byte(recv_char[PARITY_POSITION]))
	{	
		// save data to recv_float_data[]
		bys2float_array(recv_float_data, float_bytes, data_lens);
	}
	else{
		printf("parity check error !");
	}
	return data_lens;
}

// trans recv char array [] to double array:
int Data_transfer::recv_char2double()
{
	int data_lens = 0;
	unsigned char parity_flag = 0;
	
	// get data_lens of float data:
	data_lens = char2byte(recv_char[DATA_LEN_POSITION]) * 256 + char2byte(recv_char[DATA_LEN_POSITION + 1]);
	
	// get byte data:
	unsigned char double_bytes[FLOAT64_BYTE * data_lens]; // bytes
	data_array_copy(double_bytes, &recv_char[DATA_POSITION], FLOAT64_BYTE * data_lens);
		
	// get parity flag:
	parity_flag = parity_check(double_bytes, FLOAT64_BYTE * data_lens);
	
	if (parity_flag == char2byte(recv_char[PARITY_POSITION]))
	{
		// save data to recv_double_data[]
		bys2double_array(recv_double_data, double_bytes, data_lens);
	}
	else{
		printf("parity check error !");
	}
	return data_lens;
}

/**********************************send recv**************************************/
// recv float or double data 
void Data_transfer::recv_data(unsigned char *recv_flag, unsigned char *data_type, int *data_lens)
{
    int recv_data_lens = 0;
    unsigned char parity_flag = 0;  

	recv_data_lens = recv_strings(recv_char);
    if (recv_data_lens){
        // get recv flag:
	    *recv_flag = char2byte(recv_char[TRANS_FLAG_POSITION]);
		if (DATA_FLAG == (*recv_flag)){
	        // get data type:
	        *data_type = char2byte(recv_char[DATA_TYPE_POSITION]);
	        
			if (DATA_FLOAT32 == (*data_type)){
				*data_lens = recv_char2float();
			}
			else if (DATA_FLOAT64 == (*data_type)){
				*data_lens = recv_char2double();
			}
	    } // if (DATA_)
	} // if (recv_)
    else{
		printf("receive error ! num: %d\n", recv_data_lens);
	}
	return;
}

// send float data
void Data_transfer::send_data(float *data, int data_lens)
{
	float2send_char(data, data_lens);
	Number_conver::debug_print("send_char", send_char, data_lens * FLOAT32_BYTE + 5);
	send_strings(send_char, data_lens * FLOAT32_BYTE + 5);
}

// send double data
void Data_transfer::send_data(double *data, int data_lens)
{
	double2send_char(data, data_lens);
	Number_conver::debug_print("send_char", send_char, data_lens * FLOAT64_BYTE + 5);
	// debug:
	// for (int i = 0;i < data_lens * FLOAT64_BYTE + 5;i++){
	//	printf("%d ", send_char[i]);
	// }
	// printf("\n");
	send_strings(send_char, data_lens * FLOAT64_BYTE + 5);
}

// send flag:
void Data_transfer::send_flag(unsigned char flag)
{
	char flag_char = byte2char(flag);
	Number_conver::debug_print("send_flag", &flag_char, 1);
	send_strings(&flag_char, 1);
}