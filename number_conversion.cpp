#include "number_conversion.h"

/**********************************debug_print************************************************************/
Number_conver::Number_conver(bool print_flag)
{
	debug_print_flag = print_flag;
}

void Number_conver::debug_print(const char *infostr, const char *infochar, int data_lens)
{
    if (debug_print_flag){
		printf("(num___char)");
		printf("%s: ", infostr);
        for (int i = 0;i < data_lens;i++){
		    printf("%d ", infochar[i]);
		}
		printf("\n");
	}
}

void Number_conver::debug_print(const char *infostr, const unsigned char *infouchar, int data_lens)
{
	if (debug_print_flag){
		printf("(num__uchar)");
		printf("%s: ", infostr);
        for (int i = 0;i < data_lens;i++){
		    printf("%d ", infouchar[i]);
		}
		printf("\n");
	}
}

void Number_conver::debug_print(const char *infostr, const int *infoint, int data_lens)
{
    if (debug_print_flag){
		printf("(num____int)");
		printf("%s: ", infostr);
        for (int i = 0;i < data_lens;i++){
		    printf("%d ", infoint[i]);
		}
		printf("\n");
	}
}

void Number_conver::debug_print(const char *infostr, const long int *infolong, int data_lens)
{
	if (debug_print_flag){
		printf("(num___long)");
		printf("%s: ", infostr);
        for (int i = 0;i < data_lens;i++){
		    printf("%ld ", infolong[i]);
		}
		printf("\n");
	}
}

void Number_conver::debug_print(const char *infostr, const float *infofloat, int data_lens)
{
	if (debug_print_flag){
		printf("(num__float)");
		printf("%s: ", infostr);
        for (int i = 0;i < data_lens;i++){
		    printf("%f ", infofloat[i]);
		}
		printf("\n");
	}
}

void Number_conver::debug_print(const char *infostr, const double *infodouble, int data_lens)
{
	if (debug_print_flag){
		printf("(num_double)");
		printf("%s: ", infostr);
        for (int i = 0;i < data_lens;i++){
		    printf("%f ", infodouble[i]);
		}
		printf("\n");
	}
}

/**********************************************byte******************************************/

// from float (decimal) to bytes (unsigned char array)
void Number_conver::dec2byte(float x, unsigned char *bys)   //bys[19]
{
    int count_8bits = 0;
	int count_bytes = 0;
	char current_8bin[8];
	unsigned char current_bit = 0;
	x -= (int)x;
	
	while (x){
		x *= 2;
        current_bit = (x >= 1.0)?1:0;
		current_8bin[count_8bits] = current_bit;
		x -= (int)x;
		count_8bits++;
		if (8 == count_8bits){
			bys[count_bytes] = bin2byte(current_8bin);
			count_bytes++;
			if (count_bytes >= FLOAT32_BYTE_BUF){
				break;
			}
			count_8bits = 0;
		}
	}
	if (count_8bits != 0){
		for (int i = count_8bits;i < 8;i++){
			current_8bin[i] = 0;
		}
		bys[count_bytes] = bin2byte(current_8bin);
		count_bytes++;
	}
	if (count_bytes < FLOAT32_BYTE_BUF){
		for (int j = count_bytes;j < FLOAT32_BYTE_BUF;j++){
			bys[j] = 0;
		}
	}
}

// from double (decimal) to bytes (unsigned char array)
void Number_conver::dec2byte(double x, unsigned char *bys)   //bys[135]
{
    int count_8bits = 0;
	int count_bytes = 0;
	char current_8bin[8];
	unsigned char current_bit = 0;
	x -= (long int)x;
	
	while (x){
		x *= 2;
        current_bit = (x >= 1.0)?1:0;
		current_8bin[count_8bits] = current_bit;
		x -= (long int)x;
		count_8bits++;
		if (8 == count_8bits){
			bys[count_bytes] = bin2byte(current_8bin);
			count_bytes++;
			if (count_bytes >= FLOAT64_BYTE_BUF){
				break;
			}
			count_8bits = 0;
		}
	}
	if (count_8bits != 0){
		for (int i = count_8bits;i < 8;i++){
			current_8bin[i] = 0;
		}
		bys[count_bytes] = bin2byte(current_8bin);
		count_bytes++;
	}
	if (count_bytes < FLOAT64_BYTE_BUF){
		for (int j = count_bytes;j < FLOAT64_BYTE_BUF;j++){
			bys[j] = 0;
		}
	}
}
		
// from byte (unsigned char array) to double (decimal)
float Number_conver::byte2dec_float(const unsigned char *bys)
{
    float byte_float = 0;
    
    for (int i = 0;i < FLOAT32_BYTE_BUF;i++){
		byte_float += bys[i] * pow(2, -(i + 1) * 8);
	}	
	return byte_float;
}

// from byte (unsigned char array) to double (decimal)
double Number_conver::byte2dec_double(const unsigned char *bys)
{
	double byte_double = 0;
    
    for (int i = 0;i < FLOAT64_BYTE_BUF;i++){
		byte_double += bys[i] * pow(2, -(i + 1) * 8);
	}	
	return byte_double;
}

// from int to bytes (unsigned char array)
void Number_conver::int2byte(int x, unsigned char *bys)           // bys[19]  
{
	int count_8bits = 0;
	int count_bytes = 0;
	char current_8bin[8];
	unsigned char current_bit = 0;
	
	while (x){
		current_bit = x % 2;
		x = x / 2;
		current_8bin[7 - count_8bits] = current_bit;
		count_8bits++;
		if (8 == count_8bits){
			bys[FLOAT32_BYTE_BUF - 1 - count_bytes] = bin2byte(current_8bin);
			count_bytes++;
			if (count_bytes >= FLOAT32_BYTE_BUF){   
				break;
			}
			count_8bits = 0;
		}
	}
	if (count_8bits != 0){
		for (int i = count_8bits;i < 8;i++){
			current_8bin[7 - i] = 0;
		}
		bys[FLOAT32_BYTE_BUF - 1 - count_bytes] = bin2byte(current_8bin);
		count_bytes++;
	}
	if (count_bytes < FLOAT32_BYTE_BUF){
		for (int j = count_bytes;j < FLOAT32_BYTE_BUF;j++){
			bys[FLOAT32_BYTE_BUF - 1 - j] = 0;
		}
	}
}

