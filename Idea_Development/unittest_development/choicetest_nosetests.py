
""" Exploring unit tests.
    Tests for nose for choice.py.
    
"""
__author__ = "Mike McFarlane (mike@mikemcfarlane.co.uk)"
__version__ = "$Revision: 0 $"
__date__ = "$Date: 11-04-14"
__copyright__ =  "Copyright (c) Mike McFarlane 2014"
__license__ = "TBC"

import choice

def test_range():
    assert choice.choice2([1]) >= 0
    
def test_bad_range():
    assert choice.choice2([2]) >= 0
    
def test_large_range():
    assert choice.choice2([0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.01]) >= 0
    
def test_large_bad_range():
    assert choice.choice2([0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.09, 0.1]) >= 0
										