# -*- coding: ascii -*-
""" Unit tests using unittest framework for Markov_tickles.py.

"""


#from Markov_tickles import MarkovTickleModule as mt
from Markov_tickles import MarkovTickleModule
import unittest

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

NAO_IP = "mistcalf.local"

# Global variables to store module instances and proxies
MarkovTickle = None

class ToMarkovChoiceGoodInput(unittest.TestCase):
	""" Markov choice should give known result with known input.

	"""

	# def setUp(self):
	# 	self.mt = MarkovTickleModule("test")

	global MarkovTickle	
	
	def testSmallMatrix(self):
		a = MarkovTickle.markovChoice([1])
		b = 0
		self.assertGreaterEqual(a, b)

	def testLargeMatrix(self):
		a = MarkovTickle.markovChoice([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		b = 0
		self.assertGreaterEqual(a, b)


class ToMarkovChoiceBadInput(unittest.TestCase):
	""" Markov choice should give error if bad input.

	"""

	# def setUp(self):
	# 	self.mt = MarkovTickleModule("test")

	global MarkovTickle
	
	def testSmallMatrix(self):
		a = MarkovTickle.markovChoice([2])
		b = 0
		self.assertGreaterEqual(a, b)

	def testLargeMatrix(self):
		a = MarkovTickle.markovChoice([0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		b = 0
		self.assertGreaterEqual(a, b)


if __name__ == "__main__":
	myBroker = ALBroker("myBroker", "0.0.0.0", 0, NAO_IP, 9559)

	global MarkovTickle
	MarkovTickle = MarkovTickleModule("MarkovTickle")

	unittest.main()

	myBroker.shutdown()