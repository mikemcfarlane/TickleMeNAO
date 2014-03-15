
""" Exploring unit tests.
    Simple code to implement a simple Markov transition function.
    
"""
__author__ = "Mike McFarlane (mike@mikemcfarlane.co.uk)"
__version__ = "$Revision: 0 $"
__date__ = "$Date: 11-04-14"
__copyright__ =  "Copyright (c) Mike McFarlane 2014"
__license__ = "TBC"

import random
import numpy as np

def choice2(inArray):
    """ Simple function to implement a Markov transition function.

    """
    randNum = np.random.random()
    cum = 0
    sumVal = np.sum(inArray)
    if not abs(sumVal - 1.0) < 1e-10:
        #print "not a P array"
        raise ce.MatrixError("Not a valid array")
    else:
        for count, i in enumerate(inArray):
            cum += i
            if cum >= randNum:
                return count
            
def main():
    for i in range(5):
        print "Choice{}: {}".format(i, choice2([0.25, 0.25, 0.25, 0.25]))
            
if __name__ == '__main__':
    main()