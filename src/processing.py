import numpy as np

def rolling_average(X, p):
	res = [np.nan] * p
	for i in range(p, len(X)):
		start, stop = i-p, i
		res.append(X[start:stop].mean())
	return np.array(res)
	
