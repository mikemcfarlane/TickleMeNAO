# -*- coding: ascii -*-
""" Unit tests using unittest framework for Markov_tickles.py.

"""
__author__ = "Mike McFarlane (mike@mikemcfarlane.co.uk)"
__version__ = "Revision: 0.14"
__date__ = "Date: 11-04-14"
__copyright__ =  "Copyright (c) Mike McFarlane 2014"
__license__ = "TBC"

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
		self.MarkovTickle = None
		self.myBroker.shutdown()
		
	def testSmallMatrix(self):
		testValue = [1]
		self.assertRaises(Exception, self.MarkovTickle.markovChoice, testValue)

	def testLargeMatrix(self):
		testValue = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
		self.assertRaises(Exception, self.MarkovTickle.markovChoice, testValue)

class ToMarkovChoiceBadInput(unittest.TestCase):
	""" Markov choice should give error if bad input.

	"""

	def setUp(self):
		self.myBroker = ALBroker("myBroker", "0.0.0.0", 0, NAO_IP, 9559)
		self.MarkovTickle = MarkovTickleModule("MarkovTickle")

	def tearDown(self):
		self.MarkovTickle = None
		self.myBroker.shutdown()
	
	def testSmallMatrix(self):
		testValue = [2]
		self.assertRaises(Exception, self.MarkovTickle.markovChoice, testValue)

	def testLargeMatrix(self):
		testValue = [0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
		self.assertRaises(Exception, self.MarkovTickle.markovChoice, testValue)
	

if __name__ == "__main__":
	print "\n"
	print "Running Markov_tickles unit tests"
	print "\n"

	unittest.main()