// from long int to bytes (unsigned char array)
void Number_conver::long2byte(long int x, unsigned char *bys)       // bys[135]
{
    int count_8bits = 0;
	int count_bytes = 0;
	char current_8bin[8];
	unsigned char current_bit = 0;
	
	while (x){
		current_bit = x % 2;
		x = x / 2;
		current_8bin[7 - count_8bits] = current_bit;
		count_8bits++;
		if (8 == count_8bits){
			bys[FLOAT64_BYTE_BUF - 1 - count_bytes] = bin2byte(current_8bin);
			count_bytes++;
			if (count_bytes >= FLOAT64_BYTE_BUF){   
				break;
			}
			count_8bits = 0;
		}
	}
	if (count_8bits != 0){
		for (int i = count_8bits;i < 8;i++){
			current_8bin[7 - i] = 0;
		}
		bys[FLOAT64_BYTE_BUF - 1 - count_bytes] = bin2byte(current_8bin);
		count_bytes++;
	}
	if (count_bytes < FLOAT64_BYTE_BUF){
		for (int j = count_bytes;j < FLOAT64_BYTE_BUF;j++){
			bys[FLOAT64_BYTE_BUF - 1 - j] = 0;
		}
	}
}
		
// from bytes (unsigned char array) to int
int Number_conver::byte2int(const unsigned char *bys)               // bys[19]
{
	int byte_int = 0;
	for (int i =0;i < FLOAT32_BYTE_BUF;i++){
		if (bys[i] != 0){
			byte_int += bys[i] * pow(2, 8 * (FLOAT32_BYTE_BUF - 1 - i));
		}
	}
	return byte_int;
}

// from bytes (unsigned char array) to long int
long int Number_conver::byte2long(const unsigned char *bys)         // bys[135]
{
	long int byte_long = 0;
	for (int i =0;i < FLOAT64_BYTE_BUF;i++){
		if (bys[i] != 0){
			byte_long += bys[i] * pow(2, 8 * (FLOAT64_BYTE_BUF - 1 - i));
		}
	}
	return byte_long;
}

