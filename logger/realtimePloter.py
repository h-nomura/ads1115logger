# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

import csv
import numpy as np
from matplotlib import pyplot as plt
import os
import pandas as pd
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
GAIN = 1
GAIN_V = [6.144,4.096,2.048,1.024,0.512,0.256,0.256,0.256]
import pprint

def convert_nT(value):
    volte = (GAIN_V[GAIN] * (float(value) / 32768)) * 6.970260223 - 15.522769516
    return (volte * 1000) / 0.16

def main():
    plt.ion()
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    plt.ylim(10000, 30000)
    plt.xlabel("time[s]")
    plt.ylabel("Magnetic force(nT)")
    ax.set_title('Magnetic force(nT)')
    df_list = {'dataTime':[],'data':[]}

    while True:
        now = datetime.datetime.now()#get time
        today = '{0:%Y-%m-%d}'.format(now)
        with open('./data/MI{0:%y-%m-%d_%Hh%Mm%Ss}.png'.format(now),'w') as f:
            data = ['year_month_day','hour','minute','second','float','raw','Magnetic force(nT)']
            writer = csv.writer(f)
            writer.writerow(data)
            counter = 0
            while True:            
                now = datetime.datetime.now()#get time
                value = adc.read_adc(0,gain=GAIN)
                if counter == 1000:
                    print('{0:%Y-%m-%d  %H:%M:%S}'.format(now) + '  Magnetic force(nT)==' + str(convert_nT(value)))
                    counter = 0
                
                data = ['{0:%Y-%m-%d}'.format(now),'{0:%H}'.format(now),'{0:%M}'.format(now),'{0:%S}'.format(now),'{0:%f}'.format(now),value,convert_nT(value)]
                writer = csv.writer(f)
                writer.writerow(data)
                counter += 1

                df_list['data'].append(convert_nT(value))
                df_list['dataTime'].append('{0:%Y-%m-%d %H:%M:%S.%f}'.format(now))
                if len(df_list['data']) > 100:
                    df_list['data'].pop(0)
                    df_list['dataTime'].pop(0)
                df = pd.DataFrame({
                    'date time':pd.to_datetime(df_list['dataTime']),
                    'Magnetic force':df_list['data']
                })
                df = df.set_index('date time')
                ax.plot(df.index,df['Magnetic force'])
                plt.draw()
                
                if '{0:%Y-%m-%d}'.format(now) != today:
                    break
                today = '{0:%Y-%m-%d}'.format(now)

if __name__ == '__main__':
	main()