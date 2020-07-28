from planet import Planet
from planet import PLanet2


def next1(no_name_level, length, step, battery): ##width height tile rover x y list


	
	
	rover_map = []
	

	width = no_name_level[0]
	height = no_name_level[1]
	tile = no_name_level[2]
	x = no_name_level[3]
	y = no_name_level[4]

	rover_coordinates = [x, y]
	
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




	
	

	for i in coordinates:
		for n in i:
			if n == rover_coordinates:
				x_index = i.index(n)
				y_index = coordinates.index(i)


	

	

	if length != 0:
		while length != 0:
		

			u_elevation = planet_map[str(coordinates[y_index-1][x_index])][1]
			l_elevation = planet_map[str(coordinates[y_index-1][x_index])][2]
			ur_elevation = planet_map[str(coordinates[y_index-1][x_index])][1]
			lr_elevation = planet_map[str(coordinates[y_index-1][x_index])][2]
			terrain_type = planet_map[str(coordinates[y_index-1][x_index])][0]

			if l_elevation == '-' and lr_elevation == '-':
				if int(u_elevation) == int(ur_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						battery += -1
						step += 1
						length += -1
						new_xindex = coordinates[y_index-1][x_index][0]
						new_yindex = coordinates[y_index-1][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						return next1(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index-1][x_index][0]
						new_yindex = coordinates[y_index-1][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						
						return next1(new_level , length, step, battery)
						

				elif int(u_elevation) < int(ur_elevation):
					#first_line.append("-|")
					
					length == 0
					
					break

				else:
					#first_line.append('+|')
					length == 0
					
					
					break
			if l_elevation == '-' and lr_elevation != '-':
				if int(lr_elevation) == int(u_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						battery += -1
						length += -1
						new_xindex = coordinates[y_index-1][x_index][0]
						new_yindex = coordinates[y_index-1][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						return next1(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index-1][x_index][0]
						new_yindex = coordinates[y_index-1][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						
						return next1(new_level , length, step, battery)

				elif int(lr_elevation) > int(u_elevation):
					#first_line.append("-|")
					length == 0
					
					break
				else:
					if int(u_elevation) == int(ur_elevation):
						#first_line.append(' |')
						if terrain_type == "shaded":
							battery += -1
							step += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							length += -1
							new_xindex = coordinates[y_index-1][x_index][0]
							new_yindex = coordinates[y_index-1][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							return next1(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index-1][x_index][0]
							new_yindex = coordinates[y_index-1][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							
							return next1(new_level , length, step, battery)
						
						elif int(u_elevation) > int(ur_elevation):
							#first_line.append('+|')
							length == 0
							
							break
						
			if l_elevation != '-' and lr_elevation == '-':
				if int(ur_elevation) == int(l_elevation):
					#first_line.append('/|')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						battery += -1
						length += -1
						new_xindex = coordinates[y_index-1][x_index][0]
						new_yindex = coordinates[y_index-1][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						return next1(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index-1][x_index][0]
						new_yindex = coordinates[y_index-1][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						
						return next1(new_level , length, step, battery)
				elif int(ur_elevation) < int(l_elevation):
					#first_line.append("+|")
					self.length == 0
					
					break
					
				else:
					if int(u_elevation) == int(ur_elevation):
						#first_line.append('"\"|')
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							battery += -1
							new_xindex = coordinates[y_index-1][x_index][0]
							new_yindex = coordinates[y_index-1][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							return next1(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index-1][x_index][0]
							new_yindex = coordinates[y_index-1][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							
							return next1(new_level , length, step, battery)
						
					elif int(u_elevation) < int(ur_elevation):
						#first_line.append('-|')
						self.length == 0
						
						break
						
			if l_elevation != '-' and lr_elevation != '-':
				if int(l_elevation) == int(lr_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						battery += -1
						length += -1
						new_xindex = coordinates[y_index-1][x_index][0]
						new_yindex = coordinates[y_index-1][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						return next1(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index-1][x_index][0]
						new_yindex = coordinates[y_index-1][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						
						return next1(new_level , length, step, battery)
				elif int(l_elevation) < int(lr_elevation):
					if int(co_rover[2]) == int(i[1]):
						#first_line.append("'\'|")
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							battery += -1
							new_xindex = coordinates[y_index-1][x_index][0]
							new_yindex = coordinates[y_index-1][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							return next1(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index-1][x_index][0]
							new_yindex = coordinates[y_index-1][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							
							return next1(new_level , length, step, battery)
						
				elif int(l_elevation) > int(lr_elevation):
					if int(l_elevation) == int(ur_elevation):
						#first_line.append("/|")
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1

							battery += -1
							new_xindex = coordinates[y_index-1][x_index][0]
							new_yindex = coordinates[y_index-1][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							return next1(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index-1][x_index][0]
							new_yindex = coordinates[y_index-1][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							
							return next1(new_level , length, step, battery)
					elif int(l_elevation) > int(ur_elevation):
						#first_line.append("+|")
						self.length == 0
						
						break
	if length == 0:
		#width height tile rover x y step and shades
		para = PLanet2(coordinates[y_index-1][x_index])
		new_level = [width, height, tile, coordinates[y_index][x_index][0], coordinates[y_index][x_index][1],  step, battery, para]
		return new_level

	pass



def next2(no_name_level, length, step, battery): ##width height tile rover x y list


	
	
	rover_map = []
	

	width = no_name_level[0]
	height = no_name_level[1]
	tile = no_name_level[2]
	x = no_name_level[3]
	y = no_name_level[4]

	rover_coordinates = [x, y]
	
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




	
	

	for i in coordinates:
		for n in i:
			if n == rover_coordinates:
				x_index = i.index(n)
				y_index = coordinates.index(i)


	

	

	if length != 0:
		while length != 0:
			y_index2 = 0
			if y_index < len(coordinates[1])-1:
				y_index2 += y_index + 1
		

			u_elevation = planet_map[str(coordinates[y_index2][x_index])][1]
			l_elevation = planet_map[str(coordinates[y_index2][x_index])][2]
			ur_elevation = planet_map[str(coordinates[y_index2][x_index])][1]
			lr_elevation = planet_map[str(coordinates[y_index2][x_index])][2]
			terrain_type = planet_map[str(coordinates[y_index2][x_index])][0]

			if l_elevation == '-' and lr_elevation == '-':
				if int(u_elevation) == int(ur_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						new_xindex = coordinates[y_index2][x_index][0]
						new_yindex = coordinates[y_index2][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						return next2(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index2][x_index][0]
						new_yindex = coordinates[y_index2][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						
						return next2(new_level , length, step,battery)
						

				elif int(u_elevation) < int(ur_elevation):
					#first_line.append("-|")
					length == 0
					
					break

				else:
					#first_line.append('+|')
					length == 0
					
					new_level = [width, height, tile, coordinates[y_index][x_index][0], coordinates[y_index][x_index][1],  step,battery]
					return new_level
					break
			if l_elevation == '-' and lr_elevation != '-':
				if int(lr_elevation) == int(u_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						new_xindex = coordinates[y_index2][x_index][0]
						new_yindex = coordinates[y_index2][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						return next2(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index2][x_index][0]
						new_yindex = coordinates[y_index2][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						
						return next2(new_level , length, step, battery)

				elif int(lr_elevation) > int(u_elevation):
					#first_line.append("-|")
					length == 0
					
					break
				else:
					if int(u_elevation) == int(ur_elevation):
						#first_line.append(' |')
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							new_xindex = coordinates[y_index2][x_index][0]
							new_yindex = coordinates[y_index2][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							return next2(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index2][x_index][0]
							new_yindex = coordinates[y_index2][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							
							return next2(new_level , length, step, battery)
						
						elif int(u_elevation) > int(ur_elevation):
							#first_line.append('+|')
							length == 0
						
							break
						
			if l_elevation != '-' and lr_elevation == '-':
				if int(ur_elevation) == int(l_elevation):
					#first_line.append('/|')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						new_xindex = coordinates[y_index2][x_index][0]
						new_yindex = coordinates[y_index2][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						return next2(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index2][x_index][0]
						new_yindex = coordinates[y_index2][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						
						return next2(new_level , length, step, battery)
				elif int(ur_elevation) < int(l_elevation):
					#first_line.append("+|")
					self.length == 0
					
					break
					
				else:
					if int(u_elevation) == int(ur_elevation):
						#first_line.append('"\"|')
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							new_xindex = coordinates[y_index2][x_index][0]
							new_yindex = coordinates[y_index2][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							return next2(new_level , length, step,battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index2][x_index][0]
							new_yindex = coordinates[y_index2][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							
							return next2(new_level , length, step,battery)
						
					elif int(u_elevation) < int(ur_elevation):
						#first_line.append('-|')
						self.length == 0
						
						break
						
			if l_elevation != '-' and lr_elevation != '-':
				if int(l_elevation) == int(lr_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						new_xindex = coordinates[y_index2][x_index][0]
						new_yindex = coordinates[y_index2][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						return next2(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						new_xindex = coordinates[y_index2][x_index][0]
						new_yindex = coordinates[y_index2][x_index][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						
						return next2(new_level , length, step, battery)
				elif int(l_elevation) < int(lr_elevation):
					if int(co_rover[2]) == int(i[1]):
						#first_line.append("'\'|")
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							new_xindex = coordinates[y_index2][x_index][0]
							new_yindex = coordinates[y_index2][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							return next2(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index2][x_index][0]
							new_yindex = coordinates[y_index2][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							
							return next2(new_level , length, step, battery)
						
				elif int(l_elevation) > int(lr_elevation):
					if int(l_elevation) == int(ur_elevation):
						#first_line.append("/|")
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							new_xindex = coordinates[y_index2][x_index][0]
							new_yindex = coordinates[y_index2][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							return next2(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index2][x_index][0]
							new_yindex = coordinates[y_index2][x_index][1]
							new_level = [width, height, tile, new_xindex, new_yindex]
							
							return next2(new_level , length, step, battery)
					elif int(l_elevation) > int(ur_elevation):
						#first_line.append("+|")
						self.length == 0
						
						break
	if length == 0:
		#width height tile rover x y step and shades
		para = PLanet2(coordinates[y_index-1][x_index])
		new_level = [width, height, tile, coordinates[y_index][x_index][0], coordinates[y_index][x_index][1],  step, battery, para]
		return new_level

	pass



def next3(new_noname3 , length, step, battery):#width height tile rover x y list


	width = new_noname3[0]
	height = new_noname3[1]
	tile = new_noname3[2]
	x = new_noname3[3]
	y = new_noname3[4]
	
	rover_coordinates = [x, y]



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




	
	

	for i in coordinates:
		for n in i:
			if n == rover_coordinates:
				x_index = i.index(n)
				y_index = coordinates.index(i)

	for i in coordinates:
		for n in i:
			if n == rover_coordinates:
				x_index = i.index(n)
				y_index = coordinates.index(i)

	x_index2 = x_index + 1

	


	if length != 0:
		while length != 0:
		
			x_index2 = 0
			if x_index < len(coordinates[1])-1:
				x_index2 += x_index + 1



			u_elevation = planet_map[str(coordinates[y_index][x_index2])][1]
			l_elevation = planet_map[str(coordinates[y_index][x_index2])][2]
			ur_elevation = planet_map[str(coordinates[y_index][x_index2])][1]
			lr_elevation = planet_map[str(coordinates[y_index][x_index2])][2]
			terrain_type = planet_map[str(coordinates[y_index][x_index2])][0]

			if l_elevation == '-' and lr_elevation == '-':
				if int(u_elevation) == int(ur_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						new_xindex = coordinates[y_index][x_index2][0]
						new_yindex = coordinates[y_index][x_index2][1]
						new_level = [width, height, tile, new_xindex, y]
						return next3(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index][x_index2][0]
						new_yindex = coordinates[y_index][x_index2][1]
						new_level = [width, height, tile, new_xindex, y]
						
						return next3(new_level , length, step, battery)
						

				elif int(u_elevation) < int(ur_elevation):
					#first_line.append("-|")
					length == 0
					
					break

				else:
					#first_line.append('+|')
					length == 0
					
					
					break
			if l_elevation == '-' and lr_elevation != '-':
				if int(lr_elevation) == int(u_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						new_xindex = coordinates[y_index][x_index2][0]
						new_yindex = coordinates[y_index][x_index2][1]
						new_level = [width, height, tile, new_xindex, new_yindex]
						return next3(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						battery += 1
						length += -1
						new_xindex = coordinates[y_index][x_index2][0]
						new_yindex = coordinates[y_index][x_index2][1]
						new_level = [width, height, tile, new_xindex, y]
						
						return next3(new_level , length, step, battery)

				elif int(lr_elevation) > int(u_elevation):
					#first_line.append("-|")
					length == 0
					
					break
				else:
					if int(u_elevation) == int(ur_elevation):
						#first_line.append(' |')
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							new_xindex = coordinates[y_index][x_index2][0]
							new_yindex = coordinates[y_index2][x_index2][1]
							new_level = [width, height, tile, new_xindex, y]
							return next3(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index][x_index2][0]
							new_yindex = coordinates[y_index][x_index2][1]
							new_level = [width, height, tile, new_xindex, y]
							
							return next3(new_level , length, step, battery)
						
						elif int(u_elevation) > int(ur_elevation):
							#first_line.append('+|')
							length == 0
							
							break
						
			if l_elevation != '-' and lr_elevation == '-':
				if int(ur_elevation) == int(l_elevation):
					#first_line.append('/|')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						new_xindex = coordinates[y_index][x_index2][0]
						new_yindex = coordinates[y_index][x_index2][1]
						new_level = [width, height, tile, new_xindex, y]
						return next3(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						battery += 1
						length += -1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index][x_index2][0]
						new_yindex = coordinates[y_index2][x_index2][1]
						new_level = [width, height, tile, new_xindex, y]
						
						return next3(new_level , length, step, battery)
				elif int(ur_elevation) < int(l_elevation):
					#first_line.append("+|")
					self.length == 0
					
					break
					
				else:
					if int(u_elevation) == int(ur_elevation):
						#first_line.append('"\"|')
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							new_xindex = coordinates[y_index][x_index2][0]
							new_yindex = coordinates[y_index][x_index2][1]
							new_level = [width, height, tile, new_xindex, y]
							return next3(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index][x_index2][0]
							new_yindex = coordinates[y_index][x_index2][1]
							new_level = [width, height, tile, new_xindex, y]
							
							return next3(new_level , length, step, battery)
						
					elif int(u_elevation) < int(ur_elevation):
						#first_line.append('-|')
						self.length == 0
						
						break
						
			if l_elevation != '-' and lr_elevation != '-':
				if int(l_elevation) == int(lr_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						new_xindex = coordinates[y_index][x_index2][0]
						new_yindex = coordinates[y_index][x_index2][1]
						new_level = [width, height, tile, new_xindex, y]
						return next3(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index][x_index2][0]
						new_yindex = coordinates[y_index][x_index2][1]
						new_level = [width, height, tile, new_xindex, y]
						
						return next3(new_level , length, step, battery)
				elif int(l_elevation) < int(lr_elevation):
					if int(co_rover[2]) == int(i[1]):
						#first_line.append("'\'|")
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							new_xindex = coordinates[y_index][x_index2][0]
							new_yindex = coordinates[y_index][x_index2][1]
							new_level = [width, height, tile, new_xindex, y]
							return next3(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index][x_index2][0]
							new_yindex = coordinates[y_index][x_index2][1]
							new_level = [width, height, tile, new_xindex, y]
							
							return next3(new_level , length, step,battery)
						
				elif int(l_elevation) > int(lr_elevation):
					if int(l_elevation) == int(ur_elevation):
						#first_line.append("/|")
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							new_xindex = coordinates[y_index][x_index2][0]
							new_yindex = coordinates[y_index][x_index2][1]
							new_level = [width, height, tile, new_xindex, y]
							return next3(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index][x_index2][0]
							new_yindex = coordinates[y_index][x_index2][1]
							new_level = [width, height, tile, new_xindex, y]
							
							return next3(new_level , length, step, battery)
					elif int(l_elevation) > int(ur_elevation):
						#first_line.append("+|")
						self.length == 0
						
						break
	if length == 0:
		#width height tile rover x y step and shades
		para = PLanet2(coordinates[y_index-1][x_index])
		new_level = [width, height, tile, coordinates[y_index][x_index][0], y,  step, battery, para]
		return new_level

	pass

def next4(new_noname3 , length, step, battery):#width height tile rover x y list


	width = new_noname3[0]
	height = new_noname3[1]
	tile = new_noname3[2]
	x = new_noname3[3]
	y = new_noname3[4]
	
	rover_coordinates = [x, y]



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




	
	

	for i in coordinates:
		for n in i:
			if n == rover_coordinates:
				x_index = i.index(n)
				y_index = coordinates.index(i)

	for i in coordinates:
		for n in i:
			if n == rover_coordinates:
				x_index = i.index(n)
				y_index = coordinates.index(i)

	x_index2 = x_index + 1

	


	if length != 0:
		while length != 0:
		
			

			u_elevation = planet_map[str(coordinates[y_index][x_index-1])][1]
			l_elevation = planet_map[str(coordinates[y_index][x_index-1])][2]
			ur_elevation = planet_map[str(coordinates[y_index][x_index-1])][1]
			lr_elevation = planet_map[str(coordinates[y_index][x_index-1])][2]
			terrain_type = planet_map[str(coordinates[y_index][x_index-1])][0]

			if l_elevation == '-' and lr_elevation == '-':
				if int(u_elevation) == int(ur_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						
						new_xindex = coordinates[y_index][x_index-1][0]
						new_yindex = coordinates[y_index][x_index-1][1]
						new_level = [width, height, tile, new_xindex, y]
						return next4(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index][x_index-1][0]
						new_yindex = coordinates[y_index][x_index-1][1]
						new_level = [width, height, tile, new_xindex, y]
						
						return next4(new_level , length, step, battery)
						

				elif int(u_elevation) < int(ur_elevation):
					#first_line.append("-|")
					length == 0
					
					break

				else:
					#first_line.append('+|')
					length == 0
					
					new_level = [width, height, tile, coordinates[y_index][x_index][0], y,  step, battery]
					return new_level
					break
			if l_elevation == '-' and lr_elevation != '-':
				if int(lr_elevation) == int(u_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						
						new_xindex = coordinates[y_index][x_index-1][0]
						new_yindex = coordinates[y_index][x_index-1][1]
						new_level = [width, height, tile, new_xindex, y]
						return next4(new_level , length, step, battery2)
					elif terrain_type != "shaded":
						step += 1
						length += -1
						battery += 1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index][x_index-1][0]
						new_yindex = coordinates[y_index][x_index-1][1]
						new_level = [width, height, tile, new_xindex, y]
						
						return next4(new_level , length, step, battery)

				elif int(lr_elevation) > int(u_elevation):
					#first_line.append("-|")
					length == 0
					
					break
				else:
					if int(u_elevation) == int(ur_elevation):
						#first_line.append(' |')
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							
							new_xindex = coordinates[y_index][x_index-1][0]
							new_yindex = coordinates[y_index][x_index-1][1]
							new_level = [width, height, tile, new_xindex, y]
							return next4(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index][x_index-1][0]
							new_yindex = coordinates[y_index][x_index-1][1]
							new_level = [width, height, tile, new_xindex, y]
							
							return next4(new_level , length, step, battery)
						
						elif int(u_elevation) > int(ur_elevation):
							#first_line.append('+|')
							length == 0
							
							break
						
			if l_elevation != '-' and lr_elevation == '-':
				if int(ur_elevation) == int(l_elevation):
					#first_line.append('/|')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						
						new_xindex = coordinates[y_index][x_index-1][0]
						new_yindex = coordinates[y_index][x_index-1][1]
						new_level = [width, height, tile, new_xindex, y]
						return next4(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						battery += 1
						length += -1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index][x_index-1][0]
						new_yindex = coordinates[y_index][x_index-1][1]
						new_level = [width, height, tile, new_xindex, y]
						
						return next4(new_level , length, step, battery)
				elif int(ur_elevation) < int(l_elevation):
					#first_line.append("+|")
					self.length == 0
					
					break
					
				else:
					if int(u_elevation) == int(ur_elevation):
						#first_line.append('"\"|')
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							
							new_xindex = coordinates[y_index][x_index-1][0]
							new_yindex = coordinates[y_index][x_index-1][1]
							new_level = [width, height, tile, new_xindex, y]
							return next4(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index][x_index-1][0]
							new_yindex = coordinates[y_index][x_index-1][1]
							new_level = [width, height, tile, new_xindex, y]
							
							return next4(new_level , length, step, battery)
						
					elif int(u_elevation) < int(ur_elevation):
						#first_line.append('-|')
						self.length == 0
						
						break
						
			if l_elevation != '-' and lr_elevation != '-':
				if int(l_elevation) == int(lr_elevation):
					#first_line.append(' |')
					if terrain_type == "shaded":
						para = PLanet2(coordinates[y_index-1][x_index])
						step += 1
						length += -1
						
				
						new_xindex = coordinates[y_index][x_index-1][0]
						new_yindex = coordinates[y_index][x_index-1][1]
						new_level = [width, height, tile, new_xindex, y]
						return next4(new_level , length, step, battery)
					elif terrain_type != "shaded":
						step += 1
						battery += 1
						length += -1
						para = PLanet2(coordinates[y_index-1][x_index])
						new_xindex = coordinates[y_index][x_index-1][0]
						new_yindex = coordinates[y_index][x_index-1][1]
						new_level = [width, height, tile, new_xindex, y]
						
						return next4(new_level , length, step, battery)
				elif int(l_elevation) < int(lr_elevation):
					if int(co_rover[2]) == int(i[1]):
						#first_line.append("'\'|")
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							
							new_xindex = coordinates[y_index][x_index-1][0]
							new_yindex = coordinates[y_index][x_index-1][1]
							new_level = [width, height, tile, new_xindex, y]
							return next4(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							length += -1
							battery += 1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index][x_index-1][0]
							new_yindex = coordinates[y_index][x_index-1][1]
							new_level = [width, height, tile, new_xindex, y]
							
							return next4(new_level , length, step, battery)
						
				elif int(l_elevation) > int(lr_elevation):
					if int(l_elevation) == int(ur_elevation):
						#first_line.append("/|")
						if terrain_type == "shaded":
							para = PLanet2(coordinates[y_index-1][x_index])
							step += 1
							length += -1
							
							new_xindex = coordinates[y_index][x_index-1][0]
							new_yindex = coordinates[y_index][x_index-1][1]
							new_level = [width, height, tile, new_xindex, y]
							return next4(new_level , length, step, battery)
						elif terrain_type != "shaded":
							step += 1
							battery += 1
							length += -1
							para = PLanet2(coordinates[y_index-1][x_index])
							new_xindex = coordinates[y_index][x_index-1][0]
							new_yindex = coordinates[y_index][x_index-1][1]
							new_level = [width, height, tile, new_xindex, y]
							
							return next4(new_level , length, step, battery)
					elif int(l_elevation) > int(ur_elevation):
						#first_line.append("+|")
						self.length == 0
						
						break
	if length == 0:
		#width height tile rover x y step and shades
		para = PLanet2(coordinates[y_index-1][x_index])
		new_level = [width, height, tile, coordinates[y_index][x_index][0], y,  step, battery, para]
		return new_level

	pass