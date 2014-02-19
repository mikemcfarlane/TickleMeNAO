import random

class StateNode:

	def __init__(self, state_name, neighbours, trans):
		self.name = state_name
		self.neighbours = neighbours
		self.trans = trans

	def transition(self):
		print(self.name)
		random_num = random.random()
		tot = 0
		for i in range(len(self.trans)):
			tot += self.trans[i]
			if tot > random_num:
				return self.neighbours[i]


def main():
	node1 = StateNode('test', [2, 3], [0.3, 0.7])

if __name__ == "__main__":
	main()