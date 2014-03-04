# DESCRIPTION:
# Attempts to generate a realistic response for NAO to being tickled by using Markov Chains.
# PROGRAMMER: 
# Mike McFarlane
# VERSION HISTORY (version, date, description):
# 0.1,18/10/2013, basic code structure outlined in comments, and some matrices and methods set up. Working.
# USAGE: 
# Add to Choregraph script box.
# TODO:
# - add turn left and turn right to robotMotionArray
# - add more phrases and laughs to speechArray
# - modify the not being tickled array so the robot does some moves whilst waiting to be tickled, can set flag in main while loop

from naoqi import ALProxy

class MyClass(GeneratedClass):
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
		self.g_target_sensor = 0
		# Flag/mutex to stop current matrices being modified by other processes
		# 0 = not being tickled, 1 = being tickled
		self.robotBeingTickled = 0

	def rightBumperTouched(self, *_args):
		self.memory.unsubscribeToEvent("RightBumperPressed",self.getName())
		self.speechProxy.say("You touched my right foot")
		self.memory.subscribeToEvent("RightBumperPressed",self.getName(),"rightBumperTouched")

	def leftBumperTouched(self, *_args):
		self.memory.unsubscribeToEvent("LeftBumperPressed",self.getName())
		self.speechProxy.say("You touched my left foot")
		self.memory.subscribeToEvent("LeftBumperPressed",self.getName(),"leftBumperTouched")

	# THIS IS THE DEVELOPMENT TEST SENSOR
	def frontSensorTouched(self, *_args):
		# check if this is the right sensor being selected by the tickle manager before being actioned 
		# AND not currently being tickled
		# could also have an else to provide some encouragement to tickle another area
		self.memory.unsubscribeToEvent("FrontTactilTouched",self.getName())
		self.speechProxy.say("You touched the front of my head")
		# call the being tickled function and pass the name of the function so the name
		# of the area being tickled is known
		areaBeingTickled = 1
		whoIAm = self.getName()
		self.speechProxy.say("Before")
		self.beingTickled(areaBeingTickled)
		self.speechProxy.say("After")
		self.memory.subscribeToEvent("FrontTactilTouched",self.getName(),"frontSensorTouched")

	def middleSensorTouched(self, *_args):
		self.memory.unsubscribeToEvent("MiddleTactilTouched",self.getName())
		self.speechProxy.say("You touched the top of my head")
		self.memory.subscribeToEvent("MiddleTactilTouched",self.getName(),"middleSensorTouched")

	def rearSensorTouched(self, *_args):
		self.memory.unsubscribeToEvent("RearTactilTouched",self.getName())
		self.speechProxy.say("You touched the back of my head")
		self.memory.subscribeToEvent("RearTactilTouched",self.getName(),"rearSensorTouched")

	def rightHandTouched(self, *_args):
		self.memory.unsubscribeToEvent("HandRightBackTouched",self.getName())
		self.memory.unsubscribeToEvent("HandRightLeftTouched",self.getName())
		self.memory.unsubscribeToEvent("HandRightRightTouched",self.getName())
		self.speechProxy.say("You touched my right hand")
		self.memory.subscribeToEvent("HandRightBackTouched",self.getName(),"rightHandTouched")
		self.memory.subscribeToEvent("HandRightLeftTouched",self.getName(),"rightHandTouched")
		self.memory.subscribeToEvent("HandRightRightTouched",self.getName(),"rightHandTouched")        

	def leftHandTouched(self, *_args):
		self.memory.unsubscribeToEvent("HandLeftBackTouched",self.getName())
		self.memory.unsubscribeToEvent("HandLeftLeftTouched",self.getName())
		self.memory.unsubscribeToEvent("HandLeftRightTouched",self.getName())
		self.speechProxy.say("You touched my left hand")
		self.memory.subscribeToEvent("HandLeftBackTouched",self.getName(),"leftHandTouched")
		self.memory.subscribeToEvent("HandLeftLeftTouched",self.getName(),"leftHandTouched")
		self.memory.subscribeToEvent("HandLeftRightTouched",self.getName(),"leftHandTouched")

	def beingTickled(self, areaBeingTickled):
		self.speechProxy.say("Going deeper")
		argument = str(areaBeingTickled)
		self.speechProxy.say(argument)
		matrix = str(self.bodyMovementArrayNotTickle)
		self.speechProxy.say(str(matrix))

		# Set a being tickled flag to give this method ownership of the robot

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

		# Unset being tickled flag

	def onLoad(self):
		#~ puts code for box initialization here
		pass

	def onUnload(self):
		#~ puts code for box cleanup here
		pass

	def onInput_onStart(self):
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

		# Declare generalised transition matrices for each type of state.
		# Arrays while not being tickled.
		# Body movement array - [still, straight, bent forward, back arched]
		self.bodyMovementArrayNotTickle = [
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0]
		]
		# Left arm movement array - [still, shake at side, wave]
		self.leftArmMovementArrayNotTickle = [
									[1, 0, 0], 
									[1, 0, 0], 
									[1, 0, 0]
		]
		# Right arm movement array - [still, shake at side, wave]
		self.rightArmMovementArrayNotTickle = [
									[1, 0, 0], 
									[1, 0, 0], 
									[1, 0, 0]
		]
		# Head movement array - [still, straight up, bent forward, bent back]
		self.headMovementArrayNotTickle = [
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0], 
									[1, 0, 0, 0]
		]
		# Robot motion array - [stationary, walk forward, walk backward]
		self.robotMotionArrayNotTickle = [
								[1, 0, 0], 
								[1, 0, 0], 
								[1, 0, 0]
		]
		# Speech array - [quiet, phrase1, phrase2, laugh1, laugh2]
		self.speechArrayNotTickle = [
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0], 
							[1, 0, 0, 0, 0]
		]
		# Speech modifier array - [none/normal, faster, high pitch, pause]
		self.speechModifierArrayNotTickle = [
							[1, 0, 0, 0], 
							[1, 0, 0, 0], 
							[1, 0, 0, 0], 
							[1, 0, 0, 0]
		]
		# Arrays while being tickled, for not main areas ie the rest of the body.
		# Body movement array - [still, straight, bent forward, back arched]
		self.bodyMovementArrayTickleNotMain = [
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25]
		]
		# Left arm movement array - [still, shake at side, wave]
		self.leftArmMovementArrayTickleNotMain = [
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33]
		]
		# Right arm movement array - [still, shake at side, wave]
		self.rightArmMovementArrayTickleNotMain = [
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33]
		]
		# Head movement array - [still, straight up, bent forward, bent back]
		self.headMovementArrayTickleNotMain = [
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25]
		]
		# Robot motion array - [stationary, walk forward, walk backward]
		self.robotMotionArrayTickleNotMain = [
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33], 
							[0.33, 0.33, 0.33]
		]
		# Speech array - [quiet, phrase1, phrase2, laugh1, laugh2]
		self.speechArrayTickleNotMain = [
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2]
		]
		# Speech modifier array - [none/normal, faster, high pitch, pause]
		self.speechModifierArrayTickleNotMain = [
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25]
		]

		# Arrays while being tickled, for main (ie being tickled) area.
		# Body movement array - [still, straight, bent forward, back arched]
		self.bodyMovementArrayTickleMain = [
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4]
		]
		# Left arm movement array - [still, shake at side, wave]
		self.leftArmMovementArrayTickleMain = [
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4]
		]
		# Right arm movement array - [still, shake at side, wave]
		self.rightArmMovementArrayTickleMain = [
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4]
		]
		# Head movement array - [still, straight up, bent forward, bent back]
		self.headMovementArrayTickleMain = [
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4], 
							[0.1, 0.1, 0.4, 0.4]
		]
		# Robot motion array - [stationary, walk forward, walk backward]
		self.robotMotionArrayTickleMain = [
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4], 
							[0.2, 0.4, 0.4]
		]
		# Speech array - [quiet, phrase1, phrase2, laugh1, laugh2]
		self.speechArrayTickleMain = [
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2], 
							[0.2, 0.2, 0.2, 0.2, 0.2]
		]
		# Speech modifier array - [none/normal, faster, high pitch, pause]
		self.speechModifierArrayTickleMain = [
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25], 
							[0.25, 0.25, 0.25, 0.25]
		]

		
		# While, infinite - 
		while True:
			# Just loop till the end of time.
			
			# Get the current state

			# Create cumulative matrices from the current matrices

			# Generate a random number for each state type

			# Get the desired next state

			# Save the new current states

			# Action each state using seperate parallel task, pushed to the background with post

			# Wait

			pass

			


		#self.onStopped() #~ activate output of the box
		

	def onInput_onStop(self):
		self.onUnload() #~ it is recommended to call onUnload of this box in a onStop method, as the code written in onUnload is used to stop the box as well
		

  









