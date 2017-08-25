>>> import time
>>> startTime = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime())
>>> startTime
'08/25/2017 11:02:06 AM'
>>> endTime = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime())
>>> startTime > endTime
False
>>> endTime > startTime
True
>>> elapsed = endTime - startTime
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for -: 'str' and 'str'
>>> start = time.strptime(startTime)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Python27\lib\_strptime.py", line 478, in _strptime_time
    return _strptime(data_string, format)[0]
  File "C:\Python27\lib\_strptime.py", line 332, in _strptime
    (data_string, format))
ValueError: time data '08/25/2017 11:02:06 AM' does not match format '%a %b %d %H:%M:%S %Y'
>>> start = time.strptime(startTime, '%m/%d/%Y %I:%M:%S %p')
>>> start
time.struct_time(tm_year=2017, tm_mon=8, tm_mday=25, tm_hour=11, tm_min=2, tm_sec=6, tm_wday=4, tm_yday=237
)
>>> end = time.strptime(endTime, '%m/%d/%Y %I:%M:%S %p')
>>> elapsed = end - start
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for -: 'time.struct_time' and 'time.struct_time'
>>> import datetime
>>> from datetime import datetime
>>> start = datetime.strptime(startTime, '%m/%d/%Y %I:%M:%S %p'
... )
>>> start
datetime.datetime(2017, 8, 25, 11, 2, 6)
>>> end = datetime.strptime(endTime, '%m/%d/%Y %I:%M:%S %p')
>>> elapsed = end - start
>>> elapsed
datetime.timedelta(0, 65)
>>> datetime.strftime(elapsed, '%M:%S')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: descriptor 'strftime' requires a 'datetime.date' object but received a 'datetime.timedelta'
>>>
