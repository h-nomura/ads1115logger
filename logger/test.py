day = '2017-08-01 02:03:04'
print(day[8:10])
a = int(day[8:10]) + 1
b = '{0:02d}'.format(a)
day =day[0:8] + b + day[10:19]
print(day)
