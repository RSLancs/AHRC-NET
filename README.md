# README

## AHRC-NET 2021

The scripts in this folder allow you to seach a corpus of `.txt` texts with an input plant name search list. Matches are returned alongside their index within the text. 

The scripts further allow for the input corpus to be geoparsed and for matches to be returned with their index in the text, and also and with a set of geographical coordinates for plotting with GIS.

The scripts allow for collocating plant and location finds based on thier proximity to each other.

Running `main_dev_loop.py` will run the full process, but the Edinbrough Geoparser will need to be downloaded seperatly and placed in the root folder alongside the `main_dev_loop.py` script within the folder `geoparser-1.2`. The first lines of the script set the parameters of the pipe and should be considered carefully. 


## Points of Note

File names in corpus folder cannont have a space ` ` or apostrophes `'`, `"` or anyother special charcters. In general stick to alphanumeric charaters and `_` instead of speaces ` `.
