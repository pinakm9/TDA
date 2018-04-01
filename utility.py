import time
import datetime as dt
# Timing wrapper
def timer(func):
	def new_func(*args,**kwargs):
		start = time.time()
		val = func(*args,**kwargs)
		end = time.time()
		print('Time taken by function {} is {} seconds'.format(func.__name__, end-start))
		return val
	return new_func

def read_list(s):
	return list(map(int, str(s[1:-1]).split(', ')))

def read_list_f(s):
	return list(map(float, str(s[1:-1]).split(', ')))

def read_day(date):
	date = list(map(int, date.split('-')))
	return dt.date(*date).weekday()

def read_time(s):
	date, time = s.split(' ')
	to_int = lambda x, sep: list(map(int, x.split(sep)))
	date = to_int(date, '-')
	time = to_int(time, ':')
	return [dt.date(*date).weekday(), time[0]]

def read_Time(i):
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(i/1000))

def hr2str(hour):
	return '0' + str(hour) if hour < 10 else str(hour)