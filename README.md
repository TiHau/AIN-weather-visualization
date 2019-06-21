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

## Downloader

## Grib2 Extractor

The class _Level_ initializes a new level.

        Args:
            level (int): Integer of the level.
            name (str)j: Name of the level.

        Attributes:
            level (int): Integer of the level.
            name (str)j: Name of the level.
            
        add_parameter(self, parameter):
            adds an parameter to parameters dictionary
            Args:
                parameter (Parameter): an Parameter

The class _Parameter_ initializes a new parameter.    

            Args:
                name (str): Name of the parameter.
                data (float): Value of the parameter.
                unit (str): Unit of the parameter

            Attributes:
                name (str): Name of the parameter.
                data (float): Value of the parameter.
                unit (str): Unit of the parameter

The method _extract extracts data from a gfs file and saves it in an extractor dictionary.
        The extracted data is between coordinate1 and coordinate2.    
        
                Args:
                file_path (str): path to grib2 file.
                lat1 (float): minimal latitude.
                lon1 (float): minimal longitude.
                lat2 (float): maximal latitude.
                lon2 (float): maximal latitude.
                list_params_extract (list): Match pattern list for parameters
        Returns:
                the extractor dict for each coordinate raster position with parameters and the file name

The method _export_to_json_ exports an extracted dictionary to JSON.   
__Attention__: Non-readable values are replaced with "--". 

          Args:
                  dictionary (dict): dictionary to convert.
                  json_name (str): filename of the json write to
           
             
The method _import_from_json converts a JSON file back to an extractor dictionary.
__Attention__: Non-readable values are replaced with "--".

          Args:
                  file_path (str): path of the json file.
          Returns:
                  the  extractor dict for each coordinate raster position with parameters and the file name

__Example method calls__:

    import grib2_extractor as grb
    
    path, grib_data = grb.extract('Filename', min_lat, min_long, max_lat, max_long, ["wind", "height", "other_patterns"])
    grb.export_to_json(grib_data, path)
    grib_data = grb.import_from_json(path + ".json")

## util

## Flight Data

##Plotting



