# Google Glass Eyetracker

This is my Senior Project for my computer science degree. It shows the attempt to use Google Glass as a device to analyze the human reaction with the external world, concretely in the ophthalmology field, obtaining images from the real world through the Google Glass camera and comparing it in real time with the events produced by the human eye thanks to a second camera attached to the Glass.

The project is a fork of the WearScript Eyetracker project with additional logic written in Python to simulate the movement of the eye based on the images that the eye can see and collected through the Google Glass camera.

https://wearscript.readthedocs.io/en/latest/eyetracking.html

## Connection Diagram

![GitHub Logo](/images/esquema.png)

## Main files

* stream_server.py

  >It's base file is example_sensors.py provided by Wearscript. This file gets the image from the Google Glass camera as
	well as the positions obtained through track.py file.
	It also represents the images in OpenCV and the ellipse with positions
	and recs the session and stores it on the database and the filesystem.
  
  >`Get_sensors()`
  Éste método se encarga de tratar las posiciones que la cámara web
  publica mediante pub/sub. Para comenzar se recopila la información que se
  recibe en el array “result” que ha sido descomprimido por subscribe en
  `ws.subscribe('sensors', get_sensors)`.
  
  > Positions from sensors on the surface of the outer camera window.
  ![GitHub Logo](/images/positions.png)
  
  
* track.py
  
  >Is written in Python and uses the OpenCV libraries for
part of artificial vision. It contains the algorithm of the
coordinates of the pupil.
In order to adapt it to this work, the parameters of
input of eye characteristics to improve detection. Among these
values is the delta, responsible for detecting the curvature of the
iris to detect its edge.
  
  >Therefore the values of the pre-set parameters are:
`Delta:7
Pupil_intensity: 120
Pupil_ratio: 3.0`
