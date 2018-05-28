#include "number_conversion.h"


void Number_conver::number_conver(bool print_flag)
{
	debug_print_flag = print_flag
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
		    printf("%Lf ", infodouble[i]);
		}
		printf("\n");
	}
}

// from float(decimal) to binary (char array): the lens of bins must be longer than bit
void Number_conver::dec2bin(float x, char *bins, int bit);    
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

// from float or double (decimal) to binary (char array)
void dec2bin(double x, char *bins, int bit);  
		
//from binary (char array) to float or double (decimal)
float bin2float(const char *bins);
double bin2double(const char *bins);
		
//from int or long to binary (char array)
void int2bin(int x, char *bins, int bit);
void long2bin(long int x, char *bins, int bit);
		
//from binary (char array) to int or long int
int bin2int(const char *bins);
long int bin2long(const char *bins);
		
//form float or double to binary (char array)
void float2bin(float x, char *bins);
void double2bin(double x, char *bins);
		
//from binary (char array) to float or double
float bin2float(const char *bins);
double bin2double(const char *bins);
		
// from char to unsigned char
unsigned char char2byte(char x);


int main(int argc, char *argv[])
{
	Number_conver number_c(true);
	float x = 0.25;
	char dec_bin[50];
	int bit = 24;
	
	memset(dec_bin, '\0', 50);
	for (int i = 0;i < bit;i++){
		printf("%d ", dec_bin[i])
	}
	
}
