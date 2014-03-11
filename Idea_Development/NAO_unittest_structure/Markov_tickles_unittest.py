# -*- coding: ascii -*-
""" Unit tests using unittest framework for Markov_tickles.py.

"""


#from Markov_tickles import MarkovTickleModule as mt
from Markov_tickles import MarkovTickleModule
import unittest


class ToMarkovChoiceGoodInput(unittest.TestCase):
	""" Markov choice should give known result with known input.

	"""
	
	
	def smallMatrix(self):
		a = markovChoice([1])
		b = 0
		self.assertGreaterEqual(a, b)

	def largeMatrix(self):
		a = markovChoice([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		b = 0
		self.assertGreaterEqual(a, b)


class ToMarkovChoiceBadInput(unittest.TestCase):
	""" Markov choice should give error if bad input.

	"""
	
	def smallMatrix(self):
		a = markovChoice([2])
		b = 0
		self.assertGreaterEqual(a, b)

	def largeMatrix(self):
		a = markovChoice([0.9, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
		b = 0
		self.assertGreaterEqual(a, b)


if __name__ == "__main__":
	unittest.main()
