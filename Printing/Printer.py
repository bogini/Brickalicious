CARTRIDGE_X = -1
CARTRIDGE_Y = 0
CARTRIDGE_Z = 0
PICKUP_DISTANCE = 0.20

class Printer:
    def __init__(self, bricks):
        self.bricks = bricks
        self.bricks_to_print = self.bricks.copy()
        self.x = 0
        self.y = 0
        self.z = 0
        self.printing = false
        self.move_to_cartridge()
    
    def print_bricks(self):
        # Goes through the bruck list
        for brick in self.bricks:
            # Check if we are paused
            while(not self.printing):
                pass
            self.move_to_cartridge()
            self.pick_up()
            self.move(brick.pin.x, brick.pin.y, brick.pin.z + PICKUP_DISTANCE)
            self.lay_down()
            bricks_to_print.remove(brick)
        self.move_to_cartridge()
    
    def move_to_cartridge(self):
        # Mobes the head to the cartridge
        self.move(CARTRIDGE_X, CARTRIDGE_Y, PICKUP_DISTANCE)
    
    def pick_up(self):
        # Picks up the piece
        move(self.x, self.y, CARTRIDGE_Z)
        
    def lay_down(self):
        # Lays down the piece
        move(self.x, self.y, PICKUP_DISTANCE)
        # Press down
        
    def move(self, to_X, to_Y, to_Z):
        # Moves the head to the specified coordinates
        # Move x
        # Move y
        # Move z
        self.x = to_X
        self.y = to_Y
        self.z = to_Z
    
    def pause(self):
        # Pauses the printing
        self.printing = not self.printing
        self.bricks = self.bricks_to_print
        
    def cancel(self):
        # Cancel the printing
        self.printing = false
        self.move_to_cartridge()