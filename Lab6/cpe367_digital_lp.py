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
def process_wav(fpath_wav_in,fpath_wav_out):
	"""
	: this example implements a very useful system:  y[n] = x[n]
	: input and output is accomplished via WAV files
	: return: True or False 
	"""
	
	# construct objects for reading/writing WAV files
	#  assign each object a name, to facilitate status and error reporting
	wav_in = cpe367_wav('wav_in',fpath_wav_in)
	wav_out = cpe367_wav('wav_out',fpath_wav_out)
	
	# open wave input file
	ostat = wav_in.open_wav_in()
	if ostat == False:
		print('Cant open wav file for reading')
		return False
		
	# configure wave output file, mimicking parameters of input wave (sample rate...)
	wav_out.copy_wav_out_configuration(wav_in)
	
	# open WAV output file
	ostat = wav_out.open_wav_out()
	if ostat == False:
		print('Cant open wav file for writing')
		return False
	
	###############################################################
	###############################################################
	
	M = 3				#number of coefficients
	bk = [0] * M
	G = 1				#gain
	fs = 16000 			#sampling rate
	fc = 2000			#center frequency
	F = fc / fs 		#digital frequency
	index = (M-1)//2 	#the range of index
 
	#initialize coefficient list
	n=-index
	for i in range(M):
		if n == 0:
			bk[i] = (F) * 2
		else:
			bk[i] = (G * (math.sin(2*math.pi*F*n))) / (math.pi * n)
		n += 1


	
	
	#create the fifo
	fifo = my_fifo(M)
	
 
	# students - allocate filter coefficients, length (M)
	# students - these are not the correct filter coefficients
	
	
	###############################################################
	###############################################################

	# process entire input signal
	xin = 0
	while xin != None:
	
		# read next sample (assumes mono WAV file)
		#  returns None when file is exhausted
		xin = wav_in.read_wav()
		if xin == None: break
		

		###############################################################
		###############################################################
		# students - go to work!
		
		# update history with most recent input
  
		fifo.update(xin)
		
		# evaluate your difference equation		
		yout = 0
		for k in range(M):
			
			yout += bk[k] * fifo.get(k)
		
		

		###############################################################
		###############################################################


		# convert to signed int
		yout = int(round(yout))
		
		# output current sample
		ostat = wav_out.write_wav(yout)
		if ostat == False: break
	
	# close input and output files
	#  important to close output file - header is updated (with proper file size)
	wav_in.close_wav()
	wav_out.close_wav()
		
	return True





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
			
	# grab file names
	fpath_wav_in = 'in_noise.wav'
	fpath_wav_out = 'out_noise_lp.wav'
	
	
	
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
	return process_wav(fpath_wav_in,fpath_wav_out)
	
			
	
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
