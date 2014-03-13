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

class ToMarkovChoiceGoodInput(unittest.TestCase):
	""" Markov choice should give known result with known input.

	"""

	def setUp(self):
		self.myBroker = ALBroker("myBroker", "0.0.0.0", 0, NAO_IP, 9559)
		self.MarkovTickle = MarkovTickleModule("MarkovTickle")

	def tearDown(self):
		# self.MarkovTickle.dispose()
		self.MarkovTickle = None
		self.myBroker.shutdown()
		
	def testSmallMatrix(self):
		a = self.MarkovTickle.markovChoice([1])
		b = 0
		self.assertGreaterEqual(a, b)

	def testLargeMatrix(self):
		a = self.MarkovTickle.markovChoice([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		b = 0
		self.assertGreaterEqual(a, b)


class ToMarkovChoiceBadInput(unittest.TestCase):
	""" Markov choice should give error if bad input.

	"""

	def setUp(self):
		self.myBroker = ALBroker("myBroker", "0.0.0.0", 0, NAO_IP, 9559)
		self.MarkovTickle = MarkovTickleModule("MarkovTickle")

	def tearDown(self):
		# self.MarkovTickle.dispose()
		self.MarkovTickle = None
		self.myBroker.shutdown()
	
	def testSmallMatrix(self):
		a = self.MarkovTickle.markovChoice([2])
		b = 0
		self.assertGreaterEqual(a, b)

	def testLargeMatrix(self):
		a = self.MarkovTickle.markovChoice([0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		b = 0
		self.assertGreaterEqual(a, b)


if __name__ == "__main__":
	unittest.main()

	