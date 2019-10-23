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

sabse = 0
ssqe = 0
spse = 0

xyz = pd.DataFrame(pd.read_csv(r"d:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/bandara.csv")) 
bulan = [xyz["Bulan"][i] for i in range(len(xyz["Bulan"]))]
demand = [xyz["Demand"][i] for i in range(len(xyz["Demand"]))]

####################---------Simple-Moving-Average-------#######################

# Create dataframe
dfsma = pd.DataFrame(demand)

# View dataframe
for i in range(1,len(demand)):
    dfsma['Forecast'] = dfsma.rolling(window=4).mean()

# Menganalisis proses yang terdapat pada Exponential Smoothing
dic1 = {"Demand":demand,"Forecast":dfsma['Forecast'],"ABS(Error)":sabse,"Squared Error":ssqe, "Percent Error":spse}
results1 = pd.DataFrame.from_dict(dic1).round(2)
results1.index.name = 'Period'

# Simpan nilai data pada kolom ABS(Error), Squared Error, dan Percent Error
results1["Error"] = results1["Demand"] - results1["Forecast"]
results1["ABS(Error)"] =  (abs(results1["Error"])).round(2)
results1["Squared Error"] = (results1["ABS(Error)"] * results1["ABS(Error)"]).round(2)
results1["Percent Error"] = (results1["ABS(Error)"] / results1["Demand"]).round(4)

print("")
print("                Simple-Moving-Average Data Analysis                    ")
print("")
print(results1)

# Finally print the Mean Absolute Error Percentage
# Rumus Menghitung MAEP, BIAS, MAD, MSE, MAPE
smaep = results1["ABS(Error)"].sum()/(results1["Demand"].sum())
smae = (results1["Error"].sum()/(len(demand)-3)).round(2)
smse = (abs(results1["Squared Error"]).sum())/(len(demand)-3)
smad = (abs(results1["Error"]).sum())/(len(demand)-3)
smape = results1["Percent Error"].sum()/(len(demand)-3)

print("")
print("BIAS:",(smae).round(2), "      MAD:",(smad).round(2), "      MSE:",(smse).round(2), "      MAPE:", (smape).round(2), "     MAE percentage:",int(smaep*100),"%")
print("")

dfhsma = pd.DataFrame(results1)

# Plot the results
plt.plot(demand,label='Garis Data Aktual',marker="o")    
plt.plot(dfsma['Forecast'],label='Hasil Regresi / Forecast',marker="o",linewidth=2)
plt.title('Simple-Moving-Average')
plt.xlabel("Bulan")
plt.ylabel("Demand")
plt.legend()
fig = plt.figure(1)

#Ekspor Grafik
grafik = plt.savefig('peramalan/grafik/grafik_sma.png')
plt.show()
#Ekspor Excel
dfhsma.to_excel(r'd:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/excel/sma.xlsx')
