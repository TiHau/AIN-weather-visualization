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

## Getting started
To create a plot you have to add the simulation file to the project directory. After this just set the SIMULATION_FILE constant (Main.py) to the file name and run the Main class. 

## Grib2 Extractor
__Example method calls__:

    import grib2_extractor as grb
    
    path, grib_data = grb.extract('Filename', min_lat, min_long, max_lat, max_long, ["wind", "height", "other_patterns"])
    grb.export_to_json(grib_data, path)
    grib_data = grb.import_from_json(path + ".json")