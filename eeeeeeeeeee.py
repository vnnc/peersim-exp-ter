#!/usr/bin/env python3

import os, sys, csv, pandas

from statistics import mean

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html
from scipy.stats import chi2


# Une proba de 90% avec 20 degrés de liberté
#print( chi2.ppf(0.05, 20) )

#N=nb cycle, k,=suffleinterval,IDpeer = un pair (, vue)

#  NETSIZE,NB_CYCLES,SHUFFLE_INTERVAL,PEERID

################################################################################

class TestSeries:
	def __init__(self, path):
		filedata = pandas.read_csv(path,sep=',')
		self.net_size = filedata['NETSIZE'][0]
		self.nb_cycles = filedata['NB_CYCLES'][0]
		self.suffle_interval = filedata['SHUFFLE_INTERVAL'][0] # seul truc qui varie
		
		self.sample = filedata['PEERID']
		
		

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
		
		print("Computed chi² value (Distribution): " + str(res))
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
		
		print("Computed chi² value (Independence): " + str(res))
		return res

################################################################################

# Lire les fichiers CSV

if len(sys.argv) == 1:
	foldername = input("Dossier : ")
else:
	foldername = sys.argv[1]

ddl = 5000 # TODO ?????????

dist_theo = chi2.ppf(0.10, ddl)
dist_values = []

indep_theo = chi2.ppf(0.10, ddl * ddl) # FIXME non
indep_values = []

print("Theoric distribution value: " + str(dist_theo))
print("Theoric independance value: " + str(indep_theo))

for filename in os.listdir(foldername):
	if filename.endswith('.csv'):
		ts = TestSeries(foldername + filename)
		dist_values.append(ts.testDistribution())
		indep_values.append(ts.testIndependence())
		
		

print("Mean Χ² statistic for distribution: " + str(mean(dist_values)))
print("Mean Χ² statistic for independence: " + str(mean(indep_values)))


# TODO faire des graphes

#fig,ax = plt.subplots(figsize=(10,10))
#thlimit = ax.plot(shuffles,distritheo,"g",label="Valeur limite du test")
#boxes = annexe_data.boxplot(column="DIST_VALUE",by="SHUFFLE_INTERVAL",ax=ax)
#plt.suptitle("")
#plt.legend()
#plt.title("Test de distribution")
#plt.xlabel("Shuffles entre getPeer")
#plt.ylabel("Valeur statistique")
#plt.show()

#fig,ax = plt.subplots(figsize=(10,10))
#thlimit = ax.plot(shuffles,indeptheo,"g",label="Valeur limite du test")
#boxes = annexe_data.boxplot(column="INDEP_VALUE",by="SHUFFLE_INTERVAL",ax=ax)
#plt.suptitle("")
#plt.legend()
#plt.title("Test d'indépendance")
#plt.xlabel("Shuffles entre getPeer")
#plt.ylabel("Valeur statistique")
#plt.show()




