import numpy as np
import matplotlib.pyplot as plt
# Note this could be easily modified to do the same thing using a direct wav file feed 
# based on soundfile package but the same logic would apply
#
# arbitrary event length of 1.2 seconds chosen for data but could either be trained or
# game could wait until an eye movement is recorded before firing another invader
#
# event length, mean normalisations and LR sequence (up->down or down->up) are the
# simple features that would need to be trained during calibration

def Classifier(wave):

    
    # read in the .npy filtered file and use the real components to see if we can 
    # split and classify effectively based on a simple up/down
    
    
    # 1. Get the data, normalise to mean 0 and determine a rough boundary for 'event' behaviour
    #

   
    
    wm = np.mean(wave)
    
    wave = wave - wm
    boundary = 0.005

    
    passive = 0
    while passive < 0.8:
        
        boundary += 0.0001
        passive = len(wave[abs(wave) < boundary])/len(wave)
        
    #print(boundary)
    
    #
    # 2. Trim and leading false events outside boundary
    #
    
    startpos = list(wave).index(wave[abs(wave) < boundary][0])
    wave = wave[startpos + 1000:]
    

    
    # 3. Find the start of next event and decide if R/L based on sign
    
    count = 0

    modelled = list()
    
    while (count < 1):
    
        
        evPos = list(wave).index(wave[abs(wave) > boundary][0])
        
        # position of biggest positive and negative
        
        wind = wave[evPos:evPos + 12000]
        maxPos = list(wind).index(max(wind))
        minPos = list(wind).index(min(wind))
        
        if (maxPos > minPos):
            modelled.append('L')
        else:
            modelled.append('R')
            
        # advance pointer 12000
            
        wave = wave[evPos + 12000:]
        
        
        
        count += 1
    

    return modelled
