import sys
from math import *
import operator
from random import randrange
from playsound import playsound
neighbours = {(0,0):[3,4,5,6],(1,0):[3,8],(1,1):[2,4,9,1],(1,2):[1,3,5,10],(1,3):[1,4,6,11],(1,4):[1,5,7,12],(1,5):[6,13],(2,0):[2,9,14],(2,1):[3,8,10,15],(2,2):[4,9,11,16],(2,3):[5,10,12,17],(2,4):[6,11,13,18],(2,5):[7,12,19],(3,0):[8,15],(3,1):[9,14,16,20],(3,2):[10,15,17,21],(3,3):[11,16,18,22],(3,4):[12,17,19,23],(3,5):[13,18],(4,0):[15,21],(4,1):[16,20,22],(4,2):[17,21,23],(4,3):[18,22]}

tiger_jumps = {(0,0):[9,10,11,12],(1,0):[4,14],(1,1):[5,15],(1,2):[2,6,16],(1,3):[3,17,7],(1,4):[4,18],(1,5):[5,19],(2,0):[10],(2,1):[1,11,20],(2,2):[8,1,12,21],(2,3):[1,9,13,22],(2,4):[1,10,23],(2,5):[11],(3,0):[2,16],(3,1):[3,17],(3,2):[4,14,18],(3,3):[5,15,19],(3,4):[6,16],(3,5):[7,17],(4,0):[9,22],(4,1):[10,23],(4,2):[11,20],(4,3):[12,21]}

positions = {1:(0,0),2:(1,0),3:(1,1),4:(1,2),5:(1,3),6:(1,4),7:(1,5),8:(2,0),9:(2,1),10:(2,2),11:(2,3),12:(2,4),13:(2,5),14:(3,0),15:(3,1),16:(3,2),17:(3,3),18:(3,4),19:(3,5),20:(4,0),21:(4,1),22:(4,2),23:(4,3)}

reversed_positions = {}

for i in range(1,24):
	reversed_positions[positions[i]] = i

default = [[1],[2,3,4,5,6,7],[8,9,10,11,12,13],[14,15,16,17,18,19],[20,21,22,23]]
board_matrix = [['*'],['*','*','*','*','*','*'],['*','*','*','*','*','*'],['*','*','*','*','*','*'],['*','*','*','*']]
tiger_list = [1,4,5]
dead_goats = []
def print_board():
	print  "              "+(str(board_matrix[0]).strip("[]")).replace(",","")
	print "    "+(str(board_matrix[1]).strip("[]")).replace(",","")
	print "  "+(str(board_matrix[2]).strip("[]")).replace(",","")
	print " "+(str(board_matrix[3]).strip("[]")).replace(",","")
	print "   "+(str(board_matrix[4]).strip("[]")).replace(",","")


goat_counter=1

def position_placer():
	global goat_counter
	if goat_counter > 16:
		move_goat()
	else:
		print "please enter the position to place a goat"
		choose_goat_position=raw_input()
		if choose_goat_position.isdigit():
			choose_goat_position = int(choose_goat_position)
			int_to_tuples = positions[choose_goat_position]
			if (board_matrix[int_to_tuples[0]][int_to_tuples[1]] == '*'):
				board_matrix[int_to_tuples[0]][int_to_tuples[1]] = 'G'+str(goat_counter)
				goat_counter+=1
			else:
				print("the position is occupied!!! Please choose another")
				position_placer()
		else:
			print("INVALID ENTRY")
			position_placer()


def check_end():
	if len(dead_goats)==6:
		print "Tigers Won"
		sys.exit()

def get_tiger_position(tiger):
	for i in range(len(board_matrix)):
		if tiger in board_matrix[i]:
			k = board_matrix[i].index(tiger)
			return (i,k)

def check_tiger_neighbours(neigh):
	count=0
	for i in neigh:
		pos = positions[i]
		if(board_matrix[pos[0]][pos[1]]!='*'):
			count+=1
	if(len(neigh)==count):
		return 1
	else:
		return 0
	
def check_tiger_jumps(jumps):
	count=0
	for i in jumps:
		pos = positions[i]
		if(board_matrix[pos[0]][pos[1]]!='*'):
			count+=1
	if(len(jumps)==count):
		return 1
	else:
		return 0

def check_blocked_tigers():
	count = 0
	tiger_list = ['T1','T2','T3']
	for i in tiger_list:
		tiger_pos = get_tiger_position(i)
		tiger_neighbours = check_tiger_neighbours(neighbours[tiger_pos])
		tiger_j = check_tiger_jumps(tiger_jumps[tiger_pos])
		if(tiger_neighbours==1 and tiger_j==1):
			count+=1
	if(count==3):
		return 1
	else:
		return 0


