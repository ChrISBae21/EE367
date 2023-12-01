#!/usr/bin/python

import sys
import time

import base64
import random as random

import datetime
import time
import math

import matplotlib.pyplot as plt
import numpy as np

from cpe367_wav import cpe367_wav
from cpe367_sig_analyzer import cpe367_sig_analyzer
from my_fifo import my_fifo


############################################
############################################
# define routine for detecting DTMF tones
def process_wav(fpath_sig_in):
	
		
	###############################
	# define list of signals to be displayed by and analyzer
	#  note that the signal analyzer already includes: 'symbol_val','symbol_det','error'
	more_sig_list = ['sig_1','sig_2']
	
	# sample rate is 4kHz
	fs = 4000
	
	# instantiate signal analyzer and load data
	s2 = cpe367_sig_analyzer(more_sig_list,fs)
	s2.load(fpath_sig_in)
	s2.print_desc()
 
 
	C = 64	# integer constant
	N = 8		# number of samples for FFT
##########################################################################################
#                                   FILTER COEFFICIENTS
##########################################################################################
#---------------------------------------ROW FILTERS---------------------------------------
   #FILTER 697
	fifo_y_697 = my_fifo(N)
	BK_697 = [0.169290213535903760755374491964175831527 , 0,
			-1 * -0.826083303834324933490051989792846143246,
			-1 * 0.809999999999999942268402719491859897971]
	#FILTER 770
	fifo_y_770 = my_fifo(N)
	BK_770 = [0.157777999999999991587174008600413799286  , 0,
			-1 * -0.6362768971317435129364525892015080899 ,
			-1 * 0.810000000000000386357612569554476067424 ]
	#FILTER 852
	fifo_y_852 = my_fifo(N)
	G_852 = 0.015112629278329485146836752562649053289 
	BK_852 = [G_852 * 1, G_852 * -1,
				-1 * -0.452592336290489505312706342010642401874,
				-1 * 0.969774741443340970725728311663260683417]
	#FILTER 941
	fifo_y_941 = my_fifo(N)
	G_941 = 0.023002894973895144509201671212395012844  
	BK_941 = [G_941 * 1, G_941 * -1,
				-1 * -0.153478999658473863609842169353214558214,
				-1 *  0.953994210052209634653763714595697820187]

#---------------------------------------COL FILTERS---------------------------------------

	#FILTER 1209
	fifo_y_1209 = my_fifo(N) 
	BK_1209 = [0.252709077018945524883974940166808664799, 0,
				-1 * 0.547983278990897049176567179529229179025,
				-1 * 0.722500000000000031086244689504383131862]
	#FILTER 1336	
	fifo_y_1336 = my_fifo(N)
	BK_1336 = [0.164146336458953157055873361969133839011, 0,
				-1 * 0.906515709705711492105706383881624788046,
				-1 * 0.810000000000000275335310107038822025061]
	#FILTER 1477
	fifo_y_1477 = my_fifo(N)
	G_1477 = 0.028555200420074644540591179975308477879
	BK_1477 = [G_1477 * 1, G_1477 * -1,
				-1 * 1.32566402619519951855409090057946741581,
				-1 * 0.942889599159850710918817640049383044243]
	#FILTER 1633
	fifo_y_1633 = my_fifo(N)
	G_1633 = 0.021124037382806222507003468535913270898
	BK_1633 = [G_1633 * 1, G_1633 * -1,
				-1 * 1.63359382006864151115621552889933809638,
				-1 * 0.957751925234387457841478408226976171136]

#------------------------------------------------------------------------------
#               Round all BK coefficients for every filter
	for i in range(4):
		BK_697[i] = int(round(BK_697[i] * C))
		BK_770[i] = int(round(BK_770[i] * C))
		BK_852[i] = int(round(BK_852[i] * C))
		BK_941[i] = int(round(BK_941[i] * C))

		BK_1209[i] = int(round(BK_1209[i] * C))
		BK_1336[i] = int(round(BK_1336[i] * C))
		BK_1477[i] = int(round(BK_1477[i] * C))
		BK_1633[i] = int(round(BK_1633[i] * C))

