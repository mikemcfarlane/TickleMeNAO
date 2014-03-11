# -*- coding: ascii -*-
""" Unit tests using unittest framework for Markov_tickles.py.

"""
__author__ = "Mike McFarlane (mike@mikemcfarlane.co.uk)"
__version__ = "Revision: 0.14"
__date__ = "Date: 11-04-14"
__copyright__ =  "Copyright (c) Mike McFarlane 2014"
__license__ = "TBC"

from Markov_tickles.MarkovTickleModule import markovChoice
import unittest


class ToMarkovChoiceGoodInput(unittest.TestCase):
	""" Markov choice should give known result with known input.

	"""
	
	def smallMatrix(self):
		a = mt.markovChoice([1])
		b = 0
		self.assertGreaterEqual(a, b)

	def largeMatrix(self):
		a = mt.markovChoice([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		b = 0
		self.assertGreaterEqual(a, b)


class ToMarkovChoiceBadInput(unittest.TestCase):
	""" Markov choice should give error if unknown input.

	"""

	def smallMatrix(self):
		a = mt.markovChoice([2])
		b = 0
		self.assertGreaterEqual(a, b)

	def largeMatrix(self):
		a = mt.markovChoice([0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		b = 0
		self.assertGreaterEqual(a, b)


def main():
	print "\n"
	print "Running Markov_tickles unit tests"
	print "\n"
	
	print markovChoice([1])

	#unittest.main()

if __name__ == "__main__":
	main()
