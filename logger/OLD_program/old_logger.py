# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

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

import time, datetime
import csv
import pprint

def measure(port_number):
    total = 0
    for i in range(100):
        value = adc.read_adc(port_number,gain=GAIN)
        total +=  value
    #print(total/100)
    return total/100

def convert_V(value):
    return (6.144 * (float(value) / 32768)) * 6.970260223 - 15.522769516

def convert_nT(value):
    volte = (6.144 * (float(value) / 32768)) * 6.970260223 - 15.522769516
    return (volte * 1000) / 0.16

now = datetime.datetime.now()#get time
with open('./data/MI{0:%y-%m-%d_%Hh%Mm%Ss}'.format(now),'w') as f:
    data = ['year_month_day','hour','minute','second','float','raw','volte(V)','Magnetic force(nT)']
    writer = csv.writer(f)
    writer.writerow(data)
    while True:
        
        #s_time = time.time()
        #for i in range(100):
        #    value1 = adc.read_adc(0,gain = GAIN)
        #    value2 = adc.read_adc(1,gain = GAIN)
        #    value3 = adc.read_adc(2,gain = GAIN)
        #    value4 = adc.read_adc(3,gain = GAIN)
        #f_time = time.time()
        #print("need time")
        #print(f_time - s_time)
        #value = adc.read_adc(1,gain = GAIN)
        
        now = datetime.datetime.now()#get time
        value = measure(0)
        print('{0:%Y-%m-%d  %H:%M:%S}'.format(now) + '  Magnetic force(nT)==' + str(convert_nT(value)))

        data = ['{0:%Y-%m-%d}'.format(now),'{0:%H}'.format(now),'{0:%M}'.format(now),'{0:%S}'.format(now),'{0:%f}'.format(now),value,convert_V(value),convert_nT(value)]
        writer = csv.writer(f)
        writer.writerow(data)
        #time.sleep(0.5)