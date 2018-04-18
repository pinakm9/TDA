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
	date, hour = s.split(' ')
	to_int = lambda x, sep: list(map(int, x.split(sep)))
	date = to_int(date, '-')
	hour = to_int(hour, ':')
	return [dt.date(*date).weekday(), hour[0], hour[1]]

def read_Time(i):
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(i/1000))

def hr2str(hour):
	return '0' + str(hour) if hour < 10 else str(hour)

def read_strs(ls):
	ls = ls.split(', ')
	ls[0] = ls[0][1:]
	ls[-1] = ls[-1][:-1]
	return ls

def fname(yy, mm, dd, hh, mi):
	return str(yy) + '-' + hr2str(mm) + '-' + hr2str(dd) + ' ' + hr2str(hh) + ':' + hr2str(mi) + '.csv'

def dow(date, sep = '-'):
	date = list(map(int, date.split(sep)))
	return dt.date(*date).weekday()

