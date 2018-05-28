#ifndef NUMBER_CONVERSION_H_
#define NUMBER_CONVERSION_H_

#include <stdio.h>  
#include <strings.h>
#include <stdlib.h>
#include <memory.h> 


class number_conver
{
	public:
	    void Number_conver(bool print_flag);
		
	    //print data
		void debug_print(const char *infostr, const char *infochar, int data_lens);
		void debug_print(const char *infostr, const unsigned char *infouchar, int data_lens);
	    void debug_print(const char *infostr, const int *infoint, int data_lens);
		void debug_print(const char *infostr, const long int *infolong, int data_lens);
		void debug_print(const char *infostr, const float *infofloat, int data_lens);
		void debug_print(const char *infostr, const double *infodouble, int data_lens);
		
		// from float or double (decimal) to binary (char array)
        void dec2bin(float x, char *bins, int bit);    
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
	private:
	    bool debug_print_flag;
};


#endif
