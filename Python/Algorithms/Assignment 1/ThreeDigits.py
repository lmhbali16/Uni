import sys
from Classes.tree import Tree
from Classes.node import Node
from Classes.search import Search


strat = sys.argv[1]

with open(sys.argv[2]) as file:
	data = file.read().split("\n")
	start = str(data[0])
	goal = str(data[1])
	if len(data) >= 3:
		forbidden = data[2].split(",")
	else:
		forbidden = []


tree = Tree(start, forbidden)

flag = False

if strat == "A":
	flag = Search.aStar(tree, goal)

elif strat == "B":
	flag = Search.bFS(tree, goal)

elif strat == "D":
	flag = Search.dFS(tree, goal)

elif strat == "I":
	flag = Search.iDS(tree, goal)

elif strat == "G":
	flag = Search.greedy(tree, goal)

elif strat == "H":
	flag = Search.hillClimbing(tree,goal)






if flag:
	print(",".join(Search.result))
	print(",".join(tree.getNumber(tree.appendList)))

else:
	print("No solution found.")
	print(",".join(tree.getNumber(tree.appendList)))
	
