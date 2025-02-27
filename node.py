class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state       
        self.parent = parent    
        self.action = action   
        self.g = g              # Cost from start to this node (path cost)
        self.f = 0              # Total cost estimate (g + h)
        self.heuristic = 0      # Heuristic cost estimate to the goal
    
    def getPath(self):
        """Gives the list of states from the initial state to the goal node."""
        path = []
        current_node = self
        while current_node is not None:
            path.append(current_node.state)  
            current_node = current_node.parent 
        path.reverse()  # Since we went from goal to start, we reverse it
        return path

    def getSolution(self):
        """Returns the actions taken to reach this node."""
        actions = []
        current_node = self
        while current_node.parent is not None:
            actions.append(current_node.action)
            current_node = current_node.parent
        actions.reverse()  # Added reverse to get correct order
        return actions

    def setF(self):
        """Calculates the f-score as g + heuristic."""
        self.f = self.g + self.heuristic  # Implemented the f-score calculation
        print(f"Node F-value: {self.f}, G-value: {self.g}, Heuristic: {self.heuristic}")

    def __lt__(self, other):
        """Comparison method required for heapq operations."""
        return self.f < other.f

    def __str__(self):
        """String representation for better debugging."""
        return f"Node(action={self.action}, g={self.g}, h={self.heuristic}, f={self.f})"


""" class Node:
        
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state       
        self.parent = parent    
        self.action = action   
        self.g = g    
        self.f = 0
        self.heuristic = 0
    def getPath(self):
        # gives the list of states from the initial state to the goal node.
        path = []
        current_node = self
        while current_node is not None:
            path.append(current_node.state)  
            current_node = current_node.parent 
        path.reverse()  # Since we went from goal to start, we reverse it
        return path

    def getSolution(self):
        actions = []
        current_node = self
        while current_node.parent is not None:
            actions.append(current_node.action)
            current_node = current_node.parent
        actions.reverse()  # Added reverse to get correct order
        return actions

    def setF(self):
        self.f = self.g + self.heuristic  # Implemented the f-score calculation
        print(f"Node F-value: {self.f}, G-value: {self.g}, Heuristic: {self.heuristic} ")

        
    def __lt__(self, other):
        return self.f < other.f
# In node.py, you could add this method for better debugging:
    def __str__(self):
        return f"Node(action={self.action}, g={self.g}, cost={self.cost}, h={self.heuristic}, f={self.f})" """