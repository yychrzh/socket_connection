#include "number_conversion.h"

/**********************************debug_print************************************************************/
Number_conver::Number_conver(bool print_flag)
{
	debug_print_flag = print_flag;
}

void Number_conver::debug_print(const char *infostr, const char *infochar, int data_lens)
{
    if (debug_print_flag){
		printf("(num_char)");
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
		printf("(num_uchar)");
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
		printf("(num_int)");
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
		printf("(num_long)");
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
		printf("(num_float)");
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

// from byte to binary: unsigned char to char [8]: (L->R, High->Low)
void Number_conver::byte2bin(unsigned char x, char *bins)
{
	int i = 0;
	while (x){
		bins[7 - i] = x % 2;
		x = x / 2;
		i++;
	}
	if (i < 7){
		for (int j = i;j <= 7;j++){
			bins[j] = 0;
		}
	}
}
		
// from binary to byte: char [8] to unsigned char
unsigned char Number_conver::bin2byte(const char *bins)
{
	unsigned char byte_data = 0;
	for (int i = 0;i <= 7;i++){
		byte_data += bins[i] * pow(2, 7 - i);
	}
	return byte_data;
}

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

// from float or double to bytes (unsigned char array)
void Number_conver::float2byte(float x, unsigned char *bys)  // bys[4]
{
	char exponent_bin[FLOAT32_EXPONENT];        // 8 bits
	char fraction_bin[FLOAT32_FRACTION];        // 23 bits
	char temp_int_bytes[FLOAT32_BYTE_BUF];      
	char temp_dec_bytes[FLOAT32_BYTE_BUF];
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
	
	if (0 == x){
		for (int i = 0;i < FLOAT32_BYTE;i++){
			bys[i] = 0;
		}
		return;
	}
	// else if () INT_MAX.... maybe add later...
	
    // get the binary list of integer and decimal:
	int2byte(int_x, temp_int_bytes);
	dec2byte(dec_x, temp_dec_bytes);
	
	// unsigned int int_exponent = FLOAT32_EXPONENT_OFFSET - 1;
	int int_exponent = 0;
	// calculate the int_exponent and fraction_bin
	if (int_x > 0){   
	    int i, j;
		unsigned char temp_bin[8];
		memset(temp_bin, '\0', 8);
		
		// calculate the integer of exponent:
		for (i = 0;i < FLOAT32_BYTE_BUF;i++){
			if (temp_int_bytes[i] > 0){    // i: the first non zero bytes of int_x
				byte2bin(temp_int_bytes[i], temp_bin);
				for (j = 0;j < 8;j++){     // j: the first non zero bit ...
					if (temp_bin[j] > 0){
						int_exponent = ((FLOAT32_BYTE_BUF - i) * 8 - j);
						break;
					}
				} // for (j =
				break;
			} // if (temp_)
		} //for (i =
			
		// add the int's bit to the fraction:
		int dec_bits = FLOAT32_FRACTION;
	    for (int k = j + 1;k < 8;k++){
			fraction_bin[k - j - 1] = temp_bin[k]
		}
		for (int k = i + 1;k < FLOAT32_BYTE_BUF;k++){
			byte2bin(temp_int_bytes[k], temp_bin);
			for (int m = 0;m < 8;m++){
				fraction_bin[8 * (k - i - 1) + m + (7 - j)] = temp_bin[m];
			}
		}
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
			fraction_bin[int_exponent - 1 + 8 * (dec_bits / 8) + j] = temp_bin[j]
		}
	} //if (int_x)
	else{
		int i, j;
		unsigned char temp_bin[8];
		memset(temp_bin, '\0', 8);
		
		// calculate the int exponent:
		for (i = 0;i < FLOAT32_BYTE_BUF;i++){
			if (temp_dec_bytes[i] > 0){
				byte2bin(temp_byte_bytes[i], temp_bin);
				for (j = 0;j < 8;j++){     // j: the first non zero bit ...
					if (temp_bin[j] > 0){
						int_exponent = -(i * 8 + j);
						break;
					}
				} // for (j =
				break;
			} // if (temp_
		}// for (i = 
		
		// add the dec's bit to the fraction:
		int dec_bits = FLOAT32_FRACTION;
		for (int k = j + 1;k < 8;k++){
			fraction_bin[k - j - 1] = temp_bin[k];
		}
		dec_bits -= (7 - j);
		for (int k = i + 1;k < (i + 1 + dec_bits / 8);k++){
			byte2bin(temp_dec_bytes[k], temp_bin);
			for (int m = 0;m < 8;m++){
				fraction_bin[8 * (k - i - 1) + m + 7 - j] = temp_bin[m];
			}
		}
		dec_bits = dec_bits - 8 * (k - i - 1);
		byte2bin(temp_dec_bytes[k], temp_bin);
		for (j = 0;j < 8;j++){
			fraction_bin[FLOAT32_FRACTION - dec_bits - 1 + j] = temp_bin[j];
		}
	}// else
    // calculate exponent: float32, 8 bit
    int_exponent += (FLOAT32_EXPONENT_OFFSET - 1);
    byte2bin(int_exponent, exponent_bin);
	
	char float32_bin[FLOAT32_BIT];
	memset(temp_bin, '\0', 8);
	
	// copy bits:
	float32_bin[0] = sign;
	for (int i = 0;i < FLOAT32_EXPONENT;i++){
		float32_bin[i + 1] = exponent_bin[i];
	}
	for (int i = 0;i < FLOAT32_FRACTION;i++){
		float32_bin[i + 1 + FLOAT32_EXPONENT] = fraction_bin[i];
	}

	for (int i = 0;i < FLOAT32_BYTE;i++){
		bys[i] = bin2byte(&float32_bin[i * 8]);
	}
}
 
void Number_conver::double2byte(double x, unsigned char *bys)  // bys[8]
{
	
}
		
// from bytes (unsigned char array) to float or double
float Number_conver::byte2float(const unsigned char *bins)
{
	
}

double Number_conver::byte2double(const unsigned char *bins)
{
	
}


/******************************************bin*******************************************/

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



/***************************************test*************************************/

void test_dec_bin(Number_conver number_c);

void test_dec_byte(Number_conver number_c);

void test_int_byte(Number_conver number_c);

void test_dec_bin(Number_conver number_c)
{
	/*
	float x1 = 0.25;
	double x2 = 0.8175;
	char dec_f_bin[SINGLE_FLOAT];
	char dec_d_bin[DOUBLE_FLOAT];
	
	memset(dec_f_bin, '\0', SINGLE_FLOAT);
    memset(dec_d_bin, '\0', DOUBLE_FLOAT);
	
	number_c.dec2bin(x, dec_bin, SINGLE_FLOAT);
	for (int i = 0;i < bit;i++){
		printf("%d ", dec_bin[i]);
	}
	printf("\n");
	
	number_c.bin2dec_float(dec_f_bin, SINGLE_FLOAT);

	unsigned char x = 255;
	unsigned char y = 0;
	char byte_bins[8];
	
	
	memset(byte_bins, '\0', 8);
	number_c.byte2bin(x, byte_bins);
	for (int i = 0;i < 8;i++){
		printf("%d ", byte_bins[i]);
	}
	printf("\n");
	y = number_c.bin2byte(byte_bins);
	printf("%d\n", y);
	*/
}

void test_dec_byte(Number_conver number_c)
{
	float x1 = 0.1;
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

int main(int argc, char *argv[])
{
	Number_conver number_c(true);
    
	test_dec_byte(number_c);
}
