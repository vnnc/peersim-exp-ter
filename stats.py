#!/usr/bin/env python3

import os, sys, csv, pandas
import matplotlib.pyplot as plt
from statistics import mean

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html
from scipy.stats import chi2

################################################################################

# Une proba de 90% avec 20 degrés de liberté :
#print( chi2.ppf(0.90, 20) )

#  NETSIZE,NB_CYCLES,SHUFFLE_INTERVAL,PEERID

################################################################################

class TestSeries:
	def __init__(self, path):
		filedata = pandas.read_csv(path,sep=',')
		self.net_size = filedata['NETSIZE'][0]
		self.nb_cycles = filedata['NB_CYCLES'][0]
		self.shuffle_interval = filedata['SHUFFLE_INTERVAL'][0] # varie d'un fichier à l'autre
		self.sample = filedata['PEERID'] # varie d'une ligne à l'autre

	def testDistribution(self):
		expectedCount = float(len(self.sample)/(self.net_size-1))
		counts = [0.0] * self.net_size
		
		for i in self.sample:
			counts[i] = counts[i] + 1
		
		res = 0.0
		for e in counts:
#			print("Observed: "+str(e)+" Expected: "+str(expectedCount))
			if e!=0:
				tmp = e - expectedCount
				tmp = (tmp * tmp) / expectedCount
				res += tmp
		
		print("Computed chi² distribution value: " + str(res))
		return res

	def getDegreeOfFreedom(self):
		return self.net_size-1

	def testIndependence(self):
		# .......
		X = self.sample[0:][::2]
		Y = self.sample[1:][::2]
		
		XY = [(e,Y[i+1]) if (i+1)<=(Y.shape[0]*2) else (0,0) for i,e in X.iteritems()]
		
		X = pandas.DataFrame(X).reset_index().drop(columns=["index"])
		Y = pandas.DataFrame(Y).reset_index().drop(columns=["index"])
		
		countsX = X.groupby(["PEERID"])
		countsY = Y.groupby(["PEERID"])
		
		XY = pandas.DataFrame(XY,columns=["eX","eY"])
		countsXY = XY.groupby(["eX","eY"])
		
		res = 0.0
		pairCount = len(X)
		
		for i in range(1, self.net_size):
			for j in range(1, self.net_size):
				obsPaire = (i,j)
				
				if obsPaire in countsXY.groups:
					observedCount = countsXY.get_group(obsPaire).shape[0]
				else:
					observedCount = 0.0
				
				if i in countsX.groups:
					observedCount1 = countsX.get_group(i).shape[0]
				else:
					observedCount1 = 0.0
				
				if j in countsY.groups:
					observedCount2 = countsY.get_group(j).shape[0]
				else:
					observedCount2 = 0.0
				
				expectedCount = (observedCount1 * observedCount2)/pairCount;
				
				if expectedCount != 0:
					if observedCount!=0:
#						print("Observed: "+str(observedCount)+" Expected: "+str(expectedCount))
						res += (observedCount - expectedCount) * (observedCount - expectedCount) / expectedCount;
		
		print("Computed chi² independence value: " + str(res))
		return res

################################################################################

# Lire les fichiers CSV

if len(sys.argv) == 1:
	foldername = input("Dossier : ")
else:
	foldername = sys.argv[1]

dist_values = []
indep_values = []
shuffle_intervals = []

print(str(len(os.listdir(foldername))) + " files in this folder. Only CSV files will be read.")
for filename in os.listdir(foldername):
	if filename.endswith('.csv'):
		ts = TestSeries(foldername + filename)
		dist_values.append(ts.testDistribution())
		indep_values.append(ts.testIndependence())
		shuffle_intervals.append(ts.shuffle_interval)

ddl = ts.getDegreeOfFreedom()

dist_theo90 = chi2.ppf(0.10, ddl)
dist_theo95 = chi2.ppf(0.05, ddl)
dist_theo99 = chi2.ppf(0.01, ddl)
indep_theo90 = chi2.ppf(0.10, ddl * ddl)
indep_theo95 = chi2.ppf(0.05, ddl * ddl)
indep_theo99 = chi2.ppf(0.01, ddl * ddl)


dist_y_max = max(dist_theo95, max(dist_values)) * 1.05
indep_y_max = max(indep_theo95, max(indep_values)) * 1.05

print('')
print("Theoric distribution value (95%): " + str(dist_theo95))
print("Mean Χ² statistic for distribution: " + str(mean(dist_values)))
print('')
print("Theoric independance value (95%): " + str(indep_theo95))
print("Mean Χ² statistic for independence: " + str(mean(indep_values)))

# Tracer les graphes

dist_theo90 = [dist_theo90] * len(dist_values)
dist_theo95 = [dist_theo95] * len(dist_values)
dist_theo99 = [dist_theo99] * len(dist_values)
indep_theo90 = [indep_theo90] * len(indep_values)
indep_theo95 = [indep_theo95] * len(indep_values)
indep_theo99 = [indep_theo99] * len(indep_values)


print("***********************************************************************")

plt.plot(shuffle_intervals, dist_theo90,"-b",label="90%")
plt.plot(shuffle_intervals, dist_theo95,"-g",label="95%")
plt.plot(shuffle_intervals, dist_theo99,"-k",label="99%")
plt.plot(shuffle_intervals, dist_values, 'ro')
plt.axis([0, 40, 0, dist_y_max])
plt.legend()
plt.title("Test de distribution/homogénéité")
plt.xlabel("Nombre de shuffles entre chaque getPeer")
plt.ylabel("Valeur statistique")
plt.show()

plt.plot(shuffle_intervals, indep_theo90,"-b",label="90%")
plt.plot(shuffle_intervals, indep_theo95,"-g",label="95%")
plt.plot(shuffle_intervals, indep_theo99,"-k",label="99%")
plt.plot(shuffle_intervals, indep_values, 'ro')
plt.axis([0, 40, 0, indep_y_max])
plt.legend()
plt.title("Test d'indépendance")
plt.xlabel("Nombre de shuffles entre chaque getPeer")
plt.ylabel("Valeur statistique")
plt.show()



