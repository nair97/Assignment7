#!/bin/env python
# Created on March 25, 2020
#  by Keith Cherkauer
#
# This script servesa as the solution set for assignment-10 on descriptive
# statistics and environmental informatics.  See the assignment documention 
# and repository at:
# https://github.com/Environmental-Informatics/assignment-10.git for more
# details about the assignment.
#
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits.axes_grid1 import ImageGrid
from cartopy.mpl.geoaxes import GeoAxes

def read_station_info( fileName ):
    '''This function reads the contents of the soil moisture station info
    file, including the station name, code, coordiantes and elevation.  Data
    is returned to the main function as a Pandas DataFrame that uses the 
    station ID Number as the index.  Watch out that Longitude is in degrees
    west, not in negative degrees East.'''
    

def read_station_data( fileName ):
    '''Read the contents of the soil moisture data file into a Pandas DataFrame
    where the index is the observation date.  Return the dataframe.  '''

def compute_total_moisture( DataDF ):
    '''Sum the soil moisture per soil column, which has been measured as
    depth of water, so can simply be added together.  Also compute the 
    volumetric water content of the total soil column, by dividing by the 
    total depth (2000 mm) and multiplying by 100%.  Return the original 
    dataframe with two additional columns called 'Total Water Depth (mm)' 
    and 'Total VWC (%)'.'''

def compute_average_moisture_by_station( DataDF, MetaDF ):
    '''Compute the annual average total soil moisture as a depth and as VWC
    for each station.  Add as columns to a copy of the station info dataframe.
    Also compute the annual seasonal average VWC for each station and add to
    the same new dataframe.  Returned dataframe has all of the original columns 
    from the station information file, plus two columns for annual average total
    soil moisture, and four columns for annual average seasonal VWC.'''
    
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



    #
    # Make 4 plot panel with seasonal average soil moisture as VWC
    #
'''    
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

    # loop through the four panels, and the four seasons
    for sidx, ax in enumerate(grid):

        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.STATES)
        ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
    
        # make your plot here for the current season        

    cbar = grid.cbar_axes[0].colorbar(p)
    cbar.set_label_text("Total VWC (%)")
'''
