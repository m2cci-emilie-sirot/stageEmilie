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
   
     
    listeMEDI = []
    listeLAND = []
    listeSUB = []
    listeBOIS = []
    listeECOR = []
    listePROD = []
    
    
    row = 3
    
    for c in range(3, len(csvfile.columns)):
        if csvfile.iloc[2,c] == "MEDI":
            listeMEDI.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "LAND":
            listeLAND.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "SUB":
            listeSUB.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "BOIS":
            listeBOIS.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "ECOR":
            listeECOR.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "PROD":
            listePROD.append(csvfile.iloc[row,c])
            
   
            
            
    listeMEDIFloat = list(map(float, listeMEDI))
    listeLANDFloat = list(map(float, listeLAND))
    listeSUBFloat = list(map(float, listeSUB))
    listeBOISFloat = list(map(float, listeBOIS))
    listeECORFloat = list(map(float, listeECOR))
    listePRODFloat = list(map(float, listePROD))
    
   
    medianeMEDI = statistics.median(listeMEDIFloat)
    medianeLAND = statistics.median(listeLANDFloat)
    medianeSUB = statistics.median(listeSUBFloat)
    medianeBOIS = statistics.median(listeBOISFloat)
    medianeECOR = statistics.median(listeECORFloat)
    medianePROD = statistics.median(listePRODFloat)
    
    
    
    
    
    
   test = csvfile["date"].values
    plt.figure()
    
    testcolonnes = csvfile.columns
    
MEDI
LAND
SUB
BOIS
ECOR