def end_tiger_game():
	print "Goats won!!!!"
	sys.exit()
	
	
def move_tiger():
	dead_tigers = check_blocked_tigers()
	goat_list = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
	goat_pos = []
	for element in goat_list:
		e = get_goat_position(element)
		if e!=None:
			goat_pos.append(e)
	if(dead_tigers==1):
		end_tiger_game()
	else:
		s = raw_input("choose which tiger to move:")
		if s=='T1' or s=='T2' or s=='T3':
			initial = []
			for i in range(len(board_matrix)):
				if s in board_matrix[i]:
					k = board_matrix[i].index(s)
					initial.append((i,k))
			a = raw_input("choose destination:")
			if(a.isdigit()):
				a=int(a)
				destination = positions[a]
				if (a in tiger_jumps[initial[0]]) and (board_matrix[destination[0]][destination[1]]=='*'):
					common = list(set(neighbours[initial[0]]) & set(neighbours[destination]))
					if len(common)>0:
						common_element = common[0]
					 	common_position = positions[common_element]
					 	if common_position in goat_pos:
							board_matrix[destination[0]][destination[1]] = board_matrix[initial[0][0]][initial[0][1]]
							dead_goats.append(board_matrix[common_position[0]][common_position[1]])
							board_matrix[common_position[0]][common_position[1]] = board_matrix[initial[0][0]][initial[0][1]] = '*'
							playsound("Goat Bah-SoundBible.com-959734934.wav")
							check_end()
						else:
							print "YOU CANNOT JUMP THERE!!!"
							move_tiger()
				elif(board_matrix[destination[0]][destination[1]]=='*' and a in neighbours[initial[0]]):
						board_matrix[destination[0]][destination[1]],board_matrix[initial[0][0]][initial[0][1]] = board_matrix[initial[0][0]][initial[0][1]],'*'
				else:
					print "YOU CANNOT JUMP THERE!!!"
					move_tiger()
			else:
				print "INVALID ENTRY"
				move_tiger()
		else:
			print "INVALID ENTRY"
			move_tiger()

tigers_list = ['T1','T2','T3']

def get_goat_position(goat):
	for i in range(len(board_matrix)):
		if goat in board_matrix[i]:
			k = board_matrix[i].index(goat)
			return (i,k)

def check_goat_in_neighbours(tiger_pos):
	goat_list = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
	neigh = neighbours[tiger_pos]
	for i in neigh:
		neigh_pos = positions[i]
		if board_matrix[neigh_pos[0]][neigh_pos[1]] in goat_list and neigh_pos!=(0,0):
			c = list(set(neighbours[neigh_pos]) & set(tiger_jumps[tiger_pos]))
			if(len(c)>0):
				c_element = positions[int(c[0])]
				if(board_matrix[c_element[0]][c_element[1]]=='*'):
					board_matrix[c_element[0]][c_element[1]] = board_matrix[tiger_pos[0]][tiger_pos[1]]
					dead_goats.append(board_matrix[neigh_pos[0]][neigh_pos[1]])
					board_matrix[neigh_pos[0]][neigh_pos[1]] = board_matrix[tiger_pos[0]][tiger_pos[1]] = '*'
					playsound("Goat Bah-SoundBible.com-959734934.wav")
					return 1



def get_horizontal(argument):
	result = []
	horizontal = [[2,3,4,5,6,7], [8,9,10,11,12,13], [14,15,16,17,18,19], [20,21,22,23]]	
	for element in horizontal:
		if argument in element:
			result.append(element)
	return result
	
def get_vertical(argument):
	result = []
	vertical  =  [[1,3,9,15,20], [1, 4, 10, 16,21], [1,5,11,17,22], [1, 6,12,18,23], [2,8,14], [7,13,19]]
	for element in vertical:
		if argument in element:
			result.append(element)
	return result


def check_goat_in_vertical(vertical):
	goat_list = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
	goat_numbers=[]
	goat_numbers_ver = []
	for goat in goat_list:
		k = get_goat_position(goat)
		if k!=None:
			goat_numbers.append(reversed_positions[k])
	if(len(vertical)>0):
		for element in vertical:
			for goat in goat_numbers:
				if goat in element:
					goat_numbers_ver.append(goat)
	return goat_numbers_ver

