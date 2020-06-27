from Classes.node import Node




class Tree:

	root = None
	currentNode = None
	fringe = []
	appendList = []
	forbidden = []


	def __init__(self, root, forbidden):
		self.root = Node(root, None)
		self.forbidden = forbidden
		self.currentNode = self.root
		
		self.root.setChildren(self.forbidden)
		self.appendList.append(self.currentNode)


		for i in self.currentNode.children:
			i.setChildren(self.forbidden)

		self.fringe+= self.currentNode.children
		



	def generateChildren(self):


		if len(self.currentNode.children) == 0:

			self.currentNode.setChildren(self.forbidden)

		self.fringe+= self.currentNode.children

		for i in self.currentNode.children:
			i.setChildren(self.forbidden)

	def move(self, node):
		

		self.currentNode = node
		self.fringe.remove(self.currentNode)
		self.appendList.append(self.currentNode)

		self.generateChildren()
			
				

	def checkExpand(self, node):

		

		if node.number in self.getNumber(self.appendList):
			if self.checkSimilar(node, self.appendList):
				return True


		return False


	def moveToParent(self):
		self.currentNode = self.currentNode.parent



	def checkSimilar(self, node, nodeList):
 
		for i in nodeList:
			if node.number == i.number and self.checkParent(node, i):
				return False
 
		
 
		
		return True



	def checkParent(self, node, node2):


		if node.parent is None and node2.parent is None:
			return True

		if node.parent is None or node2.parent is None:
			return False

		num1 = [abs(int(node.number[0]) - int(node.parent.number[0])), abs(int(node.number[1]) - int(node.parent.number[1])),abs(int(node.number[2]) - int(node.parent.number[2]))]
		
		num2 = [abs(int(node2.number[0]) - int(node2.parent.number[0])), abs(int(node2.number[1]) - int(node2.parent.number[1])),abs(int(node2.number[2]) - int(node2.parent.number[2]))]

		

		if num1 == num2:
			return True

		else:
			return False






	def getNumber(self, numList):

		result = []

		for i in numList:
			result.append(i.number)

		return result