#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 14:12:01 2021

@author: Emilie SIROT
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import statistics


#temporel

repDonnees = r"../calculIndicesTemporels/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"


fichiersRep = os.listdir(repDonnees)
csvfile = pd.read_csv(os.path.join(repDonnees,fichiersRep[0]), header=0)



   
indices = csvfile['bandes'].unique()
indicesListe = list(indices)
indicesListe.sort()
del indicesListe[0]

dates = csvfile['date'].unique()
datesListe = list(dates)
datesListe.sort()
del datesListe[0]

date = datesListe[0]
splitDate = []
for k in range(0, len(date), 2):
    splitDate.append(date[k : k + 2])

annee = splitDate[0]+splitDate[1]

nombreIndices = len(indicesListe)
nombreDates = len(datesListe)

for ind in range(3, nombreIndices):
    
    
    
    nomSortieGraph = csvfile.iloc[ind,2]
    
    
    legendeTabInd = ["MEDI", "LAND","SUB","BOIS","ECOR","PROD"]
   
    tabInd = pd.DataFrame(columns = legendeTabInd, index = datesListe)
  
    index = 0
    
    listeMedMEDI = []
    listeMedLAND = []
    listeMedSUB = []
    listeMedBOIS = []
    listeMedECOR = []
    listeMedPROD = []

    
    for dt in range(3, len(csvfile), nombreIndices):
             
        listeMEDI = []
        listeLAND = []
        listeSUB = []
        listeBOIS = []
        listeECOR = []
        listePROD = []
        
        
        for c in range(3, len(csvfile.columns)):
            if csvfile.iloc[2,c] == "MEDI":
                listeMEDI.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "LAND":
                listeLAND.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "SUB":
                listeSUB.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "BOIS":
                listeBOIS.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "ECOR":
                listeECOR.append(csvfile.iloc[dt,c])
                
                
            elif csvfile.iloc[2,c] == "PROD":
                listePROD.append(csvfile.iloc[dt,c])
        
    

    
        listeMEDIFloat = list(map(float, listeMEDI))
        listeLANDFloat = list(map(float, listeLAND))
        listeSUBFloat = list(map(float, listeSUB))
        listeBOISFloat = list(map(float, listeBOIS))
        listeECORFloat = list(map(float, listeECOR))
        listePRODFloat = list(map(float, listePROD))
        
       
        medianeMEDI = statistics.median(listeMEDIFloat)
        listeMedMEDI.append(medianeMEDI)
        
        medianeLAND = statistics.median(listeLANDFloat)
        listeMedLAND.append(medianeLAND)
        
        medianeSUB = statistics.median(listeSUBFloat)
        listeMedSUB.append(medianeSUB)
        
        medianeBOIS = statistics.median(listeBOISFloat)
        listeMedBOIS.append(medianeBOIS)
        
        medianeECOR = statistics.median(listeECORFloat)
        listeMedECOR.append(medianeECOR)
        
        medianePROD = statistics.median(listePRODFloat)
        listeMedPROD.append(medianePROD)
        
    tabInd = tabInd.assign(MEDI=listeMedMEDI)
    tabInd = tabInd.assign(LAND=listeMedLAND)
    tabInd = tabInd.assign(SUB=listeMedSUB)
    tabInd = tabInd.assign(BOIS=listeMedBOIS)
    tabInd = tabInd.assign(ECOR=listeMedECOR)
    tabInd = tabInd.assign(PROD=listeMedPROD)
    


#graphique
    
  
    
    tabInd.plot()
    
    plt.ylabel('Valeur médiane des pixels ')
    plt.xlabel('Dates')
    plt.title("Profil des types de végétations avec l'indice\n"+nomSortieGraph+"pour l'année "+annee)
    
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    plt.tight_layout()
   
    
    plt.savefig(f"sortie/sortieT31TFJ/{nomSortieGraph}.png", dpi = 300)
    
  
    
  
    
  
    
  
    
  
    
  
    
  



# #afficher courbes tous indices pour chaque type de veget


# repDonnees = r"../calculIndicesTFE/sortie/sortieT31TFJ"
# repSortie = "sortie/sortieT31TFJ"
# listeRep = os.listdir(repDonnees)

# for i in range (len(listeRep)):
#     repCourant = os.path.join(repDonnees, listeRep[0])
#     #repCourant = os.path.join(repDonnees, listeRep[i])
#     fichiersRep = os.listdir(repCourant)