/*
// from float to bytes (unsigned char array)
void Number_conver::float2byte(float x, unsigned char *bys)  // bys[4]
{
	char exponent_bin[FLOAT32_EXPONENT];              // 8 bits
	char fraction_bin[FLOAT32_FRACTION];              // 23 bits
	unsigned char temp_int_bytes[FLOAT32_BYTE_BUF];   // 19 bytes 
	unsigned char temp_dec_bytes[FLOAT32_BYTE_BUF];   // 19 bytes
	float abs_x, dec_x;
	int int_x;
	unsigned int sign;
	
	// initiate memory:
	memset(exponent_bin, '\0', FLOAT32_EXPONENT);
    memset(fraction_bin, '\0', FLOAT32_FRACTION);
	memset(temp_int_bytes, '\0', FLOAT32_BYTE_BUF);
    memset(temp_dec_bytes, '\0', FLOAT32_BYTE_BUF);
	
	sign = (x < 0.0)? 1 : 0;
	abs_x = (x < 0.0) ? (-x) : x;
	int_x = (int)(abs_x);
	dec_x = abs_x - int_x;
	
	debug_print("int_x", &int_x, 1);
	debug_print("dec_x", &dec_x, 1);
	
	if (0 == x){
		for (int i = 0;i < FLOAT32_BYTE;i++){
			bys[i] = 0;
		}
		return;
	}
	// else if () INT_MAX.... maybe add later...
	
    // get the binary list of integer and decimal:
	int2byte(int_x, temp_int_bytes);
	debug_print("int_bytes", temp_int_bytes, FLOAT32_BYTE_BUF);
	dec2byte(dec_x, temp_dec_bytes);
	debug_print("dec_bytes", temp_dec_bytes, FLOAT32_BYTE_BUF);
	
	// unsigned int int_exponent = FLOAT32_EXPONENT_OFFSET - 1;
	int int_exponent = 0;
	
	// calculate the int_exponent and fraction_bin
	if (int_x > 0){   
	    int i, j;
		char temp_bin[8];
		memset(temp_bin, '\0', 8);
		
		// calculate the integer of exponent:
		for (i = 0;i < FLOAT32_BYTE_BUF;i++){
			if (temp_int_bytes[i] != 0){    // i: the first non zero bytes of int_x
			    debug_print("none_zero_i", &i, 1);
				debug_print("none_zero_byte", &temp_int_bytes[i], 1);
				byte2bin(temp_int_bytes[i], temp_bin);
				debug_print("none_zero_bin", temp_bin, 8);
				for (j = 0;j < 8;j++){     // j: the first non zero bit ...
					if (temp_bin[j] > 0){
						int_exponent = ((FLOAT32_BYTE_BUF - i) * 8 - j);
						debug_print("int_exponent", &int_exponent, 1);
						break;
					}
				} // for (j =
				break;
			} // if (temp_)
		} //for (i =
			
		// add the int's bit to the fraction:
		int dec_bits = FLOAT32_FRACTION;
	    for (int k = j + 1;k < 8;k++){
			fraction_bin[k - j - 1] = temp_bin[k];
		}
		debug_print("fraction_1", fraction_bin, 7 - j);
		for (int k = i + 1;k < FLOAT32_BYTE_BUF;k++){
			byte2bin(temp_int_bytes[k], temp_bin);
			for (int m = 0;m < 8;m++){
				fraction_bin[8 * (k - i - 1) + m + (7 - j)] = temp_bin[m];
			}
		}
		debug_print("fraction_2", fraction_bin, int_exponent - 1);
		
		// add the dec's bit to the fraction:
		dec_bits = dec_bits - int_exponent + 1;
		for (i = 0;i < (dec_bits / 8);i++){
			byte2bin(temp_dec_bytes[i], temp_bin);
			for (j = 0;j < 8;j++){
				fraction_bin[int_exponent - 1 + 8 * i + j] = temp_bin[j];
			}
		}
		byte2bin(temp_dec_bytes[i], temp_bin);
		for (j = 0;j < (dec_bits % 8);j++){
			fraction_bin[int_exponent - 1 + 8 * (dec_bits / 8) + j] = temp_bin[j];
		}
		debug_print("fraction_bin", fraction_bin, FLOAT32_FRACTION);
	} //if (int_x)
	else{
		int i, j;
		char temp_bin[8];
		memset(temp_bin, '\0', 8);
		
		// calculate the int exponent:
		for (i = 0;i < FLOAT32_BYTE_BUF;i++){
			if (temp_dec_bytes[i] != 0){
				byte2bin(temp_dec_bytes[i], temp_bin);
				for (j = 0;j < 8;j++){     // j: the first non zero bit ...
					if (temp_bin[j] > 0){
						int_exponent = -(i * 8 + j);
						debug_print("int_exponent", &int_exponent, 1);
						break;
					}
				} // for (j =
				break;
			} // if (temp_
		}// for (i = 
		
		// add the dec's bit to the fraction:
		int dec_bits = FLOAT32_FRACTION;
		int k = 0;
		for (k = j + 1;k < 8;k++){
			fraction_bin[k - j - 1] = temp_bin[k];
		}
		debug_print("fraction_1", fraction_bin, 7 - j);
		dec_bits -= (7 - j);
		for (k = i + 1;k < (i + 1 + dec_bits / 8);k++){
			byte2bin(temp_dec_bytes[k], temp_bin);
			for (int m = 0;m < 8;m++){
				fraction_bin[8 * (k - i - 1) + m + 7 - j] = temp_bin[m];
			}
		}
		debug_print("fraction_2", fraction_bin, (7 - j) + 8 * (k - i - 1));
		dec_bits = dec_bits - 8 * (k - i - 1);
		byte2bin(temp_dec_bytes[k], temp_bin);
		for (j = 0;j < 8;j++){
			fraction_bin[FLOAT32_FRACTION - dec_bits - 1 + j] = temp_bin[j];
		}
		debug_print("fraction_bin", fraction_bin, FLOAT32_FRACTION);
	}// else
	
    float dec = 0;
    for (int i = 0;i < 23;i++){
		dec += fraction_bin[i] * pow(2, -(i + 1));
	}
	debug_print("dec", &dec, 1);

    // calculate exponent: float32, 8 bit
    int_exponent += (FLOAT32_EXPONENT_OFFSET - 1);
	debug_print("int_exponent", &int_exponent, 1);
    byte2bin(int_exponent, exponent_bin);
	
	char float32_bin[FLOAT32_BIT];
	memset(float32_bin, '\0', FLOAT32_BIT);
	
	// copy bits:
	float32_bin[0] = sign;
	for (int i = 0;i < FLOAT32_EXPONENT;i++){
		float32_bin[i + 1] = exponent_bin[i];
	}
	for (int i = 0;i < FLOAT32_FRACTION;i++){
		float32_bin[i + 1 + FLOAT32_EXPONENT] = fraction_bin[i];
	}
    debug_print("float32_bin", float32_bin, FLOAT32_BIT);
	for (int i = 0;i < FLOAT32_BYTE;i++){
		bys[i] = bin2byte(&float32_bin[i * 8]);
	}
	debug_print("float32_byte", bys, FLOAT32_BYTE);
	return;
}
 
// from double to bytes (unsigned char array)
void Number_conver::double2byte(double x, unsigned char *bys)  // bys[8]
{
	char exponent_bin[FLOAT64_EXPONENT];        // 11 bits
	char fraction_bin[FLOAT64_FRACTION];        // 52 bits
	unsigned char temp_int_bytes[FLOAT64_BYTE_BUF];      // int(x) 's bytes
	unsigned char temp_dec_bytes[FLOAT64_BYTE_BUF];      // x - int(x) 's bytes
	double abs_x, dec_x;
	long int int_x;
	unsigned int sign;
	
	// initiate memory:
	memset(exponent_bin, '\0', FLOAT64_EXPONENT);
    memset(fraction_bin, '\0', FLOAT64_FRACTION);
	memset(temp_int_bytes, '\0', FLOAT64_BYTE_BUF);
    memset(temp_dec_bytes, '\0', FLOAT64_BYTE_BUF);
	
	sign = (x < 0.0)? 1 : 0;
	abs_x = (x < 0.0) ? (-x) : x;
	int_x = (long int)(abs_x);
	dec_x = abs_x - int_x;
	
	if (0 == x){
		for (int i = 0;i < FLOAT64_BYTE;i++){
			bys[i] = 0;
		}
		return;
	}
	// else if () INT_MAX.... maybe add later...
	
    // get the binary list of integer and decimal:
	long2byte(int_x, temp_int_bytes);
	debug_print("long_bytes", temp_int_bytes, FLOAT64_BYTE_BUF);
	dec2byte(dec_x, temp_dec_bytes);
	debug_print("dec_bytes", temp_dec_bytes, FLOAT64_BYTE_BUF);
	
	// unsigned int int_exponent = FLOAT32_EXPONENT_OFFSET - 1;
	int int_exponent = 0;
	
	// calculate the int_exponent and fraction_bin
	if (int_x > 0){   
	    int i, j;
		char temp_bin[8];
		memset(temp_bin, '\0', 8);
		
		// calculate the integer of exponent:
		for (i = 0;i < FLOAT64_BYTE_BUF;i++){
			if (temp_int_bytes[i] > 0){    // i: the first non zero bytes of int_x
				byte2bin(temp_int_bytes[i], temp_bin);
				for (j = 0;j < 8;j++){     // j: the first non zero bit ...
					if (temp_bin[j] > 0){
						int_exponent = ((FLOAT64_BYTE_BUF - i) * 8 - j);
						debug_print("int_exponent", &int_exponent, 1);
						break;
					}
				} // for (j =
				break;
			} // if (temp_)
		} //for (i =
			
		// add the int's bit to the fraction:
		int dec_bits = FLOAT64_FRACTION;
	    for (int k = j + 1;k < 8;k++){
			fraction_bin[k - j - 1] = temp_bin[k];
		}
		debug_print("fraction_1", fraction_bin, 7 - j);
		for (int k = i + 1;k < FLOAT64_BYTE_BUF;k++){
			byte2bin(temp_int_bytes[k], temp_bin);
			for (int m = 0;m < 8;m++){
				fraction_bin[8 * (k - i - 1) + m + (7 - j)] = temp_bin[m];
			}
		}
		debug_print("fraction_2", fraction_bin, int_exponent - 1);
		
		// add the dec's bit to the fraction:
		dec_bits -= (int_exponent - 1);
		for (i = 0;i < (dec_bits / 8);i++){
			byte2bin(temp_dec_bytes[i], temp_bin);
			for (j = 0;j < 8;j++){
				fraction_bin[int_exponent - 1 + 8 * i + j] = temp_bin[j];
			}
		}
		byte2bin(temp_dec_bytes[i], temp_bin);
		for (j = 0;j < (dec_bits % 8);j++){
			fraction_bin[int_exponent - 1 + 8 * (dec_bits / 8) + j] = temp_bin[j];
		}
		debug_print("fraction_bin", fraction_bin, FLOAT64_FRACTION);
	} //if (int_x)
	else{
		int i, j;
		char temp_bin[8];
		memset(temp_bin, '\0', 8);
		
		// calculate the int exponent:
		for (i = 0;i < FLOAT64_BYTE_BUF;i++){
			if (temp_dec_bytes[i] > 0){
				byte2bin(temp_dec_bytes[i], temp_bin);
				for (j = 0;j < 8;j++){     // j: the first non zero bit ...
					if (temp_bin[j] > 0){
						int_exponent = -(i * 8 + j);
						debug_print("int_exponent", &int_exponent, 1);
						break;
					}
				} // for (j =
				break;
			} // if (temp_
		}// for (i = 
		
		// add the dec's bit to the fraction:
		int dec_bits = FLOAT64_FRACTION;
		int k =0;
		for (k = j + 1;k < 8;k++){
			fraction_bin[k - j - 1] = temp_bin[k];
		}
		debug_print("fraction_1", fraction_bin, 7 - j);
		dec_bits -= (7 - j);
		for (k = i + 1;k < (i + 1 + dec_bits / 8);k++){
			byte2bin(temp_dec_bytes[k], temp_bin);
			for (int m = 0;m < 8;m++){
				fraction_bin[8 * (k - i - 1) + m + 7 - j] = temp_bin[m];
			}
		}
		debug_print("fraction_2", fraction_bin, (7 - j) + 8 * (k - i - 1));
		dec_bits = dec_bits - 8 * (k - i - 1);
		byte2bin(temp_dec_bytes[k], temp_bin);
		for (j = 0;j < 8;j++){
			fraction_bin[FLOAT64_FRACTION - dec_bits - 1 + j] = temp_bin[j];
		}
		debug_print("fraction_bin", fraction_bin, FLOAT64_FRACTION);
	}// else
		
    // calculate exponent: float64, 11 bit
    int_exponent += (FLOAT64_EXPONENT_OFFSET - 1);  // 11 bits
    debug_print("int_exponent", &int_exponent, 1);
	
	int hign_exp, low_exp;
	hign_exp = int_exponent / 256;
	low_exp = int_exponent % 256;
	
    byte2bin(hign_exp, exponent_bin);
	for (int i = 0;i < (FLOAT64_EXPONENT - 8);i++){
		exponent_bin[i] = exponent_bin[i + 16 - FLOAT64_EXPONENT];
	}
	byte2bin(low_exp, &exponent_bin[FLOAT64_EXPONENT - 8]);
	debug_print("exponent_bin", exponent_bin, FLOAT64_EXPONENT);
	
	char float64_bin[FLOAT64_BIT];
	memset(float64_bin, '\0', FLOAT64_BIT);
	
	// copy bits:
	float64_bin[0] = sign;
	for (int i = 0;i < FLOAT64_EXPONENT;i++){
		float64_bin[i + 1] = exponent_bin[i];
	}
	for (int i = 0;i < FLOAT64_FRACTION;i++){
		float64_bin[i + 1 + FLOAT64_EXPONENT] = fraction_bin[i];
	}
	debug_print("float64_bin", float64_bin, FLOAT64_BIT);

	for (int i = 0;i < FLOAT64_BYTE;i++){
		bys[i] = bin2byte(&float64_bin[i * 8]);
	}
	debug_print("float64_byte", bys, FLOAT64_BYTE);
	return;
}
		
// from bytes (unsigned char array) to float or double
float Number_conver::byte2float(const unsigned char *bys)
{
	unsigned int sign = 0;
	int int_exponent = 0;
	float float_fraction = 0.0;
	float float_data = 0.0;
	char float32_bin[FLOAT32_BIT];
	
	memset(float32_bin, '\0', FLOAT32_BIT);
	
	for (int i = 0;i < FLOAT32_BYTE;i++){
		byte2bin(bys[i], &float32_bin[8 * i]);
	}
	debug_print("float32_bin", float32_bin, 32);
	
	sign = float32_bin[0];
	for (int i = 0;i < FLOAT32_EXPONENT;i++){
		int_exponent += float32_bin[i + 1] * pow(2, 7 - i);
	}
	int_exponent -= FLOAT32_EXPONENT_OFFSET;
	debug_print("int_exponent", &int_exponent, 1);
	
	for (int i = 0;i < FLOAT32_FRACTION;i++){
		float_fraction += float32_bin[i + 1 + FLOAT32_EXPONENT] * pow(2, -(i + 1));
	}
	debug_print("float_fraction", &float_fraction, 1);
	
	//special case:
	if (int_exponent == -FLOAT32_EXPONENT_OFFSET && float_fraction == 0){
		float_data = 0.0;
		return float_data;
	}
	else if (int_exponent == (pow(2, FLOAT32_EXPONENT) - 1 - FLOAT32_EXPONENT_OFFSET) && float_fraction == 0){
		printf("float'inf'");
		return 0;
	}
	else if (int_exponent == (pow(2, FLOAT32_EXPONENT) - 1 - FLOAT32_EXPONENT_OFFSET) && float_fraction != 0){
		printf("float'nan'");
		return 0;
	}
	
	float_data = pow(-1, sign) * pow(2, int_exponent) * (1 + float_fraction);
	return float_data;
}

double Number_conver::byte2double(const unsigned char *bys)   
{
	unsigned int sign = 0;
	int int_exponent = 0;
	double double_fraction = 0.0;
	double double_data = 0.0;
	char float64_bin[FLOAT64_BIT];
	
	memset(float64_bin, '\0', FLOAT64_BIT);
	
	for (int i = 0;i < FLOAT64_BYTE;i++){
		byte2bin(bys[i], &float64_bin[8 * i]);
	}
	debug_print("float64_bin", float64_bin, 64);
	
	sign = float64_bin[0];
	for (int i = 0;i < FLOAT64_EXPONENT;i++){
		int_exponent += float64_bin[i + 1] * pow(2, 10 - i);
	}
	int_exponent -= FLOAT64_EXPONENT_OFFSET;
	debug_print("int_exponent", &int_exponent, 1);
	
	for (int i = 0;i < FLOAT64_FRACTION;i++){
		double_fraction += float64_bin[i + 1 + FLOAT64_EXPONENT] * pow(2, -(i + 1));
	}
	debug_print("double_fraction", &double_fraction, 1);
	
	//special case:
	if (int_exponent == -FLOAT64_EXPONENT_OFFSET && double_fraction == 0){
		double_data = 0.0;
		return double_data;
	}
	else if (int_exponent == (pow(2, FLOAT64_EXPONENT) - 1 - FLOAT64_EXPONENT_OFFSET) && double_fraction == 0){
		printf("double'inf'");
		return 0;
	}
	else if (int_exponent == (pow(2, FLOAT64_EXPONENT) - 1 - FLOAT64_EXPONENT_OFFSET) && double_fraction != 0){
		printf("double'nan'");
		return 0;
	}
	
	double_data = pow(-1, sign) * pow(2, int_exponent) * (1 + double_fraction);
	return double_data;
}
*/

