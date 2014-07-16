# -*- coding: ascii -*-
""" NAO responds to being tickled.


"""

__author__ = "Mike McFarlane mike@mikemcfarlane.co.uk"
__version__ = "Revision: 1.0"
__date__ = "Date: 13-05-14"
__copyright__ = "Copyright (c)Mike McFarlane 2014"
__license__ = "MIT License"


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
# - This version will provide a simple Markov transition matrix response.
# - Moved to GitHub version control, archived old version named files.
# - NAO runs numpy v1.6.2, np.random.choice() not till v1.7.x, so have to create cumulative matrices.
# USAGE: 
# Run from Terminal
# TODO:
# - add a tummy tickle with chest ultrasound sensors verified with bottom facing camera?
# - foot sensors???
# - add more phrases and laughs to speechMatrix
# - modify the not being tickled array so the robot does some moves whilst waiting to be tickled, can set flag in main while loop.
# - split test some repeatable animations, with Markov Chain driven animations. Can be done by modifying
# the matrices so only two states. [request from ASK-NAO forum].


import time
import sys
import numpy as np
from optparse import OptionParser
import Markov_tickles_motion_data as mtmd

# todo: investigate custom exceptions when more time
#import Markov_tickles_exceptions as mte

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

NAO_IP = "mistcalf.local"

# Global variables to store module instances and proxies
MarkovTickle = None
MarkovTickleStop = None
memory = None
memoryStop = None
speechProxy = None
animatedSpeechProxy = None
bodyProxy = None
robotMotionProxy = None
myBroker = None
LEDProxy = None
batteryProxy = None
asrProxy = None
systemProxy = None
aupProxy = None


class MarkovTickleModule(ALModule):
	""" Simple module for tickling NAO. 

	"""

	def __init__(self, name):
		""" Initialise module. 

		"""
		ALModule.__init__(self, name)

		# Globals for proxies
		global memory
		global speechProxy
		global animatedSpeechProxy
		global bodyProxy
		global robotMotionProxy
		global LEDProxy
		global batteryProxy
		global asrProxy
		global systemProxy
		global aupProxy

		# Variables for movement
		self.fractionMaxSpeed = 0.6
		self.defaultPose = "StandInit"

		# Variables for animated speech.
		self.bodyLanguageModeConfig = {"bodyLanguageMode":"contextual"}
		self.speechVolume = 1.0
		# Voice choices are: voice1 = "allison", voice2 = "audrey"
		# self.voice = "audrey"

		# # Variables for playing sound files.
		# self.volume = 0.75
		# self.pan = 0.0

		# # Variables for the Markov Chain Transition Matrices
		# self.currentStateWord = 0
		# self.currentStateActionLeftArm = 0
		# self.currentStateActionRightArm = 0
		# self.currentStateInvite = 0
		# self.currentStateLEDs = 0
		# self.currentStateWalk = 0
		# self.currentTickleTarget = 0
		# self.currentStateTickleSuccessPre = 0
		# self.currentStateTickleSuccessPost = 0
		# self.currentStateTickleAgain = 0
		# self.currentStateGameWinPraise = 0
		# self.currentStateGameWinAnimation = 0
		# self.currentStateGameLost = 0
		# self.tickleCounter = 0
		# self.gamecode = [0, 0, 0]
		# self.yourGamecode = [0, 0, 0]
		# self.yourGamecodeCounter = 0
		# self.isASROn = False
		# self.bIsRunning = False
		# self.ids = []
		# self.isWordRecognisedSubscribed = False
		# self.bIntroIsRunning = False
		# self.yourAnswer = ""

		
		

		

		# Lists for large setup items e.g. subscribe, unsubscribe.
		# A tickle target is picked at random from this list.
		# todo: when add in mic tickle and OpenCV tummy tickle they will raise an event.
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

				
		
		
		# Setup proxies
		try:
			bodyProxy = ALProxy("ALRobotPosture")
		except Exception, e:
			print "Could not create proxy to ALRobotPosture. Error: ", e            
		try:
			robotMotionProxy = ALProxy("ALMotion")
		except Exception, e:
			print "Could not create proxy to ALMotion. Error: ", e          
		try:
			speechProxy = ALProxy("ALTextToSpeech")
		except Exception, e:
			print "Could not create proxy to ALTextToSpeech. Error: ", e            
		try:
			animatedSpeechProxy = ALProxy("ALAnimatedSpeech")
		except Exception, e:
			print "Could not create proxy to ALAnimatedSpeech. Error: ", e          
		try:
			memory = ALProxy("ALMemory")
		except Exception, e:
			print "Could not create proxy to ALMemory. Error: ", e
		try:
			LEDProxy = ALProxy("ALLeds")
		except Exception, e:
			print "Could not create proxy to ALLeds. Error: ", e
		try:
			batteryProxy = ALProxy("ALBattery")
		except Exception, e:
			print "Could not create proxy to ALBattery. Error: ", e
		try:
			asrProxy = ALProxy("ALSpeechRecognition")
		except Exception, e:
			print "Could not create proxy to ALSpeechRecognition. Error: ", e
		try:
			systemProxy = ALProxy("ALSystem")
		except Exception, e:
			print "Could not creat proxy to ALSystem. Error: ", e
		try:
			aupProxy = ALProxy("ALAudioPlayer")
		except Exception, e:
			print "Could not creat proxy to ALAudioPlayer. Error: ", e

		
		# ---------------- END __init__ ---------------------------

	


				

	def touched(self, key, value, message):
		""" NAO does this when tickled.
			key = calling event
			value = value from event

		"""
		print key
		print value
		print message
		
		# bodyProxy.goToPosture(self.defaultPose, self.fractionMaxSpeed)

		id = speechProxy.post.say("hey")
		speechProxy.wait(id, 0)


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

	
	


	def mainTask(self):
		""" Temp main task.

		"""

		
			
		# Set voice character.
		# speechProxy.setVoice(self.voice)
		speechProxy.setVolume(self.speechVolume)
		# At 1.22.3 voice speed setting is only avaiable in Japanese.
		# speechProxy.setParameter("speed", 4.0)

		# Pick an initial tickle target.
		# self.pickTickleTarget()

		# Pick an initial game code.
		# self.generateGameCode()

		# First, wake up.
		robotMotionProxy.wakeUp()
		
		# Go to default posture.
		# bodyProxy.goToPosture(self.defaultPose, self.fractionMaxSpeed)

		# self.doIntroduction()

		# Subscribe to the sensor events.
		self.easySubscribeEvents("touched")


		# Invite to play the game:-)
		#self.inviteToTickle()

		while True:
			print "Alive!"
			time.sleep(1)
			# bodyProxy.goToPosture(self.defaultPose, self.fractionMaxSpeed)
			# If time gone by invite someone to tickle!
			# self.inviteTimer += 1
			# if self.inviteTimer >= 20:
			# 	self.inviteToTickle()

			

		
			



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
	global MarkovTickle, MarkovTickleStop
	MarkovTickle = MarkovTickleModule("MarkovTickle")
	#MarkovTickleStop = MarkovTickleStopModule("MarkovTickleStop")

	print "Running, hit CTRL+C to stop script"
	MarkovTickle.mainTask()
	

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print "Interrupted by user, shutting down"
		MarkovTickle.easyUnsubscribeEvents()
		MarkovTickle.stopSpeechRecognition2()
		MarkovTickle.bodyProxy.goToPosture("SitRelax", 0.6)
		MarkovTickle.robotMotionProxy.rest()
		
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
		

	









