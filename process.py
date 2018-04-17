import pandas as pd
import numpy as np
import random
import os
import csv
from paths import *
from utility import *

@timer # Extracts lists of squares and lines from SET file and saves them to squares.csv, lines.csv
# lines.csv also contains the number of total sites for each power_line
def write_lists():
	data = pd.read_csv(p2_energy_line)
	squares = list(set(data.SQUAREID))
	squares.sort()
	pd.DataFrame({'squares': squares}, columns = ['squares']).to_csv(p2_list_sq, index = False)
	lines = list(set(data.LINESET))
	lines.sort()
	sites = []
	for line in lines:
		sites.append(data[data.LINESET == line].NR_UBICAZIONI.sum())
	pd.DataFrame({'lines': lines, 'sites': sites}, columns = ['lines', 'sites']).to_csv(p2_list_line, index = False)

@timer # Saves the powerline-square matrix to matrix.csv
def write_matrix():
	squares = list(pd.read_csv(p2_list_sq).squares)
	lines = list(pd.read_csv(p2_list_line).lines)
	sites = list(pd.read_csv(p2_list_line).sites)
	df = pd.read_csv(p2_energy_line)
	raw_data = {'lines': lines}
	for sq in squares:
		z = np.zeros(len(lines))
		df1 = df[df.SQUAREID == sq]
		for line in df1.LINESET:
			j = lines.index(line)
			z[j] = df1[df1.LINESET == line].NR_UBICAZIONI/float(sites[j])
		raw_data[sq] = z
	pd.DataFrame(raw_data, columns = ['lines'] + squares).to_csv(p2_matrix, index = False)

@timer # From matrix.csv eliminates rows, columns for which data is not available
# and saves the new matrix in submatrix.csv
def write_submatrix():
	avl_lines = list(set(pd.read_csv(p2_energy, header = None, names = ['line_id', 'date_time', 'amp']).line_id))
	avl_lines.sort()
	squares = list(pd.read_csv(p2_list_sq).squares)
	lines = list(pd.read_csv(p2_list_line).lines)
	bad_lines = list(set(lines)-set(avl_lines))
	df = pd.read_csv(p2_matrix).set_index('lines')
	drop = []
	for i, sq in enumerate(squares):
		for line in bad_lines:
			if df.loc[line, str(sq)] != 0:
				drop.append(str(sq))	
	df = df.drop(drop, axis = 1)
	df = df.drop(bad_lines, axis = 0)
	df.to_csv(p2_submatrix)
	print('Number of power lines: {}\tNumber of squares: {}'.format(len(df.index), len(df.columns)))


@timer # Verifies is matrix.csv is correctly computed by checking given row-sum is 1
def verify_row(i):
	df = pd.read_csv(p2_matrix).iloc[[i]]
	df = df.drop(df.columns[0], axis = 1)
	print('Row-sum: {}'.format(df.sum(axis = 1)))


@timer # Breaks an sms-call-internet file into pieces where timestamp is constant
def break_file(file):
	data = pd.read_csv(file)
	fl = os.path.basename(file)[:-4]
	files = []
	frames = []
	for tm in set(data.time):
		df = data[data.time == tm]
		out_file =  p2_sci_parts + fl + '-' + str(tm) + '.csv'
		df.to_csv(out_file, index = False)
		files.append(out_file)
		frames.append(df)
	return zip(files, frames)

@timer # Converts sms-call-internet text files to csv files
def txt2csv(file):
	data = pd.read_csv(file, sep = '\t', header = None, names = ['squareid', 'time', 'countrycode', 'smsin',\
	 'smsout', 'callin', 'callout', 'internet'])
	squares = list(pd.read_csv(p2_square_power).square_id)
	data = data[data.squareid.isin(squares)]
	data.to_csv(p2_pro_sci + os.path.basename(file)[:-4] +'.csv', index = False)

@timer # Combines parts of sms-call-internet files with same timestamps
def aggregate(file, frame = None, write = False, use_frame = False):
	data = frame if use_frame == True else pd.read_csv(file)
	raw_data = {'square_id':[], 'day_of_week':[], 'hour': [], 'part_of_hour':[], 'sms_in':[],\
	 'sms_out':[], 'call_in':[], 'call_out':[], 'internet':[]}
	file = os.path.basename(file)
	tm = read_Time(list(data.time)[0])
	day_of_week, hour, minute = read_time(tm)
	minute = minute/10
	for sq in set(data.squareid):
		df = data[data.squareid == sq]
		raw_data['square_id'].append(sq)
		raw_data['day_of_week'].append(day_of_week)
		raw_data['hour'].append(hour)
		raw_data['part_of_hour'].append(minute)
		raw_data['sms_in'].append(df.smsin.sum())
		raw_data['sms_out'].append(df.smsout.sum())
		raw_data['call_in'].append(df.callin.sum())
		raw_data['call_out'].append(df.callout.sum())
		raw_data['internet'].append(df.internet.sum())
	df = pd.DataFrame(raw_data, columns = ['square_id', 'day_of_week', 'hour', 'part_of_hour', 'sms_in', 'sms_out',\
	 'call_in', 'call_out', 'internet'])
	if write == True:
		df.to_csv(p2_pro_sci + file, index = False)
	return df
				