// form float to bytes (unsigned char array)
void Number_conver::float2byte(float x, unsigned char *bys)
{
	char float_bin[FLOAT32_BIT];
	
	float2bin(x, float_bin);
	bin2bys(bys, float_bin, FLOAT32_BYTE);
}

// form double to bytes (unsigned char array)
void Number_conver::double2byte(double x, unsigned char *bys)
{
	printf("check char\n");
	char double_bin[FLOAT64_BIT];
	printf("check bin\n");
	double2bin(x, double_bin);
	printf("check bys\n");
	bin2bys(bys, double_bin, FLOAT64_BYTE);
	
}

// from bytes (unsigned char array) to float 
float Number_conver::byte2float(const unsigned char *bys)
{
    char float_bin[FLOAT32_BIT];
	float float_data = 0.0;
	
	bys2bin(bys, float_bin, FLOAT32_BYTE);
	float_data = bin2float(float_bin);
	return float_data;
}

// from bytes (unsigned char array) to double
double Number_conver::byte2double(const unsigned char *bys)
{
	char double_bin[FLOAT64_BIT];
	double double_data = 0.0;
	
	bys2bin(bys, double_bin, FLOAT64_BYTE);
	double_data = bin2double(double_bin);
	return double_data;
}

// form float array to bytes (unsigned char array)
void Number_conver::float_array2bys(const float *data, unsigned char *bys, int data_lens)
{
	for (int i = 0;i < data_lens;i++){
		float2byte(data[i], &bys[FLOAT32_BYTE * i]);
	}
}

