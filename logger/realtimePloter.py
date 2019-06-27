# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

import csv
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import os
import sys
import datetime
import time
import multiprocessing
from multiprocessing import Process, Manager
import threading
import copy
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

def convert_nT(value):
    volte = (GAIN_V[GAIN] * (float(value) / 32768)) * 6.970260223 - 15.522769516
    return (volte * 1000) / 0.16

def logger_loop(writer,f,dataTime_list,data_list,today):
    counter = 0
    while True:
        now = datetime.datetime.now()#get time
        value = adc.read_adc(0,gain=GAIN)                
        data = ['{0:%Y-%m-%d}'.format(now),'{0:%H}'.format(now),'{0:%M}'.format(now),'{0:%S}'.format(now),'{0:%f}'.format(now),value,convert_nT(value)]
        writer = csv.writer(f)
        writer.writerow(data)
        
        data_list.append(convert_nT(value))
        dataTime_list.append(now)
        if len(data_list) > 500:
            data_list.pop(0)
            dataTime_list.pop(0)
        if counter == 100:
            print('{0:%Y-%m-%d  %H:%M:%S}'.format(now) + '  Magnetic force(nT)==' + str(convert_nT(value)))
            counter = 0
        counter += 1
        if '{0:%Y-%m-%d}'.format(now) != today:
            break
        today = '{0:%Y-%m-%d}'.format(now)

def logger_thread(writer,f,dataTime_list,data_list,today):
    for i in range(1):
        p = multiprocessing.Process(target=logger_loop, args=([writer,f,dataTime_list,data_list,today]))
        p.start()
    time.sleep(1)
    print(dataTime_list)

def main():
    plt.ion()
    plt.figure(figsize=(10, 6))
    plt.ylim(19000, 22000)
    plt.xlabel("time[s]")
    plt.ylabel("Magnetic force(nT)")
    plt.grid()

    manager = Manager()    
    dataTime_list = manager.list()
    data_list = manager.list()
    li, = plt.plot(dataTime_list,data_list)

    while True:
        now = datetime.datetime.now()#get time
        today = '{0:%Y-%m-%d}'.format(now)
        with open('./data/MI{0:%y-%m-%d_%Hh%Mm%Ss}.csv'.format(now),'w') as f:
            data = ['year_month_day','hour','minute','second','float','raw','Magnetic force(nT)']
            writer = csv.writer(f)
            writer.writerow(data)
            #thread = threading.Thread(target=logger_thread, args=([writer,f,dataTime_list,data_list,today]))
            #thread.start()
            p = multiprocessing.Process(target=logger_loop, args=([writer,f,dataTime_list,data_list,today]))
            p.start()
            time.sleep(5)
            print(data_list)
            while True:
                now = datetime.datetime.now()#get time
                #xfmt = mdates.DateFormatter("%M/%S")
                li.set_xdata(dataTime_list)
                li.set_ydata(data_list)        
                #plt.xlim(min(df_list['dataTime']), max(df_list['dataTime']))
                #print(int('{0:%S}'.format(max(df_list['dataTime'])))-int('{0:%S}'.format(min(df_list['dataTime']))))
                plt.draw()
                plt.pause(0.001)
                if '{0:%Y-%m-%d}'.format(now) != today:
                    break
                today = '{0:%Y-%m-%d}'.format(now)
            #thread2.join()
        #    while True:
        #        while True:
        #            now = datetime.datetime.now()#get time
        #            value = adc.read_adc(0,gain=GAIN)                
        #            data = ['{0:%Y-%m-%d}'.format(now),'{0:%H}'.format(now),'{0:%M}'.format(now),'{0:%S}'.format(now),'{0:%f}'.format(now),value,convert_nT(value)]
        #            writer = csv.writer(f)
        #            writer.writerow(data)
        #            
        #            df_list['data'].append(convert_nT(value))
        #            df_list['dataTime'].append(now)
        #            if len(df_list['data']) > 500:
        #                df_list['data'].pop(0)
        #                df_list['dataTime'].pop(0)
        #            if counter == 100:
        #                print('{0:%Y-%m-%d  %H:%M:%S}'.format(now) + '  Magnetic force(nT)==' + str(convert_nT(value)))
        #                counter = 0
        #                break
        #            counter += 1

        #        xfmt = mdates.DateFormatter("%M/%S")
        #        li.set_xdata(df_list['dataTime'])
        #        li.set_ydata(df_list['data'])        
        #        plt.xlim(min(df_list['dataTime']), max(df_list['dataTime']))
        #        plt.draw()
        #        plt.pause(0.001)

        #        if '{0:%Y-%m-%d}'.format(now) != today:
        #            break
        #        today = '{0:%Y-%m-%d}'.format(now)

if __name__ == '__main__':
	main()