# create dictionary of tone frequency answers
	answers = {}
	answers[697]  = {1209: 1, 1336: 2, 1477: 3, 1633: 10}
	answers[770]  = {1209: 4, 1336: 5, 1477: 6, 1633: 11}
	answers[852]  = {1209: 7, 1336: 8, 1477: 9, 1633: 12}
	answers[941]  = {1209: 14, 1336: 0, 1477: 15, 1633: 13}
	answers[1209] = {697: 1, 770: 4, 852: 7, 941: 14}
	answers[1336] = {697: 2, 770: 5, 852: 8, 941: 0}
	answers[1477] = {697: 3, 770: 6, 852: 9, 941: 15}
	answers[1633] = {697: 10, 770: 11, 852: 12, 941: 13}
 

	fifo_x = my_fifo(N)	 # instantite xin fifo

	# process input	
	xin = 0
	count = 0
	for n_curr in range(s2.get_len()):
	
		# read next input sample from the signal analyzer
		xin = s2.get('xin',n_curr)
  
		########################
		# FILTER DIFFERENCE EQUATION EVALUATION
		
		y_out_770 = (xin * BK_770[0] + fifo_x.get(1) * BK_770[1]  + fifo_y_770.get(0) * BK_770[2] + fifo_y_770.get(1) * BK_770[3]) / C
		y_out_697 = (xin * BK_697[0] + fifo_x.get(1) * BK_697[1]  + fifo_y_697.get(0) * BK_697[2] + fifo_y_697.get(1) * BK_697[3]) / C
		y_out_852 = (xin * BK_852[0] + fifo_x.get(1) * BK_852[1]  + fifo_y_852.get(0) * BK_852[2] + fifo_y_852.get(1) * BK_852[3]) / C
		y_out_941 = (xin * BK_941[0] + fifo_x.get(1) * BK_941[1]  + fifo_y_941.get(0) * BK_941[2] + fifo_y_941.get(1) * BK_941[3]) / C
  
		y_out_1209 = (xin * BK_1209[0] + fifo_x.get(1) * BK_1209[1]  + fifo_y_1209.get(0) * BK_1209[2] + fifo_y_1209.get(1) * BK_1209[3]) / C
		y_out_1336 = (xin * BK_1336[0] + fifo_x.get(1) * BK_1336[1]  + fifo_y_1336.get(0) * BK_1336[2] + fifo_y_1336.get(1) * BK_1336[3]) / C
		y_out_1477 = (xin * BK_1477[0] + fifo_x.get(1) * BK_1477[1]  + fifo_y_1477.get(0) * BK_1477[2] + fifo_y_1477.get(1) * BK_1477[3]) / C
		y_out_1633 = (xin * BK_1633[0] + fifo_x.get(1) * BK_1633[1]  + fifo_y_1633.get(0) * BK_1633[2] + fifo_y_1633.get(1) * BK_1633[3]) / C
  
		# update recursive fifos
		fifo_x.update(xin)
		fifo_y_697.update(y_out_697)
		fifo_y_770.update(y_out_770)
		fifo_y_852.update(y_out_852)
		fifo_y_941.update(y_out_941)
	
		fifo_y_1209.update(y_out_1209)
		fifo_y_1336.update(y_out_1336)
		fifo_y_1477.update(y_out_1477)
		fifo_y_1633.update(y_out_1633)

	
		########################
		
		if((count % (N//N)) == 0): #16
			dft_697 = dft(N, fs, fifo_y_697)
			dft_770 = dft(N, fs, fifo_y_770)
			dft_852 = dft(N, fs, fifo_y_852)
			dft_941 = dft(N, fs, fifo_y_941)

			dft_1209 = dft(N, fs, fifo_y_1209)
			dft_1336 = dft(N, fs, fifo_y_1336)
			dft_1477 = dft(N, fs, fifo_y_1477)
			dft_1633 = dft(N, fs, fifo_y_1633)
  
		count += 1
  
		
		if (dft_697[1] > dft_770[1] and dft_697[1] > dft_852[1] and dft_697[1] > dft_941[1]):
			row = 697 
			r_mag = dft_697[1]
		elif (dft_770[1] > dft_852[1] and dft_770[1] > dft_941[1]):
			row = 770 
			r_mag = dft_770[1]
		elif (dft_852[1] > dft_941[1]):
			row = 852 
			r_mag = dft_852[1]
		else:
			row = 941 
			r_mag = dft_941[1]
   
	
		if (dft_1209[1] > dft_1336[1] and dft_1209[1] > dft_1477[1] and dft_1209[1] > dft_1633[1]):
			col = 1209
			c_mag = dft_1209[1]
		elif (dft_1336[1] > dft_852[1] and dft_1336[1] > dft_1477[1]):
			col = 1336 
			c_mag = dft_1336[1]
		elif (dft_1477[1] > dft_1633[1]):
			col = 1477 
			c_mag = dft_1477[1]
		else:
			col = 1633 
			c_mag = dft_1633[1]
		symbol_val_det =  answers[row][col]
  
		'''if count < 8 or (r_mag <= 20 and c_mag <= 20):
			symbol_val_det = 0'''
		

		# save intermediate signals as needed, for plotting
		#  add signals, as desired!
		s2.set('sig_1',n_curr,xin)
		s2.set('697',n_curr,dft_697[1]/1.5)
		s2.set('770',n_curr,dft_770[1]/1.5)
		#s2.set('852',n_curr,dft_852[1])
		#s2.set('941',n_curr,dft_941[1])
		
		s2.set('1209',n_curr,dft_1209[1]/1.5)
		s2.set('1336',n_curr,dft_1336[1]/1.5)
		#s2.set('1477',n_curr,dft_1477[1])
		#s2.set('1633',n_curr,dft_1633[1])
		

		# save detected symbol
		s2.set('symbol_det',n_curr,symbol_val_det)

		# get correct symbol (provided within the signal analyzer)
		symbol_val = s2.get('symbol_val',n_curr)

		# compare detected signal to correct signal
		symbol_val_err = 0
		if symbol_val != symbol_val_det: symbol_val_err = 1
		
		# save error signal
		s2.set('error',n_curr,symbol_val_err)
		
	
	# display mean of error signal
	err_mean = s2.get_mean('error')
	print('mean error = '+str( round(100 * err_mean,1) )+'%')
		
	# define which signals should be plotted
	#plot_sig_list = ['sig_1','sig_2','symbol_val','symbol_det','error']
	plot_sig_list = ['symbol_val','symbol_det','error', 
                  	 '697','770',
                     '1209','1336']
	'''plot_sig_list = ['sig_1','symbol_val','symbol_det', 
                  	 '697','770','852','941',
                     '1209','1336','1477','1633']'''
	
	# plot results
	s2.plot(plot_sig_list)
	
	return True



	
 
def dft(N, fs, y_fifo):
    # read N samples (assumes mono WAV file)
    T = 0
    npeak = 0
    xin = [0]*N
    for i in range(N):
        xin[i] = abs(y_fifo.get(i))
        
    xn_mag = [0]*N
    f = [0]*N
    
    for k in range(N):
        cos = 0
        sin = 0
        f[k] = fs*(k/N)									#calculates the frequency in Hz
        for n in range(N):
            cos += xin[n] * math.cos((2*math.pi*k*n)/N)
            sin += xin[n] * math.sin((2*math.pi*k*n)/N)
        real = cos / N
        imag = sin / N
        xn_mag[k] = math.sqrt((real*real) + (imag*imag))	#calculates the magnitude
        #keep track of the maximum magnitude
        if xn_mag[k] > T and f[k] < 2000:
            T = xn_mag[k]
            npeak = k

#calculate weighted averages
    num = 0
    den = 0
    fc = 0
    count = 0
    for k in range(N):
        if xn_mag[k] >= (T/2) and f[k] < 2000:    #find magnitudes greater than T/2 AND only the "left" side of the spectrum
            num += (f[k] * xn_mag[k])
            den += xn_mag[k] 	
            count += 1
        else:
            continue
    
    fc = num / den
    
    return (fc, xn_mag[round((fc*N)/fs)])
	
	
############################################
############################################
# define main program
def main():

	# check python version!
	major_version = int(sys.version[0])
	if major_version < 3:
		print('Sorry! must be run using python3.')
		print('Current version: ')
		print(sys.version)
		return False
		
	# assign file name
	#fpath_sig_in = 'dtmf_signals_slow.txt'
	fpath_sig_in = 'dtmf_signals_fast.txt'
	
	
	# let's do it!
	return process_wav(fpath_sig_in)


	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()


'''dft_r_list = [dft_697, dft_770, dft_852, dft_941]
		dft_c_list = [dft_1209, dft_1336, dft_1477, dft_1633]
		max_r_mag = 0
		max_c_mag = 0
		max_r_freq = 0
		max_c_freq = 0
		for i in range(4):
			if dft_r_list[i][1] > max_r_mag:
				max_r_mag = dft_r_list[i][1]
				max_r_freq = dft_r_list[i][0]
    
			if dft_c_list[i][1] > max_c_mag:
				max_c_mag = dft_c_list[i][1]
				max_c_freq = dft_c_list[i][0]

		r_ans = 0
		c_ans = 0

		if (max_r_freq >= 500 and max_r_freq <= 733):
			r_ans = 697
		elif (max_r_freq >= 734 and max_r_freq <= 811):
			r_ans = 770
		elif (max_r_freq >= 812 and max_r_freq <= 896):
			r_ans = 852
		elif (max_r_freq >= 897 and max_r_freq <= 1050):
			r_ans = 941
   
		if (max_c_freq >= 1109 and max_c_freq <= 1272):
			c_ans = 1209
		elif (max_c_freq >= 1273 and max_c_freq <= 1406):
			c_ans = 1336
		elif (max_c_freq >= 1407 and max_c_freq <= 1555):
			c_ans = 1477
		elif (max_c_freq >= 1556 and max_c_freq <= 1733):
			c_ans = 1633

		
		if r_ans not in answers or c_ans not in answers[r_ans]:
			symbol_val_det = 0
		else:
			symbol_val_det = answers[r_ans][c_ans]'''