// form double array to bytes (unsigned char array)
void Number_conver::double_array2bys(const double *data, unsigned char *bys, int data_lens)
{
	for (int i = 0;i < data_lens;i++){
		debug_print("double_array i", &i, 1);
		double2byte(data[i], &bys[FLOAT64_BYTE * i]);
	}
}
		
// from bytes (unsigned char array) to float array
void Number_conver::bys2float_array(float *data, const unsigned char *bys, int data_lens)
{
	for (int i = 0;i < data_lens;i++){
		data[i] = byte2float(&bys[FLOAT32_BYTE * i]);
	}
}

// from bytes (unsigned char array) to double array
void Number_conver::bys2double_array(double *data, const unsigned char *bys, int data_lens)
{
	for (int i = 0;i < data_lens;i++){
		data[i] = byte2double(&bys[FLOAT64_BYTE * i]);
	}
}

/******************************************bin*******************************************/

// from byte to binary: unsigned char to char [8]: (L->R, High->Low)
void Number_conver::byte2bin(unsigned char x, char *bins)
{
	unsigned char byte_data = x;
	int i = 0;
	
	while (byte_data){
		bins[7 - i] = byte_data % 2;
		byte_data = byte_data / 2;
		i++;
	}
	if (i < 8){
		for (int j = i;j < 8;j++){
			bins[7 - j] = 0;
		}
	}
}
		
// from binary to byte: char [8] to unsigned char
unsigned char Number_conver::bin2byte(const char *bins)
{
	unsigned char byte_data = 0;
	for (int i = 0;i < 8;i++){
		byte_data += bins[i] * pow(2, 7 - i);
	}
	return byte_data;
}

// from bytes to binary: unsigned char [] to char []: bit: lens of bytes:
void Number_conver::bys2bin(const unsigned char *bys, char *bins, int bit)
{
	for (int i = 0;i < bit;i++){
		byte2bin(bys[i], &bins[8 * i]);
	}
}

// from binary to bytes: char [] to unsigned char []: bit: lens of bytes:
void Number_conver::bin2bys(unsigned char *bys, const char *bins, int bit)
{
	for (int i = 0;i < bit;i++){
		bys[i] = bin2byte(&bins[8 * i]);
	}
}

// from float(decimal) to binary (char array): the lens of bins must be longer than bit
void Number_conver::dec2bin(float x, char *bins, int bit)
{
	int accuracy_bit = 0;
	int i = 0;
	unsigned char current_bit = 0;
	
	x -= (int)x;
	while (x){
	    x *= 2;
        current_bit = (x >= 1.0)?1:0;
		bins[i] = current_bit;
		if ((accuracy_bit == 0 && current_bit == 1) || accuracy_bit > 0){
			accuracy_bit += 1;
			if (accuracy_bit >= bit){
				break;
			}
		}
		x -= (int)x;
        i++;		
	}
	if (accuracy_bit < bit){
		for (int j = 0;j < (bit - accuracy_bit);j++){
			bins[i + j] = 0;
		}
	}
}

