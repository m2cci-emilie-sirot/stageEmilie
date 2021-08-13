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
    
    
    
    ##
    
    listeMEDI2 = []
    listeLAND2 = []
    listeSUB2 = []
    listeBOIS2 = []
    listeECOR2 = []
    listePROD2 = []
    
    
    row = 9
    
    for c in range(3, len(csvfile.columns)):
        if csvfile.iloc[2,c] == "MEDI":
            listeMEDI2.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "LAND":
            listeLAND2.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "SUB":
            listeSUB2.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "BOIS":
            listeBOIS2.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "ECOR":
            listeECOR2.append(csvfile.iloc[row,c])
            
            
        elif csvfile.iloc[2,c] == "PROD":
            listePROD2.append(csvfile.iloc[row,c])
            
   
            
            
    listeMEDIFloat2 = list(map(float, listeMEDI2))
    listeLANDFloat2 = list(map(float, listeLAND2))
    listeSUBFloat2 = list(map(float, listeSUB2))
    listeBOISFloat2 = list(map(float, listeBOIS2))
    listeECORFloat2 = list(map(float, listeECOR2))
    listePRODFloat2 = list(map(float, listePROD2))
    
   
    medianeMEDI2 = statistics.median(listeMEDIFloat2)
    medianeLAND2 = statistics.median(listeLANDFloat2)
    medianeSUB2 = statistics.median(listeSUBFloat2)
    medianeBOIS2 = statistics.median(listeBOISFloat2)
    medianeECOR2 = statistics.median(listeECORFloat2)
    medianePROD2 = statistics.median(listePRODFloat2)
    
    
    legende = ["date", "type"]
    testTab = pd.DataFrame(columns = legende)    
    testTab.loc[0,"date"] = "20200207"
    testTab.loc[0, "type"] = medianeMEDI
    testTab.loc[1,"date"] = "20200204"
    testTab.loc[1,"type"] = medianeMEDI2

    x = testTab["date"]
    y = testTab["type"]
    
    plt.figure()
    plt.plot(x,y)
    
    
    plt.xlabel("dates")
    plt.ylabel("valeur pixels")
    plt.legend(["ND_B2_B3"])
    
    testcolonnes = csvfile.columns
    
MEDI
LAND
SUB
BOIS
ECOR


#afficher courbes tous indices pour chaque type de veget


repDonnees = r"../calculIndicesTFE/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"
listeRep = os.listdir(repDonnees)

for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[0])
    #repCourant = os.path.join(repDonnees, listeRep[i])
    fichiersRep = os.listdir(repCourant)

csvfile = pd.read_csv(os.path.join(repCourant,fichiersRep[0]), header=0)
   
#ordonner le tableau
csvTrie = csvfile.sort_values(by = 'bandes', ascending = True)

#Premiere boucle : permet de passer à la ligne du dessous pour changer d'indice
#separer les graphiques par type indice


#BSITIan
for rowBSITian in range(3,362):
    
    listeMEDIBSITian = []
    listeLANDBSITian = []
    listeSUBBSITian = []
    listeBOISBSITian = []
    listeECORBSITian = []
    listePRODBSITian = []
    
    for c in range(3, len(csvTrie.columns)):
        if csvfile.iloc[2,c] == "MEDI":
            listeMEDIBSITian.append(csvfile.iloc[rowBSITian,c])
            
            
        elif csvfile.iloc[2,c] == "LAND":
            listeLANDBSITian.append(csvTrie.iloc[rowBSITian,c])
            
            
        elif csvfile.iloc[2,c] == "SUB":
            listeSUBBSITian.append(csvTrie.iloc[rowBSITian,c])
            
            
        elif csvfile.iloc[2,c] == "BOIS":
            listeBOISBSITian.append(csvTrie.iloc[rowBSITian,c])
            
            
        elif csvfile.iloc[2,c] == "ECOR":
            listeECORBSITian.append(csvTrie.iloc[rowBSITian,c])
            
            
        elif csvfile.iloc[2,c] == "PROD":
            listePRODBSITian.append(csvTrie.iloc[rowBSITian,c])
    
    
#BSI
for rowBSI in range(363,1083):
    
    listeMEDIBSI = []
    listeLANDBSI = []
    listeSUBBSI = []
    listeBOISBSI = []
    listeECORBSI = []
    listePRODBSI = []
    
    for c in range(3, len(csvTrie.columns)):
        if csvfile.iloc[2,c] == "MEDI":
            listeMEDIBSI.append(csvfile.iloc[rowBSI,c])
            
            
        elif csvfile.iloc[2,c] == "LAND":
            listeLANDBSI.append(csvTrie.iloc[rowBSI,c])
            
            
        elif csvfile.iloc[2,c] == "SUB":
            listeSUBBSI.append(csvTrie.iloc[rowBSI,c])
            
            
        elif csvfile.iloc[2,c] == "BOIS":
            listeBOISBSI.append(csvTrie.iloc[rowBSI,c])
            
            
        elif csvfile.iloc[2,c] == "ECOR":
            listeECORBSI.append(csvTrie.iloc[rowBSI,c])
            
            
        elif csvfile.iloc[2,c] == "PROD":
            listePRODBSI.append(csvTrie.iloc[rowBSI,c])
    
    

