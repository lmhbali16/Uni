from Classes.node import Node
from Classes.tree import Tree




class Search:

	result = []

	@staticmethod
	def setResult(tree):

		while tree.currentNode is not None:
			Search.result.append(tree.currentNode.number)
			tree.currentNode = tree.currentNode.parent


		Search.result = Search.result[::-1]


	@staticmethod
	def dFS(tree, goal):

		

		while len(tree.fringe) > 0:
			
			if tree.currentNode.number == goal:
				Search.setResult(tree)
				return True

			if Search.checkExpanded(tree):
				return False

			flag = False
			for child in tree.currentNode.children:
				
				if tree.checkSimilar(child, tree.appendList):
					
					tree.move(child)
					flag = True
					break


			if not flag and tree.currentNode.parent is not None:
				tree.moveToParent()

			elif not flag and tree.currentNode.parent is None:
				break


		return False


	@staticmethod
	def bFS(tree, goal):
		

		while len(tree.fringe) > 0:
			if tree.currentNode.number == goal:
				
				Search.setResult(tree)
				return True

			if Search.checkExpanded(tree):
				return False
				

			
			tree.fringe[0].setChildren(tree.forbidden)

			if tree.checkSimilar(tree.fringe[0], tree.appendList):
				tree.move(tree.fringe[0])

			else:
				tree.fringe.remove(tree.fringe[0])



		return False



	@staticmethod
	def iDS(tree, goal):

		depth = 1

		while len(tree.appendList) < 1000:
			
			

			if tree.currentNode.number == goal:
				Search.setResult(tree)
				return True
			
			tree.currentNode = tree.root
			tree.fringe = [tree.root]
			flag =False
			

			Search.idsDepth(tree, goal, depth)

			depth += 1
			


				
				




		return False


	@staticmethod
	def idsDepth(tree, goal, depth):

		currentDepth = 0

		appendList2 = []
		while len(tree.fringe) > 0:

			

			if depth == 1:
				appendList2.append(tree.currentNode)

				for child in tree.currentNode.children:

					if tree.checkSimilar(child, appendList2):
						appendList2.append(child)


						if child.number == goal:
							tree.currentNode = child
							Search.addList(tree, appendList2)
							return True

				break

			elif currentDepth == depth-1 and depth > 1:


				for child in tree.currentNode.children:
					if tree.checkSimilar(child, appendList2):
						appendList2.append(child)

						if child.number == goal:
							Search.addList(tree, appendList2)
							tree.currentNode = child
							return True

				tree.moveToParent()
				currentDepth -= 1

			else:

				if tree.checkSimilar(tree.currentNode, appendList2):
					appendList2.append(tree.currentNode)

				flag = False
				for child in tree.currentNode.children:
					if tree.checkSimilar(child, appendList2):
						child.setChildren(tree.forbidden)
						appendList2.append(child)
						flag = True
						currentDepth += 1
						tree.currentNode = child
						break

				if not flag:

					if tree.currentNode.parent is None:
						break

					else:
						tree.moveToParent()
						currentDepth -= 1
				

			
		Search.addList(tree, appendList2)
					
	@staticmethod
	def addList(tree, appendList2):


		while len(tree.appendList) < 1000 and len(appendList2) > 0:

			tree.appendList.append(appendList2[0])
			appendList2 = appendList2[1:]
					


	@staticmethod
	def getChildNum(child, tree, depth):

		idx =0 

		for i in tree.appendList:
			if child == i:
				idx += 1

		
		if idx >= depth:
			return False

		else:
			return True

	@staticmethod
	def greedy(tree, goal):

		while tree.currentNode.number != goal or len(tree.fringe) > 0:

			if tree.currentNode.number == goal:
				Search.setResult(tree)
				return True

			if Search.checkExpanded(tree):
				return False

			if len(tree.fringe) == 0:
				break

			manhattan = Search.calculateHeuristic(tree.fringe, goal)
			
			node, bestValue = Search.findBestNode(tree.fringe, manhattan)
			
			tree.move(node)


		return False

	@staticmethod
	def hillClimbing(tree, goal):


		while tree.currentNode.number != goal or len(tree.fringe) > 0:

			if tree.currentNode.number == goal:
				Search.setResult(tree)
				return True

			if Search.checkExpanded(tree):
				return False

			if len(tree.currentNode.children) == 0:
				break

			manhattan = Search.calculateHeuristic(tree.currentNode.children, goal)
			
			nodeMan = Search.calculateHeuristic([tree.currentNode], goal)[0]
			
			
			node, bestValue = Search.findBestNode(tree.currentNode.children, manhattan)


			
			if bestValue < nodeMan:
				tree.move(node)

			else:
				break


		return False


	@staticmethod
	def aStar(tree, goal):



		while len(tree.fringe) > 0:

			if tree.currentNode.number == goal:
				Search.setResult(tree)
				return True

			if len(tree.fringe) == 0:
				break

			manhattan = Search.calculateHeuristic(tree.fringe, goal)
			node, bestValue = Search.findBestNodeA(tree.fringe, manhattan, tree)
			
			
			if tree.checkSimilar(node, tree.appendList):
				tree.move(node)

			else:
				tree.fringe.remove(node)


	

		return False


	@staticmethod
	def findBestNodeA(nodeList, manhattan, tree):

		i = 0
		bestValue = 60


		for idx, j in enumerate(manhattan):
			if j+Search.getRootDistance(tree.fringe[idx]) <= bestValue:
				i = idx
				bestValue = j+Search.getRootDistance(tree.fringe[idx])

			
			


		return (nodeList[i], bestValue)


	@staticmethod
	def getRootDistance(node):

		temp = node
		i = 0
		
		while temp is not None:
			temp = temp.parent
			i+=1

		return i

	@staticmethod
	def findBestNode(nodeList, manhattan):


		i = 0
		bestValue = 60


		for idx, j in enumerate(manhattan):
			if j <= bestValue:
				i = idx
				bestValue = j

			


		return (nodeList[i], bestValue)




	@staticmethod
	def calculateHeuristic(nodeList, number):

		result = []

		for node in nodeList:

			num = node.number

			i = abs(int(num[0])- int(number[0]))+abs(int(num[1])- int(number[1]))+abs(int(num[2])- int(number[2]))
			result.append(i)


		return result


	@staticmethod
	def checkExpanded(tree):

		if len(tree.appendList) >= 1000:
			return True

		else:
			return False


