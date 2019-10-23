import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd

style.use("ggplot")
xyz = pd.DataFrame(pd.read_csv(r"d:/PyCharm Community Edition 2019.2/PyCharm Project/peramalan/RegresiLinier.csv"))
periode = [xyz["periode"][a] for a in range(len(xyz["periode"]))]
demand = [xyz["demand"][a] for a in range(len(xyz["demand"]))]
print(xyz)

def linearRegresion(data):
	'''
		indeks[0] -> response variable -> x
		indeks[1] -> predictor variable -> y
	'''
	x2=[]
	y2=[]
	xy=[]
	n = len(data[0])

	for x in data[0]:
		x2.append(x**2)

	for y in data[0]:
		y2.append(y**2)

	i=0;
	while(i<n):
		dump = data[0][i]*data[1][i]
		xy.append(dump)
		i+=1
	jmlhx = sum(data[0])
	jmlhy = sum(data[1])
	jmlhx2 = sum(x2)
	jmlhy2 = sum(y2)
	jmlhxy = sum(xy)

	a = ((jmlhy*jmlhx2)-(jmlhx*jmlhxy))/(n*jmlhx2-(jmlhx**2))
	b = ((n*jmlhxy)-(jmlhx*jmlhy))/(n*jmlhx2-(jmlhx**2))

	return(a,b)

def gambarGrafik(dataProses):
	a,b = linearRegresion(dataProses)
	print("Nilai a adalah %.2f"%(a))
	print("Nilai b adalah %.2f"%(b))
	def f1(periode,a,b):
		hit = []
		for x in periode:
			y = b*x+a
			hit.append(y)
		return(hit)      
        
	plt.scatter(dataProses[0],dataProses[1],label='data aktual',s=20)    
	plt.plot(dataProses[0],f1(dataProses[0],a,b),c='k',label='hasil regresi without',linewidth=0.7)
	plt.title("Hasil Regresi Linear Sederhana")
	plt.ylabel("Demand")
	plt.xlabel("Periode")
	plt.legend()
	fig = plt.figure(1)
	plt.show()