# csvfile = pd.read_csv(os.path.join(repCourant,fichiersRep[0]), header=0)
   
# #ordonner le tableau
# csvTrie = csvfile.sort_values(by = 'bandes', ascending = True)

# #Premiere boucle : permet de passer à la ligne du dessous pour changer d'indice
# #separer les graphiques par type indice


# #BSITIan
# for rowBSITian in range(3,362):
    
#     listeMEDIBSITian = []
#     listeLANDBSITian = []
#     listeSUBBSITian = []
#     listeBOISBSITian = []
#     listeECORBSITian = []
#     listePRODBSITian = []
    
#     for c in range(3, len(csvTrie.columns)):
#         if csvfile.iloc[2,c] == "MEDI":
#             listeMEDIBSITian.append(csvfile.iloc[rowBSITian,c])
            
            
#         elif csvfile.iloc[2,c] == "LAND":
#             listeLANDBSITian.append(csvTrie.iloc[rowBSITian,c])
            
            
#         elif csvfile.iloc[2,c] == "SUB":
#             listeSUBBSITian.append(csvTrie.iloc[rowBSITian,c])
            
            
#         elif csvfile.iloc[2,c] == "BOIS":
#             listeBOISBSITian.append(csvTrie.iloc[rowBSITian,c])
            
            
#         elif csvfile.iloc[2,c] == "ECOR":
#             listeECORBSITian.append(csvTrie.iloc[rowBSITian,c])
            
            
#         elif csvfile.iloc[2,c] == "PROD":
#             listePRODBSITian.append(csvTrie.iloc[rowBSITian,c])
    
    
# #BSI
# for rowBSI in range(363,1083):
    
#     listeMEDIBSI = []
#     listeLANDBSI = []
#     listeSUBBSI = []
#     listeBOISBSI = []
#     listeECORBSI = []
#     listePRODBSI = []
    
#     for c in range(3, len(csvTrie.columns)):
#         if csvfile.iloc[2,c] == "MEDI":
#             listeMEDIBSI.append(csvfile.iloc[rowBSI,c])
            
            
#         elif csvfile.iloc[2,c] == "LAND":
#             listeLANDBSI.append(csvTrie.iloc[rowBSI,c])
            
            
#         elif csvfile.iloc[2,c] == "SUB":
#             listeSUBBSI.append(csvTrie.iloc[rowBSI,c])
            
            
#         elif csvfile.iloc[2,c] == "BOIS":
#             listeBOISBSI.append(csvTrie.iloc[rowBSI,c])
            
            
#         elif csvfile.iloc[2,c] == "ECOR":
#             listeECORBSI.append(csvTrie.iloc[rowBSI,c])
            
            
#         elif csvfile.iloc[2,c] == "PROD":
#             listePRODBSI.append(csvTrie.iloc[rowBSI,c])
    
    

# #CVI
# for rowCVI in range(1084,1442):
    
#     listeMEDICVI = []
#     listeLANDCVI = []
#     listeSUBCVI = []
#     listeBOISCVI = []
#     listeECORCVI = []
#     listePRODCVI = []
    
#     for c in range(3, len(csvTrie.columns)):
#         if csvfile.iloc[2,c] == "MEDI":
#             listeMEDICVI.append(csvfile.iloc[rowCVI,c])
            
            
#         elif csvfile.iloc[2,c] == "LAND":
#             listeLANDCVI.append(csvTrie.iloc[rowCVI,c])
            
            
#         elif csvfile.iloc[2,c] == "SUB":
#             listeSUBCVI.append(csvTrie.iloc[rowCVI,c])
            
            
#         elif csvfile.iloc[2,c] == "BOIS":
#             listeBOISCVI.append(csvTrie.iloc[rowCVI,c])
            
            
#         elif csvfile.iloc[2,c] == "ECOR":
#             listeECORCVI.append(csvTrie.iloc[rowCVI,c])
            
            
#         elif csvfile.iloc[2,c] == "PROD":
#             listePRODCVI.append(csvTrie.iloc[rowCVI,c])
    
    
    
# #ND
# for rowND in range(1443, 1487):
    
#     listeMEDIND = []
#     listeLANDND = []
#     listeSUBND = []
#     listeBOISND = []
#     listeECORND = []
#     listePRODND = []
    
