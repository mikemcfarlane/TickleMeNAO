# -*- coding: ascii -*-
""" NAO responds to being tickled.


"""

__author__ = "Mike McFarlane mike@mikemcfarlane.co.uk"
__version__ = "Revision: 0.14"
__date__ = "Date: 11-04-14"
__copyright__ = "Copyright (c)Mike McFarlane 2014"
__license__ = "TBC"


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
memory = None
speechProxy = None
animateProxy = None
bodyProxy = None
leftArmProxy = None
rightArmProxy = None
robotMotionProxy = None
myBroker = None
LEDProxy = None



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
		global animateProxy
		global bodyProxy
		global leftArmProxy
		global rightArmProxy
		global robotMotionProxy
		global LEDProxy

		# Variables for movement
		self.fractionMaxSpeed = 0.8
		self.defaultPose = "Stand"

		# Variables for the Markov Chain Transition Matrices
		self.currentStateWord = 0
		self.currentStateActionLeftArm = 0
		self.currentStateActionRightArm = 0
		self.currentStateInvite = 0
		self.currentStateLEDs = 0
		self.currentStateWalk = 0
		
		self.wordDictionary = {0 : 'ha',
								1 : "ha ha",
								2 : "he",
								3 : "he he",
								4 : "he he he",
								5 : "ho",
								6 : "ho ho",
								7 : "Fookin hell that tickles me!"
								}

		self.inviteToTickleDictionary = {0 : "Would you like to tickle me?",
										1 : "I bet you can't find my tickly spot!",
										2 : "Go on, tickle me!",
										3 : "Tickle Me NAO!"
										}

		self.RGBColourDictionary = {0 : [255, 0, 0], # red
									1 : [0, 255, 0], # green
									2 : [0, 0, 255], # blue
									3 : [255, 255, 0], # yellow
									4 : [255, 51, 153], # pink
									5 : [204, 0, 204], # purple
									6 : [255, 153, 51], # orange
									7 : [255, 255, 255], # white
									8 : [0, 0, 0], # black?
									9 : [0 ,204, 204] # aqua
									}

		# x, y, theta values for moveTo command.
		self.walkDictionary = {0 : [0.05, 0.05, 0],
								1 : [0.0, 0.0, 0.25],
								2 : [0.0, 0.0, 0.0],
								3 : [-0.05, -0.05, 0],
								4 : [0.0, 0.0, -0.25]
								}

		# Transition matrices in numpy format
		self.transitionMatrixAction = np.array([[0.25, 0.25, 0.25, 0.25],
										[0.25, 0.25, 0.25, 0.25],
										[0.25, 0.25, 0.25, 0.25],
										[0.25, 0.25, 0.25, 0.25]]
										)

		self.transitionMatrixInviteToTickle = np.array([[0.25, 0.25, 0.25, 0.25],
														[0.25, 0.25, 0.25, 0.25],
														[0.25, 0.25, 0.25, 0.25],
														[0.25, 0.25, 0.25, 0.25]]
														)

		self.transitionMatrixWord = np.array([[0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
											[0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
											[0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
											[0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
											[0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
											[0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
											[0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01],
											[0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01]]
											)

		self.transitionMatrixLEDs = np.array([[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
											[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
											[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
											[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
											[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
											[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
											[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
											[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
											[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
											[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]]
											)

		self.transitionMatrixWalk = np.array([[0.1, 0.1, 0.6, 0.1, 0.1],
											[0.1, 0.1, 0.6, 0.1, 0.1],
											[0.1, 0.1, 0.6, 0.1, 0.1],
											[0.1, 0.1, 0.6, 0.1, 0.1],
											[0.1, 0.1, 0.6, 0.1, 0.1]]
											)
		
		# Lists for large setup items e.g. subscribe, unsubscribe
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
			animateProxy = ALProxy("ALAnimatedSpeech")
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
			

		# Subscribe to the sensor events.
		# Initially passes name of method for callback, but maybe be multiple method names in future.
		self.easySubscribeEvents("tickled")

		# First, wake up.
		robotMotionProxy.wakeUp()
		
		# Go to default posture.
		bodyProxy.goToPosture(self.defaultPose, self.fractionMaxSpeed)

		# Invite to play the game:-)
		self.inviteToTickle()


		# ---------------- END __init__ ---------------------------


	def markovChoice(self, inMatrix):
		""" Chooses a value from a Markov transition matrix.

		"""
		randNum = np.random.random()
		cum = 0
		sumMatrix = np.sum(inMatrix)

		
		if not abs(sumMatrix - 1.0) < 1e-10:
			raise ValueError("Not a p array")
		else:
			for index, probability in enumerate(inMatrix):
				cum += probability
				if cum > randNum:
					return index

	def inviteToTickle(self):
		""" Say a random phrases to invite tickling. 

		"""
		self.currentStateInvite = self.markovChoice(self.transitionMatrixInviteToTickle[self.currentStateInvite])
		randomInviteToTicklePhrase = self.inviteToTickleDictionary[self.currentStateInvite]
		speechProxy.say(randomInviteToTicklePhrase)
		# Reset invite timer.
		self.inviteTimer = 0	

	def convertRGBToHex(self, list):
		""" Converts an input list of RGB values to hex, return the hex value.

		"""
		if len(list) == 3:
			hexColour = 256 * 256 * list[0] + 256 * list[1] + list[2]
		else:
			raise ValueError("Not a valid RGB list.")
		return hexColour


	def tickled(self):
		""" NAO does this when tickled.

		"""

		# Unsubscribe from all events to prevent other sensor events
		self.easyUnsubscribeEvents()

		# Speech parameters.
		wordPitch = 1.0
		laughPitch = 1.5
		normalPitch = 0
		doubleVoiceLaugh = 1.0
		doubleVoiceNormal = 0
		voice1 = "allison"
		voice2 = "audrey"
		# Define how many action elements will be actioned each 'tickle' action.
		# Add 1 so something always happens.
		numWordsPerTickle = int(np.random.random() * 5) + 1
		wordList1 = []

		# LED parameters
		LEDGroupName = 'AllLeds'
		LEDGroupDuration = 1.0
		numLEDChangesPerTickle = int(np.random.random() * 5) + 5
		LEDdurationList = [LEDGroupDuration] * numLEDChangesPerTickle
		RGBList = []

		# Walk parameters.
		walk1 = []
		walk2 = []

		# Execute Markov transition
		# Build word list, LED colour change list, and select body movements.
		# todo: is this the best place for the try? Primarily to catch exceptions from markovChoice()
		try:
			# Words.
			for i in range(numWordsPerTickle):
				self.currentStateWord = self.markovChoice(self.transitionMatrixWord[self.currentStateWord])
				try:
					wordList1.append(self.wordDictionary[self.currentStateWord])
				except Exception, e:
					print "Word dictionary exception: ", e
			# LED colour changes.		
			for i in range(numLEDChangesPerTickle):
				self.currentStateLEDs = self.markovChoice(self.transitionMatrixLEDs[self.currentStateLEDs])
				colour = self.RGBColourDictionary[self.currentStateLEDs]
				try:
					hexColour = self.convertRGBToHex(colour)
					RGBList.append(hexColour)
				except Exception, e:
					print "LED colour selection error: ", e
			# Set Markovian actions.
			self.currentStateActionLeftArm = self.markovChoice(self.transitionMatrixAction[self.currentStateActionLeftArm])
			self.currentStateActionRightArm = self.markovChoice(self.transitionMatrixAction[self.currentStateActionRightArm])
			self.currentStateWalk = self.markovChoice(self.transitionMatrixWalk[self.currentStateWalk])
		except ValueError, e:
			print "ValueError from markovChoice: ", e

		# Build action lists.
		# Voice output.
		tickleSentence = " ".join(wordList1)
		# Build motion.
		namesMotion = []
		# todo: replace time data with parametric values, or see ipnb for other ideas.
		timesMotion = []
		keysMotion = []
		movementList = []
		movementList = mtmd.leftArmMovementList[self.currentStateActionLeftArm] + mtmd.rightArmMovementList[self.currentStateActionRightArm]
		for n, t, k in movementList:
			namesMotion.append(n)
			timesMotion.append(t)
			keysMotion.append(k)
		# Build walk.
		walk1 = self.walkDictionary[self.currentStateWalk]
		# Creating a reverse move list to return NAO to start position'ish!
		walk2 = [i * -1 for i in walk1]
		print "walk1: ", walk1
		print "walk2: ", walk2

		# Say and do.
		speechProxy.setVoice(voice1)
		speechProxy.setParameter("pitchShift", laughPitch)
		speechProxy.setParameter("doubleVoiceLevel", doubleVoiceLaugh)
		try:
			x = walk1[0]
			y = walk1[1]
			theta = walk1[2]
			robotMotionProxy.moveTo(x, y, theta)
			robotMotionProxy.waitUntilMoveIsFinished()
		except Exception, e:
			print "robotMotionProxy error: ", e
		try:
			robotMotionProxy.post.angleInterpolation(namesMotion, keysMotion, timesMotion, True)
		except Exception, e:
			print "robotMotionProxy error: ", e
		try:
			LEDProxy.post.fadeListRGB(LEDGroupName, RGBList, LEDdurationList)			
		except Exception, e:
			print "LEDProxy error: ", e
		speechProxy.say(tickleSentence)
		# Return NAO to start position.
		try:
			x = walk2[0]
			y = walk2[1]
			theta = walk2[2]
			robotMotionProxy.moveTo(x, y, theta)
			robotMotionProxy.waitUntilMoveIsFinished()
		except Exception, e:
			print "robotMotionProxy error: ", e

		# Tidy up.		
		speechProxy.setParameter("pitchShift", normalPitch)
		speechProxy.setParameter("doubleVoiceLevel", doubleVoiceLaugh)
		# Return to default pose
		bodyProxy.goToPosture(self.defaultPose, self.fractionMaxSpeed)
		# Reset invite timer.
		self.inviteTimer = 0
		# Reset all LEDs to default.
		LEDProxy.reset(LEDGroupName)

		# Resubscribe to events.
		self.easySubscribeEvents("tickled")

		

	def mainTask(self):
		""" Temp main task.

		"""
		global myBroker

		try:
			while True:
				print ("Alive!"), self.inviteTimer
				time.sleep(1)
				# If time gone by invite someone to tickle!
				self.inviteTimer += 1
				if self.inviteTimer == 20:
					self.inviteToTickle()

		except KeyboardInterrupt:
			print "Interrupted by user, shutting down"
			self.easyUnsubscribeEvents()
			bodyProxy.goToPosture("Crouch", 0.8)
			robotMotionProxy.rest()
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
	global MarkovTickle
	MarkovTickle = MarkovTickleModule("MarkovTickle")

	print "Running, hit CTRL+C to stop script"
	MarkovTickle.mainTask()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print "Interrupted by user, shutting down"
		MarkovTickle.easyUnsubscribeEvents()
		MarkovTickle.bodyProxy.goToPosture("SitRelax", 0.8)
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
		

	









