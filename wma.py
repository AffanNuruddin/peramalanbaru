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

wabse = 0
wsqe = 0
wpse = 0

xyz = pd.DataFrame(pd.read_csv(r"d:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/bandara.csv")) 
bulan = [xyz["Bulan"][i] for i in range(len(xyz["Bulan"]))]
demand = [xyz["Demand"][i] for i in range(len(xyz["Demand"]))]

#################---------Weighted-Moving-Average-----------###################

# Create dataframe
dfwma = pd.DataFrame(demand)

weights = np.array([0.1,0.3,0.6])
sum_weights = np.sum(weights)

for t2 in range(1,len(demand)-3):
    dfwma['Forecast'] = (xyz['Demand']
    .rolling(window=3, center=False)
    .apply(lambda x: np.sum(weights*x) / sum_weights, raw= True)
)

dic2 = {"Demand":demand,"Forecast":dfwma['Forecast'],"ABS(Error)":wabse,"Squared Error":wsqe, "Percent Error":wpse}
wma = pd.DataFrame.from_dict(dic2)
wma.index.name = 'Period'
wma["Error"] = wma["Demand"] - wma["Forecast"]
wma["ABS(Error)"] =  (abs(wma["Error"])).round(2)
wma["Squared Error"] = (wma["ABS(Error)"] * wma["ABS(Error)"]).round(2)
wma["Percent Error"] = (wma["ABS(Error)"] / wma["Demand"]).round(4)

# Print the dataframe for analysis
print("")
print("                      Weighted-Moving-Average Data Analysis                     ")
print("")
print(wma)

df = pd.DataFrame(wma)
# Plot the results
#wma[["Demand","Forecast"]].plot(marker="o",title="Weighted-Moving-Average")

# Rumus Menghitung MAEP, BIAS, MAD, MSE, MAPE
wmaep = abs(wma["Error"]).sum()/(wma["Demand"].sum())
wmae = (wma["Error"].sum()/(len(demand)-3)).round(2)
wmse = (abs(wma["Squared Error"]).sum())/(len(demand)-3)
wmad = (abs(wma["Error"]).sum())/(len(demand)-3)
wmape = wma["Percent Error"].sum()/(len(demand)-3)

# Print hasil dari BIAS, MAD, MAPE & MAE Percentage
print("")
print("BIAS:",(wmae).round(2), "      MAD:",(wmad).round(2), "      MSE:",(wmse).round(2), "      MAPE:", (wmape).round(2), "     MAE percentage:",int(wmaep*100),"%")
print("")

plt.plot(demand,label='Garis Data Aktual',marker="o")    
plt.plot(dfwma['Forecast'],label='Hasil Regresi / Forecast',marker="o",linewidth=2)
plt.title('Weighted-Moving-Average')
plt.xlabel("Bulan")
plt.ylabel("Demand")
plt.legend()

#Ekspor Grafik
grafik = plt.savefig('peramalan/grafik/grafik_wma.png')
plt.show()
#Ekspor Excel
df.to_excel(r'd:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/excel/wma.xlsx')