#CVI
for rowCVI in range(1084,1442):
    
    listeMEDICVI = []
    listeLANDCVI = []
    listeSUBCVI = []
    listeBOISCVI = []
    listeECORCVI = []
    listePRODCVI = []
    
    for c in range(3, len(csvTrie.columns)):
        if csvfile.iloc[2,c] == "MEDI":
            listeMEDICVI.append(csvfile.iloc[rowCVI,c])
            
            
        elif csvfile.iloc[2,c] == "LAND":
            listeLANDCVI.append(csvTrie.iloc[rowCVI,c])
            
            
        elif csvfile.iloc[2,c] == "SUB":
            listeSUBCVI.append(csvTrie.iloc[rowCVI,c])
            
            
        elif csvfile.iloc[2,c] == "BOIS":
            listeBOISCVI.append(csvTrie.iloc[rowCVI,c])
            
            
        elif csvfile.iloc[2,c] == "ECOR":
            listeECORCVI.append(csvTrie.iloc[rowCVI,c])
            
            
        elif csvfile.iloc[2,c] == "PROD":
            listePRODCVI.append(csvTrie.iloc[rowCVI,c])
    
    
    
#ND
for rowND in range(1443, 1487):
    
    listeMEDIND = []
    listeLANDND = []
    listeSUBND = []
    listeBOISND = []
    listeECORND = []
    listePRODND = []
    
    for c in range(3, len(csvTrie.columns)):
        if csvfile.iloc[2,c] == "MEDI":
            listeMEDIND.append(csvfile.iloc[rowND,c])
            
            
        elif csvfile.iloc[2,c] == "LAND":
            listeLANDND.append(csvTrie.iloc[rowND,c])
            
            
        elif csvfile.iloc[2,c] == "SUB":
            listeSUBND.append(csvTrie.iloc[rowND,c])
            
            
        elif csvfile.iloc[2,c] == "BOIS":
            listeBOISND.append(csvTrie.iloc[rowND,c])
            
            
        elif csvfile.iloc[2,c] == "ECOR":
            listeECORND.append(csvTrie.iloc[rowND,c])
            
            
        elif csvfile.iloc[2,c] == "PROD":
            listePRODND.append(csvTrie.iloc[rowND,c])
    
    
    
#SR
for rowSR in range(1488, 1577):
    
    listeMEDIND = []
    listeLASRSR = []
    listeSUBSR = []
    listeBOISSR = []
    listeECORSR = []
    listePRODSR = []
    
    for c in range(3, len(csvTrie.columns)):
        if csvfile.iloc[2,c] == "MEDI":
            listeMEDISR.append(csvfile.iloc[rowSR,c])
            
            
        elif csvfile.iloc[2,c] == "LAND":
            listeLANDSR.append(csvTrie.iloc[rowSR,c])
            
            
        elif csvfile.iloc[2,c] == "SUB":
            listeSUBSR.append(csvTrie.iloc[rowSR,c])
            
            
        elif csvfile.iloc[2,c] == "BOIS":
            listeBOISSR.append(csvTrie.iloc[rowSR,c])
            
            
        elif csvfile.iloc[2,c] == "ECOR":
            listeECORSR.append(csvTrie.iloc[rowSR,c])
            
            
        elif csvfile.iloc[2,c] == "PROD":
            listePRODSR.append(csvTrie.iloc[rowSR,c])
    
    
    
    
#indclass
for rowIndclass in range(1578, 1590):
    listeMEDIND = []
    listeLAIndclassIndclass = []
    listeSUBIndclass = []
    listeBOISIndclass = []
    listeECORIndclass = []
    listePRODIndclass = []
    
    for c in range(3, len(csvTrie.columns)):
        if csvfile.iloc[2,c] == "MEDI":
            listeMEDIIndclass.append(csvfile.iloc[rowIndclass,c])
            
            
        elif csvfile.iloc[2,c] == "LAND":
            listeLANDIndclass.append(csvTrie.iloc[rowIndclass,c])
            
            
        elif csvfile.iloc[2,c] == "SUB":
            listeSUBIndclass.append(csvTrie.iloc[rowIndclass,c])
            
            
        elif csvfile.iloc[2,c] == "BOIS":
            listeBOISIndclass.append(csvTrie.iloc[rowIndclass,c])
            
            
        elif csvfile.iloc[2,c] == "ECOR":
            listeECORIndclass.append(csvTrie.iloc[rowIndclass,c])
            
            
        elif csvfile.iloc[2,c] == "PROD":
            listePRODIndclass.append(csvTrie.iloc[rowIndclass,c])
    
#mSR
for rowmSR in range(1590,1951):
    
    listeMEDIND = []
    listeLAmSRmSR = []
    listeSUBmSR = []
    listeBOISmSR = []
    listeECORmSR = []
    listePRODmSR = []
    
    for c in range(3, len(csvTrie.columns)):
        if csvfile.iloc[2,c] == "MEDI":
            listeMEDImSR.append(csvfile.iloc[rowmSR,c])
            
            
        elif csvfile.iloc[2,c] == "LAND":
            listeLANDmSR.append(csvTrie.iloc[rowmSR,c])
            
            
        elif csvfile.iloc[2,c] == "SUB":
            listeSUBmSR.append(csvTrie.iloc[rowmSR,c])
            
            
        elif csvfile.iloc[2,c] == "BOIS":
            listeBOISmSR.append(csvTrie.iloc[rowmSR,c])
            
            
        elif csvfile.iloc[2,c] == "ECOR":
            listeECORmSR.append(csvTrie.iloc[rowmSR,c])
            
            
        elif csvfile.iloc[2,c] == "PROD":
            listePRODmSR.append(csvTrie.iloc[rowmSR,c])
    
    
