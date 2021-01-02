/***********************************
Author: Ruben Muñoz Solera
Subject: TFG UCAM 2015
***********************************/

Stream_server.py: includes the python server which receives 
all the eye info from track.py and visualizes it on a window. 
Also it saves the image in the filesystem and pass the eyedata
to the database file to store them.

dbEyeTracker.py: Includes the database connection and functions

eye_positions.py: gets the eye positions and is stored in wearscript_eyetracking_master folder. 
The rest of the files and folders aren't modified and are necesary 
in order to run wearscript file correctly

wearscript_playground.html: shows the html code executed on Google Glass through wearscript App
to take pictures and send it through the network
