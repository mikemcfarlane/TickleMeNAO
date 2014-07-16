# -*- encoding: UTF-8 -*-
""" Say `My {Body_part} is touched` when receiving a touch event
"""

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse

# Global variable to store the ReactToTouch module instance
ReactToTouch = None
memory = None

class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to HandRightLeftTouched event:
        global memory
        memory = ALProxy("ALMemory")

        self.subscriptionList = ["RightBumperPressed",
                                "LeftBumperPressed",
                                "FrontTactilTouched",
                                "MiddleTactilTouched",
                                "RearTactilTouched",
                                "HandRightBackTouched",
                                "HandRightLeftTouched",
                                "HandRightRightTouched",
                                "HandLeftBackTouched",
                                "HandLeftLeftTouched",
                                "HandLeftRightTouched"
                                ]


        self.easySubscribeEvents("onTouched")

    def easySubscribeEvents(self, callback):
        """ Subscribes to all events in subscriptionList.

        """
        for eventName in self.subscriptionList:
            try:
                memory.subscribeToEvent(eventName, self.getName(), callback)
                #print "Subscribed to %s." % eventName
            except Exception, e:
                print "Subscribe exception error %s for %s." % (e, eventName)


    def easyUnsubscribeEvents(self):
        """ Unsubscribes from all events in subscriptionList.

        """
        for eventName in self.subscriptionList:
            try:
                memory.unsubscribeToEvent(eventName, self.getName())
                #print "Unsubscribed from %s." % eventName
            except Exception, e:
                print "Unsubscribe exception error %s for %s." % (e, eventName)

    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        self.easyUnsubscribeEvents()

        

        self.tts.say("hey")

        # Subscribe again to the event
        self.easySubscribeEvents("onTouched")

    


def main(ip, port):
    """ Main entry point
    """
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,          # parent broker IP
       port)        # parent broker port


    global ReactToTouch
    ReactToTouch = ReactToTouch("ReactToTouch")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="mistcalf.local",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)