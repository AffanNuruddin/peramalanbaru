import pandas as pd
import numpy as np
from matplotlib import pyplot
from matplotlib import style
style.use("ggplot")
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error

series = pd.DataFrame(pd.read_csv(r"d:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/RegresiLinier.csv", header=0, index_col=0))
#periode = [series["periode"][a] for a in range(len(series["periode"]))]
#demand = [series["demand"][a] for a in range(len(series["demand"]))]
# split dataset
X = series.values
train, test = X[1:len(X)-7], X[len(X)-7:]
# train autoregression
model = AR(train)
model_fit = model.fit()
print('Lag: %s' % model_fit.k_ar)
print('Coefficients: %s' % model_fit.params)
# make predictions
predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
for i in range(len(predictions)):
	print('predicted=%f, expected=%f' % (predictions[i], test[i]))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
# plot results
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()