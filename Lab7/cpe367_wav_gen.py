#!/usr/bin/python

import sys
import time
import math

import base64
import random as random

import datetime
import time

from cpe367_wav import cpe367_wav
from my_fifo import my_fifo


	
############################################
############################################
# define routine for implementing a digital filter
def wav_gen(fpath_wav_out):
	"""
	: this example implements a very useful system:  y[n] = x[n]
	: input and output is accomplished via WAV files
	: return: True or False 
	"""
	
	# construct objects for reading/writing WAV files
	#  assign each object a name, to facilitate status and error reporting
	wav_out = cpe367_wav('wav_out',fpath_wav_out)
	
		
	num_channels = 1
	sample_width_8_16_bits = 16
	sample_rate_hz = 8000
	wav_out.set_wav_out_configuration(num_channels,sample_width_8_16_bits,sample_rate_hz)

	
	# open WAV output file
	ostat = wav_out.open_wav_out()
	if ostat == False:
		print('Cant open wav file for writing')
		return False
	
	###############################################################
	###############################################################
	
	fo = 1000				#sinusoid frequency
	fs = 8000				#sampling rate 
	F = fo / fs				#digital sampling frequency
	M = 8000				#number of samples for 1 second
 
	a = 125					# amplitude increase found by trial and error
	tdelay = 0.1			#delay for the envelope
	ndelay = tdelay * fs	#800
	tau = tdelay / 5 		#time constant for the envelope where 5tau = 0.1 duration: 0.02

	
	
	###############################################################
	###############################################################

	# evaluate your difference equation		
	yout = 0
	for n in range(M):
		
		yout = a* math.exp(-((n-ndelay)/(fs*tau))) * math.cos(2*math.pi*F*n)
		#yout =  a*math.exp(-((n)/(fs*tau))) * math.cos(2*math.pi*F*n)  
		yout = int(round(yout))
		ostat = wav_out.write_wav(yout)
		if ostat == False: break
	
	
	#t * fs = n
	###############################################################
	###############################################################
	
	
	# close input and output files
	#  important to close output file - header is updated (with proper file size)

	wav_out.close_wav()
		
	return True





############################################
############################################
# define main program
def main(argv):

	# check python version!
	major_version = int(sys.version[0])
	if major_version < 3:
		print('Sorry! must be run using python3.')
		print('Current version: ')
		print(sys.version)
		return False
			
	# grab file names

	if len(sys.argv) > 1:
		fpath_wav_out = argv[1]
	else:
		fpath_wav_out = 'out.wav'
	
	
	
	'''
	############################################
	############################################
	# test signal history
	#  feel free to comment this out, after verifying
		
	# allocate history
	M = 3
	fifo = my_fifo(M)

	# add some values to history
	fifo.update(1)
	fifo.update(2)
	fifo.update(3)
	fifo.update(4)
	
	# print out history in order from most recent to oldest
	print('signal history - test')
	for k in range(M):
		print('hist['+str(k)+']='+str(fifo.get(k)))

	############################################
	############################################
	'''


	# let's do it!
	return wav_gen(fpath_wav_out)
	
			
	
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main(sys.argv[1:])
	quit()
