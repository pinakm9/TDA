from time import time

# Timing wrapper
def timer(func):
	def new_func(*args,**kwargs):
		start = time()
		val = func(*args,**kwargs)
		end = time()
		print('Time taken by function {} is {} seconds'.format(func.__name__, end-start))
		return val
	return new_func

def read_list(s):
	return list(map(int, str(s[1:-1]).split(', ')))

def read_list_f(s):
	return list(map(float, str(s[1:-1]).split(', ')))