@timer # Combines parts of sms-call-internet files with same timestamps
def aggregate_day(file, write = False):
	print('Working on {} ...'.format(file))
	txt2csv(file)
	file = os.path.basename(file)[:-4]
	chunks = break_file(p2_pro_sci + file + '.csv')
	df = pd.DataFrame()
	for chunk in chunks:
		fl, frame = chunk
		df = pd.concat([df, aggregate(fl, frame, use_frame = True)], ignore_index = True)
		os.remove(fl)
		print('Deleted {}'.format(fl))
	df.to_csv(p2_pro_sci + file + '.csv', index = False)
	return df

@timer # Combines sms-call-internet files for each day of a given month and the folder where the files are located
def aggregate_month(folder, month):
	for file in os.listdir(folder):
		print('Working on {} ...'.format(file))
		aggregate(file)
	
@timer # Turns sms-call-internet files of a month into a single file
def combine_sci_month(month = 'November'):
	df = pd.DataFrame()
	for file in os.listdir(p2_pro_sci):
		df = df.append(pd.read_csv(p2_pro_sci + file))
	df.to_csv(p2_pro_sci + month + '.csv', index = False)

@timer
def aggregate_month(folder, month):
	print('Working on {} ...'.format(folder))
	df = pd.DataFrame()
	for file in os.listdir(folder):
		df = pd.concat([df, aggregate_day(folder + file)], ignore_index = True)
		print('Day {} done'.format(file))
	df.to_csv(p2_pro_sci + month + '.csv', index = False)

@timer
def break_amp():
	elec = pd.read_csv(p2_energy, header = None, names = ['line_id', 'date_time', 'amp']).sort_values('line_id')
	tms = list(set(elec.date_time))
	for tm in tms:
		print('Working on {}'.format(tm))
		elec[elec.date_time == tm].to_csv(p2_amp_parts + tm + '.csv', index = False)

@timer
def fix_amp(file, matrix, amps, squares, num_squares):
	print('Woring on file {}'.format(file))
	tm = file[:-4]
	date = int(tm.split(' ')[0][-2:])
	day_of_week, hour, part_of_hour = read_time(tm)
	part_of_hour = part_of_hour/10
	raw_data = {'square_id':[], 'amp':[]}
	raw_data['date'] = [date]*num_squares
	raw_data['day_of_week'] = [day_of_week]*num_squares
	raw_data['hour'] = [hour]*num_squares
	raw_data['part_of_hour'] = [part_of_hour]*num_squares
	for i, sq in enumerate(squares):
		raw_data['square_id'].append(int(sq))
		raw_data['amp'].append(np.dot(amps, matrix[:, i]))
	pd.DataFrame(raw_data, columns = ['square_id', 'date', 'day_of_week', 'hour', 'part_of_hour', 'amp']).\
	to_csv(p2_fixed_amp + file, index = False)

@timer
def fix_amps():
	mat = pd.read_csv(p2_submatrix)
	matrix = mat.drop('lines', axis = 1).as_matrix()
	squares = mat.columns[1:]
	num_squares = len(squares)
	for file in os.listdir(p2_amp_parts):
		amps = pd.read_csv(p2_amp_parts + file).amp
		try:
			fix_amp(file, matrix, amps, squares, num_squares)
		except:
			print('Fix attempt failed due to unavailability of data')

@timer
def combine_day_amp(date, month = 11, year = 2013):
	df = pd.DataFrame()
	files = os.listdir(p2_fixed_amp)
	for hr in range(24):
		for part in range(6):
			file = fname(year, month, date, hr, 10*part)
			if file in files:
				df = df.append(pd.read_csv(p2_fixed_amp + file))
				#os.remove(p2_fixed_amp + file)
	df.to_csv(p2_amp_final + str(year) + '-' + hr2str(month) + '-' + hr2str(date) + '.csv', index = False)

@timer
def combine_amp():
	for date in range(1, 31):
		print('Working on day: {}'.format(date))
		try:	
			combine_day_amp(date)
		except:
			print('Failed at day {}:'.format(date))
@timer
def sort_sci():
	for file in os.listdir(p2_pro_sci):
		if file.startswith('sms-call-internet'):
			print('Working on {}'.format(file))
			df = pd.read_csv(p2_pro_sci + file)
			day_of_week = dow(file[-14:-4])
			#df = df[df.day_of_week == day_of_week]
			new_df = pd.DataFrame()
			for hr in range(24):
				dfh = df[df.hour == hr]
				for part in range(6):
					new_df = new_df.append(dfh[dfh.part_of_hour == part].sort_values('square_id'))
			new_df.to_csv(p2_pro_sci + 'sci-' + file[-14:], index = False)

