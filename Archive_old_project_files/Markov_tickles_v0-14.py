# -*- encoding: UTF-8 -*-
""" NAO responds to being tickled.

@author: Mike McFarlane

"""



# DESCRIPTION:
# Attempts to generate a realistic response for NAO to being tickled by using Markov Chains.
# PROGRAMMER: 
# Mike McFarlane
# VERSION HISTORY (version, date, description):
# 0.1,18/10/2013, basic code structure outlined in comments, and some matrices and methods set up. Working.
# 0.11, 29/10/2013, start to build up modification of matrices and matrix state selection. Working - matrices blended over time
# and cycles, copied to robotMatrixCurrentList, data verified for target sensor states, and if sensor touched again.
# 0.12, 21/11/2013, add in all sensors to generate new current matrices
# 0.13, standalone code, add random number generator and transition selection
# 0.14, 04/03/2014, code too complex and ideas muddled so rewrite from scratch starting simple.
# This version will provide a simple Markov transition matrix response.
# USAGE: 
# Run from Terminal
# TODO:
# - add turn left and turn right to robotMotionMatrix
# - add a tummy tickle with chest ultrasound sensors verified with bottom facing camera?
# - foot sensors???
# - add more phrases and laughs to speechMatrix
# - modify the not being tickled array so the robot does some moves whilst waiting to be tickled, can set flag in main while loop.
# - for the purposes of this text code, ask user to say target sensor??? Might be better to guage feedback on any sensor is ticklish first?
# - add encouraging feedback to sensor touched methods if a sensor is touched, but it is not the target sensor.
# - split test some repeatable animations, with Markov Chain driven animations. Can be done by modifying
# the matrices so only two states. [request from ASK-NAO forum].


import time
import sys

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "10.0.1.188"

# Global variables to store module instances and proxies
global MarkovTickle
global memory
global speechProxy
global bodyProxy
global leftArmProxy
global rightArmProxy
global robotMotionProxy



class MarkovTickleModule(ALModule):
	""" Simple module for tickling NAO. 

	"""

	def __init__(self, name):
		ALModule.__init__(self, name)

		global memory
		global speechProxy
		global bodyProxy
		global leftArmProxy
		global rightArmProxy
		global robotMotionProxy

		# Lists for large setup items e.g. subscribe, unsubscribe
		self.subscriptionList = ["RightBumperPressed",
								"LeftBumperPressed",
								"FrontTactilTouched",
								]

		

		""" Stuff to do when module starts. 

		"""
		# Setup proxies
		try:
			bodyProxy = ALProxy("ALRobotPosture")
		except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e
		try:
			leftArmProxy = ALProxy("ALRobotPosture")
		except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e
		try:
			rightArmProxy = ALProxy("ALRobotPosture")
		except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e
		try:
			robotMotionProxy = ALProxy("ALMotion")
		except Exception, e:
			print "Could not create proxy to ALMotion"
			print "Error was: ", e
		try:
			speechProxy = ALProxy("ALTextToSpeech")
		except Exception, e:
			print "Could not create proxy to ALTextToSpeech"
			print "Error was: ", e
		try:
			memory = ALProxy("ALMemory")
		except Exception, e:
			print "Could not create proxy to ALMemory"
			print "Error was: ", e

		# Subscribe to the sensor events:
		memory.subscribeToEvent("RightBumperPressed","MarkovTickle","tickled")
		memory.subscribeToEvent("LeftBumperPressed","MarkovTickle","tickled")
		memory.subscribeToEvent("FrontTactilTouched","MarkovTickle","tickled")
		memory.subscribeToEvent("MiddleTactilTouched","MarkovTickle","tickled")
		memory.subscribeToEvent("RearTactilTouched","MarkovTickle","tickled")
		memory.subscribeToEvent("HandRightBackTouched","MarkovTickle","tickled")
		memory.subscribeToEvent("HandRightLeftTouched","MarkovTickle","tickled")
		memory.subscribeToEvent("HandRightRightTouched","MarkovTickle","tickled")
		memory.subscribeToEvent("HandLeftBackTouched","MarkovTickle","tickled")
		memory.subscribeToEvent("HandLeftLeftTouched","MarkovTickle","tickled")
		memory.subscribeToEvent("HandLeftRightTouched","MarkovTickle","tickled")

		

		
		# ---------------- END __init__ ---------------------------

	def tickled(self, key, value, msg):
		""" NAO does this when tickled.

		"""
		pass

	def main(self):
		""" Temp main task.

		"""
		# While, infinite - 
		while True:
			print ("Alive!")
			time.sleep(0.5)

	def shutDownRobot(self):
		""" Exit cleanly. """
        # un-subscribe to the sensor events:
        try:
        	memory.unsubscribeToEvent("RightBumperPressed","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)
        try:	
        	memory.unsubscribeToEvent("LeftBumperPressed","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)
        try:	
        	memory.unsubscribeToEvent("FrontTactilTouched","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)
        try:	
        	memory.unsubscribeToEvent("MiddleTactilTouched","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)	
        try:	
        	memory.unsubscribeToEvent("RearTactilTouched","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)
        try:	
        	memory.unsubscribeToEvent("HandRightBackTouched","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)
        try:	
        	memory.unsubscribeToEvent("HandRightLeftTouched","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)	
        try:	
        	memory.unsubscribeToEvent("HandRightRightTouched","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)	
        try:
        	memory.unsubscribeToEvent("HandLeftBackTouched","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)	
        try:	
        	memory.unsubscribeToEvent("HandLeftLeftTouched","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)
        try:	
        	memory.unsubscribeToEvent("HandLeftRightTouched","MarkovTickle")
        except Exception, e:
        	errorString = "Error was: " + str(e)
        	print(errorString)

	

	        

	
		

	


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
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port

    # Warning: Objects must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global MarkovTickle
    MarkovTickle = MarkovTickleModule("MarkovTickle")

    # Start the temporary main task
    MarkovTickle.main()

    print "Running, hit CTRL+C to stop script"

    try:
        while True:
        	time.sleep(1)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        MarkovTickle.shutDownRobot()
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
		

	









