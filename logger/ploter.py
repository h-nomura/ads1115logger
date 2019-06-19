import csv
import numpy as np
from matplotlib import pyplot as plt
import os
import pandas as pd
import sys

def noise_canceler(datetime,data,check_day_str,threshold):
    i = 0
    cancel_num = 0
    while i < (len(data) - 1 - cancel_num) :
        if abs(data[i] - data[i+1]) >= threshold:
            data.pop(i+1)
            datetime.pop(i+1)
            cancel_num += 1
        i += 1
    data_set = [datetime,data,check_day_str,threshold]
    return data_set

def all_plot(datetime,data,check_day_str,threshold):
    df = pd.DataFrame({
        'date time':pd.to_datetime(datetime),
        'Magnetic force':data
    })
    df =df.set_index('date time')
    # Figureの初期化
    fig = plt.figure(figsize=(30, 8)) #...1
    # Figure内にAxesを追加()
    ax = fig.add_subplot(111) #...2
    ax.plot(df.index,df['Magnetic force'])
    ax.set_title(check_day_str[0] + ' ' + 'Magnetic force(nT)_threshold=' + str(threshold))
    my_makedirs('./fig/' + check_day_str[0])
    plt.savefig('./fig/' + check_day_str[0] + '/' + check_day_str[0] + '_' + 'Magnetic force(nT)_threshold=' + str(threshold) + '.png')
    #Splt.show()

def one_hour_plot(num,time,magnetic,check_day_str,threshold):
    if check_day_str[num] != '0':
        #convert
        time_np = np.array(time)
        magnetic_np = np.array(magnetic)

        # Figureの初期化
        fig = plt.figure(figsize=(12, 8)) #...1
        # Figure内にAxesを追加()
        ax = fig.add_subplot(111) #...2
        ax.plot(time_np[num], magnetic_np[num]) #...3

        # legend and title
        #ax.legend(loc='best')
        ax.set_title(check_day_str[num] + ' ' + str(num) + ":00-" + str(num+1) + ":00-" + 'Magnetic force(nT)_threshold=' + str(threshold))
        my_makedirs('./fig/' + check_day_str[0])
        plt.savefig('./fig/' + check_day_str[0] + '/' + check_day_str[0] + '_'  + str(num) + "00-" + str(num+1) + "00-" + 'Magnetic force(nT)_threshold=' + str(threshold) + '.png')

def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def main():
    args = sys.argv
    if len(args) != 2:
        print("write ==python ploter.py csvFilePass")
        sys.exit(1)
    csv_file = open(args[1],"r",encoding = "ms932",errors = "", newline = "")
    f = csv.reader(csv_file, delimiter=",",doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    header = next(f)
    #print(header)

    time = [[] for i in range(24)]
    magnetic = [[] for i in range(24)]
    check_day_str = ['0' for i in range(24)]

    datetime = []
    data = []
    for row in f:#row is list
        datetime.append(row[0].replace('_','-') + ' ' + row[1] + ':' + row[2] + ':' + row[3])
        data.append(float(row[7]))

        for i in range(24):
            if int(row[1]) == i:
                if check_day_str[i] == '0':
                    check_day_str[i] = row[0]
                time[i].append(int(row[2]))
                magnetic[i].append(float(row[7]))
                #print(str(i) + " " + row[1] + " " + row[2] + " " +row[7])

    all_plot(datetime,data,check_day_str,0)
    data_set = noise_canceler(datetime,data,check_day_str,10)
    all_plot(data_set[0],data_set[1],data_set[2],data_set[3])
    for i in range(24):
        one_hour_plot(i,time,magnetic,check_day_str,0)

if __name__ == '__main__':
	main()