@timer
def fix_23(year = '2013', month = '11', last_day = '30'):
	for file in os.listdir(p2_pro_sci):
		if file.startswith('sci-' + year + '-' + month) == True:
			print('Working on {}'.format(file))
			df = pd.read_csv(p2_pro_sci + file)
			if file.endswith(last_day + '.csv') == False:
				date = int(file[-6:-4])
				file1 = file[:-6] + hr2str(date + 1) + '.csv'
				day = dow(file[-14:-4])
				df1 = pd.read_csv(p2_pro_sci + file1)
				df1 = df1[(df1.hour == 23) & (df1.day_of_week == day)]
				df = df.append(df1)
			df = df[df.day_of_week == day]
			df.to_csv(p2_pro_sci + 'f' + file, index = False)

@timer 
def combine_day(date, month = 11, year = 2013):
	suffix = str(year) + '-' + hr2str(month) + '-' + hr2str(date) + '.csv'
	amp_file = p2_amp_final + suffix
	tel_file = p2_pro_sci + 'fsci-' + suffix
	amp = pd.read_csv(amp_file)
	tel = pd.read_csv(tel_file)
	raw_data = {'square_id':[], 'date':[], 'day_of_week':[], 'hour':[], 'part_of_hour':[], 'sms_in':[],\
	'sms_out':[], 'call_in':[], 'call_out':[], 'internet':[], 'ampere':[]}
	rows = min(len(amp.square_id), len(tel.square_id))
	for i in range(rows):
		raw_data['square_id'].append(amp.square_id[i])
		raw_data['date'].append(amp.date[i])
		raw_data['day_of_week'].append(amp.day_of_week[i])
		raw_data['hour'].append(amp.hour[i])
		raw_data['part_of_hour'].append(amp.part_of_hour[i])
		raw_data['sms_in'].append(tel.sms_in[i])
		raw_data['sms_out'].append(tel.sms_out[i])
		raw_data['call_in'].append(tel.call_in[i])
		raw_data['call_out'].append(tel.call_out[i])
		raw_data['internet'].append(tel.internet[i])
		raw_data['ampere'].append(amp.amp[i])
	pd.DataFrame(raw_data, columns = ['square_id', 'date', 'day_of_week', 'hour',\
	 'part_of_hour', 'sms_in', 'sms_out', 'call_in', 'call_out', 'internet',\
	  'ampere']).to_csv(p2_final + 'esci-' + suffix, index = False)

@timer
def combine_month():
	for i in range(1, 31):
		print('Working on day {}'.format(i))
		combine_day(i)

@timer
def merge_esci(year = 2013, month = 11):
	df = pd.DataFrame()
	files = os.listdir(p2_final)
	files.sort()
	for file in files:
		if file.startswith('esci-'):
			df = df.append(pd.read_csv(p2_final + file))
	df.to_csv(p2_final + 'mesci-' + str(year) + '-' + str(month) + '.csv', index = False)

@timer
def sample(sz = 500, year = 2013, month = 11):
	df = pd.read_csv(p2_final + 'mesci-' + str(year) + '-' + str(month) + '.csv')
	rows = random.sample(list(range(len(df.square_id))), sz)
	df = df.iloc[rows].fillna(0)
	df.to_csv(p2_final + 'sample-' + str(year) + '-' + str(month) + '.csv', index = False)

@timer
def turn_binary(threshold = 5):
	file = p2_sample
	df = pd.read_csv(file)
	rows = len(df.ampere)
	for i in range(rows):
		if df.ampere[i] > threshold:
			df.at[i, 'ampere'] = 1
		else:
			df.at[i, 'ampere'] = 0
	file = file[:-4] + 'b.csv'
	df.to_csv(file, index = False)

@timer # Computes mean and median for given columns in sample file
def get_mean(cols = ['ampere'], file = p2_sample):
	df = pd.read_csv(file)
	for col in cols:
		x = np.nan_to_num(df[col])
		print('Mean {0} = {1},\t Median {0} = {2}'.format(col, np.average(x), np.median(x)))


#write_ratios()
#aggregate_month(p2_telecom_activity, 'November')
#break_file(p2_pro_sci + '2013-11-01.csv')
#aggregate(p2_pro_sci + '2013-11-01-1383343800000.csv', True)
#aggregate_day(p2_telecom_activity+'sms-call-internet-tn-2013-11-01.txt')
#write_matrix()
#verify_row(120)
#fix_amps()
#write_submatrix()
#combine_amp()
#sort_sci()
#combine_sci_month()
#fix_23()
#combine_day_amp(11)
#combine_day(30)
#merge_esci()
#sample(250000)
turn_binary()
#get_mean(['sms_in', 'sms_out', 'internet', 'call_in', 'call_out', 'square_id'], p2_mesci_13_11)