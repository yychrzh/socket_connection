#include "win_protocol.h"


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

/*************************************************handshake***************************************************/
void Data_transfer::handshake()
{
	if (0 == strcmp(socket_type, "server")){
		unsigned char data_type = 0;
		int data_lens = 0;
		unsigned char recv_flag = 0;

		recv_data(&recv_flag, &data_type, &data_lens);
		if (CONNECTION_FLAG == recv_flag) {
			printf("handshake success !\n");
		}
	}
	else if (0 == strcmp(socket_type, "client")) {
		send_flag((unsigned char)CONNECTION_FLAG);
		printf("handshake success !\n");
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

//parity check of the data
unsigned char Data_transfer::parity_check(const unsigned char *data, int lens)
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

// from a float array to a send byte array []
void Data_transfer::float2send_byte(const float *data, int data_lens)
{
	// unsigned char float_bytes[FLOAT32_BYTE * data_lens]; // bytes
	unsigned char float_bytes[CHAR_BUFFSIZE]; // bytes

	memset(float_bytes, '\0', FLOAT32_BYTE * data_lens);

	// trans float data array to byte data array:
	float_array2bys(data, float_bytes, data_lens);

	Number_conver::debug_print("float_bytes", float_bytes, data_lens * FLOAT32_BYTE);

	// add send flag:
	send_byte[TRANS_FLAG_POSITION] = (unsigned char)(DATA_FLAG);   // data
	// add data type:
	send_byte[DATA_TYPE_POSITION] = (unsigned char)(DATA_FLOAT32);
	// add parity flag:
	send_byte[PARITY_POSITION] = (unsigned char)(parity_check(float_bytes, FLOAT32_BYTE * data_lens));
	// add data length's high byte:
	send_byte[DATA_LEN_POSITION] = (unsigned char)(data_lens / 256);
	// add data length's low byte:
	send_byte[DATA_LEN_POSITION + 1] = (unsigned char)(data_lens % 256);

	// add data:
	data_array_copy(&send_byte[DATA_POSITION], float_bytes, FLOAT32_BYTE * data_lens);
	return;
}

// from a double array to a send byte array []
void Data_transfer::double2send_byte(const double *data, int data_lens)
{
	// unsigned char double_bytes[FLOAT64_BYTE * data_lens]; // bytes
	unsigned char double_bytes[CHAR_BUFFSIZE]; // bytes

	memset(double_bytes, '\0', FLOAT64_BYTE * data_lens);

	// trans float data array to byte data array:
	double_array2bys(data, double_bytes, data_lens);

	Number_conver::debug_print("double_bytes", double_bytes, data_lens * FLOAT64_BYTE);

	// add send flag:
	send_byte[TRANS_FLAG_POSITION] = (unsigned char)(DATA_FLAG);   // data
	// add data type:
	send_byte[DATA_TYPE_POSITION] = (unsigned char)(DATA_FLOAT64);
	// add parity flag:
	send_byte[PARITY_POSITION] = (unsigned char)(parity_check(double_bytes, FLOAT64_BYTE * data_lens));
	// add data length's high byte:
	send_byte[DATA_LEN_POSITION] = (unsigned char)(data_lens / 256);
	// add data length's low byte:
	send_byte[DATA_LEN_POSITION + 1] = (unsigned char)(data_lens % 256);

	// add data:
	data_array_copy(&send_byte[DATA_POSITION], double_bytes, FLOAT64_BYTE * data_lens);
	return;
}

// from a unsigned char array to a send byte array []
void Data_transfer::uchar2send_byte(const unsigned char *data, int data_lens)
{
	// unsigned char double_bytes[FLOAT64_BYTE * data_lens]; // bytes
	// unsigned char uchar_bytes[CHAR_BUFFSIZE]; // bytes

	// memset(uchar_bytes, '\0', FLOAT64_BYTE * data_lens);

	// for (int i = 0; i < data_lens; i++) {
    // 		uchar_bytes[i] = data[i];
	// }

	Number_conver::debug_print("uchar_bytes", data, data_lens);

	// add send flag:
	send_byte[TRANS_FLAG_POSITION] = (unsigned char)(DATA_FLAG);   // data
	// add data type:
	send_byte[DATA_TYPE_POSITION] = (unsigned char)(DATA_UCHAR);
	// add parity flag:
	send_byte[PARITY_POSITION] = (unsigned char)(parity_check(data, data_lens));
	// add data length's high byte:
	send_byte[DATA_LEN_POSITION] = (unsigned char)(data_lens / 256);
	// add data length's low byte:
	send_byte[DATA_LEN_POSITION + 1] = (unsigned char)(data_lens % 256);

	// add data:
	data_array_copy(&send_byte[DATA_POSITION], (unsigned char *)(&data[0]), data_lens);
	return;
}

// trans recv byte array [] to float array: 
void Data_transfer::recv_byte2float(int data_lens)
{
	// int data_lens = 0;
	unsigned char parity_flag = 0;

	// get data_lens of float data:
	data_lens = (recv_byte[DATA_LEN_POSITION]) * 256 + recv_byte[DATA_LEN_POSITION + 1];

	// get byte data:
	// unsigned char float_bytes[FLOAT32_BYTE * data_lens]; // bytes
	unsigned char float_bytes[CHAR_BUFFSIZE]; // bytes
	data_array_copy(float_bytes, &recv_byte[DATA_POSITION], FLOAT32_BYTE * data_lens);

	// get parity flag:
	parity_flag = parity_check(float_bytes, FLOAT32_BYTE * data_lens);

	if (parity_flag == recv_byte[PARITY_POSITION])
	{
		// save data to recv_float_data[]
		bys2float_array(recv_float_data, float_bytes, data_lens);
	}
	else{
		printf("parity check error !\n");
	}
	return;
}

// trans recv byte array [] to double array: 
void Data_transfer::recv_byte2double(int data_lens)
{
	// int data_lens = 0;
	unsigned char parity_flag = 0;

	// get data_lens of float data:
	data_lens = (recv_byte[DATA_LEN_POSITION]) * 256 + recv_byte[DATA_LEN_POSITION + 1];

	// get byte data:
	// unsigned char double_bytes[FLOAT64_BYTE * data_lens]; // bytes
	unsigned char double_bytes[CHAR_BUFFSIZE]; // bytes
	data_array_copy(double_bytes, &recv_byte[DATA_POSITION], FLOAT64_BYTE * data_lens);

	// get parity flag:
	parity_flag = parity_check(double_bytes, FLOAT64_BYTE * data_lens);

	if (parity_flag == recv_byte[PARITY_POSITION])
	{
		// save data to recv_float_data[]
		bys2double_array(recv_double_data, double_bytes, data_lens);
	}
	else{
		printf("parity check error !\n");
	}
	return;
}

// trans recv byte array [] to unsigned char array: 
void Data_transfer::recv_byte2uchar(int data_lens)
{
	// int data_lens = 0;
	unsigned char parity_flag = 0;

	// get data_lens of float data:
	data_lens = (recv_byte[DATA_LEN_POSITION]) * 256 + recv_byte[DATA_LEN_POSITION + 1];

	// get byte data:
	// unsigned char double_bytes[FLOAT64_BYTE * data_lens]; // bytes
	// unsigned char uchar_array[CHAR_BUFFSIZE]; // bytes
	data_array_copy(recv_uchar_data, &recv_byte[DATA_POSITION], data_lens);

	// get parity flag:
	parity_flag = parity_check(recv_uchar_data, data_lens);

	if (parity_flag == recv_byte[PARITY_POSITION])
	{
		;
	}
	else{
		printf("parity check error !\n");
	}
	return;
}

/**********************************send recv byte**************************************/
// receive all data if there are data rest:
void Data_transfer::recv_rest_data(int all_lens, int received_lens)
{
	int recv_data_lens = 0;
	int rest_lens = 0;

	rest_lens = all_lens - received_lens;
	while (rest_lens){
		recv_data_lens = recv_strings(&recv_byte[received_lens], rest_lens);
		if (recv_data_lens <= 0){
			printf("receive error ! num: %d\n", recv_data_lens);
			return;
		}
		received_lens += recv_data_lens;
		rest_lens -= recv_data_lens;
	}
}

// recv data flag, parameters: recv data type and data length: processing
void Data_transfer::recv_data_flag(unsigned char *data_type, int *data_lens, int received_lens)
{
	int all_lens = 0;
	int recv_data_lens = 0;
	int rest_lens = 0;

	// get data_type and data_length:
	*data_type = recv_byte[DATA_TYPE_POSITION];
	*data_lens = recv_byte[DATA_LEN_POSITION] * 256 + recv_byte[DATA_LEN_POSITION + 1];
	all_lens = 5 + (*data_lens) * int((*data_type / 8));

	recv_rest_data(all_lens, received_lens);

	if (DATA_FLOAT32 == (*data_type)){
		recv_byte2float(*data_lens);
	}
	else if (DATA_FLOAT64 == (*data_type)){
		recv_byte2double(*data_lens);
	}
	else if (DATA_UCHAR == (*data_type)) {
		recv_byte2uchar(*data_lens);
	}
}

// data format: 0: send_flag(control flag); 1: module_name length; 2: func_name length;
// 3: parameters nums; 4: data length
// flag_length: 5
// module name, func_name, [param data type, param_data]...
// data_lens: len(module_name) + len(func_name) + parameters nums + parameters bytes	
void Data_transfer::recv_control_flag(int *data_lens, int received_lens)
{
	int all_lens = 0;
	int recv_data_lens = 0;
	int rest_lens = 0;

	int current_position = 0;
	int current_data_type = 0;
	int float_count = 0;
	int double_count = 0;

	// ensure all data had received 
	*data_lens = recv_byte[4];
	all_lens = (*data_lens) + 5;

	recv_rest_data(all_lens, received_lens);

	// get module name:
	func_name.module_name_lens = recv_byte[1];
	data_array_copy(func_name.module_name, &recv_byte[5], func_name.module_name_lens);
	func_name.module_name[func_name.module_name_lens] = '\0';

	// get function name:
	func_name.func_name_lens = recv_byte[2];
	data_array_copy(func_name.func_name, &recv_byte[5 + func_name.module_name_lens], func_name.func_name_lens);
	func_name.func_name[func_name.func_name_lens] = '\0';

	// get parameter list:
	param_list.params_nums = recv_byte[3];
	current_position = 5 + func_name.module_name_lens + func_name.func_name_lens;

	for (int i = 0; i < param_list.params_nums; i++){
		current_data_type = recv_byte[current_position];
		current_position++;
		param_list.data_type_list[i] = current_data_type;
		switch (current_data_type) {
		case DATA_FLOAT32:
			param_list.float_params[float_count] = byte2float(&recv_byte[current_position]);
			float_count++;
			break;
		case DATA_FLOAT64:
			param_list.double_params[double_count] = byte2double(&recv_byte[current_position]);
			double_count++;
			break;
		default:
			printf("wrong data type when get parameter list !\n");
			break;
		}
		current_position += (int)(current_data_type / 8);
	}

	param_list.float_params_nums = float_count;
	param_list.double_params_nums = double_count;
}

// receive data or control instructions
void Data_transfer::recv_data(unsigned char *recv_flag, unsigned char *data_type, int *data_lens)
{
	int recv_data_lens = 0;

	// recv data to recv byte
	recv_data_lens = recv_strings(recv_byte);
	if (recv_data_lens <= 0){
		printf("receive error ! num: %d\n", recv_data_lens);
		return;
	}

	// get recv flag:
	*recv_flag = recv_byte[TRANS_FLAG_POSITION];

	switch (*recv_flag) {
	case DATA_FLAG:
		recv_data_flag(data_type, data_lens, recv_data_lens);
		break;
	case CONTROL_FLAG:
		recv_control_flag(data_lens, recv_data_lens);
		break;
	default:
		return;
	}
}

// send float data
void Data_transfer::send_data(float *data, int data_lens)
{
	float2send_byte(data, data_lens);
	Number_conver::debug_print("send_byte", send_byte, data_lens * FLOAT32_BYTE + 5);
	send_strings(send_byte, data_lens * FLOAT32_BYTE + 5);
}

// send double data
void Data_transfer::send_data(double *data, int data_lens)
{
	double2send_byte(data, data_lens);
	Number_conver::debug_print("send_byte", send_byte, data_lens * FLOAT64_BYTE + 5);
	send_strings(send_byte, data_lens * FLOAT64_BYTE + 5);
}

// send unsigend char data:
void Data_transfer::send_data(unsigned char *data, int data_lens)
{
	uchar2send_byte(data, data_lens);
	Number_conver::debug_print("send_byte", send_byte, data_lens + 5);
	send_strings(send_byte, data_lens + 5);
}

// send flag:
void Data_transfer::send_flag(unsigned char flag)
{
	Number_conver::debug_print("send_flag", &flag, 1);
	send_strings(&flag, 1);
}