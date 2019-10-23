####################------------Linear Regression-----------#######################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
import pandas as pd

abse = 0
sqe = 0
pse = 0

#Impor Data dari Excel
xyz = pd.DataFrame(pd.read_csv(r"d:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/RegresiLinier.csv"))
periode = [xyz["periode"][a] for a in range(len(xyz["periode"]))]
demand = [xyz["demand"][a] for a in range(len(xyz["demand"]))]

#Proses persiapan x(Periode) dan y(Demand)
x2=[]
y2=[]
xy=[]
n = len(demand)

#Pencarian Periode(t)^2
for x in periode:
	x2.append(x**2)

#Pencarian Demand(Dt)^2
for y in demand:
	y2.append(y**2)

#Proses Pencarian Dt*t
i=0;
while(i<n):
	#Proses Penghitungan dari Demand(Dt)*Periode(t)
	dump = demand[i]*periode[i]
	xy.append(dump)
	i+=1
#Total dari Periode(t)
jmlhx = sum(periode)
#Total dari Demand(Dt)
jmlhy = sum(demand)
#Total dari Periode(t)^2
jmlhx2 = sum(x2)
#Total dari Demand(Dt)^2
jmlhy2 = sum(y2)
#Total dari Demand(Dt)*Periode(t)
jmlhxy = sum(xy)


#Proses penentuan nilai a dan b
a = ((jmlhy*jmlhx2)-(jmlhx*jmlhxy))/(n*jmlhx2-(jmlhx**2))
b = ((n*jmlhxy)-(jmlhx*jmlhy))/(n*jmlhx2-(jmlhx**2))

#Proses Penentuan Forecasting
hit = []
for x in periode:
	y = b*x+a
	hit.append(y.round(2))
#print(hit)   
	
#Menampilkan hasil Linear Regression
dic = {"Periode(t)":periode,"Demand(Dt)":demand,"t^2":x2,"Dt*t":xy,"a":a.__round__(2),"b":b.__round__(2),"Forecast":hit,"ABS(Error)":abse,"Squared Error":sqe, "Percent Error":pse}
hasil = pd.DataFrame.from_dict(dic)
hasil["Error"] = (hasil["Demand(Dt)"] - hasil["Forecast"]).round(2)
hasil["ABS(Error)"] =  (abs(hasil["Error"])).round(2)
hasil["Squared Error"] = (hasil["ABS(Error)"] * hasil["ABS(Error)"]).round(2)
hasil["Percent Error"] = (hasil["ABS(Error)"] / hasil["Demand(Dt)"]).round(2)

# Print the dataframe for analysis
print("")
print("                                     Linear Regression Data Analysis                                  ")
print("")
print(hasil)

# Rumus Menghitung MAEP, BIAS, MAD, MSE, MAPE
mae = (hasil["Error"].sum()/(len(demand))).round(2)
mad = (abs(hasil["Error"]).sum())/(len(demand))
mse = (abs(hasil["Squared Error"]).sum())/(len(demand))
mape = hasil["Percent Error"].sum()/(len(demand))
maep = abs(hasil["Error"]).sum()/(hasil["Demand(Dt)"].sum())

# Print hasil dari Periode(t), Demand(Dt), Periode(t)^2 & Demand(Dt)*Periode(t)
print("")
print("Total dari Periode(t) adalah %.0f"%jmlhx)
print("Total dari Demand(Dt) adalah %.0f"%jmlhy)
print("Total dari Periode(t)^2 adalah %.0f"%jmlhx2)
print("Total dari Demand(Dt)*Periode(t) adalah %.0f"%jmlhxy)

# Print hasil dari BIAS, MAD, MAPE & MAE Percentage
print("")
print(" BIAS:",(mae).round(2), "      MAD:",(mad).round(2), "      MSE:",(mse).round(2), "      MAPE:", (mape).round(2), "     MAE Percentage:",int(maep*100),"%")
print("")

#Grafik Linear Regression
plt.scatter(periode,demand,label='Data Aktual',s=20)
plt.plot(periode,demand,label='Garis Data Aktual')    
plt.plot(periode,hit,c='k',label='Hasil Regresi / Forecast',linewidth=2)
plt.title("Hasil Linear Regression Barang Angkut Juanda")
plt.ylabel("Demand(Dt)")
plt.xlabel("Periode(t)")
plt.legend()
fig = plt.figure(1)

#Ekspor Grafik
plt.savefig(r'd:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/grafik/grafik_linearregression.png')
plt.show()

#Ekspor Excel
df = pd.DataFrame(hasil)
df.to_excel(r'd:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/excel/linearregression.xlsx')