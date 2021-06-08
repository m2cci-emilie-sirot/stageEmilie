#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:15:37 2021

@author: Emilie sirot
"""
import os
from osgeo import gdal
from osgeo import ogr
import numpy
import numpy as np
import rasterio
from PIL import Image
import geopandas as gpd
from pyproj import Proj, transform
import matplotlib.pyplot as plt
import affine
import xarray as xr


#drivers

gdal.AllRegister()

#se placer dans le répertoire "applicationMasqueSnow"


  
####################
####################
### Tuile 31TFJ ####
####################
####################


#Ouverture fichiers



repDonnees = r"../decoupageEmpriseZipSnow/sortie/sortieT31TFJ"
repSortie = "sortie/sortieT31TFJ"


dico = {}
dicoPourcentage = {}

#creation liste des sous-répertoires (les différentes dates de la tuile)

listeRep = os.listdir(repDonnees)


for i in range (len(listeRep)):
    repCourant = os.path.join(repDonnees, listeRep[i])#se positionne dans le répertoire d'une date
    fichiersRep = os.listdir(repCourant)#liste les fichiers
    
    masque = [f for f in fichiersRep if 'masque' in f]
    
    nomPartiesImage = os.path.basename(masque[0]).split("_")#séparer les parties du fichier en cours de traitement pour les réutiliser pour la sortie
    sat = nomPartiesImage[0]
    date = nomPartiesImage[1]
    tuile = nomPartiesImage[2]
    masqueConverti = nomPartiesImage[3]+"Snow"
    
    
#définir les répertoires en sortie  
    rep = f"{sat}_{date}_{tuile}"
    repSortieDate = os.path.join(repSortie, rep)
    os.makedirs(repSortieDate, exist_ok=True) # création du dossier sur le disque
 
            
#Lire la valeur des points TFE sur les pixels correspondant du masque



    TFEChemin = "TFE/tfe_bio_T31TFJ_WGS84.shp"
    TFE = gpd.read_file(TFEChemin) #ouverture du shp
    # TFE2 = TFE.to_crs(epsg=4326)
    
    listePixTFE = []
    
    
    listeC = []  
    
    for j in range(len(TFE)):
          
    
        x = TFE.iloc[j].geometry.centroid.x #récupère les coordonnées d'un point
        y = TFE.iloc[j].geometry.centroid.y
        
        listeC.append((x,y))

        
        masqueSnow = Image.open(repDonnees+'/'+listeRep[i]+'/'+masque[0], 'r')
        
        
        print(masquesnow.GetMetadata)
        masque2 = masquesnow.GetGeoTransform()

        TL_x, x_res, _, TL_y, _, y_res = masquesnow.GetGeoTransform()
        coordinate = (x,y)
        x_index = (x - TL_x) / x_res
        y_index = (y - TL_y) / y_res
        masquearrayG = masquesnow.ReadAsArray()
        pixel_val = masquearrayG[y_index, x_index]






        
        pix = masqueSnow.load()
        
        # print(masqueSnow.size)
        # pixel_values = list(masqueSnow.getdata())
        
    
        listePixTFE.append(pix[x,y])
      
              
        nombreNoData = listePixTFE.count(205)
        pourcentage = (100*nombreNoData)/111
        
        dico[date] = listePixTFE
        dicoPourcentage[date] = pourcentage
        

        




def retrieve_pixel_value(geo_coord, data_source):
    """Return floating-point value that corresponds to given point."""
    x, y = geo_coord[0], geo_coord[1]
    forward_transform =  \
        affine.Affine.from_gdal(*data_source.GetGeoTransform())
    reverse_transform = ~forward_transform
    px, py = reverse_transform * (x, y)
    px, py = int(px + 0.5), int(py + 0.5)
    pixel_coord = px, py

    data_array = np.array(data_source.GetRasterBand(1).ReadAsArray())
    return data_array[pixel_coord[0]][pixel_coord[1]]


coordonnees = [x,y]


testfonc = retrieve_pixel_value(coordonnees,masquesnow)



masqueRasterio = rasterio.open(repDonnees+'/'+listeRep[i]+'/'+masque[0])

def getCoordinatePixel(map,lon,lat):
    # open map
    dataset = rasterio.open(map)
    # get pixel x+y of the coordinate
    py, px = dataset.index(lon, lat)
    # create 1x1px window of the pixel
    window = rasterio.windows.Window(px - 1//2, py - 1//2, 1, 1)
    # read rgb values of the window
    clip = dataset.read(window=window)
    return(clip[0][0][0],clip[1][0][0],clip[2][0][0])

print(getCoordinatePixel(repDonnees+'/'+listeRep[i]+'/'+masque[0],x,y))




####GDAL


    TFEGDAL = ogr.Open(TFEChemin)
    TFELayer = TFEGDAL.GetLayer()
    srs = TFELayer.GetSpatialRef()    
    print(srs)   
    
    
    masquesnow = gdal.Open(repDonnees+'/'+listeRep[i]+'/'+masque[0])
    srsRaster = masquesnow.GetSpatialRef()
    print(srsRaster)
    band = masquesnow.GetRasterBand(1)
    
    cols = masquesnow.RasterXSize
    rows = masquesnow.RasterYSize

    transform = masquesnow.GetGeoTransform()
    
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = -transform[5]
    
    data = band.ReadAsArray(0, 0, cols, rows)
    
    # points_list = [ (x, y) ] #list of X,Y coordinates
    
    # for point in listeC:
    #     col = int((point[0] - xOrigin) / pixelWidth)
    #     row = int((yOrigin - point[1] ) / pixelHeight)
    
    
     for point in listeC:
        col = int((point[0] - xOrigin) / pixelWidth)
        row = int((yOrigin - point[1] ) / pixelHeight)
        
        
       
        print(row,col, data[row][col])


     
    
        print(row,col, data[row][col])

####xarray




masqueX = xr.open_rasterio(repDonnees+'/'+listeRep[i]+'/'+masque[0])
img = masqueX[0, :, :]

val = img.sel(x=x, y=y)


####rasterio conversion 

xs = np.array(x)
ys = np.array(y)

masqueRasterio = rasterio.open(repDonnees+'/'+listeRep[i]+'/'+masque[0])
rows, cols = rasterio.transform.rowcol(masqueRasterio.transform, xs, ys)


########

janvier = [[0,50.50,49.50,0],[25.50,65.18,0,9.32]]
fevrier = [[54.36,0,45.64],[0,50.0,0,50.0]]
mars = [[23.80,0,0,76.2],[32,45.6,0,22.4]]
avril = [[0,50.50,49.50,0],[25.50,65.18,0,9.32]]
mai = [[54.36,0,45.64],[0,50.0,0,50.0]]
juin = [[23.80,0,0,76.2],[32,45.6,0,22.4]]
juillet = [[0,50.50,49.50,0],[25.50,65.18,0,9.32]]
aout = [[54.36,0,45.64],[0,50.0,0,50.0]]
septembre = [[23.80,0,0,76.2],[32,45.6,0,22.4]]
octobre = [[0,50.50,49.50,0],[25.50,65.18,0,9.32]]
novembre = [[54.36,0,45.64],[0,50.0,0,50.0]]
decembre = [[23.80,0,0,76.2],[32,45.6,0,22.4]]


  
    Gjanvier = janvier
    Gfevrier = fevrier
    Gmars = mars
    Gavril = avril
    
    ind = [x for x, _ in enumerate(legendeDates)]#taille
    
    
    plt.bar(ind, GNoData, width=1, label='NoData',color='black', bottom=GNeige+GNuages+GRien)
    plt.bar(ind, GNeige, width=1, label='Neige',color='silver', bottom=GNuages+GRien)
    plt.bar(ind, GNuages, width=1, label='Nuages',color='blue', bottom=GRien)
    plt.bar(ind, GRien, width=1, label='Rien',color='green')
    
    
    
    plt.xticks(ind, legendeDates)
    plt.ylabel('dates')
    plt.xlabel('pourcentage')
    plt.legend(labels=['NoData','Neige','Nuages','Rien'],loc="upper right")
    plt.title("TFE masque")
    
    plt.ylim = 1.0
    
    plt.setp(plt.gca().get_xticklabels(),rotation=45, horizontalalignment='right')
    
    
    plt.show()
    
    print(dicoPourcentage[date][3])