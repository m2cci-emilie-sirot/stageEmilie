#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 14:12:01 2021

@author: Emilie SIROT
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
#import seaborn as sns
import statistics


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"


listeRep = os.listdir(repDonnees)


for i in range (len(listeRep)):
    #repCourant = os.path.join(repDonnees, listeRep[0])
    #repCourant = os.path.join(repDonnees, listeRep[i])
    fichiersRep = os.listdir(repDonnees)



    csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)
   
    colonnes = len(csvfile.columns)
    
    listeMEDI = []
    
    for c in range(3, len(csvfile.columns)):
        if csvfile.iloc[2,i] = "MEDI":
            listeMEDI.append(csvfile.iloc[2,i])
            
    
   
    
   
   
    mediane = statistics.median(lst)
    
   test = csvfile["date"].values
    plt.figure()
    
    testcolonnes = csvfile.columns
    
MEDI
LAND
SUB
BOIS
ECOR