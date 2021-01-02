import wearscript
import argparse


#####CODE TESTING######
from PIL import Image
im = Image.open("glass.jpg")

#######################
def callback(ws, **kw):

    def get_image(chan, timestamp, image):
        print('Image[%s] Time[%f] Bytes[%d]' % (chan, timestamp, len(image)))
        ws.publish('cimage',chan, timestamp, image)

    def get_sensors(chan, names, samples):
        print('Sensors[%s] Names[%r] Samples[%r]' % (chan, names, samples))
        ws.publish('sensors:prueba', {'resultado':2},{'re2':3},{'re3':4});
        #ws.publish('csensors',chan,names,samples)
        print('trato de csensors')

    print('beginPrueba')
    ws.publish('sensors:prueba', {'resultado':2},{'re2':3},{'re3':4});
    print('finPrueba')    
    ws.subscribe('image', get_image)
    ws.subscribe('sensors', get_sensors)
    ws.handler_loop()

wearscript.parse(callback, argparse.ArgumentParser())
