from planet import Planet


class Tile:
		
	def __init__(self, no_name_level):#width height tile rover x y list
		"""
		Initialises the terrain tile and attributes
		"""
		self.no_name_level = no_name_level
		pass
	
	
	def elevation(self):
		"""
		Returns an integer value of the elevation number 
		of the terrain object
		"""

		width = self.no_name_level[0]
		height = self.no_name_level[1]
		tile = self.no_name_level[2]
		x = self.no_name_level[3]
		y = self.no_name_level[4]
		
		tiles = []
		for i in tile:
			i = i[:-1]
			tiles.append(i)	
		tiles_arranged = [tiles[i:i + width] for i in range(0, len(tile), width)]
	
		planet_co = []
		
		for i in tiles_arranged:
			
			planet = []
			for n in i:
				n = n.split(',')
				if len(n) != 3:
					a = ['-']
					n += a
					
					planet.append(n)
				else:
					planet.append(n)
					
			planet_co.append(planet)
			
	
		planet_map = Planet(planet_co, width, height)
		coordinates = Planet(planet_co, width, height)
		coordinates = Planet.coordinates(coordinates)
		planet_map = Planet.coordinates_dict(planet_map)#this is my map in dictionary format(coordinates : tile)
		
		for y1 in coordinates:
			if coordinates.index(y1) == y:
				y_value = coordinates.index(y1)
				for x1 in y1:
					if x1 == [x, y]:
						x_value = y1.index(x1)
		rover_d = coordinates[y_value][x_value]
	
		x1 = x_value + 1
		x2 = x_value + 2
		y1 = y_value + 1
		y2 = y_value + 2
	
		if x1 == len(coordinates[1]):
			x1 == 0
		if y1 == len(coordinates):
			y1 == 0
	
		if x2 > len(coordinates[1]):
			x2 = 1
		if y2 > len(coordinates[1]):
			y2 == 1
	
		front2 = coordinates[y2][x_value]
		front1 = coordinates[y1][x_value]
		back1 = coordinates[y_value-1][x_value]
		back2 = coordinates[y_value-2][x_value]
		right1 = coordinates[y_value][x1]
		right2 = coordinates[y_value][x2]
		left1 = coordinates[y_value][x_value-1]
		left2 = coordinates[y_value][x_value-2]
	
	
		front1_right1 = coordinates[y1][x1]
		front1_right2 = coordinates[y1][x2]
		front2_right1 = coordinates[y2][x1]
		front2_right2 = coordinates[y2][x2]
		front1_left1 = coordinates[y1][x_value-1]
		front1_left2 = coordinates[y1][x_value-2]
		front2_left1 = coordinates[y2][x_value-1]
		front2_left2 = coordinates[y2][x_value-2]
	
		back1_right1 = coordinates[y_value-1][x1]
		back1_right2 = coordinates[y_value-1][x2]
		back2_right1 = coordinates[y_value-2][x1]
		back2_right2 = coordinates[y_value-2][x2]
		back1_left1 = coordinates[y_value-1][x_value-1]
		back1_left2 = coordinates[y_value-1][x_value-2]
		back2_left1 = coordinates[y_value-2][x_value-1]
		back2_left2 = coordinates[y_value-2][x_value-2]
		
		co_f2r2 = planet_map[str(front2_right2)]
		co_f2r1 = planet_map[str(front2_right1)]
		co_f2 = planet_map[str(front2)]
		co_f2l1 = planet_map[str(front2_left1)]
		co_f2l2 = planet_map[str(front2_left2)]
		co_f1r2 = planet_map[str(front1_right2)]
		co_f1r1 = planet_map[str(front1_right1)]
		co_f1 = planet_map[str(front1)]
		co_f1l1 = planet_map[str(front1_left1)]
		co_f1l2 = planet_map[str(front1_left2)]
		co_r2 = planet_map[str(right2)]
		co_r1 = planet_map[str(right1)]
		co_rover = planet_map[str([x, y])]
		co_l1 = planet_map[str(left1)]
		co_l2 = planet_map[str(left2)]
		co_b1r2 = planet_map[str(back1_right2)]
		co_b1r1 = planet_map[str(back1_right1)]
		co_b1 = planet_map[str(back1)]
		co_b1l1 = planet_map[str(back1_left1)]
		co_b1l2 = planet_map[str(back1_left2)]
		co_b2r2 = planet_map[str(back2_right2)]
		co_b2r1 = planet_map[str(back2_right1)]
		co_b2 = planet_map[str(back2)]
		co_b2l1 = planet_map[str(back2_left1)]
		co_b2l2 = planet_map[str(back2_left2)]
	
		first_lineco = [co_f2l2, co_f2l1, co_f2, co_f2r1, co_f2r2]
		second_lineco = [co_f1l2, co_f1l1, co_f1, co_f1r1, co_f1r2]
		third_lineco = [co_l2, co_l1, co_rover, co_r1, co_r2]
		fourth_lineco = [co_b1l2, co_b1l1, co_b1, co_b1r1, co_b1r2]
		fifth_lineco = [co_b2l2, co_b2l1, co_b2, co_b2r1, co_b2r2]

		first_line = ['|']
		sec_line = ['|']
		third_line = ['|']
		fourth_line = ['|']
		fifth_line = ['|']
		for i in first_lineco:
			if i[2] == '-' and co_rover[2] == '-':
				if int(i[1]) == int(co_rover[1]):
					first_line.append(' |')
				elif int(i[1]) < int(co_rover[1]):
					first_line.append("-|")
				else:
					first_line.append('+|')
			if i[2] == '-' and co_rover[2] != '-':
				if int(co_rover[2]) == int(i[1]):
					first_line.append(' |')
				elif int(co_rover[2]) > int(i[1]):
					first_line.append("-|")
				else:
					if int(i[1]) == int(co_rover[1]):
						first_line.append(' |')
					
					elif int(i[1]) > int(co_rover[1]):
						first_line.append('+|')
			if i[2] != '-' and co_rover[2] == '-':
				if int(co_rover[1]) == int(i[2]):
					first_line.append('/|')
				elif int(co_rover[1]) < int(i[2]):
					first_line.append("+|")
				else:
					if int(i[1]) == int(co_rover[1]):
						first_line.append("\|")
					
					elif int(i[1]) < int(co_rover[1]):
						first_line.append('-|')
			if i[2] != '-' and co_rover[2] != '-':
				if int(i[2]) == int(co_rover[2]):
					first_line.append(' |')
				elif int(i[2]) < int(co_rover[2]):
					if int(co_rover[2]) == int(i[1]):
						first_line.append("'\'|")
					elif int(co_rover[2]) > int(i[1]):
						first_line.append('-|')
				elif int(i[2]) > int(co_rover[2]):
					if int(i[2]) == int(co_rover[1]):
						first_line.append("/|")
					elif int(i[2]) > int(co_rover[1]):
						first_line.append("+|")



		for i in second_lineco:
			if i[2] == '-' and co_rover[2] == '-':
				if int(i[1]) == int(co_rover[1]):
					sec_line.append(' |')
				elif int(i[1]) < int(co_rover[1]):
					sec_line.append("-|")
				else:
					sec_line.append('+|')
			if i[2] == '-' and co_rover[2] != '-':
				if int(co_rover[2]) == int(i[1]):
					sec_line.append(' |')
				elif int(co_rover[2]) > int(i[1]):
					sec_line.append("-|")
				else:
					if int(i[1]) == int(co_rover[1]):
						sec_line.append(' |')
					
					elif int(i[1]) > int(co_rover[1]):
						sec_line.append('+|')
			if i[2] != '-' and co_rover[2] == '-':
				if int(co_rover[1]) == int(i[2]):
					sec_line.append('/|')
				elif int(co_rover[1]) < int(i[2]):
					sec_line.append("+|")
				else:
					if int(i[1]) == int(co_rover[1]):
						sec_line.append("'\'|")
					
					elif int(i[1]) < int(co_rover[1]):
						sec_line.append('-|')
			if i[2] != '-' and co_rover[2] != '-':
				if int(i[2]) == int(co_rover[2]):
					sec_line.append(' |')
				elif int(i[2]) < int(co_rover[2]):
					if int(co_rover[2]) == int(i[1]):
						sec_line.append("'\'|")
					elif int(co_rover[2]) > int(i[1]):
						sec_line.append('-|')
				elif int(i[2]) > int(co_rover[2]):
					if int(i[2]) == int(co_rover[1]):
						sec_line.append("/|")
					elif int(i[2]) > int(co_rover[1]):
						sec_line.append("+|")
	
		for i in third_lineco:
			if i[2] == '-' and co_rover[2] == '-':
				if int(i[1]) == int(co_rover[1]):
					third_line.append(' |')
				elif int(i[1]) < int(co_rover[1]):
					third_line.append("-|")
				else:
					third_line.append('+|')
			if i[2] == '-' and co_rover[2] != '-':
				if int(co_rover[2]) == int(i[1]):
					third_line.append(' |')
				elif int(co_rover[2]) > int(i[1]):
					third_line.append("-|")
				else:
					if int(i[1]) == int(co_rover[1]):
						third_line.append(' |')
					
					elif int(i[1]) > int(co_rover[1]):
						third_line.append('+|')
			if i[2] != '-' and co_rover[2] == '-':
				if int(co_rover[1]) == int(i[2]):
					third_line.append('/|')
				elif int(co_rover[1]) < int(i[2]):
					third_line.append("+|")
				else:
					if int(i[1]) == int(co_rover[1]):
						third_line.append("'\'|")
					
					elif int(i[1]) < int(co_rover[1]):
						third_line.append('-|')
			if i[2] != '-' and co_rover[2] != '-':
				if int(i[2]) == int(co_rover[2]):
					third_line.append(' |')
				elif int(i[2]) < int(co_rover[2]):
					if int(co_rover[2]) == int(i[1]):
						third_line.append("'\'|")
					elif int(co_rover[2]) > int(i[1]):
						third_line.append('-|')
				elif int(i[2]) > int(co_rover[2]):
					if int(i[2]) == int(co_rover[1]):
						third_line.append("/|")
					elif int(i[2]) > int(co_rover[1]):
						third_line.append("+|")
	
		for i in fourth_lineco:
			if i[2] == '-' and co_rover[2] == '-':
				if int(i[1]) == int(co_rover[1]):
					fourth_line.append(' |')
				elif int(i[1]) < int(co_rover[1]):
					fourth_line.append("-|")
				else:
					fourth_line.append('+|')
			if i[2] == '-' and co_rover[2] != '-':
				if int(co_rover[2]) == int(i[1]):
					fourth_line.append(' |')
				elif int(co_rover[2]) > int(i[1]):
					fourth_line.append("-|")
				else:
					if int(i[1]) == int(co_rover[1]):
						fourth_line.append(' |')
					
					elif int(i[1]) > int(co_rover[1]):
						fourth_line.append('+|')
			if i[2] != '-' and co_rover[2] == '-':
				if int(co_rover[1]) == int(i[2]):
					fourth_line.append('/|')
				elif int(co_rover[1]) < int(i[2]):
					fourth_line.append("+|")
				else:
					if int(i[1]) == int(co_rover[1]):
						fourth_line.append("'\'|")
					
					elif int(i[1]) < int(co_rover[1]):
						fourth_line.append('-|')
			if i[2] != '-' and co_rover[2] != '-':
				if int(i[2]) == int(co_rover[2]):
					fourth_line.append(' |')
				elif int(i[2]) < int(co_rover[2]):
					if int(co_rover[2]) == int(i[1]):
						fourth_line.append("'\'|")
					elif int(co_rover[2]) > int(i[1]):
						fourth_line.append('-|')
				elif int(i[2]) > int(co_rover[2]):
					if int(i[2]) == int(co_rover[1]):
						fourth_line.append("/|")
					elif int(i[2]) > int(co_rover[1]):
						fourth_line.append("+|")
	
		for i in fifth_lineco:
			if i[2] == '-' and co_rover[2] == '-':
				if int(i[1]) == int(co_rover[1]):
					fifth_line.append(' |')
				elif int(i[1]) < int(co_rover[1]):
					fifth_line.append("-|")
				else:
					fifth_line.append('+|')
			if i[2] == '-' and co_rover[2] != '-':
				if int(co_rover[2]) == int(i[1]):
					fifth_line.append(' |')
				elif int(co_rover[2]) > int(i[1]):
					fifth_line.append("-|")
				else:
					if int(i[1]) == int(co_rover[1]):
						fifth_line.append(' |')
					
					elif int(i[1]) > int(co_rover[1]):
						fifth_line.append('+|')
			if i[2] != '-' and co_rover[2] == '-':
				if int(co_rover[1]) == int(i[2]):
					fifth_line.append('/|')
				elif int(co_rover[1]) < int(i[2]):
					fifth_line.append("+|")
				else:
					if int(i[1]) == int(co_rover[1]):
						fifth_line.append("'\'|")
					
					elif int(i[1]) < int(co_rover[1]):
						fifth_line.append('-|')
			if i[2] != '-' and co_rover[2] != '-':
				if int(i[2]) == int(co_rover[2]):
					fifth_line.append(' |')
				elif int(i[2]) < int(co_rover[2]):
					if int(co_rover[2]) == int(i[1]):
						fifth_line.append("'\'|")
					elif int(co_rover[2]) > int(i[1]):
						fifth_line.append('-|')
				elif int(i[2]) > int(co_rover[2]):
					if int(i[2]) == int(co_rover[1]):
						fifth_line.append("/|")
					elif int(i[2]) > int(co_rover[1]):
						fifth_line.append("+|")
		third_line2 = []
	
		for n, i in enumerate(third_line):
			if n == 3:
				a = "H|"
				 
				third_line2.append(a)
			else:
				third_line2.append(i)
		number1_line = "\n{}\n{}\n{}\n{}\n{}\n".format("".join(fifth_line), "".join(fourth_line), "".join(third_line2),"".join(sec_line) , "".join(first_line))
		
		return number1_line




		pass
	
	def is_shaded(self):
		"""
		Returns True if the terrain tile is shaded, otherwise False
		"""
		pass
	
	def set_occupant(self, obj):
		"""
		Sets the occupant on the terrain tile
		"""
		pass
	
	def get_occupant(self):
		"""
		Gets the entity on the terrain tile
		If nothing is on this tile, it should return None
		"""
		pass
	
	