def check_goat_in_horizontal(horizontal):
	goat_list = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
	goat_numbers=[]
	goat_numbers_hor = []
	for goat in goat_list:
		k = get_goat_position(goat)
		if k!=None:
			goat_numbers.append(reversed_positions[k])
	if(len(horizontal)>0):
		for element in horizontal:
			for goat in goat_numbers:
				if goat  in element:
					goat_numbers_hor.append(goat)
	return goat_numbers_hor


def next_move(horizontal,vertical,goat_in_horizontal,goat_in_vertical,tiger_number):
	valid_goats = []
	if(len(horizontal)>0):
		for element in horizontal:
			for goat in goat_in_horizontal:
				if goat<tiger_number:
					goat_index = element.index(goat)
					k = element.index(tiger_number)
					if(k-1>=0 and goat_index-1>=0):
						ele = element[k-1]
						ele_pos = positions[ele]
						goat_next = element[goat_index-1]
						goat_next_pos = positions[goat_next]
						if(board_matrix[ele_pos[0]][ele_pos[1]]=='*' and board_matrix[goat_next_pos[0]][goat_next_pos[1]]=='*'):
							valid_goats.append(goat)
				elif goat>tiger_number:
					goat_index = element.index(goat)
					k = element.index(tiger_number)
					if(k+1<len(element) and goat_index+1<len(element)):
						ele = element[k+1]
						ele_pos = positions[ele]
						goat_next = element[goat_index+1]
						goat_next_pos = positions[goat_next]
						if(board_matrix[ele_pos[0]][ele_pos[1]]=='*' and board_matrix[goat_next_pos[0]][goat_next_pos[1]]=='*'):
							valid_goats.append(goat)
	if(len(vertical)>0):	
		for element in vertical:
			for goat in goat_in_vertical:
				if goat in element:
					if goat<tiger_number:
						goat_index = element.index(goat)
						k = element.index(tiger_number)
						if(k-1>=0 and goat_index-1>=0):
							ele = element[k-1]
							ele_pos = positions[ele]
							goat_next = element[goat_index-1]
							goat_next_pos = positions[goat_next]
							if(board_matrix[ele_pos[0]][ele_pos[1]]=='*' and board_matrix[goat_next_pos[0]][goat_next_pos[1]]=='*'):
								valid_goats.append(goat)
					elif goat>tiger_number:
						goat_index = element.index(goat)
						k = element.index(tiger_number)
						if(k+1<len(element) and goat_index+1<len(element)):
							ele = element[k+1]
							ele_pos = positions[ele]
							goat_next = element[goat_index+1]
							goat_next_pos = positions[goat_next]
							if(board_matrix[ele_pos[0]][ele_pos[1]]=='*' and board_matrix[goat_next_pos[0]][goat_next_pos[1]]=='*'):
								valid_goats.append(goat)
	return valid_goats


def get_random(x,y,increment):
	random = randrange(x,y,increment)
	tiger  = tigers_list[random]
	tiger_pos = get_tiger_position(tiger)
	neigh = neighbours[tiger_pos]
	result = []
	for i in neigh:
		pos = positions[i]
		if(board_matrix[pos[0]][pos[1]]=='*'):
			result.append(i)
	if(len(result)>0):
		print result
		random2 = randrange(0,len(result),1)
		element = result[random2]
		return (tiger_pos,positions[element])
	else:
		get_random(x,y,increment)


def get_distance(element_pos,j):
	return round(sqrt(pow(j[0]-element_pos[0],2)+pow(j[1]-element_pos[1],2)),2)

def tigers_next_pos(key,goat_position):
	key_pos = get_tiger_position(key)
	key_number = reversed_positions[key_pos]
	goat_number = reversed_positions[goat_position]
	horizontal = get_horizontal(key_number)
	vertical = get_vertical(key_number)
	common_horizontal = []
	common_vertical = []
	if(len(horizontal)>0):
		for element in horizontal:
			if goat_number in element and key_number in element:
				next_index = element.index(key_number)
				if(goat_number<key_number):
					if(next_index-1>=0):
						next_pos = positions[element[next_index-1]]
						board_matrix[key_pos[0]][key_pos[1]],board_matrix[next_pos[0]][next_pos[1]] = board_matrix[next_pos[0]][next_pos[1]],board_matrix[key_pos[0]][key_pos[1]]
				elif(goat_number>key_number):
					if(next_index+1<len(element)):
						next_pos = positions[element[next_index+1]]
						board_matrix[key_pos[0]][key_pos[1]],board_matrix[next_pos[0]][next_pos[1]] = board_matrix[next_pos[0]][next_pos[1]],board_matrix[key_pos[0]][key_pos[1]]
					
	if(len(vertical)>0):
		for element in vertical:
			if goat_number in element and key_number in element:
				next_index = element.index(key_number)
				if(goat_number<key_number):
					if(next_index-1>=0):
						next_pos = positions[element[next_index-1]]
						board_matrix[key_pos[0]][key_pos[1]],board_matrix[next_pos[0]][next_pos[1]] = board_matrix[next_pos[0]][next_pos[1]],board_matrix[key_pos[0]][key_pos[1]]
				elif(goat_number>key_number):
					if(next_index+1<len(element)):
						next_pos = positions[element[next_index+1]]
						board_matrix[key_pos[0]][key_pos[1]],board_matrix[next_pos[0]][next_pos[1]] = board_matrix[next_pos[0]][next_pos[1]],board_matrix[key_pos[0]][key_pos[1]]
					
