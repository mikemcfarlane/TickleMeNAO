from StateNode import StateNode

my_graph = {1:StateNode('here', [2, 3], [0.5, 0.5]), 2:StateNode('there', [1, 3], [0.7, 0.3]), 3:StateNode('everywhere', [3], [1]) }

pos = 1
for i in range(20):
	pos = my_graph[pos].transition()
