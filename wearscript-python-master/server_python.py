import argparse
#from Tkinter import *
from PIL import Image
import wearscript

#window = Tk() #Ventana principal
#window.geometry("800x600") #Tamanio Ventana
#window.mainloop() #Llama al inicio de nuestro programa

def callback(ws, **kw):

    def get_image(chan, timestamp, image):
    	image.show();
        print('Image[%s] Time[%f] Bytes[%d]' % (chan, timestamp, len(image)))
        

    def get_sensors(chan, names, samples):
        print('Sensors[%s] Names[%r] Samples[%r]' % (chan, names, samples))

    ws.subscribe('image', get_image)
    ws.subscribe('sensors', get_sensors)
    ws.handler_loop()

    

wearscript.parse(callback, argparse.ArgumentParser())