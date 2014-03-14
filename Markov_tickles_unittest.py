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
import numpy as np

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
		testValue = self.MarkovTickle.markovChoice([1])
		result = 0
		self.assertEquals(testValue, result)

	def testLargeMatrix(self):
		testValue = self.MarkovTickle.markovChoice([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		result = 0
		self.assertGreaterEqual(testValue, result)

	def testHugeMatrix(self):
		""" Pass v large matrix e.g. 1000 elements."""
		arraySize = 1000
		array = np.random.random(arraySize)
		arraySum = np.sum(array)
		arrayNormalised = array / arraySum
		testValue = self.MarkovTickle.markovChoice(arrayNormalised)
		result = 0
		self.assertGreaterEqual(testValue, result)
		

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
		self.assertRaises(ValueError, self.MarkovTickle.markovChoice, testValue)

	def testLargeMatrix(self):
		""" Test larger matrix, not a p matrix. """
		testValue = [0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
		self.assertRaises(ValueError, self.MarkovTickle.markovChoice, testValue)

	def testBadMatrixFormat1(self):
		""" Matrix not properly formed e.g. comma not decimal point. """
		testValue = [0,1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
		self.assertRaises(ValueError, self.MarkovTickle.markovChoice, testValue)

	def testBadMatrixFormat2(self):
		""" Matrix not properly formed e.g. decimal point not comma. """
		# testValue = [0.1. 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
		# self.assertRaises(ValueError, self.MarkovTickle.markovChoice, testValue)
		# not a valid test as would need to pass a string to create a number like '0.1.'
		pass

	def testMultiRowMatrix(self):
		""" More than a single row passed as argument. """
		testValue = [[0.5, 0.5], [0.5, 0.5]]
		self.assertRaises(ValueError, self.MarkovTickle.markovChoice, testValue)

	def testWhatHappensIfPEquals1(self):
		""" What happens if p = 1? """
		testValue = self.MarkovTickle.markovChoice([0, 0, 1])
		result = 2
		self.assertEquals(testValue, result)

	def testIsRandomRandom(self):
		""" Is choice function returning a randomly distributed result across many runs? """
		numRuns = 100000
		transitionMatrix = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		# Run choice function many times.
		list = [self.MarkovTickle.markovChoice(transitionMatrix) for i in range(numRuns)]
		listHistogram, listBins = np.histogram(list)
		listPercentage = [(x / float(numRuns))*100 for x in listHistogram]
		testValue = np.sum(listPercentage)
		result = 100.0
		self.assertAlmostEqual(testValue, result)

if __name__ == "__main__":
	print "\n"
	print "Running Markov_tickles unit tests"
	print "\n"

	unittest.main()
