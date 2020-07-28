


class Node:


	parent = None

	children = []
	number = ""
	nodeForbidden =[]


	def __init__(self, number, parent):
		
		self.number = number
		self.parent = parent
		



	def checkFirstDigit(self):

		parentDigit = int(self.parent.number[0])
		numberDigit = int(self.number[0])

		if numberDigit == 0 and parentDigit == 1:
			return -1

		elif parentDigit - numberDigit == 1:
			return str(numberDigit-1)+self.number[1:]

		elif parentDigit - numberDigit == -1:
			return str(numberDigit+1)+self.number[1:]

		else:
			return -1

	def checkSecondDigit(self):

		parentDigit = int(self.parent.number[1])
		numberDigit = int(self.number[1])

		if numberDigit == 0 and parentDigit == 1:
			return -1

		elif parentDigit - numberDigit == 1:
			return self.number[0]+str(numberDigit-1)+self.number[-1]

		elif parentDigit - numberDigit == -1:
			return self.number[0]+str(numberDigit+1)+self.number[-1]

		else:
			return -1


	def checkThirdDigit(self):

		parentDigit = int(self.parent.number[2])
		numberDigit = int(self.number[2])

		if numberDigit == 0 and parentDigit == 1:
			return -1

		elif parentDigit - numberDigit == 1:
			return self.number[:-1]+str(numberDigit-1)

		elif parentDigit - numberDigit == -1:
			return self.number[:-1]+str(numberDigit+1)

		else:
			return -1



	def setNodeForbidden(self):

		self.nodeForbidden = []

		if self.parent is not None:
			self.nodeForbidden.append(self.parent.number)

			if self.checkFirstDigit() != -1:
				self.nodeForbidden.append(self.checkFirstDigit())

			if self.checkSecondDigit() != -1:
				self.nodeForbidden.append(self.checkSecondDigit())

			if self.checkThirdDigit() != -1:
				self.nodeForbidden.append(self.checkThirdDigit())


		else:
			self.nodeForbidden = []
		

	def setChildren(self, forbidden):
		self.setNodeForbidden()

		forbidden = forbidden + self.nodeForbidden





		self.children = []

		

		if self.number[0] != "0" and str(int(self.number[0])-1)+self.number[1:] not in forbidden:
			self.children.append(Node(str(int(self.number[0])-1)+self.number[1:], self))

		if self.number[0] != "9" and str(int(self.number[0])+1)+self.number[1:] not in forbidden:
			self.children.append(Node(str(int(self.number[0])+1)+self.number[1:], self))

		if self.number[1] != "0" and self.number[0]+str(int(self.number[1])-1)+self.number[-1] not in forbidden:
			self.children.append(Node(self.number[0]+str(int(self.number[1])-1)+self.number[-1], self))

		if self.number[1] != "9" and self.number[0]+str(int(self.number[1])+1)+self.number[-1] not in forbidden:
			self.children.append(Node(self.number[0]+str(int(self.number[1])+1)+self.number[-1], self))

		if self.number[2] != "0" and self.number[:-1]+str(int(self.number[2])-1) not in forbidden:
			self.children.append(Node(self.number[:-1]+str(int(self.number[2])-1), self))

		if self.number[2] != "9" and self.number[:-1]+str(int(self.number[2])+1) not in forbidden:
			self.children.append(Node(self.number[:-1]+str(int(self.number[2])+1), self))




		

	def getChildrenNumber(self):
		result = {}

		for i in self.children:
			result[i.number] = i

		return result

