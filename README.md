# AIN-weather-visualization

## Installation 
First install the following packages, as they are requirements for the package pygrib:   
eccodes: sudo apt-get install libeccodes-dev / yaourt -S eccodes   
jasper: sudo apt-get install jasper / sudo pacman -S jasper   
proj: sudo apt-get install proj-bin /sudo pacman -S proj   
cython: sudo apt-get install cython / sudo pacman -S cython
libjpeg: sudo apt-get install libjpeg-dev libjpeg-turbo8-dev / sudo pacman -S libjpeg

Install all packages that are listed in _requirements.txt_.

Further reading: https://jswhit.github.io/pygrib/docs/index.html

##Getting started

To create a plot you have to add the simulation file to the project directory. After this just set the
SIMULATION_FILE constant (Main.py) to the file name and run the Main class.

## Downloader

__Example method call__:    
            
    downloader.download(first_timestamp, last_timestamp)

## Grib2 Extractor

__Example method calls__:

    import grib2_extractor as grb
    
    path, grib_data = grb.extract('Filename', min_lat, min_long, max_lat, max_long, ["wind", "height", "other_patterns"])
    grb.export_to_json(grib_data, path)
    grib_data = grb.import_from_json(path + ".json")

## util
    
__Example method calls__:   

    #calculating interpolated values
    grib_data[key][key2].parameters[key3].data = 
    util.interp(x1, x2, value3.data, 
    grib_data_future[key][key2].parameters[key3].data, x_res)
    
    # Geo interpolation
        tl_lat = util.round_to_nearest_quarter_up(entry.latitude)
        tl_long = util.round_to_nearest_quarter_down(entry.longitude)
        ...
    #
    ip = util.get_interpolated_value(tl_lat, tl_long, tl_param.data, tr_lat, tr_long, tr_param.data,
         bl_lat, bl_long, bl_param.data, br_lat, br_long, br_param.data,
         entry.latitude, entry.longitude)
         
## Flight Data

A dictionary of extracted simulation data. Entries contain latitude,
longitude, altitude, timestamp and the Boolean _is_waypoint_.


##Plotting

The parameters contain:
 - the number of waypoints or timestamps that you want to have displayed
 - the list with entries of filtered and interpolated grib data
 - the list with entries of filtered and interpolated FlightData
 - a Boolean that needs to be set to true if you want the x-axis to show waypoints
 and false for timestamps

__Example method calls__:
  
    plotting(number_of_waypoints, res, at_waypoint, False)