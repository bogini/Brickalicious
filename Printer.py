CARTRIDGE_X = -1
CARTRIDGE_Y = 0
CARTRIDGE_Z = 0

class Printer:
	"""
	The class reresents the printer itself. It keeps track of it's position, 
	and communicates with the arduino to call functions there.
	
	Functions:
	convert brick list into stepper motor steps
	has a servo and a stepper
	"""
	def generate_build_list(brick_list):
		build_list = []
		#Move to [0,0,0]
		build_list.append([MOVE_X,0],[MOVE_Y,0],[MOVE_Z,0])
		for brick in brick_list:
			#conversion between lego pins and stepper motor steps
			x = brick.pin_x * 100
			y = brick.pin_y * 100
			z = 360 - (brick.pin_z * 100)
			#Move to cartridge and move down to pick up brick
			build_list.append([MOVE_X,CARTRIDGE_X][MOVE_Y,CARTRIDGE_Y][MOVE_Z,CARTRIDGE_Z])
			#Orient Head
			if brick.orientation == 'E':
				build_list.append(ROTATE_HEAD_E)
			else:
				build_list.append(ROTATE_HEAD_N)
			#Move to brick placing location
			build_list.append([MOVE_X,x],[MOVE_Y,y],[MOVE_z,z])
			#Push brick out
			build_list.append(PUSH_DOWN_CAM, MOVE_CAM_UP)
		return build_list