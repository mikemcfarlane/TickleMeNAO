# -*- coding: ascii -*-
""" NAO responds to being tickled.


"""

import time
import sys
import numpy as np


from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

NAO_IP = "mistcalf.local"

# Global variables to store module instances and proxies
MarkovTickle = None

class MarkovTickleModule(ALModule):
	""" Simple module for tickling NAO. 

	"""

	def __init__(self, name):
		""" Initialise module. 

		"""
		ALModule.__init__(self, name)
		

	def markovChoice(self, inMatrix):
		""" Chooses a value from a Markov transition matrix.

		"""
		randNum = np.random.random()
		cum = 0
		
		if round(np.sum(inMatrix)) != 1:
			print "This is not a p array."
		else:
			for index, probability in enumerate(inMatrix):
				cum += probability
				if cum > randNum:
					return index
		
	def mainTask(self):
		""" Temp main task.

		"""
		# Run forever
		while True:
			print ("Alive!")
			print "I choose: ", self.markovChoice([0.25, 0.25, 0.25, 0.25])
			time.sleep(1.0)


def main():
	""" Main entry point

	"""
	myBroker = ALBroker("myBroker", "0.0.0.0", 0, NAO_IP, 9559)

	global MarkovTickle
	MarkovTickle = MarkovTickleModule("MarkovTickle")

	print "Running, hit CTRL+C to stop script"
	MarkovTickle.mainTask()

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
		

	









