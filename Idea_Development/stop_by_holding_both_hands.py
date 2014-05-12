import time
import sys
from optparse import OptionParser

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

NAO_IP = "mistcalf.local"

# Global variables to store module instances and proxies
HandTouch = None
touchProxy = None
memoryProxy = None

class HandTouchModule(ALModule):
    """ Simple module for tickling NAO. 

    """

    def __init__(self, name):
        """ Initialise module. 

        """
        ALModule.__init__(self, name)

        # Globals for proxies
        global touchProxy
        global memoryProxy

        self.rightHandFlag = False
        self.leftHandFlag = False
        
        self.subscriptionListRight = [
                                "HandRightBackTouched",
                                "HandRightLeftTouched",
                                "HandRightRightTouched"
                                ]

        self.subscriptionListLeft = [
                                "HandLeftBackTouched",
                                "HandLeftLeftTouched",
                                "HandLeftRightTouched"
                                ]
        
        # Setup proxies
        try:
            touchProxy = ALProxy("ALTouch")
        except Exception, e:
            print "Could not create proxy to ALTouch. Error: ", e            
        try:
            memoryProxy = ALProxy("ALMemory")
        except Exception, e:
            print "Could not create proxy to ALTouch. Error: ", e  

        
        self.easySubscribeEventsRight()
        self.easySubscribeEventsLeft()

    

    def easySubscribeEventsRight(self):
        for eventName in self.subscriptionListRight:
            try:
                memoryProxy.subscribeToEvent(eventName, self.getName(), "rightHandTouched")
                #print "Subscribed to %s." % eventName
            except Exception, e:
                print "Subscribe exception error %s for %s." % (e, eventName)

    def easySubscribeEventsLeft(self):
        for eventName in self.subscriptionListLeft:
            try:
                memoryProxy.subscribeToEvent(eventName, self.getName(), "leftHandTouched")
                #print "Subscribed to %s." % eventName
            except Exception, e:
                print "Subscribe exception error %s for %s." % (e, eventName)

    def easyUnsubscribeEventsRight(self):
        for eventName in self.subscriptionListRight:
            try:
                memoryProxy.unsubscribeToEvent(eventName, self.getName())
                #print "Subscribed to %s." % eventName
            except Exception, e:
                print "Unsubscribe exception error %s for %s." % (e, eventName)

    def easyUnsubscribeEventsLeft(self):
        for eventName in self.subscriptionListLeft:
            try:
                memoryProxy.unsubscribeToEvent(eventName, self.getName())
                #print "Subscribed to %s." % eventName
            except Exception, e:
                print "unsubscribe exception error %s for %s." % (e, eventName)



    def rightHandTouched(self):
        self.easyUnsubscribeEventsRight()
        print "---------- right ----------"
        self.rightHandFlag = True
        print self.rightHandFlag
        print self.leftHandFlag
        
        if self.leftHandFlag:
            print "stop"
        time.sleep(1.0)
        self.rightHandFlag = False
        self.easySubscribeEventsRight()

    def leftHandTouched(self):
        self.easyUnsubscribeEventsLeft()
        print "-------- left ---------"
        self.leftHandFlag = True
        print self.rightHandFlag
        print self.leftHandFlag
        if self.rightHandFlag:
            print "stop"
        time.sleep(1.0)
        self.leftHandFlag = False
        self.easySubscribeEventsLeft()

def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address of your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=9559)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must   stay alive until the program exists
    global myBroker
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port

    # Warning: Objects must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global HandTouch
    HandTouch = HandTouchModule("HandTouch")


    print "Running, hit CTRL+C to stop script"
    while True:
        time.sleep(1)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        
        # stop any post tasks
        # eg void ALModule::stop(const int& id)
        try:
            myBroker.shutdown()
        except Exception, e:
            print "Error shutting down broker: ", e
        try:
            sys.exit(0)
        except Exception, e:
            print "Error exiting system: ", e


if __name__ == "__main__":
    main()