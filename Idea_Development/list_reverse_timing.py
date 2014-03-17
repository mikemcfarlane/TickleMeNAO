
""" Time list reversal.

"""

from timeit import timeit

repeats = 10000000

print "reverse(): ", timeit('list.reverse()', 'list = [1, 2, 3]', number = repeats)
print
print "slice: ", timeit('newList = list[::-1]', 'list = [1, 2, 3]', number = repeats)
print
print "list comp:", timeit('newList = [i for i in reversed(list)]', 'list = [1, 2, 3]', number = repeats)
print