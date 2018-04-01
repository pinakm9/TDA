import pandas as pd
import numpy as np
from paths import *
from utility import *

@timer
def write_square_power():
	data = pd.read_csv(p2_energy_line)
	power_lines = list(set(data.LINESET))	
	raw_data = {'square_id':[], 'power_lines':[], 'indices':[], 'customer_sites':[]}
	for sq in set(data.SQUAREID):
		indices = np.where(data.SQUAREID == sq)[0]
		raw_data['square_id'].append(sq)
		lines = list(data.LINESET[indices])
		raw_data['power_lines'].append(lines)
		raw_data['indices'].append(list(map(lambda x: power_lines.index(x), lines)))
		raw_data['customer_sites'].append(list(data.NR_UBICAZIONI[indices]))
	with open(p2_square_power, 'w+'):
		pass
	pd.DataFrame(raw_data, columns = ['square_id', 'power_lines', 'indices', 'customer_sites'])\
	.to_csv(p2_square_power, index = False)

@timer
def write_power_square():
	data = pd.read_csv(p2_energy_line)	
	square_id = data.SQUAREID
	line_set = data.LINESET
	customer_sites = data.NR_UBICAZIONI
	raw_data = {'power_line':[], 'square_ids':[], 'customer_sites':[], 'total_sites':[], 'fractions':[]}
	for line in set(line_set):
		indices = np.where(line_set == line)[0]
		raw_data['power_line'].append(line)
		raw_data['square_ids'].append(list(square_id[indices]))
		sites = list(customer_sites[indices])
		total = sum(sites)
		raw_data['customer_sites'].append(sites)
		raw_data['total_sites'].append(total)
		raw_data['fractions'].append([s/float(total) for s in sites])
	with open(p2_square_power, 'w+'):
		pass
	pd.DataFrame(raw_data, columns = ['power_line', 'square_ids', 'customer_sites', 'total_sites', 'fractions'])\
	.to_csv(p2_power_square, index = False)

@timer
def write_ratios():
	sp = pd.read_csv(p2_square_power)
	ps = pd.read_csv(p2_power_square)
	fractions = []
	for i, sq in enumerate(sp['square_id']):
		frac = []
		for j in read_list(sp['indices'][i]):
			k = read_list(ps['square_ids'][j]).index(sq)
			frac.append(read_list_f(ps['fractions'][j])[k])
		fractions.append(frac)
	sp['fractions'] = fractions
	sp.to_csv(p2_square_power, index = False)

def aggregate_s_c_i():
	data = pd.read_csv(p2_telecom_activity)
	raw_data = {'square_id':[], 'day_of_week':[], 'hour_of_day': [], 'sms_in':[], 'sms_out':[], 'call_in':[],\
	'call_out':[], 'internet':[]}
	"""for sq in set(data['CellID']):
		indices = np.where(data['CellID'] == sq)[0]
		raw_data['square_id'].append(sq)"""
	print data['CellID'==151]['square_id']







write_power_square()
write_square_power()
write_ratios()
aggregate_s_c_i()