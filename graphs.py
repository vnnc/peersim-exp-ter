#!/usr/bin/env python3

import os, sys, csv, pandas
import matplotlib.pyplot as plt
from statistics import mean

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html
from scipy.stats import chi2

################################################################################

# Lire les données

if len(sys.argv) == 1:
	filename = input("Fichier : ")
else:
	filename = sys.argv[1]

data = pandas.read_csv(filename, sep=',')
DOF = data['DOF'][0]
SHUFFLE_INTERVALS = data['SHUFFLE_INTERVAL'].values
DIST_VALUES = data['DIST_VALUE'].values
INDEP_VALUES = data['INDEP_VALUE'].values

simax = max(SHUFFLE_INTERVALS)
abscisses = range(1, simax+1)

def dist_theoric(percent, length):
	theo = chi2.ppf(percent, DOF)
	curv_theo = [theo] * length
	return curv_theo

def indep_theoric(percent, length):
	theo = chi2.ppf(percent, DOF * DOF)
	curv_theo = [theo] * length
	return curv_theo

def get_dots(values, simax):
	dots = []
	global SHUFFLE_INTERVALS
	for i in range(1, simax+1):
		count = 0
		res = 0
		for (k, v) in enumerate(SHUFFLE_INTERVALS):
			if v == i:
				count = count + 1
				res = res + values[k]
		if count > 0: # on aura des 0 si le shuffle interval n'existe pas dans le csv
			res = res / count
		dots.append(res)
	return dots

################################################################################

# Tracer les graphes

if len(DIST_VALUES) > 0:
	print('')
	print("Theoric distribution value (95%): " + str(dist_theoric(0.95, DIST_VALUES)[0]))
	print("Mean Χ² statistic for distribution: " + str(mean(DIST_VALUES)))
	plt.plot(abscisses, dist_theoric(0.99, simax), '-k', label="99%")
	plt.plot(abscisses, dist_theoric(0.95, simax), '-g', label="95%")
	plt.plot(abscisses, dist_theoric(0.90, simax), '-b', label="90%")
	plt.plot(abscisses, get_dots(DIST_VALUES, simax), 'ro')
	plt.legend()
	plt.title("Test de distribution/homogénéité")
	plt.xlabel("Nombre de shuffles entre chaque getPeer")
	plt.ylabel("Valeur statistique")
	plt.show()

if len(INDEP_VALUES) > 0:
	print('')
	print("Theoric independence value (95%): " + str(indep_theoric(0.95, INDEP_VALUES)[0]))
	print("Mean Χ² statistic for independence: " + str(mean(INDEP_VALUES)))
	plt.plot(abscisses, indep_theoric(0.99, simax), '-k', label="99%")
	plt.plot(abscisses, indep_theoric(0.95, simax), '-g', label="95%")
	plt.plot(abscisses, indep_theoric(0.90, simax), '-b', label="90%")
	plt.plot(abscisses, get_dots(INDEP_VALUES, simax), 'ro')
	plt.legend()
	plt.title("Test d'indépendance")
	plt.xlabel("Nombre de shuffles entre chaque getPeer")
	plt.ylabel("Valeur statistique")
	plt.show()



