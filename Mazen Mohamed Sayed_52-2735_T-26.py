# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 16:26:37 2022

@author: Mazen
"""

import math

import numpy as np

import matplotlib.pyplot as plt

import sounddevice as sd

from scipy.fftpack import fft



# 1st Function

def SingleToneGeneration(n,I,F,Ti,Tp):
    
    '''
    
    I  : Interval
    Ti : Initial Time
    Tp : Period Time
    F  : Tone Frequency
    
    '''
    
    t =  np.linspace(0, I, n) 
    
    # UNIT STEP FUNCTION
    
    start_step = np.where(((t-Ti)>=0),1,0)
    
    end_step = np.where(((t-Ti-Tp)>=0),1,0)
    
    # Pulse
    
    pulse = start_step - end_step
    
    # Sin Function
    
    sin = np.sin(2 * np.pi * F * t)
    
    # Tone
    
    tone = sin * pulse
    
    # Display Tone
    
    ''' 
    
    plt.figure()
    
    plt.plot(t, tone , label = 'Tone')
    
    plt.grid(True)
    
    '''
    
    return tone


# 2nd Function


def SinglePairNote( left_note , right_note, n, I, Ti, Tp):
    
    '''
    
     get() method of dictionary data type returns
     value of passed argument if it is present
     in dictionary otherwise second argument will
     be assigned as default value of passed argument
     
    '''
    # GET LEFT NOTE FREQUENCY
    
    switcher_left = {
        
        'C3' : 130.81, 
        'D3' : 146.83,
        'E3' : 164.81,
        'F3' : 174.61,
        'G3' : 196,
        'A3' : 220,
        'B3' : 246.93,
        
    }
    
    left_freq = switcher_left.get(left_note,0)
    
   # GET rIGHT NOTE FREQUENCY
    
    switcher_right = {
        
        'C4' : 261.63, 
        'D4' : 293.66,
        'E4' : 329.63,
        'F4' : 349.23,
        'G4' : 392,
        'A4' : 440,
        'B4' : 493.88,
        
    }
    
    right_freq = switcher_right.get(right_note,0)
    
    # Generate Left Tone
    
    left_tone = SingleToneGeneration(n, I, left_freq, Ti, Tp)
    
    
    right_tone = SingleToneGeneration(n, I, right_freq, Ti, Tp)
    
    # Generate Mixed Tone
    
    mixed_tone = left_tone + right_tone 
    
    # Display Mixed Signal
    '''
    
    t =  np.linspace(0, I, n)
    
    plt.figure()
    
    plt.plot(t, mixed_tone,label = 'Mixed Note')
    
    plt.grid('True')
    
    '''

    return  mixed_tone


#3rd Function

def Play():
    
    list = []
    
    n = int(input("Please Enter Number of Samples : ")) # you can out value you want here
    
    I = int(input("Please Enter a Range : ")) # you can out value you want here
    
   # global t
    
    t = np.linspace(0, 3, 3*1024)
    
    # First Call
    
    in_1 = input("Please Enter a Left Note : ")
    
    in_2 = input("Please Enter a Right Note : ")
    
    if (in_1 == 'done' and in_2 =='done'):
        return 0
    
    Ti = float(input("Please Enter a Initial Time : "))
    
    Tp = float(input("Please Enter a Period : "))
    
    
    
    mixed = SinglePairNote(in_1, in_2, n, I, Ti, Tp)
    
    
    while(in_1 != 'done' or in_2 !='done'):
        
        mixed = SinglePairNote(in_1, in_2, n, I, Ti, Tp)
        
        list.append(mixed)
        
        in_1 = input("Please Enter a Left Note : ")
        
        in_2 = input("Please Enter a Right Note : ")
        
        if (in_1 == 'done' and in_2 =='done'):
            break
        
        Ti = float(input("Please Enter a Initial Time : "))
        
        Tp = float(input("Please Enter a Period : "))
        
       
        
        
    final_tone = 0
        
   
    for i in list :
        
        final_tone += i

    '''
    
    # Display Final Note
    
    t = np.linspace(0,I,n)
    
    plt.figure()
    
    plt.plot(t, final_tone)

    plt.grid('True')
    
    '''

    return final_tone



'''


Milestone 2


'''


# 4th Function
def NoiseGeneration():
    
    t = np.linspace(0, 3, 3*1024)
    
    # Pick Two Random Frequencies
    f1 = np.random.randint(0,512,1)
    f2 = np.random.randint(0,512,1)

    # Generate Noise
    sin_1 = np.sin(2*f1*np.pi*t)
    sin_2 = np.sin(2*f2*np.pi*t)
    noise = sin_1 + sin_2
    
    '''
    # Display Noise 
    
    plt.figure()
    
    plt.plot(t, noise)

    plt.grid('True')
    
    '''
    
    # Return Noise
    return noise

    
# Remove Noise from Signal
def NoiseCancellation(x_before,x_noised):
    
    # initialize two frequencies with zero
    f1s = 0
    f2s = 0
    
    # Transfer from Time Domain -> Frequency Domain
    t = np.linspace(0, 3, 3*1024)
    N = 3*1024
    ff = np.linspace(0,512,int(N/2))
    x_f = fft(x_noised)
    x_f = 2/N * np.abs(x_f[0:np.int(N/2)])
    
    x_bef = fft(x_before)
    x_bef = 2/N * np.abs(x_bef[0:np.int(N/2)])
    
    # Get Maximum Amplitude
    max1 = np.max(x_bef)
    print("Maximum1" ,max1)
    
    freqArr = [] # create empty list for frequency
    AmpArr  = [] # create empty list for amplitudes


    i = 0
    for z in x_f :
        if z > max1 :
            freqArr.append(i // 3)
            AmpArr.append(z)
        i+=1
        
    print(freqArr)
    # Generate F1
    maximum = 0
    f1s = 0
    i = 0
    for z in AmpArr :
        if z > maximum :
            f1s = freqArr[i]
            maximum = z
        i += 1
        
    freqArr.remove(f1s)
    AmpArr.remove(maximum)
    sin_1 = np.sin(2*f1s*np.pi*t)
    # Generate F2
    maximum = 0
    f2s = 0
    i = 0
    for z in AmpArr :
        if z > maximum :
            f2s = freqArr[i]
            maximum = z
        i += 1
    sin_2 = np.sin(2*f2s*np.pi*t)
    
    
    # Generate Filtered Signal
    x_filtered = x_noised - (sin_1 + sin_2)
    
    print("f1 ",f1s) 
    print("f2 ",f2s)
    
    # Return Filtered Frequency
    return x_filtered

''' Helper Methods '''
    
def Display(x_before,noise,x_filtered,x_noised):
    
    # Transfer From Time Domain -> Frequencyy Domain
    N = 3*1024
    f = np.linspace(0,512,int(N/2))
    
    
    x_before_f = fft(x_before)
    x_before_f = 2/N * np.abs(x_before_f[0:np.int(N/2)])
    
    noise_f  = fft(noise)
    noise_f  = 2/N * np.abs(noise_f [0:np.int(N/2)])
    
    x_filtered_f  = fft(x_filtered)
    x_filtered_f = 2/N * np.abs( x_filtered_f [0:np.int(N/2)])
    
    x_noised_f  = fft(x_noised)
    x_noised_f = 2/N * np.abs(  x_noised_f [0:np.int(N/2)])
    
    t = np.linspace(0, 3, 3*1024)
    
    # Display
    
    plt.subplot(4,2,1); plt.plot(t, x_before);
    plt.subplot(4,2,2); plt.plot(f, x_before_f);
    plt.subplot(4,2,3); plt.plot(t, noise);
    plt.subplot(4,2,4); plt.plot(f, noise_f);
    plt.subplot(4,2,5); plt.plot(t, x_noised);
    plt.subplot(4,2,6); plt.plot(f, x_noised_f);
    plt.subplot(4,2,7); plt.plot(t, x_filtered);
    plt.subplot(4,2,8); plt.plot(f, x_filtered_f);
    

''' Driver Code  '''

x_before = Play()

noise = NoiseGeneration()

x_noised = x_before + noise

x_filtered = NoiseCancellation(x_before,x_noised)

Display(x_before,noise,x_filtered,x_noised)

#sd.play(x_before,3*1024)

sd.play(x_noised,3*1024)

#sd.play(x_filtered,3*1024)