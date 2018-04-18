from sklearn import linear_model, ensemble 
import pandas as pd
from paths import *
import numpy as np
from utility import *
from process import collect_data

@timer
def regressor(file, model, is_tree = False):
	X, y, var = collect_data(file) 
	model.fit(X, y)
	error = (y - model.predict(X))**2
	print('Predictor\tImportance\n{}\t{}'.format('-'*9, '-'*11))
	imp = model.coef_[0] if is_tree == False else model.feature_importances_
	for i, v in enumerate(var[:-1]):	
		print('{: <11}\t{:+f}'.format(v, imp[i]))
	print('Mean squared error = {}\nCoefficient of prediction = {}'\
		.format(np.mean(error), model.score(X,y)))


#regressor(p2_mesci_13_11, ensemble.RandomForestRegressor(), True)
regressor(p2_sample_b, linear_model.LogisticRegression())