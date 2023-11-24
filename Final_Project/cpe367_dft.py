#!/usr/bin/python

import sys
import time
import math

import base64
import random as random

import datetime
import time

import matplotlib.pyplot as plt
import numpy as np

from cpe367_wav import cpe367_wav
from my_fifo import my_fifo


	
############################################
############################################
# define routine for implementing a digital filter
def dft(fpath_wav_in):
	"""
	: this example implements a very useful system:  y[n] = x[n]
	: input and output is accomplished via WAV files
	: return: True or False 
	"""
	
	# construct objects for reading/writing WAV files
	#  assign each object a name, to facilitate status and error reporting
	wav_in = cpe367_wav('wav_in',fpath_wav_in)
	
	
	# open wave input file
	ostat = wav_in.open_wav_in()
	if ostat == False:
		print('Cant open wav file for reading')
		return False
		
	# configure wave output file, mimicking parameters of input wave (sample rate...)

	
	###############################################################
	###############################################################
	
	N = 8000 	#number of samples
	fs = 4000 	#sampling rate	makes copies at the sampling rate => (fo / fs) * N
	###############################################################
	###############################################################
	
	#initialize lists
	xin = [0]*N
	f = [0]*N
	xn_mag = [0]*N
	
	T = 0	#raw peak value
	npeak = 0
 
	# read N samples (assumes mono WAV file)
	for i in range(N):
		xin[i] = wav_in.read_wav()
		if xin == None: break
		
	###############################################################
	###############################################################	
 
	#calculate the frequency and magnitude of the DFT for each k
	for k in range(N):
		cos = 0
		sin = 0
		f[k] = fs*(k/N)									#calculates the frequency in Hz
  
		for n in range(N):
			if xin[n] == None: break
			cos += xin[n] * math.cos((2*math.pi*k*n)/N)
			sin += xin[n] * math.sin((2*math.pi*k*n)/N)
		real = cos / N
		imag = sin / N
		xn_mag[k] = math.sqrt((real*real) + (imag*imag))	#calculates the magnitude
  
		#keep track of the maximum magnitude
		if xn_mag[k] > T and f[k] < 2000:
			T = xn_mag[k]
			npeak = k
	# close input and output files
	#  important to close output file - header is updated (with proper file size)
	wav_in.close_wav()

	###############################################################
	###############################################################	

	#calculate weighted averages
	num = 0
	den = 0
	fc=0
	count = 0
	for k in range(N):
		if xn_mag[k] >= (T/2) and f[k] < 2000:	#find magnitudes greater than T/2 AND only the "left" side of the spectrum
			num += (f[k] * xn_mag[k])
			den += xn_mag[k]
			count += 1
		else:
			continue
	
	if den == 0:
		fc = 0
	else:
		fc = num / den

	###############################################################
	###############################################################	

	

	print('Max Magnitude: ' + str(T))
	print('Frequency of Raw Peak (Hz): ' + str(f[npeak]))
	print('Frequency of the peak found via weighted average: ' + str(fc))
 
	# matplotlib mimics the plotting environment of MatLab. Plots can be displayed like this
	# given two lists of data for x and y: xpoint_list and ypoint_list
	fig, ax = plt.subplots()
	ax.plot(np.array(f[:]), np.array(xn_mag[:]))
	ax.set(xlabel='Frequency (Hz)', ylabel='Counts', title=fpath_wav_in + ' ')
	ax.grid()
	fig.savefig('image_file.png')
	plt.show()
		
		
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
		fpath_wav_in = sys.argv[1]
	else:
		fpath_wav_in = 'cos_1khz_pulse_20msec.wav'
		#fpath_wav_in = 'part2.wav'
		#fpath_wav_in = 'tile1b.wav'
		
	
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
	return dft(fpath_wav_in)
	
			
	
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main(sys.argv[1:])
	quit()