// from double (decimal) to binary (char array)
void Number_conver::dec2bin(double x, char *bins, int bit)
{
	int accuracy_bit = 0;
	int i = 0;
	unsigned char current_bit = 0;
	
	x -= (long int)x;
	while (x){
	    x *= 2;
        current_bit = (x >= 1.0)?1:0;
		bins[i] = current_bit;
		if ((accuracy_bit == 0 && current_bit == 1) || accuracy_bit > 0){
			accuracy_bit += 1;
			if (accuracy_bit >= bit){
				break;
			}
		}
		x -= (long int)x;
        i++;		
	}
	if (accuracy_bit < bit){
		for (int j = 0;j < (bit - accuracy_bit);j++){
			bins[i + j] = 0;
		}
	}
}

//from binary (char array) to float (decimal)
float Number_conver::bin2dec_float(const char *bins, int bit)
{
	float dec_float = 0;
	
	for (int i = 0;i < bit;i++){
		dec_float += bins[i] * pow(2, -i-1);
	}
	return dec_float;
}

//from binary (char array) to double (decimal)
double Number_conver::bin2dec_double(const char *bins, int bit)
{
	double dec_float = 0;
	
	for (int i = 0;i < bit;i++){
		dec_float += bins[i] * pow(2, -i-1);
	}
	return dec_float;
}

// from int to binary (char array) (L->R, High->Low)
void Number_conver::int2bin(int x, char *bins, int bit)   // lens of bins > bit
{
	int int_data = x;
	int i = 0;
	
	while (int_data){
		bins[bit - 1 - i] = int_data % 2;
		int_data = int_data / 2;
		i++;
	}
	if (i < bit){
		for (int j = i;j < bit;j++){
			bins[bit - 1 - j] = 0;
		}
	}
}

// from long int to binary (char array)
void Number_conver::long2bin(long int x, char *bins, int bit)
{
	long int long_data = x;
	int i = 0;
	
	while (long_data){
		bins[bit - 1 - i] = long_data % 2;
		long_data = long_data / 2;
		i++;
	}
	if (i < bit){
		for (int j = i;j < bit;j++){
			bins[bit - 1 - j] = 0;
		}
	}
}
		
// from binary (char array) to int 
int Number_conver::bin2int(const char *bins, int bit)
{
	int int_data = 0;
	
	for (int i = 0;i < bit;i++){
		if (bins[i]){
			int_data += pow(2, bit - 1 - i);
		}
	}
	return int_data;
}

// from binary (char array) to long int
long int Number_conver::bin2long(const char *bins, int bit)
{
	long int int_data = 0;
	
	for (int i = 0;i < bit;i++){
		if (bins[i]){
			int_data += pow(2, bit - 1 - i);
		}
	}
	return int_data;
}

// form float or double to binary (char array)
void Number_conver::float2bin(float x, char *bins)   // bins[32]
{
	char exponent_bin[FLOAT32_EXPONENT];              // 8 bits
	char fraction_bin[FLOAT32_FRACTION];              // 23 bits
    char int_bin[FLOAT32_BIT];                        // 32 bytes 
	char dec_bin[FLOAT32_BIT];                        // 32 bytes
	float abs_x, dec_x;
	int int_x;
	unsigned int sign;
	
	// initiate memory:
	memset(exponent_bin, '\0', FLOAT32_EXPONENT);
    memset(fraction_bin, '\0', FLOAT32_FRACTION);
	memset(int_bin, '\0', FLOAT32_BIT);
    memset(dec_bin, '\0', FLOAT32_BIT);
	
	sign = (x < 0.0)? 1 : 0;
	abs_x = (x < 0.0) ? (-x) : x;
	int_x = (int)(abs_x);
	dec_x = abs_x - int_x;
	
	debug_print("int_x", &int_x, 1);
	debug_print("dec_x", &dec_x, 1);
	
	if (0 == x){
		for (int i = 0;i < FLOAT32_BIT;i++){
			bins[i] = 0;
		}
		return;
	}
	// else if () INT_MAX.... maybe add later...
	
    // get the binary list of integer and decimal:
	int2bin(int_x, int_bin, FLOAT32_BIT);
	debug_print("int_bin", int_bin, FLOAT32_BIT);
	dec2bin(dec_x, dec_bin, FLOAT32_BIT);
	debug_print("dec_bin", dec_bin, FLOAT32_BIT);
	
	// unsigned int int_exponent = FLOAT32_EXPONENT_OFFSET - 1;
	int int_exponent = 0;
	
	// calculate the int_exponent and fraction_bin
	if (int_x > 0){   
	    int i, j;
		
		// int_x
		for (i = 0;i < FLOAT32_BIT;i++){
			if (int_bin[i] != 0){
				int_exponent = FLOAT32_BIT - i;
			    debug_print("int_exponent", &int_exponent, 1);
				for (j = i + 1;j < FLOAT32_BIT;j++){
					fraction_bin[j - i - 1] = int_bin[j];
				}
				break;
			}
		}
		debug_print("fraction_1", fraction_bin, int_exponent - 1);
		// dec_x:
		int rest_bits = FLOAT32_FRACTION - (int_exponent - 1);
		for (i = 0;i < rest_bits;i++){
			fraction_bin[int_exponent - 1 + i] = dec_bin[i];
		}
		debug_print("fraction_bin", fraction_bin, FLOAT32_FRACTION);
	} //if (int_x)
	else{
		int i, j;
		
		for (i = 0;i < FLOAT32_BIT;i++){
			if (dec_bin[i] != 0){
				int_exponent = -i;
				for (j = i + 1;j < (FLOAT32_FRACTION + i + 1);j++){
					fraction_bin[j - i - 1] = dec_bin[j];
				}
				break;
			}
		}
		debug_print("fraction_bin", fraction_bin, FLOAT32_FRACTION);
	}// else
	
    float dec = 0;
    for (int i = 0;i < FLOAT32_BIT;i++){
		if (fraction_bin[i] != 0){
		    dec += fraction_bin[i] * pow(2, -(i + 1));
	    }
	}
	debug_print("dec", &dec, 1);

    // calculate exponent: float32, 8 bit
    int_exponent += (FLOAT32_EXPONENT_OFFSET - 1);
	debug_print("int_exponent", &int_exponent, 1);
	
    int2bin(int_exponent, exponent_bin, FLOAT32_EXPONENT);
	debug_print("exponent_bin", exponent_bin, FLOAT32_EXPONENT);
	
	// copy bits:
	bins[0] = sign;
	for (int i = 0;i < FLOAT32_EXPONENT;i++){
		bins[i + 1] = exponent_bin[i];
	}
	for (int i = 0;i < FLOAT32_FRACTION;i++){
		bins[i + 1 + FLOAT32_EXPONENT] = fraction_bin[i];
	}
    debug_print("bins", bins, FLOAT32_BIT);
	return;
}

