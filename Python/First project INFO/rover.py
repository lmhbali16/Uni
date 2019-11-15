from planet import Planet
from loader import next1
from loader import next2
from loader import next3
from loader import next4

class Rover:
	
	def __init__(self,no_name_level, battery): ##width height tile rover x y list, battery
		"""
		Initialises the rover
		"""
		self.no_name_level = no_name_level
		
		self.rover_map = []
		self.battery = battery

		self.width = self.no_name_level[0]
		self.height = self.no_name_level[1]
		self.tile = self.no_name_level[2]
		self.x = self.no_name_level[3]
		self.y = self.no_name_level[4]

		self.rover_coordinates = [self.x, self.y]
		
		self.tiles = []
		for i in self.tile:
			i = i[:-1]
			self.tiles.append(i)	
		self.tiles_arranged = [self.tiles[i:i + self.width] for i in range(0, len(self.tile),self. width)]

		planet_co = []
		
		for i in self.tiles_arranged:
			
			self.planet = []
			for n in i:
				n = n.split(',')
				if len(n) != 3:
					a = ['-']
					n += a
					
					self.planet.append(n)
				else:
					self.planet.append(n)
					
			planet_co.append(self.planet)
		

		self.planet_map = Planet(planet_co, self.width, self.height)
		self.coordinates = Planet(planet_co, self.width, self.height)
		self.coordinates = Planet.coordinates(self.coordinates)
		self.planet_map = Planet.coordinates_dict(self.planet_map)#this is my map in dictionary format(coordinates : tile)
	
		
		pass
	
	def move(self, direction, cycles):#direction, cycles
		"""
		Moves the rover on the planet
		"""
		self.direction = direction
		self.cycles = cycles
		


		for i in self.coordinates:
			for n in i:
				if n == self.rover_coordinates:
					x_index = i.index(n)
					y_index = self.coordinates.index(i)

		number_shade = 0
		step = 0
		

		if self.direction == 'N':
			new_noname4 = [self.width, self.height, self.tile, self.x, self.y]

			data4 = next1(new_noname4 , self.cycles, step, self.battery)

			#new_battery = data4[7]
			new_no_name_level = [data4[0], data4[1], data4[2], data4[3], data4[4]]

			return data4
			
		if self.direction == 'S':
			new_noname4 = [self.width, self.height, self.tile, self.x, self.y]

			data4 = next2(new_noname4 , self.cycles, step, self.battery)

			#new_battery = data4[7]
			new_no_name_level = [data4[0], data4[1], data4[2], data4[3], data4[4]]

			return data4

		if self.direction == 'E':
			new_noname4 = [self.width, self.height, self.tile, self.x, self.y]

			data4 = next3(new_noname4 , self.cycles, step, self.battery)

			#new_battery = data4[7]
			new_no_name_level = [data4[0], data4[1], data4[2], data4[3], data4[4]]

			return data4
		if self.direction == 'W':
			new_noname4 = [self.width, self.height, self.tile, self.x, self.y]

			data4 = next4(new_noname4 , self.cycles, step, self.battery)

			#new_battery = data4[7]
			new_no_name_level = [data4[0], data4[1], data4[2], data4[3], data4[4]]

			return data4
		pass
	
	def wait(self, cycles):
		"""
		The rover will wait for the specified cycles
		"""
		pass
	
	def starting(self):
		found = False
		for i in self.rover_map:
			if i == self.rover_start:
				found == True

		if not found:
			self.rover_map.append(self.rover_start)

		explored = int((len(self.rover_map) / len(self.planet_map)) * 100)

		return explored
