import numpy as np
import cv2
from primesense import openni2#, nite2
from primesense import _openni2 as c_api

## Path of the OpenNI redistribution OpenNI2.so or OpenNI2.dll
# Windows
dist = 'C:\Program Files\OpenNI2\Redist'
# OMAP
#dist = '/home/carlos/Install/kinect/OpenNI2-Linux-ARM-2.2/Redist/'
# Linux
# dist ='/home/carlos/Install/openni2/OpenNI-Linux-x64-2.2/Redist'

## Initialize openni and check
openni2.initialize(dist) #
if (openni2.is_initialized()):
    print ("openNI2 initialized")
else:
    print ("openNI2 not initialized")

## Register the device
dev = openni2.Device.open_any()

## Create the streams stream
rgb_stream = dev.create_color_stream()

## Check and configure the depth_stream -- set automatically based on bus speed
# print 'The rgb video mode is', rgb_stream.get_video_mode() # Checks rgb video configuration
rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=320, resolutionY=240, fps=30))

## Start the streams
rgb_stream.start()

## Use 'help' to get more info
# help(dev.set_image_registration_mode)


def get_rgb():
    """
    Returns numpy 3L ndarray to represent the rgb image.
    """
    bgr   = np.fromstring(rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(240,320,3)
    rgb   = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
    return rgb    
#get_rgb


## Define the lower and upper boundaries of the colors in HSV format
lower_red = (0, 50, 50)
upper_red = (10, 255, 255)
lower_green = (40, 50, 50)
upper_green = (80, 255, 255)
lower_blue = (100, 50, 50)
upper_blue = (130, 255, 255)

## Main loop
s=0
done = False
while not done:
    key = cv2.waitKey(1) & 255
    ## Read keystrokes
    if key == 27: # terminate
        # print "\tESC key detected!"
        done = True
    elif chr(key) =='s': #screen capture
        # print "\ts key detected. Saving image {}".format(s)
        cv2.imwrite("ex2_"+str(s)+'.png', rgb)
        #s+=1 # uncomment for multiple captures
    #if
    
    ## Streams    
    #RGB
    rgb = get_rgb()
    
    ## Convert the image to HSV color space
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    
    ## Threshold the image to obtain binary masks for each color
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    red_object = cv2.bitwise_and(rgb, rgb, mask=red_mask)
    green_object = cv2.bitwise_and(rgb, rgb, mask=green_mask)
    blue_object = cv2.bitwise_and(rgb, rgb, mask=blue_mask)

    cv2.imshow('red object', red_object)
    cv2.imshow('green object', green_object)
    cv2.imshow('blue object', blue_object)
# end while

## Release resources
cv2.destroyAllWindows()
rgb_stream.stop()
openni2.unload()
print ("Terminated")

    
