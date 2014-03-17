
""" Explore LED colour changes in a list.

"""
import sys
from naoqi import ALProxy

IP = "mistcalf.local"
PORT = 9559

try:
    proxy = ALProxy("ALLeds", IP, PORT)
except Exception,e:
    print "Could not create proxy to ALLeds"
    print "Error was: ",e
    sys.exit(1)


def convertRGBToHex(list):
    if len(list) == 3:
        colour = 256 * 256 * list[0] + 256 * list[1] + list[2]
    else:
        raise ValueError("Not a valid RGB list")
    return colour
    
name = 'AllLeds'
duration = 1.0
numEyeChanges = 5
durationList = [duration] * numEyeChanges
RGBColourDict = { "red" : [255, 0, 0], # red
                 "green" : [0, 255, 0], # green
                 "blue" : [0, 0, 255], # blue
                 "yellow" : [255, 255, 0], # yellow
                 "pink" : [255, 51, 153], # pink
                 "purple" : [204, 0, 204], # purple
                 "orange" : [255, 153, 51] # orange
                 
                 }
RGBList = [None] * 5
for i, j in enumerate(RGBList):
    colour = RGBColourDict["yellow"] # Do Markov choice here.
    RGBList[i] = convertRGBToHex(colour)
    
    
print RGBList    
    
proxy.fadeListRGB(name, RGBList, durationList)
proxy.reset(name)
print "Done being a rainbow"