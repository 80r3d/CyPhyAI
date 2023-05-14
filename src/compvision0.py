# #write python code for openni camera to get depth image and rgb image

# import cv2
# import numpy as np
# from primesense import openni2
# from primesense import _openni2 as c_api

# openni2.initialize("C:\Program Files\OpenNI2\Redist")     # can also accept the path of the OpenNI redistribution

# dev = openni2.Device.open_any()
# rgb_stream = dev.create_color_stream()
# rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=320, resolutionY=240, fps=30))
# rgb_stream.start()


# while True:
#     frame = rgb_stream.read_frame()
#     bgr   = np.fromstring(frame.get_buffer_as_uint16(),dtype=np.uint8)
#     rgb   = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
#     cv2.imshow("rgb",rgb)

# rgb_stream.stop()
# depth_stream.stop()
# openni2.unload()
# cv2.destroyAllWindows()



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
depth_stream = dev.create_depth_stream()

## Check and configure the depth_stream -- set automatically based on bus speed
# print 'The rgb video mode is', rgb_stream.get_video_mode() # Checks rgb video configuration
rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=320, resolutionY=240, fps=30))
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 320, resolutionY = 240, fps = 30))
## Start the streams
rgb_stream.start()
depth_stream.start()

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

def get_depth():
    """
    Returns numpy ndarrays representing the raw and ranged depth images.
    Outputs:
        dmap:= distancemap in mm, 1L ndarray, dtype=uint16, min=0, max=2**12-1
        d4d := depth for dislay, 3L ndarray, dtype=uint8, min=0, max=255
    Note1:
        fromstring is faster than asarray or frombuffer
    Note2:
        .reshape(120,160) #smaller image for faster response
                OMAP/ARM default video configuration
    """
    dmap = np.fromstring(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(240,320)  # Works & It's FAST
    d4d = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
    d4d = 255 - cv2.cvtColor(d4d,cv2.COLOR_GRAY2RGB)
    return dmap, d4d

# define the lower and upper boundaries of the colors in HSV format
lower_red = (0, 50, 50)
upper_red = (10, 255, 255)
lower_green = (40, 50, 50)
upper_green = (80, 255, 255)
lower_blue = (100, 50, 50)
upper_blue = (130, 255, 255)

## main loop
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
    #DEPTH
    dmap,d4d = get_depth()
    # print 'Center pixel is {}mm away'.format(dmap[119,159])


    ## Convert the image to HSV color space
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    
    ## Threshold the image to obtain binary masks for each color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    frame = cv2.Canny(rgb, 100, 200)

    contours_red, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    


    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area > 100 and area < 500:
            cv2.drawContours(rgb, [contour], 0, (255, 0, 0), 2)
            cv2.putText(rgb, 'Red', (contour[0][0][0], contour[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    # for contour in contours_green:
    #     area = cv2.contourArea(contour)
    #     if area > 100:
    #         cv2.drawContours(rgb, [contour], 0, (0, 255, 0), 2)
    #         cv2.putText(rgb, 'Green', (contour[0][0][0], contour[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # for contour in contours_blue:
    #     area = cv2.contourArea(contour)
    #     if area > 100:
    #         cv2.drawContours(rgb, [contour], 0, (0, 0, 255), 2)
    #         cv2.putText(rgb, 'Blue', (contour[0][0][0], contour[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    

    ## Show the image
    cv2.imshow('RGB', frame)

    ## Display the stream syde-by-side
    cv2.imshow('rgb', rgb)
    cv2.imshow('depth', d4d)

# end while

## Release resources 
cv2.destroyAllWindows()
rgb_stream.stop()
openni2.unload()
print ("Terminated")




