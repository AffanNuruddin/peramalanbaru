import numpy as np
import pandas as pd
import statsmodels
import patsy
import statsmodels.api as sm
import matplotlib.pyplot as plt

#Import model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

#Masukin data yang telah berbentuk csv dengan memanggil datanya sesuai tempat penyimpanannya
data=pd.read_csv(r"d:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/RegresiLinier1.csv")
periode = data.iloc[:, 0].values.reshape(-1, 1)
demand = data.iloc[:, 1].values.reshape(-1, 1)
#Kemudian memisahkan X dan y ke dalam data latih (train) dan data pengujian (test):
X_train, X_test, y_train, y_test = train_test_split(periode,demand,random_state=1)
print(X_train)
#print(X_test)
print(y_train)
# Linear Regression Model
Linreg=LinearRegression()

#Membuat model dengan data latihan
Linreg.fit(y_train,X_train)

#Membuat prediksi pada data pengujian
y_pred=Linreg.predict(y_test)
#linear_regressor = LinearRegression()  # create object for the class
#linear_regressor.fit(X, Y)  # perform linear regression
#Y_pred = linear_regressor.predict(X)  # make predictions
#menghitung RMSE
print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))

#mencari model regresi
model=sm.OLS(periode,demand).fit()
predictions=model.predict(y_test)
print(model.summary())

#menambahkan variabel konstan
#X=sm.add_constant(X)
#model=sm.OLS(y,X).fit()
#print(model.summary())

plt.scatter(periode, demand)
plt.plot(periode, predictions, color='red')
plt.show()