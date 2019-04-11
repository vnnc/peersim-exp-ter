#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,sys,pandas
import matplotlib.pyplot as plt

def plot_distribution(data: pandas.DataFrame):
    shuffle_interval = data.head(1)["SHUFFLE_INTERVAL"][0]
    data.drop(columns=["NETSIZE","NB_CYCLES","SHUFFLE_INTERVAL"],inplace=True)
    counts = data["PEERID"].value_counts()
    nb = max(data["PEERID"])
    plt.figure(1,figsize=(20,15))
    data["PEERID"].plot(kind="hist",bins=nb)
    plt.title("Peer ID distribution, picking a peer every "+str(shuffle_interval)+" shuffle")
    plt.hlines(counts.mean(),0,1000,colors="r",label="Average")
    plt.hlines(counts.min(),0,1000,colors="g",label="Minimum")
    plt.xlabel("Peer ID")
    plt.legend()
    plt.figure(2)
    counts.plot(kind="box")
    

def process(file):
    data = pandas.read_csv(file,sep=",")
    if restriction != 0:
        if int(data.head(1)["SHUFFLE_INTERVAL"][0]) == int(restriction):
            print("found")
            plot_distribution(data)
    else:
        plot_distribution(data)


if len(sys.argv) == 1:
    foldername = input("Dossier : ")
    restriction = 0
else:
    foldername = sys.argv[1]
    if len(sys.argv)>2:
        restriction = sys.argv[2]

for filename in os.listdir(foldername):
    if filename.endswith('.csv'):
        process(foldername+filename)