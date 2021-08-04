#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 14:12:01 2021

@author: Emilie SIROT
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"


listeRep = os.listdir(repDonnees)


for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[0])
    #repCourant = os.path.join(repDonnees, listeRep[i])
    fichiersRep = os.listdir(repCourant)



    csvfile = pd.read_csv(os.path.join(repCourant,fichiersRep[0]), header=0)
    test = csvfile["date"].values
    plt.figure()
    
    testcolonnes = csvfile.columns
    
MEDI
LAND
SUB
BOIS
ECOR