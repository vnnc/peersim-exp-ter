#!/usr/bin/env python3

import os, sys, csv, pandas
import matplotlib.pyplot as plt
from statistics import mean

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html
from scipy.stats import chi2

################################################################################

# Une proba de 90% avec 20 degrés de liberté :
#print( chi2.ppf(0.05, 20) )

#N=nb cycle, k,=suffleinterval,IDpeer = un pair (, vue)

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
			tmp = e - expectedCount
			tmp = (tmp * tmp) / expectedCount
			res += tmp
		
		print("Computed chi² distribution value: " + str(res))
		return res

	def testIndependence(self):
		# .......
		X = []
		Y = []
		countsPaires = {}
		countsX = {}
		countsY = {}
		
		i = 0
		while i < len(self.sample) - 1:
			newX = self.sample[i]
			newY = self.sample[i+1]
			
			X.append(newX)
			Y.append(newY)
			
			i = i+2
			
			newX = str(newX)
			newY = str(newY)
			if newX in countsX:
				prev = countsX[newX]
				countsX[newX] = prev + 1
			else:
				countsX[newX] = 1
			
			if newY in countsY:
				prev = countsY[newY]
				countsY[newY] = prev + 1
			else:
				countsY[newY] = 1
			
			xyPaire = newX + ',' + newY
			if xyPaire in countsPaires:
				prev = countsPaires[xyPaire]
				countsPaires[xyPaire] = prev + 1
			else:
				countsPaires[xyPaire] = 1
			
		res = 0.0
		pairCount = len(X)
		
		for i in range(1, self.net_size):
			for j in range(1, self.net_size):
				obsPaire = str(i) + ', ' + str(j)
				
				if obsPaire in countsPaires:
					observedCount = countsPaires[str(obsPaire)]
				else:
					observedCount = 0.0
				
				if str(i) in countsX:
					observedCount1 = countsX[str(i)]
				else:
					observedCount1 = 0.0
				
				if str(j) in countsY:
					observedCount2 = countsY[str(j)]
				else:
					observedCount2 = 0.0
				
				expectedCount = (observedCount1 * observedCount2)/pairCount;
				
				if expectedCount != 0:
					res += (observedCount - expectedCount) * (observedCount - expectedCount) / expectedCount;
		
		print("Computed chi² independence value: " + str(res))
		return res

################################################################################

# Lire les fichiers CSV

if len(sys.argv) == 1:
	foldername = input("Dossier : ")
else:
	foldername = sys.argv[1]

ddl = 1000 - 1 # XXX ?????????

dist_theo = chi2.ppf(0.90, ddl)
dist_values = []

indep_theo = chi2.ppf(0.90, ddl * ddl) # FIXME non
indep_values = []

print("Theoric distribution value: " + str(dist_theo))
print("Theoric independance value: " + str(indep_theo))
print('')

shuffle_intervals = []

print(str(len(os.listdir(foldername))) + " files in this folder. Only CSV files will be read.")
for filename in os.listdir(foldername):
	if filename.endswith('.csv'):
		ts = TestSeries(foldername + filename)
		dist_values.append(ts.testDistribution())
		indep_values.append(ts.testIndependence())
		shuffle_intervals.append(ts.shuffle_interval)
#		dist_theo.append(???)
#		indep_theo.append(???)

print('')
print("Theoric distribution value: " + str(dist_theo))
print("Mean Χ² statistic for distribution: " + str(mean(dist_values)))
print('')
print("Theoric independance value: " + str(indep_theo))
print("Mean Χ² statistic for independence: " + str(mean(indep_values)))

# Tracer les graphes

dist_theo = [dist_theo] * len(dist_values)
indep_theo = [indep_theo] * len(indep_values)

print("***********************************************************************")

plt.plot(shuffle_intervals, dist_theo)
plt.plot(shuffle_intervals, dist_values, 'ro')
plt.axis([0, 40, 0, 2000])
plt.legend()
plt.title("Test de distribution/homogénéité")
plt.xlabel("Nombre de shuffles entre chaque getPeer")
plt.ylabel("Valeur statistique")
plt.show()

plt.plot(shuffle_intervals, indep_theo)
plt.plot(shuffle_intervals, indep_values, 'ro')
plt.axis([0, 40, 0, 1000000])
plt.legend()
plt.title("Test d'indépendance")
plt.xlabel("Nombre de shuffles entre chaque getPeer")
plt.ylabel("Valeur statistique")
plt.show()




