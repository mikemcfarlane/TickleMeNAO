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
from threading import Lock

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
		self.voice = "allison"

		# Variables for playing sound files.
		self.volume = 0.75
		self.pan = 0.0

		# Variables for the Markov Chain Transition Matrices
		self.currentStateWord = 0
		self.currentStateActionLeftArm = 0
		self.currentStateActionRightArm = 0
		self.currentStateInvite = 0
		self.currentStateLEDs = 0
		self.currentStateWalk = 0
		self.currentTickleTarget = 0
		self.currentStateTickleSuccessPre = 0
		self.currentStateTickleSuccessPost = 0
		self.currentStateTickleAgain = 0
		self.currentStateGameWinPraise = 0
		self.currentStateGameWinAnimation = 0
		self.currentStateGameLost = 0
		self.tickleCounter = 0
		self.gamecode = [0, 0, 0]
		self.yourGamecode = [0, 0, 0]
		self.yourGamecodeCounter = 0
		self.isASROn = False
		self.bIsRunning = False
		self.ids = []
		self.isWordRecognisedSubscribed = False
		self.bIntroIsRunning = False
		self.yourAnswer = ""

		# Variables for tickle game
		self.tickleTarget = ""

		# Thread locks/mutexes.
		self.eventLock = Lock()
		self.iAmBeingTickled = False
		
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
										2 : "Go on, try to tickle me!",
										3 : "Tickle Me NAO if you can!"
										}

		self.tickleSuccessPreDictionary = {0 : "Wow! My ",
											1 : "So tickly. My ",
											2 : "Phew! My ",
											3 : "My "
										}

		self.tickleSuccessPostDictionary = {0 : " is really tickly!",
											1 : " was tickled. You are tickle master!",
											2 : " is so ticklish!",
											3 : " , so ticklish! You tickle good!"
											}

		self.tickleAgainDictionary = {0 : " That was sort of ticklish. Can you find where I am very tickly?",
										1 : " You are going to have to try harder to tickle me!",
										2 : " Come on, really tickle me!",
										3 : " Try tickling somewhere else!"
										}

		self.gameWinPraiseDictionary = { 0 : "You are the tickle and memory master!",
										1 : "Yay, you tickle well and remember well.",
										2 : "You are a tickle fiend with a great memory."
										}

		self.gameWinAnimationDictionary = { 0 : "You have achieved tickle greatness", # Use with mystic.
											1 : "Tickle on great one", # Use with heavy metal.
											2 : "Listen to the crowd roar you are so great!" # Use with applause.
											}
		self.gameWinAnimationSoundsDictionary = { 	0 : "/home/nao/audio/mystic1.wav",
													1 : "/home/nao/audio/heavyMetal1.wav",
													2 : "/home/nao/audio/applause1.wav"
												}

		self.gameLostDictionary = { 0 : "That was the wrong code, or my microphones need cleaned out!",
									1 : "Sorry, incorrect code, or you need to speak more clearly.",
									2 : "Hmmm, that doesn't seem right."
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
		self.walkDictionary = {0 : [0.05, 0.05, 0], # forward and sidestep
								1 : [0.0, 0.0, 0.25],   # turn on spot
								2 : [0.0, 0.0, 0.0],    # do nothing
								3 : [-0.05, -0.05, 0],  # back and sidestep
								4 : [0.0, 0.0, -0.25]   # turn on spot
								}

		self.tickleTargetDictionary = {"RightBumperPressed" : "right foot",
										"LeftBumperPressed" : "left foot",
										"FrontTactilTouched" : "head top",
										"MiddleTactilTouched" : "head top",
										"RearTactilTouched" : "head top",
										"HandRightBackTouched" : "right hand",
										"HandRightLeftTouched" : "right hand",
										"HandRightRightTouched" : "right hand",
										"HandLeftBackTouched" : "left hand",
										"HandLeftLeftTouched" : "left hand",
										"HandLeftRightTouched" : "left hand"
										}


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

				
		# Transition matrices in numpy format
		self.transitionMatrixGameWinPraise = np.array([[0.33, 0.34, 0.33],
												[0.33, 0.34, 0.33],
												[0.33, 0.34, 0.33]]
												)

		self.transitionMatrixGameWinAnimation = np.array([[0.33, 0.34, 0.33],
												[0.33, 0.34, 0.33],
												[0.33, 0.34, 0.33]]
												)

		self.transitionMatrixGameLost = np.array([[0.33, 0.34, 0.33],
												[0.33, 0.34, 0.33],
												[0.33, 0.34, 0.33]]
												)

		self.transitionMatrixAction = np.array([[0.25, 0.25, 0.25, 0.25],
												[0.25, 0.25, 0.25, 0.25],
												[0.25, 0.25, 0.25, 0.25],
												[0.25, 0.25, 0.25, 0.25]]
												)

		self.transitionMatrixTickleSuccessPre = np.array([[0.25, 0.25, 0.25, 0.25],
															[0.25, 0.25, 0.25, 0.25],
															[0.25, 0.25, 0.25, 0.25],
															[0.25, 0.25, 0.25, 0.25]]
														)

		self.transitionMatrixTickleSuccessPost = np.array([[0.25, 0.25, 0.25, 0.25],
										[0.25, 0.25, 0.25, 0.25],
										[0.25, 0.25, 0.25, 0.25],
										[0.25, 0.25, 0.25, 0.25]]
										)

		self.transitionMatrixTickleAgain = np.array([[0.25, 0.25, 0.25, 0.25],
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

		self.transitionMatrixTickleTarget = np.array([
													[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0],
													[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0],
													[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0],
													[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0],
													[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0],
													[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0],
													[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0],
													[0.2, 0.2, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0]
													])
		
		
		
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

	def generateGameCode(self):
		""" Generates a three digit game code.

		"""
		self.gamecode = [0, 0, 0]
		for i in range(3):
			# Generate random number, change from float to int, then to str as needs to match WordRecognised event.
			randNum = str(int(np.random.random() * 9))
			self.gamecode[i] = randNum
		print "Your new gamecode: ", self.gamecode

	def batteryChange(self):
		print "Charging plug status changed."
		animatedSpeechProxy.say("Hey, what happened to my power!", self.bodyLanguageModeConfig)

	def pickTickleTarget(self):
		""" Pick a body area to be the target of tickling.

		"""
		sizeOfBodyList = len(self.subscriptionList)
		randomIndex = int(np.random.random() * sizeOfBodyList)
		tickleTargetDictionaryKey = self.subscriptionList[randomIndex]
		# Tickle target is set to a value from tickleTargetDictionary rather than event names as:
		# 1. Need to group some sensors together as they are not always reliable e.g. hands.
		# 2. Need to group some sensors together for better gameplay e.g. head, no point in having seperate tickle spots.
		# 3. Also allows a sensible value to used in speech.
		self.tickleTarget = self.tickleTargetDictionary[tickleTargetDictionaryKey]
		print "tickleTarget: ", self.tickleTarget


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
		if not self.isASROn and not self.bIsRunning:
			self.currentStateInvite = self.markovChoice(self.transitionMatrixInviteToTickle[self.currentStateInvite])
			randomInviteToTicklePhrase = self.inviteToTickleDictionary[self.currentStateInvite]
			id = animatedSpeechProxy.post.say(randomInviteToTicklePhrase, self.bodyLanguageModeConfig)
			animatedSpeechProxy.wait(id, 0)
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


	def tickled(self, laughPitch = 1.5, numWordsPerTickleConstant = 5, LEDGroupDuration = 1.0, motionEnabled = True):
		""" NAO does this when tickled.
			Arguments and defaults:
			laughPitch = 1.5, 
			numWordsPerTickleConstant = 5, 
			LEDGroupDuration = 1.0, 
			motionEnabled = True

		"""
		
		# Speech parameters.
		wordPitch = 1.0
		# laughPitch = 1.5
		normalPitch = 0
		doubleVoiceLaugh = 1.0
		doubleVoiceNormal = 0
		
		# Define how many action elements will be actioned each 'tickle' action.
		# Add 1 so something always happens.
		numWordsPerTickle = int(np.random.random() * numWordsPerTickleConstant) + 3
		wordList1 = []

		# LED parameters
		LEDGroupName = 'AllLeds'
		# LEDGroupDuration = 1.0
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
			if motionEnabled:
				""" Only does this when the target tickle area is tickled."""
				self.currentStateActionLeftArm = self.markovChoice(self.transitionMatrixAction[self.currentStateActionLeftArm])
				self.currentStateActionRightArm = self.markovChoice(self.transitionMatrixAction[self.currentStateActionRightArm])
				self.currentStateWalk = self.markovChoice(self.transitionMatrixWalk[self.currentStateWalk])
		except ValueError, e:
			print "ValueError from markovChoice: ", e

		# Build action lists.
		# Voice output.
		tickleSentence = " ".join(wordList1)
		if motionEnabled:
			""" Only does this when the target tickle area is tickled."""
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

		# Say and do.
		speechProxy.setParameter("pitchShift", laughPitch)
		speechProxy.setParameter("doubleVoiceLevel", doubleVoiceLaugh)
		if motionEnabled:
			""" Only does this when the target tickle area is tickled."""
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
		animatedSpeechProxy.say(tickleSentence, self.bodyLanguageModeConfig)
		# Return NAO to start position.
		if motionEnabled:
			""" Only does this when the target tickle area is tickled."""
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
		#bodyProxy.goToPosture(self.defaultPose, self.fractionMaxSpeed)
		# Reset invite timer.
		self.inviteTimer = 0
		# Reset all LEDs to default.
		LEDProxy.reset(LEDGroupName)

	
	def startSpeechRecognition(self):
		""" Setup and start speech recognition. 

		"""
		if not self.isASROn:
			asrProxy.setLanguage("English")
			vocabulary = ["0" , "1", "2", "3", "4", "5", "6", "7", "8", "9"]
				   
			try:
				asrProxy.setVocabulary(vocabulary, False)
			except Exception, e:
				print " asr set vocab error ", e
			try:
				asrProxy.setParameter("NbHypotheses", 2)
			except Exception, e:
				print "asr set parameter error ", e
			# try:
			#     print asrProxy.getParameter("NbHypotheses")
			# except Exception, e:
			#     print "asr can not get parameter ", e
			try:
				asrProxy.subscribe("ASR")
			except Exception, e:
				print "asr can not subscribe ", e
			self.isASROn = True
		else:
			pass
		# Lastly subscribe to wordrecognized.
		self.subscribeToWord()

	def subscribeToWord(self):
		""" Subscribe to WordRecognized.

		"""
		if not self.isWordRecognisedSubscribed:
			try:
				memory.subscribeToEvent("WordRecognized",self.getName(),"codeRecognized")
			except Exception, e:
				print "memory can not subscribe to wordrecognized ", e
			self.isWordRecognisedSubscribed = True
		else:
			pass

	def stopSpeechRecognition(self):
		""" Stop speech recognition.

		"""
		if self.isASROn:
			try:
				asrProxy.unsubscribe("ASR")
			except Exception, e:
				print "Exception stopping speech recognition, error: ", e
			self.isASROn = False
		else:
			pass
		# Lastly unsubscribe from WordRecognized.
		self.unSubscribeToWord()


	def unSubscribeToWord(self):
		""" Unsubscribe from WordRecognized.

		"""
		if self.isWordRecognisedSubscribed:
			try:
				memory.unsubscribeToEvent("WordRecognized", self.getName())
			except Exception, e:
				print "Could not unsubscribe from WordRecognized, error: ", e
			self.isWordRecognisedSubscribed = False
		else:
			pass


	def startSpeechRecognition2(self):
		""" Setup and start speech recognition. 

		"""
		if not self.isASROn:
			asrProxy.setLanguage("English")
			vocabulary = ["yes", "no"]
				   
			try:
				asrProxy.setVocabulary(vocabulary, False)
			except Exception, e:
				print " asr set vocab error ", e
			try:
				asrProxy.setParameter("NbHypotheses", 2)
			except Exception, e:
				print "asr set parameter error ", e
			# try:
			#     print asrProxy.getParameter("NbHypotheses")
			# except Exception, e:
			#     print "asr can not get parameter ", e
			try:
				asrProxy.subscribe("ASR")
			except Exception, e:
				print "asr can not subscribe ", e
			self.isASROn = True
		else:
			pass
		# Lastly subscribe to wordrecognized.
		self.subscribeToWord2()

	def subscribeToWord2(self):
		""" Subscribe to WordRecognized.

		"""
		if not self.isWordRecognisedSubscribed:
			try:
				memory.subscribeToEvent("WordRecognized",self.getName(),"answerRecognized")
			except Exception, e:
				print "memory can not subscribe to wordrecognized ", e
			self.isWordRecognisedSubscribed = True
		else:
			pass

	def stopSpeechRecognition2(self):
		""" Stop speech recognition.

		"""
		if self.isASROn:
			try:
				asrProxy.unsubscribe("ASR")
			except Exception, e:
				print "Exception stopping speech recognition, error: ", e
			self.isASROn = False
		else:
			pass
		# Lastly unsubscribe from WordRecognized.
		self.unSubscribeToWord2()


	def unSubscribeToWord2(self):
		""" Unsubscribe from WordRecognized.

		"""
		if self.isWordRecognisedSubscribed:
			try:
				memory.unsubscribeToEvent("WordRecognized", self.getName())
			except Exception, e:
				print "Could not unsubscribe from WordRecognized, error: ", e
			self.isWordRecognisedSubscribed = False
		else:
			pass

	def answerRecognized(self):
		""" NAO does this when he recognises the word.

		"""
		self.bIsRunning = True

		try:
			self.unSubscribeToWord2()
			# get WordRecognized
			youSaid = memory.getData("WordRecognized")
			# tell the human some stuff
			wordSaid = youSaid[0]
			wordSaidProbability = youSaid[1]
			tellMeWordSaid = "You said " + wordSaid
			id = animatedSpeechProxy.post.say(tellMeWordSaid, self.bodyLanguageModeConfig)
			animatedSpeechProxy.wait(id, 0)
			if wordSaidProbability <= 0.4:
				id = animatedSpeechProxy.post.say("But you mumbled a bit!", self.bodyLanguageModeConfig)
				animatedSpeechProxy.wait(id, 0)
			self.yourAnswer = wordSaid
			# wait a bit to avoid robot speech triggering WordRecognized event
			time.sleep(2)
			# Check if ASR still on ie not been turned off by gameManagement()
			if self.isASROn:
				self.subscribeToWord2()

		finally:
			if self.ids == []:
				self.bIsRunning = False
				self.bIntroIsRunning = False


	def codeRecognized(self, key, value, message):
		""" NAO does this when he recognizes the code number.

		"""
		self.bIsRunning = True

		try:
			self.unSubscribeToWord()
			# get WordRecognized
			youSaid = memory.getData("WordRecognized")
			# tell the human some stuff
			wordSaid = youSaid[0]
			wordSaidProbability = youSaid[1]
			tellMeWordSaid = "You said " + wordSaid
			id = animatedSpeechProxy.post.say(tellMeWordSaid, self.bodyLanguageModeConfig)
			animatedSpeechProxy.wait(id, 0)
			if wordSaidProbability <= 0.4:
				id = animatedSpeechProxy.post.say("But you mumbled a bit!", self.bodyLanguageModeConfig)
				animatedSpeechProxy.wait(id, 0)
			self.yourGamecode[self.yourGamecodeCounter] = wordSaid
			self.yourGamecodeCounter += 1
			print "yourGamecodeCounter: ", self.yourGamecodeCounter  
			# wait a bit to avoid robot speech triggering WordRecognized event
			time.sleep(2)
			# Check if ASR still on ie not been turned off by gameManagement()
			if self.isASROn:
				self.subscribeToWord()

		finally:
			if self.ids == []:
				self.bIsRunning = False

	def gameWinAnimation(self):
		""" NAO performs an animation and a speech when the gameplayer gets the code correct.

		"""
		try:
			self.currentStateGameWinPraise = self.markovChoice(self.transitionMatrixGameWinPraise[self.currentStateGameWinPraise])
		except ValueError, e:
			print "ValueError from markovChoice: ", e
		
		sayPhrase1 = self.gameWinPraiseDictionary[self.currentStateGameWinPraise]

		try:
			self.currentStateGameWinAnimation = self.markovChoice(self.transitionMatrixGameWinAnimation[self.currentStateGameWinAnimation])
		except ValueError, e:
			print "ValueError from markovChoice: ", e

		soundFile = self.gameWinAnimationSoundsDictionary[self.currentStateGameWinAnimation]
		sayPhrase2 = self.gameWinAnimationDictionary[self.currentStateGameWinAnimation]

		# Build motion.
		namesMotion = []
		# todo: replace time data with parametric values, or see ipnb for other ideas.
		timesMotion = []
		keysMotion = []
		movementList = []
		movementList = mtmd.successList[self.currentStateGameWinAnimation]
		for n, t, k in movementList:
			namesMotion.append(n)
			timesMotion.append(t)
			keysMotion.append(k)
		
		self.bIsRunning = True
		try:
			id = animatedSpeechProxy.post.say(sayPhrase1, self.bodyLanguageModeConfig)
			self.ids.append(id)
			animatedSpeechProxy.wait(id, 0)

			id1 = aupProxy.post.playFile(soundFile, self.volume, self.pan)
			self.ids.append(id1)

			id2 = robotMotionProxy.post.angleInterpolationBezier(namesMotion, timesMotion, keysMotion)
			self.ids.append(id2)			
			robotMotionProxy.wait(id2, 0)

			id3 = animatedSpeechProxy.post.say(sayPhrase2, self.bodyLanguageModeConfig)
			self.ids.append(id3)
			animatedSpeechProxy.wait(id3, 0)
		finally:
			try:
				self.ids.remove(id)
				self.ids.remove(id1)
				self.ids.remove(id2)
				self.ids.remove(id3)
			except:
				pass
			if self.ids == []:
				self.bIsRunning = False
		
	def gameLost(self):
		""" NAO does a speech if player gets the code wrong.

		"""
		try:
			self.currentStateGameLost = self.markovChoice(self.transitionMatrixGameLost[self.currentStateGameLost])
		except ValueError, e:
			print "ValueError from markovChoice: ", e

		sayPhrase = self.gameLostDictionary[self.currentStateGameLost]

		id = animatedSpeechProxy.post.say(sayPhrase, self.bodyLanguageModeConfig)
		animatedSpeechProxy.wait(id, 0)


	def gameManagement(self):
		""" This manages the tickle game.

		"""
		sayPhrase = "Remember your code, " + str(self.gamecode[self.tickleCounter])
		id = animatedSpeechProxy.post.say(sayPhrase, self.bodyLanguageModeConfig)
		animatedSpeechProxy.wait(id, 0)

		self.tickleCounter += 1
		if self.tickleCounter >= 3:
			id = animatedSpeechProxy.post.say("Wow, you are the tickle master. Can you remember the three number code I gave you? Tell me one number at a time.", self.bodyLanguageModeConfig)
			animatedSpeechProxy.wait(id, 0)
			self.startSpeechRecognition()
			while self.yourGamecodeCounter <= 2:
				time.sleep(0.5)
			self.stopSpeechRecognition()
			print "Your gamecode: ", self.yourGamecode
			if self.gamecode == self.yourGamecode:
				# You are a winner!
				self.gameWinAnimation()
			else:
				self.gameLost()         
			self.generateGameCode()
			self.tickleCounter = 0
			self.yourGamecodeCounter = 0
			# self.inviteToTickle()
				

	def touched(self, key, value, message):
		""" NAO does this when tickled.
			key = calling event
			value = value from event

		"""
		if not self.iAmBeingTickled:
			self.iAmBeingTickled = True
			self.easyUnsubscribeEvents()
			
			# Was the target area tickled?
			sensorGroupTouched = self.tickleTargetDictionary[key]
			if sensorGroupTouched == self.tickleTarget:
				self.tickled(1.5, 10, 1.0, True)
				self.currentStateTickleSuccessPre = self.markovChoice(self.transitionMatrixTickleSuccessPre[self.currentStateTickleSuccessPre])
				self.currentStateTickleSuccessPost = self.markovChoice(self.transitionMatrixTickleSuccessPost[self.currentStateTickleSuccessPost])
				prePhrase = self.tickleSuccessPreDictionary[self.currentStateTickleSuccessPost]
				postPhrase = self.tickleSuccessPostDictionary[self.currentStateTickleSuccessPost]
				sayPhrase = prePhrase + sensorGroupTouched + postPhrase
				id = animatedSpeechProxy.post.say(sayPhrase, self.bodyLanguageModeConfig)
				animatedSpeechProxy.wait(id, 0)
				# Chose a new area to tickle if target tickly area was tickled.
				self.pickTickleTarget()
				# Check game.
				self.gameManagement()
				self.inviteToTickle()	


			else:
				self.tickled(1.25, 5, 0.5, False)
				self.currentStateTickleAgain = self.markovChoice(self.transitionMatrixTickleAgain[self.currentStateTickleAgain])
				sayPhrase = "You touched my " + sensorGroupTouched + self.tickleAgainDictionary[self.currentStateTickleAgain]
				id = animatedSpeechProxy.post.say(sayPhrase, self.bodyLanguageModeConfig)
				animatedSpeechProxy.wait(id, 0)
			
			# Resubscribe to events.
			self.easySubscribeEvents("touched")
			self.iAmBeingTickled = False


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

	def shutdown(self):
		""" We are done!

		"""
		while self.iAmBeingTickled:
			time.sleep(0.5)
		id = animatedSpeechProxy.post.say("ok, let's stop tickling!")
		animatedSpeechProxy.wait(id, 0)
		self.easyUnsubscribeEvents()
		self.stopSpeechRecognition()
		bodyProxy.goToPosture("Crouch", 0.6)
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

	def doIntroduction(self):
		""" NAO does an introduction to the app and asks person if they want instructions.

		"""
		sayPhrase = "Hi, this is Tickle Me NAO, do you want to hear instructions?"
		id = animatedSpeechProxy.post.say(sayPhrase, self.bodyLanguageModeConfig)
		animatedSpeechProxy.wait(id, 0)
		self.bIntroIsRunning = True
		self.startSpeechRecognition2()
		while self.bIntroIsRunning:
			time.sleep(1.0)
		self.stopSpeechRecognition2()
		if self.yourAnswer == "yes":
			sayPhrase = "You have to find my tickly spot. It might be my head top, my hands, or the front of my feet. The tickly spot will change through the game. If you find my tickly spot I will give you a code number. Remember the code number I give you, when you tickle me three times I will ask for the code. One number at a time. If you get it right I will do something fun just for you. To stop the game hold both my hands in yours."
			id = animatedSpeechProxy.post.say(sayPhrase, self.bodyLanguageModeConfig)
			animatedSpeechProxy.wait(id, 0)
		else:
			sayPhrase = "ok, let's tickle!"
			id = animatedSpeechProxy.post.say(sayPhrase, self.bodyLanguageModeConfig)
			animatedSpeechProxy.wait(id, 0)


	def mainTask(self):
		""" Temp main task.

		"""

		try:
			# Subscribe to the sensor events.
			self.easySubscribeEvents("touched")

			# Set voice character.
			speechProxy.setVoice(self.voice)
			speechProxy.setVolume(self.speechVolume)
			# At 1.22.3 voice speed setting is only avaiable in Japanese.
			# speechProxy.setParameter("speed", 4.0)

			# Pick an initial tickle target.
			self.pickTickleTarget()

			# Pick an initial game code.
			self.generateGameCode()

			# First, wake up.
			robotMotionProxy.wakeUp()
			
			# Go to default posture.
			bodyProxy.goToPosture(self.defaultPose, self.fractionMaxSpeed)

			self.doIntroduction()

			# Invite to play the game:-)
			self.inviteToTickle()

			while (not memory.getData("rightHandFlag")) or (not memory.getData("leftHandFlag")):
				print "Alive! {}".format(self.inviteTimer)
				time.sleep(1)
				# If time gone by invite someone to tickle!
				self.inviteTimer += 1
				if self.inviteTimer >= 20:
					self.inviteToTickle()

			self.shutdown()


		except KeyboardInterrupt:
			print "Interrupted by user, shutting down"
			self.shutdown()
			

class MarkovTickleStopModule(ALModule):
	""" Simple module for moitoring the hand sensors and stopping NAO via an ALMemory flag. 

	"""

	def __init__(self, name):
		""" Initialise module. 

		"""
		ALModule.__init__(self, name)

		# Globals for proxies.
		global memoryStop

		try:
			memoryStop = ALProxy("ALMemory")
		except Exception, e:
			print "Could not create proxy to ALMemory. Error: ", e

		memoryStop.insertData("rightHandFlag", False)
		memoryStop.insertData("leftHandFlag", False)

		self.subscriptionStopList = [
									"HandRightBackTouched",
									"HandRightLeftTouched",
									"HandRightRightTouched",
									"HandLeftBackTouched",
									"HandLeftLeftTouched",
									"HandLeftRightTouched"
									]

		self.subscribeEventsForStop("both")

	def subscribeEventsForStop(self, robotSide = "both"):
		""" Subscribes to hand touch events. If both hands are touched then stop.

		"""
		for eventName in self.subscriptionStopList:
			try:
				if robotSide == "right": 
					if "HandRight" in eventName:
						memoryStop.subscribeToEvent(eventName, self.getName(), "setRightHandFlag")
				elif robotSide == "left":
					if "HandLeft" in eventName:
						memoryStop.subscribeToEvent(eventName, self.getName(), "setLeftHandFlag")
				elif robotSide == "both":
					# Subscribe for both sides of robot as appropriate.
					if "HandRight" in eventName:
						memoryStop.subscribeToEvent(eventName, self.getName(), "setRightHandFlag")
					elif "HandLeft" in eventName:
						memoryStop.subscribeToEvent(eventName, self.getName(), "setLeftHandFlag")
					else:
						print "Oops, nothing subscribed!"
				else:
					print "Incorrect argument in subscribe."
			except Exception, e:
				print "Subscribe exception error %s for %s." % (e, eventName)

	def unSubscribeEventsForStop(self, robotSide = "both"):
		""" Unsubscribes from hand touch events for stop.

		"""
		for eventName in self.subscriptionStopList:
			try:
				if robotSide == "right": 
					if "HandRight" in eventName:
						memoryStop.unsubscribeToEvent(eventName, self.getName())
				elif robotSide == "left":
					if "HandLeft" in eventName:
						memoryStop.unsubscribeToEvent(eventName, self.getName())
				elif robotSide == "both":
					# Unsubscribe for both sides of robot as appropriate.
					if "HandRight" in eventName:
						memoryStop.unsubscribeToEvent(eventName, self.getName())
					elif "HandLeft" in eventName:
						memoryStop.unsubscribeToEvent(eventName, self.getName())
					else:
						print "Oops, nothing unsubscribed!"
				else:
					print "Incorrect argument in unsubscribe."
			except Exception, e:
				print "Subscribe exception error %s for %s." % (e, eventName)


	def setRightHandFlag(self, key, value, msg):
		""" Sets a right hand touched flag for stop.

		"""
		if not memoryStop.getData("rightHandFlag"):
			try:
				self.unSubscribeEventsForStop("right")
				print(" --------------- right hand touched --------------")
				memoryStop.insertData("rightHandFlag", True)
				time.sleep(1.0)
				self.subscribeEventsForStop("right")
			except:
				pass
			finally:
				memoryStop.insertData("rightHandFlag", False)
			

	def setLeftHandFlag(self, key, value, msg):
		""" Sets a left hand touched flag for stop.

		"""
		if not memoryStop.getData("leftHandFlag"):
			try:
				self.unSubscribeEventsForStop("left")
				print(" --------------- left hand touched --------------")
				memoryStop.insertData("leftHandFlag", True)
				time.sleep(1.0)
				self.subscribeEventsForStop("left")
			except:
				pass
			finally:
				memoryStop.insertData("leftHandFlag", False)

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
	MarkovTickleStop = MarkovTickleStopModule("MarkovTickleStop")

	print "Running, hit CTRL+C to stop script"
	MarkovTickle.mainTask()
	

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print "Interrupted by user, shutting down"
		MarkovTickle.easyUnsubscribeEvents()
		MarkovTickle.stopSpeechRecognition()
		MarkovTickle.bodyProxy.goToPosture("SitRelax", 0.6)
		MarkovTickle.robotMotionProxy.rest()
		MarkovTickle.stopSpeechRecognition()
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
		

	