void Number_conver::double2bin(double x, char *bins)  // bins[64] 
{
	char exponent_bin[FLOAT64_EXPONENT];              // 8 bits
	char fraction_bin[FLOAT64_FRACTION];              // 23 bits
    char long_bin[FLOAT64_BIT];                        // 32 bytes 
	char dec_bin[FLOAT64_BIT];                        // 32 bytes
	double abs_x, dec_x;
	long int long_x;
	unsigned int sign;
	
	// initiate memory:
	memset(exponent_bin, '\0', FLOAT64_EXPONENT);
    memset(fraction_bin, '\0', FLOAT64_FRACTION);
	memset(long_bin, '\0', FLOAT64_BIT);
    memset(dec_bin, '\0', FLOAT64_BIT);
	
	sign = (x < 0.0)? 1 : 0;
	abs_x = (x < 0.0) ? (-x) : x;
	long_x = (long int)(abs_x);
	dec_x = abs_x - long_x;
	
	debug_print("long_x", &long_x, 1);
	debug_print("dec_x", &dec_x, 1);
	
	if (0 == x){
		for (int i = 0;i < FLOAT64_BIT;i++){
			bins[i] = 0;
		}
		return;
	}
	// else if () INT_MAX.... maybe add later...
	
    // get the binary list of integer and decimal:
	long2bin(long_x, long_bin, FLOAT64_BIT);
	debug_print("long_bin", long_bin, FLOAT64_BIT);
	dec2bin(dec_x, dec_bin, FLOAT64_BIT);
	debug_print("dec_bin", dec_bin, FLOAT64_BIT);
	
	// unsigned int int_exponent = FLOAT32_EXPONENT_OFFSET - 1;
	int int_exponent = 0;
	
	// calculate the int_exponent and fraction_bin
	if (long_x > 0){   
	    int i, j;
		
		// int_x
		for (i = 0;i < FLOAT64_BIT;i++){
			if (long_bin[i] != 0){
				int_exponent = FLOAT64_BIT - i;
			    debug_print("int_exponent", &int_exponent, 1);
				for (j = i + 1;j < FLOAT64_BIT;j++){
					fraction_bin[j - i - 1] = long_bin[j];
				}
				break;
			}
		}
		debug_print("fraction_1", fraction_bin, int_exponent - 1);
		// dec_x:
		int rest_bits = FLOAT64_FRACTION - (int_exponent - 1);
		for (i = 0;i < rest_bits;i++){
			fraction_bin[int_exponent - 1 + i] = dec_bin[i];
		}
		debug_print("fraction_bin", fraction_bin, FLOAT64_FRACTION);
	} //if (int_x)
	else{
		int i, j;
		
		for (i = 0;i < FLOAT64_BIT;i++){
			if (dec_bin[i] != 0){
				int_exponent = -i;
				for (j = i + 1;j < (FLOAT64_FRACTION + i + 1);j++){
					fraction_bin[j - i - 1] = dec_bin[j];
				}
				break;
			}
		}
		debug_print("fraction_bin", fraction_bin, FLOAT64_FRACTION);
	}// else
	
    double dec = 0;
    for (int i = 0;i < FLOAT64_BIT;i++){
		if (fraction_bin[i] != 0){
		    dec += fraction_bin[i] * pow(2, -(i + 1));
	    }
	}
	debug_print("dec", &dec, 1);

    // calculate exponent: float64, 11 bit
    int_exponent += (FLOAT64_EXPONENT_OFFSET - 1);
	debug_print("int_exponent", &int_exponent, 1);
    
	int2bin(int_exponent, exponent_bin, FLOAT64_EXPONENT);
	debug_print("exponent_bin", exponent_bin, FLOAT64_EXPONENT);
	
	// copy bits:
	bins[0] = sign;
	for (int i = 0;i < FLOAT64_EXPONENT;i++){
		bins[i + 1] = exponent_bin[i];
	}
	for (int i = 0;i < FLOAT64_FRACTION;i++){
		bins[i + 1 + FLOAT64_EXPONENT] = fraction_bin[i];
	}
    debug_print("bins", bins, FLOAT64_BIT);
	return;
}
		
// from binary (char array) to float 
float Number_conver::bin2float(const char *bins)
{
    char sign = 0;
	int int_exponent = 0;
	float float_fraction = 0.0;
	float float_data = 0.0;
	
	sign = bins[0];
	int_exponent = bin2int(&bins[1], FLOAT32_EXPONENT) - FLOAT32_EXPONENT_OFFSET;
	float_fraction = bin2dec_float(&bins[1 + FLOAT32_EXPONENT], FLOAT32_FRACTION) + 1.0;
	
	if (int_exponent == 0 && float_fraction == 0){
		return 0.0;
	}
	
	float_data = pow(-1, sign) * float_fraction * pow(2, int_exponent);
	return float_data;
}

// from binary (char array) to double
double Number_conver::bin2double(const char *bins)
{
	char sign = 0;
	int int_exponent = 0;
	double double_fraction = 0.0;
	double double_data = 0.0;
	
	sign = bins[0];
	int_exponent = bin2int(&bins[1], FLOAT64_EXPONENT) - FLOAT64_EXPONENT_OFFSET;
	double_fraction = bin2dec_double(&bins[1 + FLOAT64_EXPONENT], FLOAT64_FRACTION) + 1.0;
	
	if (int_exponent == 0 && double_fraction == 0){
		return 0.0;
	}
	
	double_data = pow(-1, sign) * double_fraction * pow(2, int_exponent);
	return double_data;
}

