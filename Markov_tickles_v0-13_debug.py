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
global headProxy
global robotMotionProxy



class MarkovTickleModule(ALModule):
	""" Simple module for tickling NAO. """

	def __init__(self, name):
		ALModule.__init__(self, name)

		global memory
		global speechProxy
		global bodyProxy
		global leftArmProxy
		global rightArmProxy
		global headProxy
		global robotMotionProxy

		#

		# Flag/mutex to stop current matrices being modified by other processes
		# 0 = not being tickled, 1 = being tickled
		self.lockCurrentMatrices = 0

		""" Stuff to do when module starts. """
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
			headProxy = ALProxy("ALRobotPosture")
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
		memory.subscribeToEvent("RightBumperPressed","MarkovTickle","rightBumperTouched")
		memory.subscribeToEvent("LeftBumperPressed","MarkovTickle","leftBumperTouched")
		memory.subscribeToEvent("FrontTactilTouched","MarkovTickle","frontSensorTouched")
		memory.subscribeToEvent("MiddleTactilTouched","MarkovTickle","middleSensorTouched")
		memory.subscribeToEvent("RearTactilTouched","MarkovTickle","rearSensorTouched")
		memory.subscribeToEvent("HandRightBackTouched","MarkovTickle","rightHandTouched")
		memory.subscribeToEvent("HandRightLeftTouched","MarkovTickle","rightHandTouched")
		memory.subscribeToEvent("HandRightRightTouched","MarkovTickle","rightHandTouched")
		memory.subscribeToEvent("HandLeftBackTouched","MarkovTickle","leftHandTouched")
		memory.subscribeToEvent("HandLeftLeftTouched","MarkovTickle","leftHandTouched")
		memory.subscribeToEvent("HandLeftRightTouched","MarkovTickle","leftHandTouched")

		
		# Call a main task, temporary code
		# self.mainTask()

		# ---------------- END __init__ ---------------------------

	# def mainTask(self):
		""" This is a temporary task till I figure out the main activity! """
		# While, infinite - 
		# while True:
		# 	# Loop till both hands are held.
			
		# 	# Get the current state
		# 	speechProxy.say("Testing 1, 2, 3")
			
		# 	time.sleep(0.5)
		
		


			# Create cumulative matrices from the current matrices

			# Generate a random number for each state type

			# Get the desired next state

			# Save the new current states

			# Action each state using seperate parallel task, pushed to the background with post

			# Wait

	def rightBumperTouched(self, key, value, msg):
		""" Right bumper touched. """
		print key
		print value
		print msg
		memory.unsubscribeToEvent("RightBumperPressed","MarkovTickle")
		speechProxy.say("You touched my right foot")
		print("You touched my right foot")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 12
		self.beingTickled(sensorTriggered)
		memory.subscribeToEvent("RightBumperPressed","MarkovTickle","rightBumperTouched")

	def leftBumperTouched(self, key, value, msg):
		""" Left bumper touched. """
		memory.unsubscribeToEvent("LeftBumperPressed","MarkovTickle")
		speechProxy.say("You touched my left foot")
		print("You touched my left foot")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 11
		self.beingTickled(sensorTriggered)
		memory.subscribeToEvent("LeftBumperPressed","MarkovTickle","leftBumperTouched")
	
	def frontSensorTouched(self, key, value, msg):
		""" Front sensor touched. """
		memory.unsubscribeToEvent("FrontTactilTouched","MarkovTickle")
		speechProxy.say("You touched the front of my head")
		print("You touched the front of my head")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 1
		self.beingTickled(sensorTriggered)
		memory.subscribeToEvent("FrontTactilTouched","MarkovTickle","frontSensorTouched")

	def middleSensorTouched(self, key, value, msg):
		""" Middle sensor touched. """
		memory.unsubscribeToEvent("MiddleTactilTouched","MarkovTickle")
		speechProxy.say("You touched the top of my head")
		print("You touched the top of my head")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 2
		self.beingTickled(sensorTriggered)
		memory.subscribeToEvent("MiddleTactilTouched","MarkovTickle","middleSensorTouched")

	def rearSensorTouched(self, key, value, msg):
		""" Rear sensor touched. """
		memory.unsubscribeToEvent("RearTactilTouched","MarkovTickle")
		speechProxy.say("You touched the back of my head")
		print("You touched the back of my head")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 3
		self.beingTickled(sensorTriggered)
		memory.subscribeToEvent("RearTactilTouched","MarkovTickle","rearSensorTouched")

	def rightHandTouched(self, key, value, msg):
		""" Any right hand sensor touched. """
		memory.unsubscribeToEvent("HandRightBackTouched","MarkovTickle")
		memory.unsubscribeToEvent("HandRightLeftTouched","MarkovTickle")
		memory.unsubscribeToEvent("HandRightRightTouched","MarkovTickle")
		speechProxy.say("You touched my right hand")
		print("You touched my right hand")
		self.rightHandActivated = 1
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 8
		self.beingTickled(sensorTriggered)
		self.rightHandActivated = 0
		memory.subscribeToEvent("HandRightBackTouched","MarkovTickle","rightHandTouched")
		memory.subscribeToEvent("HandRightLeftTouched","MarkovTickle","rightHandTouched")
		memory.subscribeToEvent("HandRightRightTouched","MarkovTickle","rightHandTouched")        

	def leftHandTouched(self, key, value, msg):
		""" Any left hand sensor touched. """
		memory.unsubscribeToEvent("HandLeftBackTouched","MarkovTickle")
		memory.unsubscribeToEvent("HandLeftLeftTouched","MarkovTickle")
		memory.unsubscribeToEvent("HandLeftRightTouched","MarkovTickle")
		speechProxy.say("You touched my left hand")
		print("You touched my left hand")
		self.leftHandActivated = 1
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 5
		self.beingTickled(sensorTriggered)
		self.leftHandActivated = 0
		memory.subscribeToEvent("HandLeftBackTouched","MarkovTickle","leftHandTouched")
		memory.subscribeToEvent("HandLeftLeftTouched","MarkovTickle","leftHandTouched")
		memory.subscribeToEvent("HandLeftRightTouched","MarkovTickle","leftHandTouched")

	def beingTickled(self, sensorTriggered):
		""" If a sensor touched, this is being tickled. """
				
		# Lock the current matrices to give this method ownership of the robots actions
		self.lockCurrentMatrices = 1

		speechProxy.say("I'm acting ticklish now, honest!")
		
		## First guess at code flow
		# Transition from NotTickle to Tickle states
		# Get the relevant being tickled Main and NotMain matrices
		# Get the current matrices
		# Add the matrices
		# Normalise the matrices
		# Save the new current matrices
		# Start the timer, this is how long the robot will respond once tickling started
		# While timer active - 
			# Repeat add and normalise of being tickled matrices to current as gives 2nd order history
			# and builds the matrice towards the full being tickled matrix.
			# wait
		# Transition quickly back to waiting state matrices
		# - background task?

		## Actual code		
		

		for i in range(5):
			## loop through the blender a few times to transition from one matrix to the next
			self.blender(sensorTriggered)
			time.sleep(0.5)

		# Unset being tickled flag
		speechProxy.say("Oyy e! I hope you are done making me recite dumb stuff!")
		# Unlock the current matrices
		self.lockCurrentMatrices = 0


	def blender(self, sensorTriggered):
		""" Blends the current matrix values over time. """
		# nb in main code this will have to be done as each body areas matrices are iterated over
		for i in range(0, len(self.robotStateList)):
			if sensorTriggered == self.g_target_sensor:
				g_robot_state = 3
			else:
				g_robot_state = 2
			
			# Add the current matrix to the being tickled matrix, normalise to give a total probability sum of 1.
			# probability values need to be to 3 decimal places for reasonable results ie sum to 1.
			# Round function has limitations due to nature of floating points inc summing a 
			# row of matrix probability values is not exactly 1, but is reasonable here.
			self.robotMatrixCurrentList[i]  = [[(round(((e1+e2)/2),3)) for e1, e2 in zip(row1, row2)] 
								for row1, row2 in zip(self.robotMatrixCurrentList[i], self.robotStateList[i][g_robot_state])]
			
	def speakMe(self, words):
		"""Says stuff"""
		speechProxy.say(words)

	
		

	
		

		

			





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

    try:
        while True:
            # 	# Loop till both hands are held.
			
			# Get the current state
			MarkovTickle.speakMe("Testing 1, 2, 3")
			time.sleep(0.5)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
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


		# stop any post tasks
		# eg void ALModule::stop(const int& id)

		



        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()
		

	









