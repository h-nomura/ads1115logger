# Import the ADS1x15 module.
#import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()

import csv

from matplotlib import pyplot as plt
import os

import sys
import datetime
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
# 000 : FSR = +/- 6.144 V(1) 
# 001 : FSR = +/- 4.096 V(1) 
# 010 : FSR = +/- 2.048 V (default) 
# 011 : FSR = +/- 1.024 V 
# 100 : FSR = +/- 0.512 V 
# 101 : FSR = +/- 0.256 V 
# 110 : FSR = +/- 0.256 V 
# 111 : FSR = +/- 0.256 V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 0
GAIN_V = [6.144,4.096,2.048,1.024,0.512,0.256,0.256,0.256]

import random
import matplotlib.dates as mdates

def convert_nT(value):
    volte = (GAIN_V[GAIN] * (float(value) / 32768)) * 6.970260223 - 15.522769516
    return (volte * 1000) / 0.16

def main():
    plt.ion()
    plt.figure(figsize=(10, 6))
    plt.ylim(19000, 25000)
    plt.xlabel("time[s]")
    plt.ylabel("Magnetic force(nT)")
    plt.grid()    
    df_list = {'dataTime':[],'data':[]}
    li, = plt.plot(df_list['dataTime'],df_list['data'])

    counter = 0
    while True:            
        now = datetime.datetime.now()#get time
        #value = adc.read_adc(0,gain=GAIN)
        value = random.randint(14500,14600)
        if counter == 100:
            print('{0:%Y-%m-%d  %H:%M:%S}'.format(now) + '  Magnetic force(nT)==' + str(convert_nT(value)))
            counter = 0
        df_list['data'].append(convert_nT(value))
        df_list['dataTime'].append(now)
        if len(df_list['data']) > 500:
            df_list['data'].pop(0)
            df_list['dataTime'].pop(0)
        xfmt = mdates.DateFormatter("%M/%S")
        li.set_xdata(df_list['dataTime'])
        li.set_ydata(df_list['data'])        
        plt.xlim(min(df_list['dataTime']), max(df_list['dataTime']))
        plt.draw()
        plt.pause(0.01)
        counter += 1

if __name__ == '__main__':
	main()