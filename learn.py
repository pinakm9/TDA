from sklearn import linear_model 
import pandas as pd
from paths import *
import numpy as np

def collect_data(file):
	df = pd.read_csv(file)
	y = df.ampere
	cols = len(df.columns)
	X = np.nan_to_num(df.iloc[:, 0: cols-1].as_matrix())
	return X, y, df.columns

def lasso(alpha, file):
	X, y, var = collect_data(file) 
	clf = linear_model.Lasso(alpha)
	clf.fit(X, y)
	mse = np.mean((y - clf.predict(X))**2)
	print(clf.coef_, mse, clf.score(X,y))

def logit(file):
	X, y, var = collect_data(file) 
	clf = linear_model.LogisticRegression()
	clf.fit(X, y)
	mse = np.mean((y - clf.predict(X))**2)
	print(clf.coef_, mse, clf.score(X,y))

#lasso(1, p2_sample)
logit(p2_sample_b)