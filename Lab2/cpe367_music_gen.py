#!/usr/bin/python

import sys
import time

import base64
import random as random

import datetime
import time
import math

from cpe367_wav import cpe367_wav



############################################
############################################
# define function to add one note to list
# students - modify this function as needed!

def add_note(xlist,amp,w0,nstart,nlen):
	# creates the signal for each note, with a decaying envelope. 
	for n in range(nstart,nstart+nlen):
		xlist[n] += amp * math.exp(-((n-nstart)/(4560*3))) * math.sin(w0 * n)
	# note summed into signal
	return
	
			


############################################
############################################
# define routine for generating signal in WAV format
def gen_wav(fpath_wav_out):
	"""
	: this example generates a WAV file
	: output is accomplished via WAV files
	: return: True or False 
	"""
	
	
 
	# construct object for writing WAV file
	#  assign object a name, to facilitate status and error reporting
	wav_out = cpe367_wav('wav_out',fpath_wav_out)
		
	# setup configuration for output WAV
	num_channels = 1
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

	# dictionary of frequencies
	freqs = {
		"C4":  261.63,
		"C#4": 277.18, "Db4": 277.18,
		"D4":  293.66,
		"D#4": 311.14, "Eb4": 311.13,
		"E4":  329.63,
		"F4":  349.23,
		"F#4": 369.99, "Gb4": 369.99,
		"G4":  392,
		"G#4": 415.30, "Ab4": 415.30,
		"A4":  440,
		"A#4": 466.16, "Bb4": 466.16,
		"B4": 493.88
	}

	total_num_samples = 48000 # 3 second length  41040
	
	# allocate list of zeros to store an empty signal
	xlist = [0] * total_num_samples

 
	# melody and harmony
 
	# list of the notes for the song
	list_of_notes = [freqs["G4"], freqs["A4"], freqs["B4"], freqs["D4"]*2, freqs["C4"]*2, freqs["C4"]*2, freqs["E4"]*2, freqs["D4"]*2]
	n_start = 4560 # start time
	n_durr = 4560 # duration for 1 beat
	amp = 8191.75 # amplitude for main melody
	hamp = 1638.35 # amplitude for harmony
	for x in list_of_notes:
		w = get_rad_freq(x, sample_rate_hz)		# get the note frequency
		add_note(xlist,amp,w,n_start,n_durr)	# adds main melody note
		add_note(xlist,hamp,w*4,n_start,n_durr)	# adds upper harmony note
		add_note(xlist,hamp,w/3,n_start,n_durr)	# adds lower harmony note

		n_start += n_durr
  
	# bass
	# list of the bass notes for the song
	list_of_bass = [freqs["G4"]/4, freqs["G4"]/2, freqs["E4"]/2]
	bn_start = 0	# start time
	bn_durr = 13680	# duration for bass notes (dotted half)
	amp = 8191.75	# amplitude for bass
	for x in list_of_bass:
		w = get_rad_freq(x, sample_rate_hz)	# bass note frequency
		add_note(xlist,amp,w,bn_start,bn_durr)	# adds bass note
		bn_start += bn_durr
	# students - well done!
	###############################################################
	###############################################################



	# write samples to output file one at a time
	for n in range(total_num_samples):
	
		# convert to signed int
		yout = int(round(xlist[n]))
		
		# output current sample 
		ostat = wav_out.write_wav(yout)
		if ostat == False: break
	
	# close input and output files
	#  important to close output file - header is updated (with proper file size)
	wav_out.close_wav()
		
	return True


def get_rad_freq(freq, sample_rate):
    return 2 * math.pi * freq / sample_rate



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
	# fpath_wav_out = sys.argv[1]
	fpath_wav_out = 'music_synth.wav'

	# let's do it!
	return gen_wav(fpath_wav_out)
	
			
	
	
############################################
############################################
# call main function
if __name__ == '__main__':
	
	main()
	quit()
