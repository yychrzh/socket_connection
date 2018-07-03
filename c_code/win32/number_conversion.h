#ifndef NUMBER_CONVERSION_H_
#define NUMBER_CONVERSION_H_

#include <stdio.h>  
#include <stdlib.h>
#include <memory.h> 
#include <math.h>

// single float: 32 bits, 4 bytes
#define FLOAT32_BIT               32
#define FLOAT32_BYTE              4
#define FLOAT32_EXPONENT          8
#define FLOAT32_EXPONENT_OFFSET   127
#define FLOAT32_FRACTION          23
#define FLOAT32_BIN_BUF           150 //FLOAT32_FRACTION + (int)(pow(2, FLOAT32_EXPONENT) - 1)  // 150
#define FLOAT32_BYTE_BUF          4 // 19  // (int)(FLOAT32_BIN_BUF / 8) + 1   // 19

// double float: 64 bits, 8 bytes
#define FLOAT64_BIT               64
#define FLOAT64_BYTE              8
#define FLOAT64_EXPONENT          11
#define FLOAT64_EXPONENT_OFFSET   1023
#define FLOAT64_FRACTION          52
#define FLOAT64_BIN_BUF           1075 //FLOAT64_FRACTION + (int)(pow(2, FLOAT64_EXPONENT) - 1)  // 1075
#define FLOAT64_BYTE_BUF          8 // 135  // (int)(FLOAT64_BIN_BUF / 8) + 1    // 135

class Number_conver
{
	public:
		Number_conver(bool print_flag);
		
	    // print data
		void debug_print(const char *infostr, const char *infochar, int data_lens);
		void debug_print(const char *infostr, const unsigned char *infouchar, int data_lens);
	    void debug_print(const char *infostr, const int *infoint, int data_lens);
		void debug_print(const char *infostr, const long int *infolong, int data_lens);
		void debug_print(const char *infostr, const float *infofloat, int data_lens);
		void debug_print(const char *infostr, const double *infodouble, int data_lens);
		
		/*******************************byte********************************/
		// from float or double (decimal) to bytes (unsigned char array)
		void dec2byte(float x, unsigned char *bys);   // bys[19]
		void dec2byte(double x, unsigned char *bys);  // bys[135]
		
		// from byte (unsigned char array) to float or double (decimal)
		float byte2dec_float(const unsigned char *bys);   // bys[19]
		double byte2dec_double(const unsigned char *bys); // bys[135]
		
		// from int or long to bytes (unsigned char array)
        void int2byte(int x, unsigned char *bys);               // bys[19]  
		void long2byte(long int x, unsigned char *bys);         // bys[135]
		
		// from bytes (unsigned char array) to int or long int
        int byte2int(const unsigned char *bys);            // bys[19]
		long int byte2long(const unsigned char *bys);      // bys[135]
		
		// form float or double to bytes (unsigned char array)
        void float2byte(float x, unsigned char *bys);
		void double2byte(double x, unsigned char *bys);
		
		// from bytes (unsigned char array) to float or double
        float byte2float(const unsigned char *bys);
		double byte2double(const unsigned char *bys);
		
		// form float or double array to bytes (unsigned char array): data_lens: float or double data length
        void float_array2bys(const float *data, unsigned char *bys, int data_lens);
		void double_array2bys(const double *data, unsigned char *bys, int data_lens);
		
		// from bytes (unsigned char array) to float or double array: data_lens: float or double data length
        void bys2float_array(float *data, const unsigned char *bys, int data_lens);
		void bys2double_array(double *data, const unsigned char *bys, int data_lens);
		
		/*******************************bin********************************/
		// from byte to binary: unsigned char to char [8]
		void byte2bin(unsigned char x, char *bins);
		// from binary to byte: char [8] to unsigned char
        unsigned char bin2byte(const char *bins);
		
		// from bytes to binary: unsigned char [] to char []: bit: lens of bytes:
		void bys2bin(const unsigned char *bys, char *bins, int bit);
		// from binary to bytes: char [] to unsigned char []: bit: lens of bytes:
		void bin2bys(unsigned char *bys, const char *bins, int bit);
		
		// from float or double (decimal) to binary (char array)
        void dec2bin(float x, char *bins, int bit);    
		void dec2bin(double x, char *bins, int bit);  
		
		// from binary (char array) to float or double (decimal)
        float bin2dec_float(const char *bins, int bit);
		double bin2dec_double(const char *bins, int bit);
		
	    // from int or long to binary (char array)
        void int2bin(int x, char *bins, int bit);
		void long2bin(long int x, char *bins, int bit);
		
		// from binary (char array) to int or long int
        int bin2int(const char *bins, int bit);
		long int bin2long(const char *bins, int bit);
		
	    // form float or double to binary (char array)
        void float2bin(float x, char *bins);
		void double2bin(double x, char *bins);
		
		// from binary (char array) to float or double
        float bin2float(const char *bins);
		double bin2double(const char *bins);
		
		/*******************************char********************************/
		// from unsigned char to char: [0, 255] ~ [-128, 127]
		char byte2char(unsigned char x);
		
		// from char to char: [-128, 127] ~ [0, 255]
        unsigned char char2byte(char x);
		
	private:
	    bool debug_print_flag;
};


#endif
