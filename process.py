import pandas as pd
import numpy as np
import os
import csv
from paths import *
from utility import *

@timer
def write_square_power():
	data = pd.read_csv(p2_energy_line)
	power_lines = list(set(data.LINESET))	
	raw_data = {'square_id':[], 'power_lines':[], 'indices':[], 'customer_sites':[]}
	for sq in set(data.SQUAREID):
		df = data[data.SQUAREID == sq]
		raw_data['square_id'].append(sq)
		lines = list(df.LINESET)
		raw_data['power_lines'].append(lines)
		raw_data['indices'].append(list(map(lambda x: power_lines.index(x), lines)))
		raw_data['customer_sites'].append(list(df.NR_UBICAZIONI))
	pd.DataFrame(raw_data, columns = ['square_id', 'power_lines', 'indices', 'customer_sites'])\
	.to_csv(p2_square_power, index = False)

@timer
def write_power_square():
	data = pd.read_csv(p2_energy_line)	
	raw_data = {'power_line':[], 'square_ids':[], 'customer_sites':[], 'total_sites':[], 'fractions':[]}
	for line in set(data.LINESET):
		df = data[data.LINESET == line]
		raw_data['power_line'].append(line)
		raw_data['square_ids'].append(list(df.SQUAREID))
		sites = list(df.NR_UBICAZIONI)
		total = sum(sites)
		raw_data['customer_sites'].append(sites)
		raw_data['total_sites'].append(total)
		raw_data['fractions'].append([s/float(total) for s in sites])
	pd.DataFrame(raw_data, columns = ['power_line', 'square_ids', 'customer_sites', 'total_sites', 'fractions'])\
	.to_csv(p2_power_square, index = False)

@timer
def write_ratios():
	sp = pd.read_csv(p2_square_power)
	ps = pd.read_csv(p2_power_square)
	fractions = []
	for i, sq in enumerate(sp.square_id):
		frac = []
		for j in read_list(sp.indices[i]):
			k = read_list(ps.square_ids[j]).index(sq)
			frac.append(read_list_f(ps.fractions[j])[k])
		fractions.append(frac)
	sp['fractions'] = fractions
	sp.to_csv(p2_square_power, index = False)

@timer
def shorten_file(file):
	data = pd.read_csv(file)
	squares = list(pd.read_csv(p2_square_power).square_id)
	data = data[data.square_id.isin(squares)]
	data.to_csv(p2_pro_sci + file[-14:], index = False)

@timer
def break_file(file):
	data = pd.read_csv(file)
	file = file[len(p2_pro_sci):-4]
	for hour in range(24):
		time = file + ' ' + hr2str(hour) + ':00:00'
		df = data[data.datetime == time]
		out_file =  p2_pro_sci + file + '-' + hr2str(hour) + '.csv'
		df.to_csv(out_file, index = False)

@timer
def txt2csv(file):
	in_txt = csv.reader(open(file, "rb"), delimiter = '\t')
	out_csv = csv.writer(open(file[:-4] + '.csv', 'wb+'))
	out_csv.writerow(['square_id', 'datetime', 'countrycode', 'smsin', 'smsout', 'callin', 'callout', 'internet'])
	out_csv.writerows(in_txt)

@timer
def fix_time(file):
	df = pd.read_csv(file)
	df.datetime = [read_Time(t) for t in df.datetime]
	df.to_csv(file, index = False)

@timer
def txt_to_csv(file):
	txt2csv(file)
	with open(file[:-4] + '.csv'):
		pass
	shorten_file(file[:-4] + '.csv')
	fix_time(p2_pro_sci + file[len(p2_telecom_activity):-4] + '.csv')

@timer
def aggregate_hour(file, write = False):
	data = pd.read_csv(file)
	squares = pd.read_csv(p2_square_power).square_id
	raw_data = {'square_id':[], 'day_of_week':[], 'hour_of_day': [], 'sms_in':[], 'sms_out':[], 'call_in':[],\
	'call_out':[], 'internet':[]}
	file = file[len(p2_pro_sci):-4]
	day_of_week = read_day(file[:-3])
	hour_of_day = int(file[-2:])
	for sq in set(data.CellID):
		df = data[data.CellID == sq]
		raw_data['square_id'].append(sq)
		raw_data['day_of_week'].append(day_of_week)
		raw_data['hour_of_day'].append(hour_of_day)
		raw_data['sms_in'].append(df.smsin.sum())
		raw_data['sms_out'].append(df.smsout.sum())
		raw_data['call_in'].append(df.callin.sum())
		raw_data['call_out'].append(df.callout.sum())
		raw_data['internet'].append(df.internet.sum())
	df = pd.DataFrame(raw_data, columns = ['square_id', 'day_of_week', 'hour_of_day', 'sms_in', 'sms_out', 'call_in',\
	'call_out', 'internet'])
	if write == True:
		df.to_csv(p2_pro_sci + file +'.csv', index = False)
	return df
				
@timer 
def aggregate_day(file, write = False):
	print('Working on {} ...'.format(file))
	shorten_file(file)
	file = file[-14:-4]
	break_file(p2_pro_sci + file + '.csv')
	df = pd.DataFrame()
	for hour in range(24):
		fl = p2_pro_sci + file + '-' + hr2str(hour) + '.csv'
		df = pd.concat([df, aggregate_hour(fl)], ignore_index = True)
		os.remove(fl)
		print('Hour {} done'.format(hour))
	if write == True:
		df.to_csv(p2_pro_sci + file + '.csv', index = False)
	return df

@timer
def aggregate_month(folder, month):
	print('Working on {} ...'.format(folder))
	df = pd.DataFrame()
	for file in os.listdir(folder):
		print file
		df = pd.concat([df, aggregate_day(folder + file)], ignore_index = True)
		print('Day {} done'.format(file))
	df.to_csv(p2_pro_sci + month + '.csv', index = False)












#write_power_square()
#write_square_power()
#write_ratios()
#aggregate_month(p2_telecom_activity, 'November')
txt_to_csv(p2_telecom_activity + 'sms-call-internet-tn-2013-11-01.txt')

