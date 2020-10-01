#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:17:44 2020

@author: meerarakesh09
"""

import pandas as pd
if __name__ == '__main__': 
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import matplotlib.cm as cm
    from mpl_toolkits.axes_grid1 import ImageGrid
    from cartopy.mpl.geoaxes import GeoAxes

def read_station_info( fileName ):
     # reading the station info csv txt
    statinfoDF = pd.read_csv(fileName, delimiter=',', header=0)
     # using the station ID No. as index 
    statinfoDF = statinfoDF.set_index('No.')
     # setting Longitude in degrees west
    statinfoDF['Lon'] = statinfoDF['Lon'].multiply(-1)
    #Return the dataframe.  
    return statinfoDF

#Read the contents of the soil moisture data file into a Pandas DataFrame    
def read_station_data( fileName ): 
   
   #reading the station soil moisture data txt 
   statDataDF = pd.read_table(fileName, delimiter='\t', header=2, parse_dates=['Date'])
   #set column index to Date
   statDataDF = statDataDF.set_index('Date')
   #Return the dataframe
   return statDataDF

def compute_total_moisture( DataDF ):
      # read soil moisture data columns
    soilmoistcol = DataDF.columns[1:]    
    
    #Sum the soil moisture per soil column for finding total water depth in mm
    DataDF['Total Water Depth (mm)'] = DataDF[soilmoistcol].sum(axis=1) 
                                        
    #calculating VWC% (volumetric water content) by TWD divided by  
    #total depth (2000 mm) and multiplied by 100%
    DataDF['Total VWC (%)'] = DataDF['Total Water Depth (mm)'].div(2000).multiply(100) 
   
    #return the dataframe
    return DataDF 

def compute_average_moisture_by_station( DataDF, MetaDF ):
    #copying station information dataframe into new dataframe by copy() method
    newMetaDF = MetaDF.copy()
    #define loop to process newMetaDF
    for i, row in newMetaDF.iterrows():
         subsDataDF = DataDF[DataDF['Sta']==i] 
         #filter data for selected station
         
         #resample TWD by year & avg, annual 
         annualTWD = subsDataDF['Total Water Depth (mm)'].resample('A-SEP').mean()
         #resample total VWC by year & avg, annual 
         annualTWC = subsDataDF['Total VWC (%)'].resample('A-SEP').mean()
        
         #avg annualTWD and total VWC annual and store in newMetaDF for station index
         newMetaDF.loc[i, 'Annual Total Water Depth (mm)'] = annualTWD.mean()
         newMetaDF.loc[i, 'Annual Total VWC (%)'] = annualTWC.mean()
         
         #resample quaterly
         quarterDF = subsDataDF['Total VWC (%)'].resample('QS-DEC').mean()
         
         #resample total VWC on seasonal basis
         winterTWC = quarterDF[quarterDF.index.month==12] # filter quarter start DEC
         springTWC = quarterDF[quarterDF.index.month==3] # filter quarter start MAR
         summerTWC = quarterDF[quarterDF.index.month==6] # filter quarter start JUN
         fallTWC = quarterDF[quarterDF.index.month==9] # filter quarter start SEP
         
         #adding annual average VWC of seasonal values to newMetaDF
         newMetaDF.loc[i, 'Winter Total VWC (%)'] = winterTWC.mean()
         newMetaDF.loc[i, 'Spring Total VWC (%)'] = springTWC.mean()
         newMetaDF.loc[i, 'Summer Total VWC (%)'] = summerTWC.mean()
         newMetaDF.loc[i, 'Fall Total VWC (%)'] = fallTWC.mean()
         
         #return dataframe
    return newMetaDF
        
# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__': 
 
    # Open and read the contents of the metadata file
    stnInfoFileName = 'datasets/ill-station-info.csv'
    stnInfo = read_station_info( stnInfoFileName )
    
    # Open and read the contents of the data file
    stationDataFileName = 'datasets/ill-soilmoist-data.txt'
    stationData = read_station_data( stationDataFileName )
    
    # Compute total soil column soil moisture
    stationData = compute_total_moisture( stationData )
        
    # Compute annual averages
    annualAvg = compute_average_moisture_by_station( stationData, stnInfo )

    # set bounds for Illinois
    lon1, lon2, lat1, lat2 = -93, -86, 36, 44 # illinois (left, right, bottom, top)
    
    #
    # make map of annual average total soil moisture values
    #
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1,1,1, projection = ccrs.UTM('16N')) #setting projection to UTM 16N
    
    ax.add_feature(cfeature.COASTLINE, edgecolor="black")#set coastline 
    ax.add_feature(cfeature.BORDERS, edgecolor="black")#set borders
    ax.add_feature(cfeature.STATES, edgecolor="black")#set US states
    ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
    col = annualAvg["Annual Total Water Depth (mm)"].values #set to column values
   
    #plot Annual Total Water depth data in scatter plot
    plt.scatter(x=annualAvg.Lon, y=annualAvg.Lat,
                c=(col),cmap='jet',  
                s=500, alpha=1, edgecolors = "black", 
                transform=ccrs.PlateCarree()
               )
    plt.colorbar(label=" in mm ") # set color bar 
    fig.suptitle('Annual Total Water Depth (mm) in Illinois', fontsize = 16)#map title
    plt.savefig('Annual Total Water Depth (mm).PNG') #save plot
    plt.show() #show plot
    plt.close() #close plot
    
    # Make 4 plot panel with seasonal average soil moisture as VWC


    projection = ccrs.UTM('16N')
    axes_class = (GeoAxes,
                  dict(map_projection=projection))
    
    fig = plt.figure(figsize=(6,6))
    # establish 2x2 grid for plots    
    grid = ImageGrid(fig, 111, axes_class=axes_class,
                 nrows_ncols=(2, 2),  # creates 2x2 grid of axes
                 axes_pad=0.2,  # pad between axes in inches
                 cbar_location='right',
                 cbar_mode='single',
                 cbar_pad=0.2,
                 cbar_size='3%',
                 label_mode='')
    
        # make your plot here for the current season        
    season = (annualAvg['Winter Total VWC (%)'], annualAvg['Spring Total VWC (%)'],
                annualAvg['Summer Total VWC (%)'], annualAvg['Fall Total VWC (%)'])
       
          # loop through the four panels, and the four seasons
    for sidx, ax in enumerate(grid):
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.STATES)
        ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
        
        #draw plot of 4 seasons    
        p = grid[sidx].scatter(x=annualAvg.Lon, y=annualAvg.Lat,
                       c=(season[sidx].values),cmap='jet', s=75, 
                       alpha=1, edgecolors="black", 
                       transform=ccrs.PlateCarree())
        
        
        cbar = grid.cbar_axes[0].colorbar(p)
        cbar.set_label_text("Total VWC (%)")

       #save plot and close figure
    plt.savefig('TotalVWC.PNG') #save plot
    plt.show() #show plot
    plt.close() #close plot 
       
