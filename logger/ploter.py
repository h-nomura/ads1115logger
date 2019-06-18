import csv
import numpy as np
from matplotlib import pyplot as plt

import pandas as pd


csv_file = open("./data/MI19-06-17_17h14m37s","r",encoding = "ms932",errors = "", newline = "")
f = csv.reader(csv_file, delimiter=",",doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
header = next(f)
#print(header)

time = [[0] for i in range(24)]
magnetic = [[0] for i in range(24)]
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

df = pd.DataFrame({
    'date time':pd.to_datetime(datetime),
    'Magnetic force':data
})
df =df.set_index('date time')
# Figureの初期化
fig = plt.figure(figsize=(12, 8)) #...1
# Figure内にAxesを追加()
ax = fig.add_subplot(111) #...2
ax.plot(df.index,df['Magnetic force'])
ax.set_title(check_day_str[i] + ' ' + 'Magnetic force(nT)')
plt.savefig('./fig/' + check_day_str[i] + '_' + 'Magnetic force(nT).png')
plt.show()

for i in range(24):
    if check_day_str[i] != '0':
        #first 0 remove
        time[i].pop(0)
        magnetic[i].pop(0)
        #convert
        time_np = np.array(time)
        magnetic_np = np.array(magnetic)

        # Figureの初期化
        fig = plt.figure(figsize=(12, 8)) #...1
        # Figure内にAxesを追加()
        ax = fig.add_subplot(111) #...2
        ax.plot(time_np[i], magnetic_np[i]) #...3

        # legend and title
        #ax.legend(loc='best')
        ax.set_title(check_day_str[i] + ' ' + str(i) + ":00-" + str(i+1) + ":00-" + 'Magnetic force(nT)')
        plt.savefig('./fig/' + check_day_str[i] + '_' + str(i) + "00-" + str(i+1) + "00-" + 'Magnetic force(nT).png')