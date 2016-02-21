# -*- coding: utf-8 -*-
"""
Checking if a latlon coordinate is inside a list of polygon
"""

import csv,sys, shapefile
import numpy as np
import pandas as pd
import grid.grid as grid
import datetime

def calculateSlope(line):
    return (line[3] - line[1])/(line[2] - line[0])

output = pd.DataFrame(columns=columns)

for latlon in xrange(0, sg_latlon.shape[0]):
    lat2 = sg_latlon[latlon,0]
    lon2 = sg_latlon[latlon,1]
    for i in xrange(0, int(max(keep_polygon[:,0]))+1):
        ############ keeping polygon i as a record
        record = keep_polygon[keep_polygon[...,0].astype(int) == i]   
        ############ creating lines [fromx, fromy, tox,toy]###################
        #columns =['fromlat','fromlon', 'tolat','tolon']
        if record.shape[0] == 0:
            continue
        lines = np.array([record[0,2],record[0,3], record[1,2], record[1,3]])
        for j in range(1, record.shape[0]-1): 
            lines= vstacking([lines, np.array([record[j,2],record[j,3], record[j+1,2], record[j+1,3]])])       ########### lines creation
        
        ############ checking if the longitude is between the longitudes of the line ###########
        ################################ if not, we will drop it. ##############################
        drop_index = []
        original_num_rows = lines.shape[0]
        for j in xrange(0,lines.shape[0]):
            max_y = max(lines[j, 1], lines[j,3])
            min_y = min(lines[j, 1], lines[j,3])
            if not (lon2 > min_y and lon2 < max_y):
                drop_index.append(j)
        
        lines = np.delete(lines, drop_index,0)
        ##### if the lines matrix is already empty, we just skip and go to the next iteration of the lon2 loop ######
        if lines.shape[0] == 0:
            continue
        ##### if the lines matrix isn't empty, continue next stage
        ###### from.getX() + (y - from.getY()) / slope;
        ###### calculate line x at y 
        #columns =['x', 'y']
        newpoints = np.array([(lines[0,0] + ((lon2 - lines[0,1]) / calculateSlope(lines[0]))), lon2])            
        for j in xrange(1, lines.shape[0]):
            newpoints = vstacking([newpoints, [(lines[j,0] + (lon2 - lines[j,1]) / calculateSlope(lines[j])), lon2]])
        newpoints = newpoints[newpoints[:,0].argsort()]            
        #################### finally, check if the lat lon is inside or outside the polygon using
        ########## the ray-casting algorithm
        inside = False
        for j in xrange(0, newpoints.shape[0]):
            if (lat2 < newpoints[j,0]):
                break
            inside = not inside
        if inside == True:      
            output.append({'lat': lat2, 'lon': lon2, 'poly_id':i}, ignore_index=True)
            break
      #  print datetime.datetime.now() - fstart
   