/**********************************************char******************************************/
// from unsigned char to char: [0, 255] ~ [-128, 127]
char Number_conver::byte2char(unsigned char x)
{
	char temp_bin[8];
	int sign = 0;
	int char_data = 0;
	
	byte2bin(x, temp_bin);
	debug_print("temp_bin", temp_bin, 8);
	sign = temp_bin[0];  
	temp_bin[0] = 0;
	char_data = bin2int(temp_bin, 8);
	debug_print("abs_char_data", &char_data, 1);
	if (sign == 1 && char_data == 0){
		return -128;
	}
	else{
		return (char)(pow(-1, sign) * char_data); 
	}
}
		
// from char to char: [-128, 127] ~ [0, 255]
unsigned char Number_conver::char2byte(char x)
{
	char temp_bin[8];
	unsigned char uchar_data = 0;
	
	int2bin((int)x, temp_bin, 8);
	uchar_data = bin2byte(temp_bin);
	return uchar_data;
}

/***************************************test*************************************/

void test_char_byte(Number_conver number_c);

void test_dec_bin(Number_conver number_c);

void test_dec_byte(Number_conver number_c);

void test_int_byte(Number_conver number_c);

void test_float_byte(Number_conver number_c);

void test_char_byte(Number_conver number_c)
{
	char x1[5] = {-128, -64, 0, 64, 127};
	unsigned char t1[5];
	char t2[5];
	unsigned char x2[5] = {0, 64, 128, 192, 255};
	
	for (int i = 0;i < 5;i++){
		t1[i] = number_c.char2byte(x1[i]);
		printf("%d ", t1[i]);
	}
	printf("\n");
	for (int i = 0;i < 5;i++){
		t2[i] = number_c.byte2char(t1[i]);
		printf("%d ", t2[i]);
	}
	printf("\n");
	return;
}

void test_dec_bin(Number_conver number_c)
{
}

void test_dec_byte(Number_conver number_c)
{
	float x1 = 0.0000001;
	double x2 = 0.1;
	float f1 = 0.0;
	double d1 = 0.0;
	unsigned char dec_f_byte[FLOAT32_BYTE_BUF];
	unsigned char dec_d_byte[FLOAT64_BYTE_BUF];
	
	memset(dec_f_byte, '\0', FLOAT32_BYTE_BUF);
    memset(dec_d_byte, '\0', FLOAT64_BYTE_BUF);
	
	// test float32
	number_c.dec2byte(x1, dec_f_byte);
	for (int i = 0;i < FLOAT32_BYTE_BUF;i++){
		printf("%d ", dec_f_byte[i]);
	}
	printf("\n");
	f1 = number_c.byte2dec_float(dec_f_byte);
	printf("%.15f\n", f1);
	
	// test float64
	number_c.dec2byte(x2, dec_d_byte);
	for (int i = 0;i < FLOAT64_BYTE_BUF;i++){
		printf("%d ", dec_d_byte[i]);
	}
	printf("\n");
	d1 = number_c.byte2dec_double(dec_d_byte);
	printf("%.15f\n", d1);
}

void test_int_byte(Number_conver number_c)
{
	int x1 = 111234;
	long int x2 = 123456789;
	int i1 = 0;
	long int l1 = 0;
	unsigned char int_byte[FLOAT32_BYTE_BUF];
	unsigned char long_byte[FLOAT64_BYTE_BUF];
	
	memset(int_byte, '\0', FLOAT32_BYTE_BUF);
    memset(long_byte, '\0', FLOAT64_BYTE_BUF);
	
	// test int:
	number_c.int2byte(x1, int_byte);
	for (int i = 0;i < FLOAT32_BYTE_BUF;i++){
		printf("%d ", int_byte[i]);
	}
	printf("\n");
	i1 = number_c.byte2int(int_byte);
	printf("%d\n", i1);
	
	//test long:
	number_c.long2byte(x2, long_byte);
	for (int i = 0;i < FLOAT64_BYTE_BUF;i++){
		printf("%d ", long_byte[i]);
	}
	printf("\n");
	l1 = number_c.byte2long(long_byte);
	printf("%ld\n", l1);
}

void test_float_byte(Number_conver number_c)
{
	float x1 = 178.123456789123456;
	double x2 = 178.123456789123456;
	float f1 = 0.0;
	double d1 = 0.0;
	unsigned char float_byte[FLOAT32_BYTE];   // 4
	unsigned char double_byte[FLOAT64_BYTE];  // 8
	
	memset(float_byte, '\0', FLOAT32_BYTE);
    memset(double_byte, '\0', FLOAT64_BYTE);
	
	printf("x1: %f, x2: %f\n", x1, x2);
	
	// test float
	printf("test float32:\n");
	number_c.float2byte(x1, float_byte);
	f1 = number_c.byte2float(float_byte);
	printf("%.7f\n", f1);
	
	// test double
	printf("test float64:\n");
	number_c.double2byte(x2, double_byte);
	d1 = number_c.byte2double(double_byte);
	printf("%.16f\n", d1);
	
	return;
}

void test_float_bin(Number_conver number_c)
{
	float x1 = 178.0;
	double x2 = 178.0;
	float f1 = 0.0;
	double d1 = 0.0;
	char float_bin[FLOAT32_BIT];   // 4
	char double_bin[FLOAT64_BIT];  // 8
	
	memset(float_bin, '\0', FLOAT32_BIT);
    memset(double_bin, '\0', FLOAT64_BIT);
	
	printf("x1: %f, x2: %f\n", x1, x2);
	
	// test float
	printf("test float32:\n");
	number_c.float2bin(x1, float_bin);
	f1 = number_c.bin2float(float_bin);
	printf("%.7f\n", f1);
	
	// test double
	printf("test float64:\n");
	number_c.double2bin(x2, double_bin);
	d1 = number_c.bin2double(double_bin);
	printf("%.16f\n", d1);
	
	return;
}

/* 
int main(int argc, char *argv[])
{
	Number_conver number_c(true);
    
	test_float_byte(number_c);
	// test_char_byte(number_c);
	// test_float_bin(number_c);
	
	return 0;
}
*/
