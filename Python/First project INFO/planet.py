
class Planet:
	def __init__(self, name, width, height):
		"""
		Initialise the planet object
		"""

		self.name = name
		self.width = width
		self.height = height
		pass

	def coordinates_dict(self):

		coordinates = []

		for i in range(0, self.height):#give the [x,y] coordinates in a list based on the planet height and width
			p = []
			for n in range(0, self.width):
				a = [n, i]
				p.append(a)
			coordinates.append(p)
		
		map_coordinates = {}
		
		for i in range(0,len(coordinates)):
			for p in range(0,len(coordinates[i])):#assign the tiles to it's coordinates
				map_coordinates[str(coordinates[i][p])] = self.name[i][p]

		return map_coordinates

	def coordinates(self):

		coordinates = []
		for i in range(0, self.height):#give the [x,y] coordinates in a list based on the planet height and width
			p = []
			for n in range(0, self.width):
				a = [n, i]
				p.append(a)
			coordinates.append(p)
		


		return coordinates
		pass


parameters = []

def PLanet2(coordinat):

	coordinat = coordinat
	
	
	if not coordinat in parameters:
		
		parameters.append(coordinat)


	return len(parameters)
	pass










