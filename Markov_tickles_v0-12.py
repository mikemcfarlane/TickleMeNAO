# DESCRIPTION:
# Attempts to generate a realistic response for NAO to being tickled by using Markov Chains.
# PROGRAMMER: 
# Mike McFarlane
# VERSION HISTORY (version, date, description):
# 0.1,18/10/2013, basic code structure outlined in comments, and some matrices and methods set up. Working.
# 0.11, 29/10/2013, start to build up modification of matrices and matrix state selection. Working - matrices blended over time
# and cycles, copied to robotMatrixCurrentList, data verified for target sensor states, and if sensor touched again.
# 0.12, 21/11/2013, add in all sensors to generate new current matrices
# 0.13, ?, add random number generator and transition selection
# USAGE: 
# Add to Choregraph script box.
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

from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
	""" Simple module for tickling NAO. """

	def __init__(self):
		GeneratedClass.__init__(self)

		# Set initial current states for Markov matrices
		self.bodyMovementState = 0
		self.leftArmMovementState = 0
		self.rightArmMovementState = 0
		self.headMovementState = 0
		self.robotMotionState = 0
		self.speechState = 0
		self.speechModifierState = 0
		# This is the flag that will be set from the tickle manager, prob as global variable or memory key
		# From Thomas's code, called g_target_sensor:
		# Sensors assignation
		# 1 : Head - front
		# 2 : Head - middle
		# 3 : Head - back
		# 4 : Chest
		# 5 : left hand - upper
		# 6 : left hand - middle
		# 7 : left hand - lower
		# 8 : right hand - upper
		# 9 : right hand - middle
		# 10 : right hand - lower
		# 11 : left foot
		# 12 : right foot
		# Due to the lack of response in the hand sensors, propose combine them, with numbering as follows,
		# 1 : Head - front
		# 2 : Head - middle
		# 3 : Head - back
		# 4 : Chest
		# 5 : left hand - upper
		# 5 : left hand - middle
		# 5 : left hand - lower
		# 8 : right hand - upper
		# 8 : right hand - middle
		# 8 : right hand - lower
		# 11 : left foot
		# 12 : right foot
		


		########################################################
		## SET TARGET SENSOR HERE IN PLACE OF TICKLE MANAGER ###
		########################################################
		self.g_target_sensor = 5

		# Flag/mutex to stop current matrices being modified by other processes
		# 0 = not being tickled, 1 = being tickled
		self.lockCurrentMatrices = 0

	def rightBumperTouched(self, *_args):
		""" Right bumper touched. """
		self.memory.unsubscribeToEvent("RightBumperPressed",self.getName())
		self.speechProxy.say("You touched my right foot")
		self.log("You touched my right foot")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 12
		self.beingTickled(sensorTriggered)
		self.memory.subscribeToEvent("RightBumperPressed",self.getName(),"rightBumperTouched")

	def leftBumperTouched(self, *_args):
		""" Left bumper touched. """
		self.memory.unsubscribeToEvent("LeftBumperPressed",self.getName())
		self.speechProxy.say("You touched my left foot")
		self.log("You touched my left foot")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 11
		self.beingTickled(sensorTriggered)
		self.memory.subscribeToEvent("LeftBumperPressed",self.getName(),"leftBumperTouched")
	
	def frontSensorTouched(self, *_args):
		""" Front sensor touched. """
		self.memory.unsubscribeToEvent("FrontTactilTouched",self.getName())
		self.speechProxy.say("You touched the front of my head")
		self.log("You touched the front of my head")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 1
		self.beingTickled(sensorTriggered)
		self.memory.subscribeToEvent("FrontTactilTouched",self.getName(),"frontSensorTouched")

	def middleSensorTouched(self, *_args):
		""" Middle sensor touched. """
		self.memory.unsubscribeToEvent("MiddleTactilTouched",self.getName())
		self.speechProxy.say("You touched the top of my head")
		self.log("You touched the top of my head")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 2
		self.beingTickled(sensorTriggered)
		self.memory.subscribeToEvent("MiddleTactilTouched",self.getName(),"middleSensorTouched")

	def rearSensorTouched(self, *_args):
		""" Rear sensor touched. """
		self.memory.unsubscribeToEvent("RearTactilTouched",self.getName())
		self.speechProxy.say("You touched the back of my head")
		self.log("You touched the back of my head")
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 3
		self.beingTickled(sensorTriggered)
		self.memory.subscribeToEvent("RearTactilTouched",self.getName(),"rearSensorTouched")

	def rightHandTouched(self, *_args):
		""" Any right hand sensor touched. """
		self.memory.unsubscribeToEvent("HandRightBackTouched",self.getName())
		self.memory.unsubscribeToEvent("HandRightLeftTouched",self.getName())
		self.memory.unsubscribeToEvent("HandRightRightTouched",self.getName())
		self.speechProxy.say("You touched my right hand")
		self.log("You touched my right hand")
		self.rightHandActivated = 1
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 8
		self.beingTickled(sensorTriggered)
		self.rightHandActivated = 0
		self.memory.subscribeToEvent("HandRightBackTouched",self.getName(),"rightHandTouched")
		self.memory.subscribeToEvent("HandRightLeftTouched",self.getName(),"rightHandTouched")
		self.memory.subscribeToEvent("HandRightRightTouched",self.getName(),"rightHandTouched")        

	def leftHandTouched(self, *_args):
		""" Any left hand sensor touched. """
		self.memory.unsubscribeToEvent("HandLeftBackTouched",self.getName())
		self.memory.unsubscribeToEvent("HandLeftLeftTouched",self.getName())
		self.memory.unsubscribeToEvent("HandLeftRightTouched",self.getName())
		self.speechProxy.say("You touched my left hand")
		self.log("You touched my left hand")
		self.leftHandActivated = 1
		# call the being tickled function and pass the number of the sensor being tickled
		sensorTriggered = 5
		self.beingTickled(sensorTriggered)
		self.leftHandActivated = 0
		self.memory.subscribeToEvent("HandLeftBackTouched",self.getName(),"leftHandTouched")
		self.memory.subscribeToEvent("HandLeftLeftTouched",self.getName(),"leftHandTouched")
		self.memory.subscribeToEvent("HandLeftRightTouched",self.getName(),"leftHandTouched")

	def beingTickled(self, sensorTriggered):
		""" If a sensor touched, this is being tickled. """
				
		# Lock the current matrices to give this method ownership of the robots actions
		self.lockCurrentMatrices = 1

		self.speechProxy.say("I'm acting ticklish now, honest!")
		
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
		self.speechProxy.say("Oyy e! I hope you are done making me recite dumb stuff!")
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
			
			

	def stopMe(self):
		""" Exit cleanly. """
		# un-subscribe to the sensor events:
		try:
			self.memory.unsubscribeToEvent("RightBumperPressed",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)
		try:	
			self.memory.unsubscribeToEvent("LeftBumperPressed",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)
		try:	
			self.memory.unsubscribeToEvent("FrontTactilTouched",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)
		try:	
			self.memory.unsubscribeToEvent("MiddleTactilTouched",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)	
		try:	
			self.memory.unsubscribeToEvent("RearTactilTouched",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)
		try:	
			self.memory.unsubscribeToEvent("HandRightBackTouched",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)
		try:	
			self.memory.unsubscribeToEvent("HandRightLeftTouched",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)	
		try:	
			self.memory.unsubscribeToEvent("HandRightRightTouched",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)	
		try:
			self.memory.unsubscribeToEvent("HandLeftBackTouched",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)	
		try:	
			self.memory.unsubscribeToEvent("HandLeftLeftTouched",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)
		try:	
			self.memory.unsubscribeToEvent("HandLeftRightTouched",self.getName())
		except Exception, e:
			errorString = "Error was: " + str(e)
			self.log(errorString)

		# stop any post tasks
		# eg void ALModule::stop(const int& id)

		# reset any flags
		self.rightHandActivated = 0
		self.rightHandActivated = 0


	def onLoad(self):
		#~ puts code for box initialization here
		pass

	def onUnload(self):
		#~ puts code for box cleanup here
		pass

	def onInput_onStart(self):
		""" Stuff to do when module starts. """
		# Setup proxies
		try:
			self.bodyProxy = ALProxy("ALRobotPosture")
		except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e
		try:
			self.leftArmProxy = ALProxy("ALRobotPosture")
		except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e
		try:
			self.rightArmProxy = ALProxy("ALRobotPosture")
		except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e
		try:
			self.headProxy = ALProxy("ALRobotPosture")
		except Exception, e:
			print "Could not create proxy to ALRobotPosture"
			print "Error was: ", e
		try:
			self.robotMotionProxy = ALProxy("ALMotion")
		except Exception, e:
			print "Could not create proxy to ALMotion"
			print "Error was: ", e
		try:
			self.speechProxy = ALProxy("ALTextToSpeech")
		except Exception, e:
			print "Could not create proxy to ALTextToSpeech"
			print "Error was: ", e
		try:
			self.memory = ALProxy("ALMemory")
		except Exception, e:
			print "Could not create proxy to ALMemory"
			print "Error was: ", e

		# Subscribe to the sensor events:
		self.memory.subscribeToEvent("RightBumperPressed",self.getName(),"rightBumperTouched")
		self.memory.subscribeToEvent("LeftBumperPressed",self.getName(),"leftBumperTouched")
		self.memory.subscribeToEvent("FrontTactilTouched",self.getName(),"frontSensorTouched")
		self.memory.subscribeToEvent("MiddleTactilTouched",self.getName(),"middleSensorTouched")
		self.memory.subscribeToEvent("RearTactilTouched",self.getName(),"rearSensorTouched")
		self.memory.subscribeToEvent("HandRightBackTouched",self.getName(),"rightHandTouched")
		self.memory.subscribeToEvent("HandRightLeftTouched",self.getName(),"rightHandTouched")
		self.memory.subscribeToEvent("HandRightRightTouched",self.getName(),"rightHandTouched")
		self.memory.subscribeToEvent("HandLeftBackTouched",self.getName(),"leftHandTouched")
		self.memory.subscribeToEvent("HandLeftLeftTouched",self.getName(),"leftHandTouched")
		self.memory.subscribeToEvent("HandLeftRightTouched",self.getName(),"leftHandTouched")

		# to stop the behaviour hold both hands at the same time
		self.rightHandActivated = 0
		self.rightHandActivated = 0		

		# Declare generalised transition matrices for each type of state.

		# Current matrices that will be used by main loop 
		# Body movement array - [still, straight, bent forward, back arched]
		self.bodyMovementMatrixInitial = [
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0]
		]
		# Left arm movement array - [still, shake at side, wave]
		self.leftArmMovementMatrixInitial = [
									[1, 0, 0], 
									[1, 0, 0], 
									[1, 0, 0]
		]
		# Right arm movement array - [still, shake at side, wave]
		self.rightArmMovementMatrixInitial = [
									[1, 0, 0], 
									[1, 0, 0], 
									[1, 0, 0]
		]
		# Head movement array - [still, straight up, bent forward, bent back]
		self.headMovementMatrixInitial = [
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0]
		]
		# Robot motion array - [stationary, walk forward, walk backward]
		self.robotMotionMatrixInitial = [
								[1, 0, 0], 
								[1, 0, 0], 
								[1, 0, 0]
		]
		# Speech array - [quiet, phrase1, phrase2, laugh1, laugh2]
		self.speechMatrixInitial = [
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0]
		]
		# Speech modifier array - [none/normal, faster, high pitch, pause]
		self.speechModifierMatrixInitial = [
							[1, 0, 0, 0], 
							[1, 0, 0, 0], 
							[1, 0, 0, 0], 
							[1, 0, 0, 0]
		]

		# Matrixs while not being tickled.
		# Body movement array - [still, straight, bent forward, back arched]
		self.bodyMovementMatrixNotTickle = [
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0]
		]
		# Left arm movement array - [still, shake at side, wave]
		self.leftArmMovementMatrixNotTickle = [
									[1, 0, 0], 
									[1, 0, 0], 
									[1, 0, 0]
		]
		# Right arm movement array - [still, shake at side, wave]
		self.rightArmMovementMatrixNotTickle = [
									[1, 0, 0], 
									[1, 0, 0], 
									[1, 0, 0]
		]
		# Head movement array - [still, straight up, bent forward, bent back]
		self.headMovementMatrixNotTickle = [
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0]
		]
		# Robot motion array - [stationary, walk forward, walk backward]
		self.robotMotionMatrixNotTickle = [
								[1, 0, 0], 
								[1, 0, 0], 
								[1, 0, 0]
		]
		# Speech array - [quiet, phrase1, phrase2, laugh1, laugh2]
		self.speechMatrixNotTickle = [
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0]
		]
		# Speech modifier array - [none/normal, faster, high pitch, pause]
		self.speechModifierMatrixNotTickle = [
							[1, 0, 0, 0], 
							[1, 0, 0, 0], 
							[1, 0, 0, 0], 
							[1, 0, 0, 0]
		]
		# Matrixs while being tickled, for not main areas ie the rest of the body.
		# Body movement array - [still, straight, bent forward, back arched]
		self.bodyMovementMatrixTickleNotMain = [
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25]
		]
		# Left arm movement array - [still, shake at side, wave]
		self.leftArmMovementMatrixTickleNotMain = [
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33]
		]
		# Right arm movement array - [still, shake at side, wave]
		self.rightArmMovementMatrixTickleNotMain = [
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33]
		]
		# Head movement array - [still, straight up, bent forward, bent back]
		self.headMovementMatrixTickleNotMain = [
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25]
		]
		# Robot motion array - [stationary, walk forward, walk backward]
		self.robotMotionMatrixTickleNotMain = [
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33]
		]
		# Speech array - [quiet, phrase1, phrase2, laugh1, laugh2]
		self.speechMatrixTickleNotMain = [
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2]
		]
		# Speech modifier array - [none/normal, faster, high pitch, pause]
		self.speechModifierMatrixTickleNotMain = [
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25]
		]

		# Matrixs while being tickled, for main (ie being tickled) area.
		# Body movement array - [still, straight, bent forward, back arched]
		self.bodyMovementMatrixTickleMain = [
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4]
		]
		# Left arm movement array - [still, shake at side, wave]
		self.leftArmMovementMatrixTickleMain = [
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4]
		]
		# Right arm movement array - [still, shake at side, wave]
		self.rightArmMovementMatrixTickleMain = [
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4]
		]
		# Head movement array - [still, straight up, bent forward, bent back]
		self.headMovementMatrixTickleMain = [
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4]
		]
		# Robot motion array - [stationary, walk forward, walk backward]
		self.robotMotionMatrixTickleMain = [
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4]
		]
		# Speech array - [quiet, phrase1, phrase2, laugh1, laugh2]
		self.speechMatrixTickleMain = [
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2]
		]
		# Speech modifier array - [none/normal, faster, high pitch, pause]
		self.speechModifierMatrixTickleMain = [
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25]
		]

		# list for all body part states
		self.bodyMovementStateList = [self.bodyMovementMatrixInitial, self.bodyMovementMatrixNotTickle, self.bodyMovementMatrixTickleNotMain, self.bodyMovementMatrixTickleMain]
		self.leftArmStateMovementList = [self.leftArmMovementMatrixInitial, self.leftArmMovementMatrixNotTickle, self.leftArmMovementMatrixTickleNotMain, self.leftArmMovementMatrixTickleMain]
		self.rightArmMovementStateList = [self.rightArmMovementMatrixInitial, self.rightArmMovementMatrixNotTickle, self.rightArmMovementMatrixTickleNotMain, self.rightArmMovementMatrixTickleMain]
		self.headMovementStateList = [self.headMovementMatrixInitial, self.headMovementMatrixNotTickle, self.headMovementMatrixTickleNotMain, self.headMovementMatrixTickleMain]
		self.robotMotionStateList = [self.robotMotionMatrixInitial, self.robotMotionMatrixNotTickle, self.robotMotionMatrixTickleNotMain, self.robotMotionMatrixTickleMain]
		self.speechStateList = [self.speechMatrixInitial, self.speechMatrixNotTickle, self.speechMatrixTickleNotMain, self.speechMatrixTickleMain]
		self.speechModifierStateList = [self.speechModifierMatrixInitial, self.speechModifierMatrixNotTickle, self.speechModifierMatrixTickleNotMain, self.speechModifierMatrixTickleMain]

		# list of all robot body areas
		self.robotStateList = [self.bodyMovementStateList, 
							self.leftArmStateMovementList, 
							self.rightArmMovementStateList, 
							self.headMovementStateList, 
							self.robotMotionStateList, 
							self.speechStateList, 
							self.speechModifierStateList
							]
		
		# final result matrix that will be used by other methods and classes to animate the robot
		# - don't need to declare stuff in python, but think it might need to be declared somewhere to do with being available to 
		# - other methods and classes?? Should this be done in __init__ ??
		self.bodyMovementMatrixCurrent = []
		self.leftArmMovementMatrixCurrent = []
		self.rightArmMovementMatrixCurrent = []
		self.headMovementMatrixCurrent = []
		self.robotMotionMatrixCurrent = []
		self.speechMatrixCurrent = []
		self.speechModifierMatrixCurrent = []

		# and a list of all the current matrices
		self.robotMatrixCurrentList = [self.bodyMovementMatrixCurrent, 
								self.leftArmMovementMatrixCurrent, 
								self.rightArmMovementMatrixCurrent, 
								self.headMovementMatrixCurrent, 
								self.robotMotionMatrixCurrent, 
								self.speechMatrixCurrent, 
								self.speechModifierMatrixCurrent]

		# dictionary of robot body areas, combines the three sensors in each hand into one
		self.robotBodyArea = {
						'body' : 0,
						'leftArm' : 1,
						'rightArm' : 2,
						'head' : 3,
						'robotMotion' : 4,
						'speech' : 5,
						'speechModifier' : 6
						}

		# dictionary of robot states
		# 0: Initial - initialisation/no target sensor set
		# 1: NotTickle - waiting for tickler to tickle g_target_sensor
		# 2: TickleNotMain - being tickled, but not the area being tickled, anything that is not g_target_sensor
		# 3: TickleMain - being tickled, the area being tickled, corresponds to g_target_sensor
		self.robotStateDictionary = {
						'Initial' : 0, 
						'NotTickle' : 1, 
						'TickleNotMain' : 2,
						'TickleMain' : 3
						}

		# and fill those matrices
		self.robotMatrixCurrentList = [i[self.robotStateDictionary['Initial']] for i in self.robotStateList]

		# While, infinite - 
		while not(self.rightHandActivated and self.leftHandActivated):
			# Loop till both hands are held.
			
			# Get the current state
			self.speechProxy.say("Matrix Current!")
			matrix = str(self.robotMatrixCurrentList)
			self.log("Matrix Current")
			self.log(matrix)
			time.sleep(0.5)


			# Create cumulative matrices from the current matrices

			# Generate a random number for each state type

			# Get the desired next state

			# Save the new current states

			# Action each state using seperate parallel task, pushed to the background with post

			# Wait

			

			

		self.speechProxy.say("I'm going to stop now!")
		self.stopMe()
		self.onStopped() #~ activate output of the box
		

	def onInput_onStop(self):

		self.onUnload() #~ it is recommended to call onUnload of this box in a onStop method, as the code written in onUnload is used to stop the box as well
		

  









