import time, datetime
import csv
import pprint
while True:
    now = datetime.datetime.now()#get time
    today = '{0:%Y-%m-%d}'.format(now)
    with open('./data/MI{0:%y-%m-%d_%Hh%Mm%Ss}.csv'.format(now),'w') as f:
        data = ['year_month_day','hour','minute','second','float','raw','Magnetic force(nT)']
        writer = csv.writer(f)
        writer.writerow(data)
        counter = 0
        while True:            
            if counter == 1000:
                print('  Magnetic force(nT)==')
                counter = 0
            
            data = ['{0:%Y-%m-%d}'.format(now),'{0:%H}'.format(now),'{0:%M}'.format(now),'{0:%S}'.format(now),'{0:%f}'.format(now),value,convert_nT(value)]
            writer = csv.writer(f)
            writer.writerow(data)
            counter += 1
            if '{0:%Y-%m-%d}'.format(now) != today:
                break
            today = '{0:%Y-%m-%d}'.format(now)