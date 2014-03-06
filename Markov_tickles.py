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

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

NAO_IP = "mistcalf.local"

# Global variables to store module instances and proxies
MarkovTickle = None
memory = None
speechProxy = None
bodyProxy = None
leftArmProxy = None
rightArmProxy = None
robotMotionProxy = None



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
		global bodyProxy
		global leftArmProxy
		global rightArmProxy
		global robotMotionProxy

		# Variables for the Markov Chain Transition Matrices
		self.currentState = 0
		self.stateDictionary = {0 : 'stand still',
								1 : 'wave left arm',
								2 : 'wave right arm'
								}

		self.wordDictionary = {0 : 'hee',
								1 : "ha",
								2 : "ho",
								3 : "who",
								4 : "tee",
								5 : "ho ho",
								6 : "so, tickly!",
								7 : "no!",
								8 : "not there",
								9 : "sigh!"
								}

		# Transition matrices in numpy format
		self.transitionMatrixAction = np.array([[0.33, 0.33, 0.34],
										[0.2, 0.4, 0.4],
										[0.1, 0.1, 0.8]]
										)
		self.transitionMatrixWord = np.array([[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
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

		# # Check matrix test code.
		# sum = 0
		# for i, j in enumerate(self.transitionMatrixWord):
		# 	for k, l in enumerate(j):
		# 		print "i: %s, k: %s, l: %s" % (i, k, l)
		# 		sum += l
		# print "sum of matrix: %s" % sum
		
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

		# Subscribe to the sensor events.
		# Initially passes name of method for callback, but maybe be multiple method names in future.
		self.easySubscribeEvents("tickled")		

		# ---------------- END __init__ ---------------------------


	def markovChoice(self, inMatrix):
		""" Chooses a value from a Markov transition matrix.

		"""
		randNum = np.random.random()
		cum = 0
		
		if round(np.sum(inMatrix)) != 1:
			print "Not a P matrix"
			# todo: exception handling
		else:
			for index, probability in enumerate(inMatrix):
				cum += probability
				if cum > randNum:
					return index



	def tickled(self):
		""" NAO does this when tickled.

		"""
		self.easyUnsubscribeEvents()
		# Execute Markov transition
		# Define how many action elements will be actioned each 'tickle' action.
		numberElementsPerAction = int(np.random.random() * 10)
		print numberElementsPerAction
		sayPhrase1 = ""
		wordList1 = []
		for i in range(numberElementsPerAction):
			self.currentState = self.markovChoice(self.transitionMatrixWord[self.currentState])
			try:
				wordList1.append(self.wordDictionary[self.currentState])
			except Exception, e:
				print "Word dictionary exception: ", e
		# Repeat for second phrase.
		numberElementsPerAction = int(np.random.random() * 10)
		print numberElementsPerAction
		sayPhrase2 = ""
		wordList2 = []
		for i in range(numberElementsPerAction):
			self.currentState = self.markovChoice(self.transitionMatrixWord[self.currentState])
			try:
				wordList2.append(self.wordDictionary[self.currentState])
			except Exception, e:
				print "Word dictionary exception: ", e

		# Voice output
		sayPhrase1 = ".    ".join(wordList1)
		sayPhrase2 = ".    ".join(wordList2)
		wordPitch = 1.5
		laughPitch = 2.0
		normalPitch = 0

		speechProxy.setParameter("pitchShift", wordPitch)
		speechProxy.say("Hey, ")
		
		speechProxy.setParameter("pitchShift", laughPitch)
		speechProxy.say(sayPhrase1)
		
		speechProxy.setParameter("pitchShift", wordPitch)
		speechProxy.say("that")

		speechProxy.setParameter("pitchShift", laughPitch)
		speechProxy.say(sayPhrase2)

		speechProxy.setParameter("pitchShift", wordPitch)
		speechProxy.say("really tickles me!")

		
		speechProxy.setParameter("pitchShift", normalPitch)
				
		self.easySubscribeEvents("tickled")

	def mainTask(self):
		""" Temp main task.

		"""
		# Run forever
		while True:
			print ("Alive!")
			# lastState = numpy.random.choice(5, 3, p=[0.1, 0, 0.3, 0.6, 0])
			# print "lastState: %s" % lastState,
			time.sleep(1.0)

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
		MarkovTickle.bodyProxy("Crouch", 0.8)
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
		

	









