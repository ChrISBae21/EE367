#!/usr/bin/python

import sys
import time

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
	: this example does not implement an echo!
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
		
	# setup configuration for output WAV
	num_channels = 2
	sample_width_8_16_bits = 16
	sample_rate_hz = 16000
	wav_out.set_wav_out_configuration(num_channels,sample_width_8_16_bits,sample_rate_hz)

	# open WAV output file
	ostat = wav_out.open_wav_out()
	if ostat == False:
		print('Cant open wav file for writing')
		return False
	
	###############################################################
	###############################################################
	M = 720				# longest number of samples in the filters
 
	###############################################################
	###############################################################
	# initialize all the fifo's
	fifo_xin = my_fifo(M)	# fifo for input wav file
 
 	###############################################################
	###############################################################
 
	# iircomb filter fifo instantiations
	fifo_s1 = my_fifo(M)
	fifo_s2 = my_fifo(M)
	fifo_s3 = my_fifo(M)
	fifo_s4 = my_fifo(M)
	
	fifo_iir = my_fifo(M)	# iir output fifo
 	###############################################################
	###############################################################
 
	# all-pass filter fifo instantiations
	fifo_l1w = my_fifo(M)
	fifo_l1y = my_fifo(M)

	fifo_l2w = my_fifo(M)
	fifo_l2y = my_fifo(M)
 
  	###############################################################
	###############################################################
 
	# instantiate time delays
	t1 = 480
	t2 = 560
	t3 = 640
	t4 = 720
	t5 = 80
	t6 = 27
 
	g1 = 0.7
	g2 = 0.3
	###############################################################
	###############################################################

	# process entire input signal
	xin = 0
	impulse = 0
	while xin != None:
	
		# read next sample (assumes mono WAV file)
		#  returns None when file is exhausted
		xin = wav_in.read_wav()
		if xin == None: break
  
		'''if impulse == 12000:
			break
		if impulse == 100:
			xin = 30000
		else:
			xin = 0
		impulse+=1
  
		if xin == None:
			break'''

		###############################################################
		###############################################################
		
		# first filters
  
		xin *= 0.5
		fifo_xin.update(xin)
  
		# iir comb filters
		fifo_s1.update(fifo_xin.get(t1-1) + g1*fifo_s1.get(t1-1)) 
		fifo_s2.update(fifo_xin.get(t2-1) + g1*fifo_s2.get(t2-1))
		fifo_s3.update(fifo_xin.get(t3-1) + g1*fifo_s3.get(t3-1))
		fifo_s4.update(fifo_xin.get(t4-1) + g1*fifo_s4.get(t4-1))
		iir_filter = fifo_s1.get(0) + fifo_s2.get(0) + fifo_s3.get(0) + fifo_s4.get(0)
	
		fifo_iir.update(iir_filter) # irr comb filter output
  
		# all-pass filters
		fifo_l1w.update(fifo_iir.get(t5-1) + g1*fifo_l1w.get(t5-1))
		fifo_l1y.update((-g1 * iir_filter) + (1-g1*g1)*(fifo_l1w.get(0)))
  
		apf = fifo_l1y.get(0) # all pass filter output

		fifo_l2w.update(fifo_l1y.get(t6-1) + g1*fifo_l2w.get(t6-1))
		fifo_l2y.update((-g1 * fifo_l1y.get(0)) + (1-g1*g1)*(fifo_l2w.get(0)))
  

		yout_left = yout_right = g2*fifo_l2y.get(0) + xin # output
		
		
		# students - well done!
		###############################################################
		###############################################################

		# convert to signed int
		yout_left = int(round(yout_left))
		yout_right = int(round(yout_right))
		
		# output current sample
		ostat = wav_out.write_wav_stereo(yout_left,yout_right)
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
	fpath_wav_in = 'joy.wav'
	fpath_wav_out = 'joy_reverb.wav'
	
	
	
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
	


	# let's do it!
	return process_wav(fpath_wav_in,fpath_wav_out)
	
			
	
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
