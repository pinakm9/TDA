import pandas as pd
import numpy as np

def collect_data(cols):
	df = pd.read_csv('/home/pinak/Projects/data/Processed/final/sample-2013-11.csv')
	y = df.ampere
	X = df.iloc[:, cols].as_matrix()
	return X.astype(np.float)