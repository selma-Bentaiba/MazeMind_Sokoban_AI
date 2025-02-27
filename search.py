from collections import deque #for fifo
import heapq #priority queue a*
from node import Node #all states in

class Search:
    def __init__(self):
        pass

    def is_deadlocked(self, state):
        """Check for deadlocks in the current state."""
        # Get the positions of all boxes and storage points
        boxes = []
        storage_points = []
        
        for i in range(len(state.grid)):
            for j in range(len(state.grid[0])):
                if state.grid[i][j] == 'B':
                    boxes.append((i, j))
                elif state.grid[i][j] == 'S':
                    storage_points.append((i, j))
        
        # If there are no boxes or storage points, can't be deadlocked
        if not boxes or not storage_points:
            return False

        # Check each box position against storage points to see if they can reach any
        for box in boxes:
            if not self.can_reach_storage(box, storage_points, state):
                return True
        
        return False

    def can_reach_storage(self, box, storage_points, state):
        """Use BFS to check if the box can reach any storage point."""
        # BFS to see if the box can reach a storage point
        queue = deque([box])
        visited = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            # Check if this position is a storage point
            if current in storage_points:
                return True
            
            # Check possible moves
            for d in directions:
                next_pos = (current[0] + d[0], current[1] + d[1])
                # Ensure the move is within bounds and not a wall
                if (0 <= next_pos[0] < len(state.grid) and
                    0 <= next_pos[1] < len(state.grid[0]) and
                    state.grid[next_pos[0]][next_pos[1]] != '#'):  # Assuming '#' represents walls
                    queue.append(next_pos)

        return False

    def BFS(self, initial_state):
        """Breadth-First Search implementation for Sokoban puzzle."""
        initial_node = Node(initial_state)
        frontier = deque([initial_node])
        explored = set()
        
        while frontier:
            current_node = frontier.popleft()
            current_state = current_node.state
            
            # Check for deadlock before proceeding
            if self.is_deadlocked(current_state):
                print("Deadlock detected!")
                return None
            
            # Check if current state is goal state
            if current_state.isGoal():
                return current_node
            
            grid_tuple = tuple(tuple(row) for row in current_state.grid)
            if grid_tuple in explored:
                continue
                
            explored.add(grid_tuple)
            
            for action, successor_state in current_state.successorFunction():
                successor_node = Node(successor_state, current_node, action, current_node.g + 1)
                successor_grid_tuple = tuple(tuple(row) for row in successor_state.grid)
                
                if successor_grid_tuple not in explored:
                    frontier.append(successor_node)
        
        return None

    def astar(self, initial_state, heuristic_type):
        """A* search implementation."""
        frontier = []
        explored = set()
        
        initial_node = Node(initial_state)
        initial_node.heuristic = self.calculate_heuristic(initial_state, heuristic_type)
        initial_node.setF()
        heapq.heappush(frontier, (initial_node.f, id(initial_node), initial_node))
        
        while frontier:
            _, _, current_node = heapq.heappop(frontier)
            current_state = current_node.state
            
            # Check for deadlock before proceeding
            if self.is_deadlocked(current_state):
                print("Deadlock detected!")
                return None
            
            if current_state.isGoal():
                return current_node
            
            grid_tuple = tuple(tuple(row) for row in current_state.grid)
            if grid_tuple in explored:
                continue
            
            explored.add(grid_tuple)
            
            for action, successor_state in current_state.successorFunction():
                successor_grid_tuple = tuple(tuple(row) for row in successor_state.grid)
                
                if successor_grid_tuple not in explored:
                    child = Node(successor_state, current_node, action, current_node.g + 1)
                    child.heuristic = self.calculate_heuristic(successor_state, heuristic_type)
                    child.setF()
                    heapq.heappush(frontier, (child.f, id(child), child))
        
        return None

    def calculate_heuristic(self, state, heuristic_type):
        if heuristic_type == "h1":
            return self.h1(state)
        elif heuristic_type == "h2":
            return self.h2(state)
        elif heuristic_type == "h3":
            return self.h3(state)
        return 0
    
    def h1(self, state):
        count = 0
        for i in range(len(state.grid)):
            for j in range(len(state.grid[0])):
                if state.grid[i][j] == 'B':
                    count += 1
        return count
    
    def h2(self, state):
        total_distance = 0
        storage_points = []
        boxes = []
        
        for i in range(len(state.grid)):
            for j in range(len(state.grid[0])):
                if state.grid[i][j] == 'S':
                    storage_points.append((i, j))
                elif state.grid[i][j] == 'B':
                    boxes.append((i, j))
        
        if not storage_points or not boxes:
            return 0
            
        for box in boxes:
            min_dist = float('inf')
            for storage in storage_points:
                dist = abs(box[0] - storage[0]) + abs(box[1] - storage[1])
                min_dist = min(min_dist, dist)
            total_distance += min_dist
            
        return total_distance
    
    def h3(self, state):
        box_to_storage = self.h2(state)
        player_pos = state.findPlayer()
        if not player_pos or player_pos[0] is None:
            return float('inf')
            
        min_dist_to_box = float('inf')
        has_box = False
        for i in range(len(state.grid)):
            for j in range(len(state.grid[0])):
                if state.grid[i][j] == 'B':
                    has_box = True
                    dist = abs(player_pos[0] - i) + abs(player_pos[1] - j)
                    min_dist_to_box = min(min_dist_to_box, dist)
        
        if not has_box:
            return 0
            
        return box_to_storage + min_dist_to_box
