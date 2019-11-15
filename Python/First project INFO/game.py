import os
import os.path
from terrain import Tile
from planet import Planet
from rover import Rover
#from loader import Loading
#from loader import Menu


name = []

def game_finish(no_name_level, battery, name): #width height tile rover x y, planet name list

	map_len = len(no_name_level[2])
	planet_name = name[0]
	rover = int((int(no_name_level[-1])*100 / map_len))
	

	print("\nYou explored {}% of {}\n".format(rover, planet_name))

	quit()

	

	pass

def stats(no_name_level, battery):

	map_len = len(no_name_level[2])
	planet_name = name[0]
	rover = int((int(no_name_level[-1])*100 / map_len))

	return "\nExplored: {}%\nBattery: {}/100\n".format(rover, battery)




def scanning(no_name_level, battery):#width height tile rover x y list
	width = no_name_level[0]
	height = no_name_level[1]
	tile = no_name_level[2]
	x = no_name_level[3]
	y = no_name_level[4]
	
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

	x1 = 0
	x2 = 1
	y1 = 0
	y2 = 1



	if x_value + 1 < len(coordinates[1])-1:
		x1 += x_value + 1

	if y_value + 1 < len(coordinates)-1:
		y1 += y_value + 1

	if x_value + 1 < len(coordinates[1])-1:
		x2 += x_value + 1
	if y_value + 1 < len(coordinates)-1:
		y2 += y_value + 1

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
	co_rover = planet_map[str(coordinates[y_value][x_value])]
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
		if i[0] == 'shaded':
			first_line.append('#|')
		else:
			first_line.append(' |')

	for i in second_lineco:
		if i[0] == 'shaded':
			sec_line.append('#|')
		else:
			sec_line.append(' |')

	for i in third_lineco:
		if i[0] == 'shaded':
			third_line.append('#|')
		else:
			third_line.append(' |')

	for i in fourth_lineco:
		if i[0] == 'shaded': 
			fourth_line.append('#|')
		else:
			fourth_line.append(' |')

	for i in fifth_lineco:
		if i[0] == 'shaded':
			fifth_line.append('#|')
		else:
			fifth_line.append(' |')
	third_line2 = []

	for n, i in enumerate(third_line):
		if n == 3:
			a = "H|"
			 
			third_line2.append(a)
		else:
			third_line2.append(i)
	number1_line = "\n{}\n{}\n{}\n{}\n{}\n".format("".join(fifth_line), "".join(fourth_line), "".join(third_line2),"".join(sec_line) , "".join(first_line))

	choice_change = False

	

	while not choice_change:
		choice = input()

		if choice == "FINISH" or choice == "finish":
			choice_change == True


			return game_finish(no_name_level, battery, name)

		elif choice == "STATS":

			 print(stats(no_name_level, battery))

		elif choice.startswith("SCAN"):
			try:
				choice = choice.split(" ")
				part2 = choice[1]

			except IndexError:
				print("\nCannot perform this command\n")
				return scanning(no_name_level, battery)

			if part2 == "shade":
				print(number1_line)
			elif part2 == "elevation":
				print(Tile.elevation(Tile(no_name_level)))
			else:
				print("\nCannot perform this command\n")
				return scanning(no_name_level, battery)
		elif choice.startswith("MOVE W ") or choice.startswith("MOVE N ") or choice.startswith("MOVE E ") or choice.startswith("MOVE S "):
			choice_change == False
			choice = choice.split(" ")
			part2 = choice[1]
			part3 = choice[2]

			try:
				int(part3)

			except ValueError:
				print("\nCannot perform this command\n")
				return scanning(no_name_level, battery)
			if part2 == "N" or part2 == "S" or part2 == "E" or part2 == "W":
				choice_change == False
				
			
				file = Rover(no_name_level, battery)
				data = file.move(part2, int(part3))
				no_name_level2 = [data[0], data[1], data[2], data[3], data[4]]
				
				return scanning(no_name_level2, data[6])

		else:
			print("\nCannot perform this command\n")
			return scanning(no_name_level, battery)

		
	

	return "a"



	pass



def quit():
	"""
	Will quit the program
	"""

	exit()
	pass
	
def menu_help():
	"""
	Displays the help menu of the game
	"""

	print("\nSTART <level file> - Starts the game with a provided file.\nQUIT - Quits the game\nHELP - Shows this message\n")
	choice = input() #print out the help option and then ask for input to put it into the start function
	choice = Menu(choice)
	return choice.menu()
	pass

