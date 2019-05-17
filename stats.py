#!/usr/bin/env python3

import os, sys, csv, pandas

################################################################################

class TestSeries:
	def __init__(self, path):
		filedata = pandas.read_csv(path, sep=',')
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
			if e != 0:
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
					if observedCount != 0:
						res += (observedCount - expectedCount) * (observedCount - expectedCount) / expectedCount;
		
		print("Computed chi² independence value: " + str(res))
		return res
	
	def get_csv_line(self):
		return str(self.testDistribution()) + ',' + \
		       str(self.testIndependence()) + ',' + \
		       str(self.shuffle_interval) + ',' + \
		       str(self.getDegreeOfFreedom()) + '\n'

################################################################################

# Lire les fichiers CSV

if len(sys.argv) == 1:
	foldername = input("Dossier : ")
else:
	foldername = sys.argv[1]

print(str(len(os.listdir(foldername))) + " files in this folder. Only CSV files will be read.")
f = open("stats.csv", 'w+')
f.write('DIST_VALUE,INDEP_VALUE,SHUFFLE_INTERVAL,DOF\n')
for filename in os.listdir(foldername):
	if filename.endswith('.csv'):
		ts = TestSeries(foldername + filename)
		f.write(ts.get_csv_line())
f.close()
print("Data written in stats.csv")


