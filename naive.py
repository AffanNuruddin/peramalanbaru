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

nabse = 0
nsqe = 0
npse = 0

####################------------Naive-Approach-----------#######################
xyz = pd.DataFrame(pd.read_csv(r"d:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/bandara.csv")) 
bulan = [xyz["Bulan"][i] for i in range(len(xyz["Bulan"]))]
demand = [xyz["Demand"][i] for i in range(len(xyz["Demand"]))]
# Mendefinisikan forecast pertama adalah null
fn = [np.nan]
# Forecast kedua sama dengan demand pertama
fn.append(demand[0])
#df = pd.DataFrame(demand)
# Looping forecast
for t2 in range (1,len(demand)-1):
  fn.append(demand[t2])

# Memproses data dengan rumus pada Naive Approach
dic2 = {"Demand":demand,"Forecast":fn,"ABS(Error)":nabse,"Squared Error":nsqe, "Percent Error":npse}
results2 = pd.DataFrame.from_dict(dic2)
results2.index.name = 'Period'
results2["Error"] = results2["Demand"] - results2["Forecast"]
results2["ABS(Error)"] =  (abs(results2["Error"])).round(2)
results2["Squared Error"] = (results2["ABS(Error)"] * results2["ABS(Error)"]).round(2)
results2["Percent Error"] = (results2["ABS(Error)"] / results2["Demand"]).round(4)

# Print the dataframe for analysis
print("")
print("                      Naive Approach Data Analysis                     ")
print("")
print(results2)

df = pd.DataFrame(results2)

# Rumus Menghitung MAEP, BIAS, MAD, MSE, MAPE
nmaep = abs(results2["Error"]).sum()/(results2["Demand"].sum())
nmae = (results2["Error"].sum()/(len(demand)-1)).round(2)
nmse = (abs(results2["Squared Error"]).sum())/(len(demand)-1)
nmad = (abs(results2["Error"]).sum())/(len(demand)-1)
nmape = results2["Percent Error"].sum()/(len(demand)-1)

# Print hasil dari BIAS, MAD, MAPE & MAE Percentage
print("")
print("BIAS:",(nmae).round(2), "      MAD:",(nmad).round(2), "      MSE:",(nmse).round(2), "      MAPE:", (nmape).round(2), "     MAE percentage:",int(nmaep*100),"%")
print("")

# Plot the results
#plt.scatter(demand,bulan,label='Data Aktual',s=20)
plt.plot(demand,label='Garis Data Aktual',marker="o")    
plt.plot(fn,label='Hasil Regresi / Forecast',marker="o",linewidth=2)
plt.title('Naive Approach')
plt.xlabel("Bulan")
plt.ylabel("Demand")
plt.legend()
fig = plt.figure(1)

#Ekspor Grafik
grafik = plt.savefig('peramalan/grafik/grafik_naive.png')
plt.show()
#Ekspor Excel
df.to_excel(r'd:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/excel/naive.xlsx')