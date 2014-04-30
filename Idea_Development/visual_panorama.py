# An example with visual panorama
import sys
from naoqi import ALProxy
import time


def main():
    ip = "mistcalf.local"


    try:
        motion = ALProxy("ALMotion", ip, 9559)
        panorama = ALProxy("ALPanoramaCompass", ip, 9559)
    except:
        print "Cannot create proxies: %s" % sys.exc_info()[0]
        return

    time.sleep(5)
    motion.wakeUp()
    rc = -1

    rc = panorama.setupPanorama()

    description = []
    if (rc != 0):
        print "Cannot load or setup panorama"
        return

    description = panorama.getCurrentPanoramaDescriptor()
    print "Panorama " + str(description[0]) + " loaded and ready"

    position = panorama.getCurrentPosition()

    print "Angle is now " + str(position[0])

    time.sleep(2)

    print "Moving to position 0 with odometry"
    motion.moveTo(0, 0, 3.14)

    position = panorama.getCurrentPosition()
    print "Angle is now " + str(position[0])

    time.sleep(2)

    print "Going to position 1.5"
    position = panorama.goToPosition(1.5)

    position = panorama.getCurrentPosition()
    print "Angle is now " + str(position[0])

    time.sleep(2)

    motion.rest()

if __name__=="__main__":

    main()
    sys.exit(0)