def menu_start_game(filepath):
	"""
	Will start the game with the given file path
	"""

	file_level = Loading(filepath) #goes to the Loading function
	file_level = file_level.load_level()#contains planet name, planet width, planet height, tiles, rover x and y in a list

	x = file_level[4] #x value and y value of rover
	y = file_level[5]

	name1 = file_level[0]
	name.append(name1) #put it into a list so we can use it in the end
	battery = 100 #the start of the game is always with 100% battery
	no_name_level =[file_level[1], file_level[2], file_level[3], x, y, file_level[0], 0, battery, 1]#width height tile rover x y, planet name list
	
	
	
	scan = scanning(no_name_level, battery) #bringing those info to the next function
	
	return scan


	
	pass

def back(choice):
	if choice != "quit" or choice != "help" or choice != "start":
		
		print("\nNo menu item\n") #it print the necessary text

		choice2 = input() # ask for an input again
		choice2 = Menu(choice2)
		return choice2.menu() # send it to the menu function
	pass
	

class Menu:

	def __init__(self, choice):
		self.choice = choice# the very first input

		pass
	def menu(self):
		"""
		Start the menu component of the game
		"""
		
		if self.choice == "Quit" or self.choice == "quit" or self.choice == "QUIT":
			
			return quit() # if it is quit...then qoes to the quit function
		
		if self.choice == "help" or self.choice == "HELP" or self.choice == "Help":
			return menu_help() #goes to the help function
		if self.choice.startswith("start ") or self.choice.startswith("Start ") or self.choice.startswith("START "):
				self.choice = self.choice.split(' ') #it splits the the file
				menu_start_game(self.choice[1]) # put the file path into the function
			
		else:

			return back(self.choice) #if anything else other than those answers, it will goes to the back function
		
		pass

class Loading:

	def __init__(self, filepath):

		self.filepath = filepath

		pass

	def load_level(self):
		"""
		Loads the level and returns an object of your choosing
		"""
		try:
			with open(self.filepath, 'r') as a:
				level_file = a.readlines() #tries to open the file

		except FileNotFoundError:
			print("\nLevel file could not be found\n")

			choice = input()
			choice = Menu(choice)
			return choice.menu()#if it can't then it will return to the menu start after asking for input
		other = []

		for n in level_file[7:]: #get rid of the unnnecessary parts of the tile part
			if ',' in n:
				other.append(n)

		if level_file[6] != '[tiles]\n':
		
			print("\nUnable to load level file\n")
			choice = input()
			choice = Menu(choice)
			return choice.menu()
	
		field1 = level_file[2][:-1]# we know the 3rd row has the width and in the end of it \n. So we get rid of it.
		field1 = field1.split(',')#split it based on comma so we can keep the negatie sign if we have.
		field2 = level_file[3][:-1]#this is the same but with height
		field2 =field2.split(',')
		planet_name = level_file[1][:-1]
		planet_name = planet_name.split(',')
		planet_name = planet_name[1]

		width = int(field1[-1])
		height = int(field2[-1])
		if width < 5: #mustbe at least 5 unit width
			print("\nUnable to load level file\n")
			choice = input()
			choice = Menu(choice)
			return choice.menu()
		if height < 5:#must be at least 5 unit width
			print("\nUnable to load level file\n")
			choice = input()
			choice = Menu(choice)
			return choice.menu()

		max_tiles = width * height
		if len(other) != max_tiles: # must be exactly the same dimension
			print("\nUnable to load level file\n")
			choice = input()
			choice = Menu(choice)
			return choice.menu()
		rover = level_file[4][:-1].split(",")# we left out the \n
		x = int(rover[-2]) #rover x and y coordinates
		y = int(rover[-1])
		if x > width or x < 0: #cant be negative and less then the map coordinates
			print("\nUnable to load level file\n")
			choice = input()
			choice = Menu(choice)
			return choice.menu()
		if y > height or y < 0:
			print("\nUnable to load level file\n")
			choice = input()
			choice = Menu(choice)
			return choice.menu()
		tile = level_file[7:]# data about the tile
		for i in tile: #checking all the rows
			i = i.split(',')#separate the numbers
			if len(i) == 3:
				if int(i[-2]) <= int(i[-1]):#first is the highest elevation second is the lowest
					print("\nUnable to load level file\n")
					choice = input()
					choice = Menu(choice)
					return choice.menu()
		data = [planet_name, width, height, tile, x, y] #put all the data into a list

		return data

		pass








choice = input()

choice = Menu(choice)



choice.menu()