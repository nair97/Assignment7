# Environmental Informatics

## Assignment 07: Python - Spatial Data Analysis

### Lab Objectives

On completion of this lab, students will be able to:

1. Install or update Python packages using a package manager;
2. Use Cartopy and Geopandas to generate spatial plots of environmental data; and
3. Apply those tools to a dataset and generate summary spatial analysis and plots.

### Reading Assignment

- [Intro to GIS and Spatial Analysis](https://mgimond.github.io/Spatial/).  Lecture and assignment are based on concepts from Chapters 2, and 9 through 14.

### Practical Practice

Use the Anaconda Navigator tutorial to help install geopandas and cartopy on your local system
- [Managing packages with Anaconda Navigator](https://docs.anaconda.com/anaconda/navigator/tutorials/manage-packages/)

Then complete these two tutorials to learn how to use geopands and cartopy to work with and visualize spatial datasets in Python.  
- Complete the tutorial [Plotting static maps with geopandas](https://coderzcolumn.com/tutorials/data-science/plotting-static-maps-with-geopandas-working-with-geospatial-data), and 
- Complete the tutorial [Cartopy \[basic maps, scatter maps, bubble maps, and connection map,\]](https://coderzcolumn.com/tutorials/data-science/cartopy-basic-maps-scatter-map-bubble-map-and-connection-map)

> **WARNING:** Download all datasets required for the tutorials and install them in the sub-directory of the repository called "datasets".  These are very large datasets, which is something that GitHub is not designed to track.  The *datasets* directory has been added to the repository *.gitignore* file, so that git does not try to add them.  The local instance of git will not have a problem, but if you put the datafiles somewhere in the repository other than the *datasets* directory, then pushing the repository will fail because default GitHub cannot track files of that size.

> **NOTE:** Potential problem with Section 3.7 of the GeoPandas tutorial.  The missing_kwds only works with geopandas version 0.7.0 or beyond. The default installation from pip was still version 0.6.1 with Python 3.7 when I tested this tutorial, but it now appears to be 0.8.0.  If you have an older version of GeoPandas, you can skip this part of the tutorial as it will not work, but I would expect that it will be part of the default installation soon.  [This link](https://gist.github.com/martinfleis/62d48a607d1cf4dc7d67841b3f3e8792) goes to a demonstration of the missing value capabilities being added to the latest version of geopandas, so a feature that you will be able to access.  (Code versions starting with "0" are very much works in progress, so changes can happen fast, keep your Anaconda modules up to date to get the most from the development process)

> **NOTE:** For some installations of geopandas it appears that the statement "import geopandas" will crash due to a missing part of the module fiona.  This can be resolved by importing fiona first: "import fiona" then "import geopandas".

### The Assignment

For this assignment, you will open a set of two data files containing information on soil moisture measurements for the state of Illinois.  The two data files serve as a simple relational database, where detailed information about the location, name and elevation of the soil moisture measurement stations is stored in a station information file, **datasets/ill-station-info.csv**, while the actual data for each day of observation and each station is stored in a separate data file, **datasets/ill-soilmoist-data.txt**.  The station data file includes the station ID number on each line, indicating the day and location of the soil moisture measurements.  The station ID can then be used to link (join or relate) the data file with the additional site specific information in the station information file.  This reduces the size of the data file, and the potential for errors introduced by having to repeat all of the station information for each line of the data file.  It does mean, however, that you have to work with two files to summarize the data and plot the results of those summaries on a map of Illinois.

1. Copy the template file **template_Spatial_Data_Analysis.py** to the submission file **Spatial_Data_Analysis.py** and edit the template to complete the assigned tasks

2. Read the station supplementary data file **datasets/ill-station-info.csv** into a Pandas dataframe.  
   - Open the file first, and make sure that you understand what information is in the file and how it is formatted. 
   - Use the first line of the file as a header for the dataframe.  
   - Watch the units of latitude and longitude.  You cannot keep track of the units of North and South for Latitude and East and West for Longitude, so make sure that the units reflect the location of the stations in Illinois.
   - Coordinates in latitude and longitude for Illinois must fall within: longitude -93 deg and -86 deg, and latitude 36 deg and 44 deg.
3. Read the soil moisture data file **datasets/ill-soilmoist-data.txt** into a second Pandas dataframe.
   - Open the file first, and make sure that you understand what information is in the file and how it is formatted. 
   - Use the appropriate row from the file as the header for your dataframe.
   - Use the date column for the dataframe index.
4. Write a function that will compute the following metrics from the soil moisture data *on a station by station basis* and add the results to a new dataframe based on the station information dataframe.
   - The total soil moisture for each day of observation, by summing all soil moisture depths for all soil layers.
     - This value should be appended to the dataframe to create a new column called 'Total Water Depth (mm)'
   - Convert the total column soil moisture into the volumetric water content (VWC; volume of water in the soil / volume of soil).
     - Divide the Annual Total Water Depth in mm by the total soil column depth in mm.
     - Convert the resulting fractional value to a percentage and store in the dataframe with the column name 'Total VWC (%)'.
5. Write a function that will compute the following metrics from the soil moisture data *on a station by station basis* and add the results to a new dataframe based on the station information dataframe.
   - Use the pandas .copy() method to copy the existing station information dataframe into a new dataframe.
   - Build a loop that will filter the soil moisture data frame for each station in turn.  Within that loop compute the following:
     - Compute annual average values for Total Water Depth and Total VWC by resampling individual measurements to average annual values for each water year.
       - Water year is defined as October 1 through September 30.
       - Compute the average value for all years and store it in the new dataframe using the station ID for the row index, and the column names 'Annual Total Water Depth (mm)' and 'Annual Total VWC (%)'.
     - Compute the total soil column VWC (%) on a seasonal basis.
       - Define seasons as three month intervals as follows:
         - *Winter* = December, January and February
         - *Spring* = March, April, and May
         - *Summer* = June, July, and August
         - *Fall* = September, October, and November
       - Add the annual average of the seasonal values to the new dataframe using the station ID for the row index, and the column name '*SEASON* Total VWC (%)', where *SEASON* is replaced with the name of the season, as defined above.
6. Use geopandas or cartopy to generate the following figures.  All figures should show spatial data using the UTM Zone 16N projection.

   > **NOTE:** You can use geopandas, cartopy or a mixture to complete this assignment.  At this time, I suggest that you use cartopy for at least the basemap since getting the state boundaries is pretty easy, and included in the tutorial provided.  
      
   - A map of Illinois showing 'Annual Total Water Depth (mm)' as color coded symbols on the map.  
     - Include a colorbar that defines which colors go with what range of values.  The following links will likely be useful to you:
       - [The matplotlib pyplot documentation on the scatter function](https://matplotlib.org/3.3.1/api/_as_gen/matplotlib.pyplot.scatter.html).
       - [The matplotlib pyplot made on choosing color scales](https://matplotlib.org/3.1.1/tutorials/colors/colormaps.html)
       - [The matplotlib documentation on colorbars](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.colorbar.html)
     - Be sure to select a marker size that is big enough to fill much of the plot area, without resulting in too much overlap.  **NOTE:**. There are two measurements taken at Dixon Springs, so there will be overlap for that site no matter what.
     - Set the marker edge color to black so that no matter what colormap you select all sites are visible.
   - A multi-part figure showing seasonal Total VWC (%) using the same color scale for all figures.
     - The plot should start with Winter in the upper right of a 2x2 matrix, spring should be upper right, summer lower left, and fall in the lower right.
     - All four plots should use the same color scale - so same magnitude, same color scale.
     - I have provided additional template code for this because getting everything to work was annoying and not part of the assignment.  This is not my preferred plotting package, but is worth learning.  Here are links to some of the pages I used to develop this template - you might want to explore them to do more with your own figures in the future.
       - [This link provides details on GeoAxes the method by which cartopy (and geopandas) interact with matplotlib](https://scitools.org.uk/cartopy/docs/v0.13/matplotlib/geoaxes.html)
       - [The last example on this page was useful for plotting two images](https://scitools.org.uk/cartopy/docs/v0.15/matplotlib/advanced_plotting.html)
       - [In the end, it helped to use the AxesGrid module from matplotlib](https://matplotlib.org/mpl_toolkits/axes_grid/users/overview.html), with more explicit information on the [ImageGrid (or AxisGrid - seems to be interchangeable) function available here](https://matplotlib.org/api/_as_gen/mpl_toolkits.axes_grid1.axes_grid.ImageGrid.html?highlight=mpl_toolkits%20axes_grid1%20imagegrid#mpl_toolkits.axes_grid1.axes_grid.AxesGrid)
       - [This was probably the most useful page for plotting multiple grids in a single figure with cartopy](https://scitools.org.uk/cartopy/docs/v0.16/gallery/axes_grid_basic.html)
       - [In the end, I still needed this helpful guide for getting the colorbar label to plot](https://stackoverflow.com/questions/32469579/how-can-i-add-a-label-to-colorbar-using-imagegrid) because an early release package (which s version 0.x always is, requires a little black magic.
   
7. Save all of the figures as PNG files and submit with your assignment.

#### What to turn in...

The following should be included in your GitHUB repository:

1. One figure from each of the Practical Practice tutorials, but NONE of the data used for the tutorials (that should be stored in the datasets directory and excluded from the GitHub repository.

2. A completed version of the code **Spatial_Data_Analysis.py**.

3. The two spatial figures required, both as PNG files.

4. Check your final scripts into the assignment repository and push to GitHUB. 

5. Use the provided link to submit the GitHUB repository to GradeScope.  The autograder will return a report on whether the submitted code met the performance checks.  If errors are found, fix the code, and resubmit.

#### Grading Rubric (50 pts Total)

| Question | Description | Score |
| -------- | ----------- | ----- |
| 1. |  | 15 pts |
| 2. |  | 15 pts |
| 3. |  | 5 pts |
| 4. |  | 5 pts |
| 5. |  | 5 pts |
| 6. |  | 5 pts |