def tiger_moves():
	valid_moves={}
	for element in tigers_list:
		tiger_pos = get_tiger_position(element)
		tiger_number = reversed_positions[tiger_pos]
		horizontal = get_horizontal(tiger_number)
		vertical = get_vertical(tiger_number)
		goat_in_horizontal = check_goat_in_horizontal(horizontal)
		goat_in_vertical = check_goat_in_vertical(vertical)
		valid_moves[element] = next_move(horizontal,vertical,goat_in_horizontal,goat_in_vertical,tiger_number)
	count = 0
	for element in valid_moves:
		if(len(valid_moves[element])==0):
			count+=1
	if(count==3):
		while(True):
			r  = get_random(0,3,1)
			if(r!=None):
				break
		board_matrix[r[0][0]][r[0][1]],board_matrix[r[1][0]][r[1][1]] = board_matrix[r[1][0]][r[1][1]],board_matrix[r[0][0]][r[0][1]]
	else:
		goat_distances = {'T1':[],'T2':[],'T3':[]}
		distances = {}
		for element in valid_moves:
			element_pos = get_tiger_position(element)
			minimum = 1000000000000
			if(len(valid_moves[element])>0):
				for j  in valid_moves[element]:
					d = get_distance(element_pos,positions[j])
					if(d<minimum):
						minimum = d
						pos = positions[j]
				goat_distances[element] = pos
				distances[element] = minimum
		sorted_distances = sorted(distances.items(), key=operator.itemgetter(1))
		key = sorted_distances[0][0]
		tigers_next_pos(key,goat_distances[key])

def intelligent_tiger():
	flag = 0
	for i in tigers_list:
		check_end()
		tiger_pos = get_tiger_position(i)
		point  = check_goat_in_neighbours(tiger_pos)
		if(point==1):
			flag = 1
	check_end()
	if(flag==0):
		tiger_moves()	

def check_tigers_in_neighbours():
	goat_list = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
	for element in tigers_list:
		tiger_pos = get_tiger_position(element)
		tiger_neigh = neighbours[tiger_pos]
		for i in tiger_neigh:
			pos = positions[i]
			if(board_matrix[pos[0]][pos[1]] in goat_list):
				next_element = list(set(neighbours[pos]) & set(tiger_jumps[tiger_pos]))
				if(len(next_element)>0):
					next_element = int(next_element[0])
					next_element_pos = positions[next_element]
					if(board_matrix[next_element_pos[0]][next_element_pos[1]]=='*'):
						return next_element

def get_random_in_range_goat():
	number = randrange(1,24,1)
	number_pos = positions[number]
	neigh = neighbours[number_pos]
	tigers_pos = []
	for i in tigers_list:
		tigers_pos.append(get_tiger_position(i))
	if(board_matrix[number_pos[0]][number_pos[1]]=='*'):
		count = 0 
		for element in neigh:
			if positions[element] not in tigers_pos:
				count+=1
				#print "going"
		if(count==len(neigh)):
			return number_pos

def place_goats(goat):
	result = check_tigers_in_neighbours()
	if(result):
		result_pos = positions[result]
		board_matrix[result_pos[0]][result_pos[1]] = goat
	else:
		while(True):
			answer = get_random_in_range_goat()
			if(answer):
				break
		board_matrix[answer[0]][answer[1]] = goat
	
