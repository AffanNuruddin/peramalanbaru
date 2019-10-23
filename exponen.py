import xlsxwriter
from functools import partial
import numpy as np
from numpy import convolve
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
import re
# import seaborn as sns
from datetime import datetime

# Forecasting Jumlah barang yang diangkut/bulan di Bandara Juanda.

alpha = 0.3
abse = 0
sqe = 0
pse = 0

xyz = pd.DataFrame(pd.read_csv(r"d:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/bandara.csv")) 
bulan = [xyz["Bulan"][i] for i in range(len(xyz["Bulan"]))]
demand = [xyz["Demand"][i] for i in range(len(xyz["Demand"]))]

##################---------Exponential Smoothing---------#######################

# Mendefinisikan forecast, forcast pertama pasti null 
f = [np.nan]

# Forcast kedua, nilainya sama dengan nilai permintaan pertama
f.append(demand[0])

# Loop Forcast
for t in range(1,len(demand)-1):
    f.append((1-alpha)*f[-1]+alpha*demand[t])

# Menganalisis proses yang terdapat pada Exponential Smoothing
dic = {"Demand":demand,"Forecast":f,"ABS(Error)":abse,"Squared Error":sqe, "Percent Error":pse}
results = pd.DataFrame.from_dict(dic).round(2)
results.index.name = 'Period'

# Simpan nilai data pada kolom ABS(Error), Squared Error, dan Percent Error
results["Error"] = results["Demand"] - results["Forecast"]
results["ABS(Error)"] =  (abs(results["Error"])).round(2)
results["Squared Error"] = (results["ABS(Error)"] * results["ABS(Error)"]).round(2)
results["Percent Error"] = (results["ABS(Error)"] / results["Demand"]).round(4)

# Print the dataframe for analysis
print("")
print("                Exponential Smoothing Data Analysis                    ")
print("")
print(results)

# Finally print the Mean Absolute Error Percentage
# Rumus Menghitung MAEP, BIAS, MAD, MSE, MAPE
maep = results["ABS(Error)"].sum()/(results["Demand"].sum())
mae = (results["Error"].sum()/(len(demand)-1)).round(2)
mse = (abs(results["Squared Error"]).sum())/(len(demand)-3)
mad = (abs(results["Error"]).sum())/(len(demand)-1)
mape = results["Percent Error"].sum()/(len(demand)-1)
print("")
print("BIAS:",(mae).round(2), "      MAD:",(mad).round(2), "      MSE:",(mse).round(2), "      MAPE:", (mape).round(2), "     MAE percentage:",int(maep*100),"%")
print("")

dfes = pd.DataFrame(results)

# Plot the results
plt.plot(demand,label='Garis Data Aktual',marker="o")    
plt.plot(f,label='Hasil Regresi / Forecast',marker="o",linewidth=2)
plt.title('Exponential Smoothing')
plt.xlabel("Bulan")
plt.ylabel("Demand")
plt.legend()

#Ekspor Grafik
grafik = plt.savefig('peramalan/grafik/grafik_exponential_smoothing.png')
plt.show()
#Ekspor Excel
dfes.to_excel(r'd:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/excel/exponential_smoothing.xlsx')
