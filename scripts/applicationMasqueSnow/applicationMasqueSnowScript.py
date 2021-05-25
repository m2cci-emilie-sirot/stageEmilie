#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:15:37 2021

@author: Emilie sirot
"""
import os
from PIL import Image
from osgeo import ogr

point = "TFE/test.shp"

testPoint = ogr.Open(point, update = 0)
testPointRef = testPoint.GetLayer()

ref = testPointRef.GetSpatialRef
print(testPointRef.schema())