def move_goats_intelligent_to_next():
	goat_list = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
	for element in tiger_list:
		element_pos = get_tiger_position(element)
		if(element_pos!=None):
			element_neigh = neighbours[element_pos]
			for i in element_neigh:
				i_pos = position[i]
				if(board_matrix[i_pos[0]][i_pos[1]] in goat_list):
					common = list(set(tiger_jumps[element_pos]) & set(neighbours[i_pos]))
					if(len(common)>0):
						common_pos = positions[int(common[0])]
						if(board_matrix[common_pos[0]][common_pos[1]]=='*'):
							common_pos_neigh = neighbours[common_pos]
							for c in common_pos_neigh:
								c_pos = positions[c]
								if(c_pos!=i_pos and board_matrix[c_pos[0]][c_pos[1]] in goat_list):
									board_matrix[c_pos[0]][c_pos[1]],board_matrix[common_pos[0]][common_pos[1]]=board_matrix[common_pos[0]][common_pos[1]],board_matrix[c_pos[0]][c_pos[1]]
									return 1
					
def move_goats_intelligent_to_next_random():
	goat_list = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
	random = randrange(0,16,1)
	goat_pos = get_goat_position(goat_list[random])
	if goat_pos!=None:
		goat_neigh = neighbours[goat_pos]
		for neigh in goat_neigh:
			neigh_pos = positions[neigh]
			if(board_matrix[neigh_pos[0]][neigh_pos[1]]=='*'):
				board_matrix[goat_pos[0]][goat_pos[1]],board_matrix[neigh_pos[0]][neigh_pos[1]]=board_matrix[neigh_pos[0]][neigh_pos[1]],board_matrix[goat_pos[0]][goat_pos[1]]
				return 1


def intelligent_goat_next_move():
	answer = move_goats_intelligent_to_next()
	if(answer==None):
		while(True):
			k = move_goats_intelligent_to_next_random()
			if(k==1):
				break

def intelligent_goat(i):
	goat_list = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
	place_goats(goat_list[i])
		
def move_goat():
	goat_list = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16']
	s = raw_input("choose which goat to move")
	if s in goat_list:
		initial = []
		for i in range(len(board_matrix)):
			if s in board_matrix[i]:
				k = board_matrix[i].index(s)
				initial.append((i,k))
		a = input("choose destination")
		destination = positions[a]
		if(a in neighbours[destination] and board_matrix[destination[0]][destination[1]]=='*'):
			board_matrix[destination[0]][destination[1]],board_matrix[initial[0][0]][initial[0][1]] = board_matrix[initial[0][0]][initial[0][1]],board_matrix[destination[0]][destination[1]]
		else:
			print "YOU CANNOT MOVE THERE!!!!"
			move_goat()
	else:
		print "INVALID ENTRY"
		move_goat()
		

board_matrix[0][0]='T1'
board_matrix[1][2]='T2'
board_matrix[1][3]='T3'
print_board()
empty_list = [i for i in range(1,24) if i not in tiger_list]
goat_list = []

def one_player():
	player = raw_input("Player choose Goat or Tiger:")
	if(player=="Goat"):
		for _ in range(0,16):
			position_placer()
			print_board()
			dead = check_blocked_tigers()
			if(dead==1):
				end_tiger_game()
			intelligent_tiger()
			print_board()
			check_end()
		while(True):
			move_goat()
			print_board()
			dead = check_blocked_tigers()
			if(dead==1):
				end_tiger_game()
			intelligent_tiger()
			print_board()
			check_end()
	elif(player=="Tiger"):
		intelligent_goat(0)
		print_board()
		for i in range(1,16):
			dead = check_blocked_tigers()
			if(dead==1):
				playsound("Tiger6.wav")
				end_tiger_game()
			move_tiger()
			print_board()
			intelligent_goat(i)
			print_board()
			check_end()
			
		while(True):
			dead = check_blocked_tigers()
			if(dead==1):
				playsound("Tiger6.wav")
				end_tiger_game()
			move_tiger()
			print_board()
			intelligent_goat_next_move()
			print_board()
			check_end()
	else:
		print "INVALID ENTRY!!!"
		one_player()

def two_player():
	player1 = raw_input("Player1 choose Goat or Tiger:")
	if player1 == 'Goat' or player1=='Tiger':
		for i in range(1,16):
			dead = check_blocked_tigers()
			if(dead==1):
				playsound("Tiger6.wav")
				end_tiger_game()
			position_placer()
			print_board()
			move_tiger()
			print_board()
			check_end()
			
		while(True):
			dead = check_blocked_tigers()
			if(dead==1):
				playsound("Tiger6.wav")
				end_tiger_game()
			move_goat()
			print_board()
			move_tiger()
			print_board()
			check_end()
	else:
		print "INVALID ENTRY!!!"
	
def start_game():
	game = raw_input("enter 1P or 2P:")
	if(game=="1P"):
		 one_player()
	elif(game=="2P"):
		two_player()
	else:
		print "INVALID ENTRY!!!"
		start_game()	

start_game()
