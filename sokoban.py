class SokobanPuzzle:
    """
    Sokoban puzzle implementation
    R: Robot (player)
    O: Obstacle (wall)
    ' ': Empty space
    S: Storage (target space)
    B: Block (box)
    '.': Player on target space
    '*': Box on target space
    """
    def __init__(self, grid):
        self.grid = grid

    """ def isGoal(self):
        for row in self.grid:
            if 'B' in row:  # If there's any box not on storage
                return False
        return True """
    def isGoal(self):
        for row in self.grid:
            for cell in row:
                if cell == 'B':  #found a box that is not on storage
                    return False
        #check if all storage points have boxes
        storage_count = sum(row.count('S') for row in self.grid)
        box_on_storage_count = sum(row.count('*') for row in self.grid)
        return storage_count == 0 and box_on_storage_count > 0

    def successorFunction(self):
        #generate all possible next states
        successors = []
        directions = {
            'right': (0, 1),
            'left': (0, -1),
            'up': (-1, 0),
            'down': (1, 0)
        }
        
        robot_x, robot_y = self.findPlayer()
        if robot_x is None:
            return []
            
        for action, (dir_x, dir_y) in directions.items():
            row_new = robot_x + dir_x
            col_new = robot_y + dir_y
            
            if self.validMove(row_new, col_new, (dir_x, dir_y)):
                new_state = SokobanPuzzle(self.copy_grid())
                robot_on_storage = self.grid[robot_x][robot_y] == '.'
                
                # Handle movement from current position
                new_state.grid[robot_x][robot_y] = 'S' if robot_on_storage else ' '
                
                # Handle different cases for new position
                if new_state.grid[row_new][col_new] in [' ', 'S']:
                    new_state.grid[row_new][col_new] = '.' if new_state.grid[row_new][col_new] == 'S' else 'R'
                
                elif new_state.grid[row_new][col_new] in ['B', '*']:
                    box_x = row_new + dir_x
                    box_y = col_new + dir_y
                    
                    if self.validMove(box_x, box_y, (dir_x, dir_y)):
                        #moving the box
                        new_state.grid[box_x][box_y] = '*' if new_state.grid[box_x][box_y] == 'S' else 'B'
                        #mve the player
                        new_state.grid[row_new][col_new] = '.' if new_state.grid[row_new][col_new] == '*' else 'R'
                
                successors.append((action, new_state))
                    
        return successors


    def validMove(self, new_row, new_col, direction):
        #Check if a move is valid mchi contradict some game rules
        if not (0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0])):
            return False
        
        if self.grid[new_row][new_col] == 'O':
            return False
        
        if self.grid[new_row][new_col] in ['B', '*']:
            next_row = new_row + direction[0]
            next_col = new_col + direction[1]
            
            if not (0 <= next_row < len(self.grid) and 0 <= next_col < len(self.grid[0])):
                return False
            
            if self.grid[next_row][next_col] not in [' ', 'S']:
                return False
        
        return True
    
    def copy_grid(self):
        #Create a deep copy of the grid to not lose when changing states
        return [row[:] for row in self.grid]
    
    def findPlayer(self):
        #Find the player's position in the grid 
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] in ['R', '.']:
                    return row, col
        return None, None
    
    def print_grid(self):
        #Print the current state of the grid : to see each step
        for row in self.grid:
            print(' '.join(row))

    def get_boxes(self):
            #Return a list of positions of the boxes in the grid
            boxes = []
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] in ['B', '*']:  # Box or Box on Storage
                        boxes.append((row, col))
            return boxes


"""     def successorFunction(self):
        #Generate all possible next states
        successors = []
        directions = {
            'right': (0, 1),
            'left': (0, -1),
            'up': (-1, 0),
            'down': (1, 0)
        }
        
        robot_x, robot_y = self.findPlayer()
        if robot_x is None:
            return []
            
        for action, (dir_x, dir_y) in directions.items():
            row_new = robot_x + dir_x
            col_new = robot_y + dir_y
            
            if self.validMove(row_new, col_new, (dir_x, dir_y)):
                new_state = SokobanPuzzle(self.copy_grid())
                
                # Handle different cases for movement
                current_cell = new_state.grid[row_new][col_new]
                
                if current_cell == ' ':
                    new_state.grid[robot_x][robot_y] = ' '
                    new_state.grid[row_new][col_new] = 'R'
                
                elif current_cell == 'S':
                    new_state.grid[robot_x][robot_y] = ' '
                    new_state.grid[row_new][col_new] = '.'
                
                elif current_cell in ['B', '*']:
                    box_x = row_new + dir_x
                    box_y = col_new + dir_y
                    
                    if self.validMove(box_x, box_y, (dir_x, dir_y)):
                        new_state.grid[robot_x][robot_y] = ' '
                        new_state.grid[row_new][col_new] = 'R'
                        new_state.grid[box_x][box_y] = '*' if new_state.grid[box_x][box_y] == 'S' else 'B'
                
                successors.append((action, new_state))
                    
        return successors
 """    