#     for c in range(3, len(csvTrie.columns)):
#         if csvfile.iloc[2,c] == "MEDI":
#             listeMEDIND.append(csvfile.iloc[rowND,c])
            
            
#         elif csvfile.iloc[2,c] == "LAND":
#             listeLANDND.append(csvTrie.iloc[rowND,c])
            
            
#         elif csvfile.iloc[2,c] == "SUB":
#             listeSUBND.append(csvTrie.iloc[rowND,c])
            
            
#         elif csvfile.iloc[2,c] == "BOIS":
#             listeBOISND.append(csvTrie.iloc[rowND,c])
            
            
#         elif csvfile.iloc[2,c] == "ECOR":
#             listeECORND.append(csvTrie.iloc[rowND,c])
            
            
#         elif csvfile.iloc[2,c] == "PROD":
#             listePRODND.append(csvTrie.iloc[rowND,c])
    
    
    
# #SR
# for rowSR in range(1488, 1577):
    
#     listeMEDIND = []
#     listeLASRSR = []
#     listeSUBSR = []
#     listeBOISSR = []
#     listeECORSR = []
#     listePRODSR = []
    
#     for c in range(3, len(csvTrie.columns)):
#         if csvfile.iloc[2,c] == "MEDI":
#             listeMEDISR.append(csvfile.iloc[rowSR,c])
            
            
#         elif csvfile.iloc[2,c] == "LAND":
#             listeLANDSR.append(csvTrie.iloc[rowSR,c])
            
            
#         elif csvfile.iloc[2,c] == "SUB":
#             listeSUBSR.append(csvTrie.iloc[rowSR,c])
            
            
#         elif csvfile.iloc[2,c] == "BOIS":
#             listeBOISSR.append(csvTrie.iloc[rowSR,c])
            
            
#         elif csvfile.iloc[2,c] == "ECOR":
#             listeECORSR.append(csvTrie.iloc[rowSR,c])
            
            
#         elif csvfile.iloc[2,c] == "PROD":
#             listePRODSR.append(csvTrie.iloc[rowSR,c])
    
    
    
    
# #indclass
# for rowIndclass in range(1578, 1590):
#     listeMEDIND = []
#     listeLAIndclassIndclass = []
#     listeSUBIndclass = []
#     listeBOISIndclass = []
#     listeECORIndclass = []
#     listePRODIndclass = []
    
#     for c in range(3, len(csvTrie.columns)):
#         if csvfile.iloc[2,c] == "MEDI":
#             listeMEDIIndclass.append(csvfile.iloc[rowIndclass,c])
            
            
#         elif csvfile.iloc[2,c] == "LAND":
#             listeLANDIndclass.append(csvTrie.iloc[rowIndclass,c])
            
            
#         elif csvfile.iloc[2,c] == "SUB":
#             listeSUBIndclass.append(csvTrie.iloc[rowIndclass,c])
            
            
#         elif csvfile.iloc[2,c] == "BOIS":
#             listeBOISIndclass.append(csvTrie.iloc[rowIndclass,c])
            
            
#         elif csvfile.iloc[2,c] == "ECOR":
#             listeECORIndclass.append(csvTrie.iloc[rowIndclass,c])
            
            
#         elif csvfile.iloc[2,c] == "PROD":
#             listePRODIndclass.append(csvTrie.iloc[rowIndclass,c])
    
# #mSR
# for rowmSR in range(1590,1951):
    
#     listeMEDIND = []
#     listeLAmSRmSR = []
#     listeSUBmSR = []
#     listeBOISmSR = []
#     listeECORmSR = []
#     listePRODmSR = []
    
#     for c in range(3, len(csvTrie.columns)):
#         if csvfile.iloc[2,c] == "MEDI":
#             listeMEDImSR.append(csvfile.iloc[rowmSR,c])
            
            
#         elif csvfile.iloc[2,c] == "LAND":
#             listeLANDmSR.append(csvTrie.iloc[rowmSR,c])
            
            
#         elif csvfile.iloc[2,c] == "SUB":
#             listeSUBmSR.append(csvTrie.iloc[rowmSR,c])
            
            
#         elif csvfile.iloc[2,c] == "BOIS":
#             listeBOISmSR.append(csvTrie.iloc[rowmSR,c])
            
            
#         elif csvfile.iloc[2,c] == "ECOR":
#             listeECORmSR.append(csvTrie.iloc[rowmSR,c])
            
            
#         elif csvfile.iloc[2,c] == "PROD":
#             listePRODmSR.append(csvTrie.iloc[rowmSR,c])
    
    
