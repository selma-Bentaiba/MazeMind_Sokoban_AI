import pygame
from search import Search
from node import Node
from sokoban import SokobanPuzzle
import os
from typing import Dict, List, Optional
import sys

class SokobanGame:
    # Define constants
    TILE_SIZE = 40
    BUTTON_HEIGHT = 40
    BUTTON_WIDTH = 200
    BUTTON_MARGIN = 20
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    BLUE = (0, 0, 255)
    
    # Game states
    MENU = "menu"
    LEVEL_SELECT = "level_select"
    ALGORITHM_SELECT = "algorithm_select"
    PLAYING = "playing"
    SOLUTION = "solution"
    
    SYMBOLS = {
        'PLAYER': 'R',
        'BOX': 'B',
        'WALL': 'O',
        'TARGET': 'S',
        'FLOOR': ' ',
        'PLAYER_ON_TARGET': '.',
        'BOX_ON_TARGET': '*'
    }

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.examples = self._load_examples()
        self.images = self._load_images()
        self.selected_example = 0
        self.selected_algorithm = None
        self.selected_heuristic = "h1"
        self.search = Search()
        self.game_state = self.MENU
        self.solution_path = None
        self.current_step = 0
        
        # Set up display with menu space
        self.window_width = max(len(row) for example in self.examples for row in example) * self.TILE_SIZE
        self.window_width = max(self.window_width, self.BUTTON_WIDTH + 2 * self.BUTTON_MARGIN)
        self.window_height = (max(len(example) for example in self.examples) * self.TILE_SIZE + 
                            4 * (self.BUTTON_HEIGHT + self.BUTTON_MARGIN))
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Sokoban Puzzle Solver")

    def draw_button(self, text: str, rect: pygame.Rect, active: bool = False) -> None:
        """Draw a button with text."""
        color = self.BLUE if active else self.GRAY
        pygame.draw.rect(self.screen, color, rect)
        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_menu(self) -> List[pygame.Rect]:
        """Draw the main menu and return button rectangles."""
        self.screen.fill(self.BLACK)
        buttons = []
        
        # Title
        title = self.font.render("Sokoban Puzzle Solver", True, self.WHITE)
        title_rect = title.get_rect(centerx=self.window_width // 2, y=self.BUTTON_MARGIN)
        self.screen.blit(title, title_rect)
        
        # Start button
        start_rect = pygame.Rect(
            (self.window_width - self.BUTTON_WIDTH) // 2,
            self.window_height // 3,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        self.draw_button("Start Game", start_rect)
        buttons.append(start_rect)
        
        # Quit button
        quit_rect = pygame.Rect(
            (self.window_width - self.BUTTON_WIDTH) // 2,
            self.window_height // 2,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        self.draw_button("Quit", quit_rect)
        buttons.append(quit_rect)
        
        return buttons

    def draw_level_select(self) -> List[pygame.Rect]:
        """Draw the level selection screen and return button rectangles."""
        self.screen.fill(self.BLACK)
        buttons = []
        
        title = self.font.render("Select Level", True, self.WHITE)
        title_rect = title.get_rect(centerx=self.window_width // 2, y=self.BUTTON_MARGIN)
        self.screen.blit(title, title_rect)
        
        for i in range(len(self.examples)):
            button_rect = pygame.Rect(
                (self.window_width - self.BUTTON_WIDTH) // 2,
                self.BUTTON_MARGIN * 2 + title_rect.height + i * (self.BUTTON_HEIGHT + 10),
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT
            )
            self.draw_button(f"Level {i + 1}", button_rect)
            buttons.append(button_rect)
            
        # Back button
        back_rect = pygame.Rect(
            (self.window_width - self.BUTTON_WIDTH) // 2,
            self.window_height - self.BUTTON_HEIGHT - self.BUTTON_MARGIN,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        self.draw_button("Back", back_rect)
        buttons.append(back_rect)
        
        return buttons

    def draw_algorithm_select(self) -> List[pygame.Rect]:
        #Draw the algorithm selection screen and return button rectangles
        self.screen.fill(self.BLACK)
        buttons = []
        
        title = self.font.render("Select Algorithm", True, self.WHITE)
        title_rect = title.get_rect(centerx=self.window_width // 2, y=self.BUTTON_MARGIN)
        self.screen.blit(title, title_rect)
        
        # BFS button
        bfs_rect = pygame.Rect(
            (self.window_width - self.BUTTON_WIDTH) // 2,
            self.window_height // 3,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        self.draw_button("BFS", bfs_rect, self.selected_algorithm == "BFS")
        buttons.append(bfs_rect)
        
        # A* buttons
        astar_rect = pygame.Rect(
            (self.window_width - self.BUTTON_WIDTH) // 2,
            self.window_height // 3 + self.BUTTON_HEIGHT + 10,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        self.draw_button("A* (h1)", astar_rect, 
                        self.selected_algorithm == "A*" and self.selected_heuristic == "h1")
        buttons.append(astar_rect)
        
        astar_h2_rect = pygame.Rect(
            (self.window_width - self.BUTTON_WIDTH) // 2,
            self.window_height // 3 + 2 * (self.BUTTON_HEIGHT + 10),
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        self.draw_button("A* (h2)", astar_h2_rect,
                        self.selected_algorithm == "A*" and self.selected_heuristic == "h2")
        buttons.append(astar_h2_rect)
        
        astar_h3_rect = pygame.Rect(
            (self.window_width - self.BUTTON_WIDTH) // 2,
            self.window_height // 3 + 3 * (self.BUTTON_HEIGHT + 10),
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        self.draw_button("A* (h3)", astar_h3_rect,
                        self.selected_algorithm == "A*" and self.selected_heuristic == "h3")
        buttons.append(astar_h3_rect)
        
        # Back button
        back_rect = pygame.Rect(
            (self.window_width - self.BUTTON_WIDTH) // 2,
            self.window_height - self.BUTTON_HEIGHT - self.BUTTON_MARGIN,
            self.BUTTON_WIDTH,
            self.BUTTON_HEIGHT
        )
        self.draw_button("Back", back_rect)
        buttons.append(back_rect)
        
        return buttons

    def draw_solution_controls(self) -> List[pygame.Rect]:
        #Draw solution playback controls and return button rectangles."""
            buttons = []
            
            # Draw control panel background
            control_panel = pygame.Rect(
                0,
                self.window_height - self.BUTTON_HEIGHT - 2 * self.BUTTON_MARGIN,
                self.window_width,
                self.BUTTON_HEIGHT + 2 * self.BUTTON_MARGIN
            )
            pygame.draw.rect(self.screen, self.GRAY, control_panel)
            
            # Previous step button
            prev_rect = pygame.Rect(
                self.BUTTON_MARGIN,
                self.window_height - self.BUTTON_HEIGHT - self.BUTTON_MARGIN,
                self.BUTTON_WIDTH // 2,
                self.BUTTON_HEIGHT
            )
            self.draw_button("Previous", prev_rect)
            buttons.append(prev_rect)
            
            # Next step button
            next_rect = pygame.Rect(
                self.BUTTON_MARGIN + self.BUTTON_WIDTH // 2 + 10,
                self.window_height - self.BUTTON_HEIGHT - self.BUTTON_MARGIN,
                self.BUTTON_WIDTH // 2,
                self.BUTTON_HEIGHT
            )
            self.draw_button("Next", next_rect)
            buttons.append(next_rect)
            
            # Back to menu button
            menu_rect = pygame.Rect(
                self.window_width - self.BUTTON_WIDTH // 2 - self.BUTTON_MARGIN,
                self.window_height - self.BUTTON_HEIGHT - self.BUTTON_MARGIN,
                self.BUTTON_WIDTH // 2,
                self.BUTTON_HEIGHT
            )
            self.draw_button("Menu", menu_rect)
            buttons.append(menu_rect)
            
    # Draw step counter and cost
            if self.solution_path:
                step_text = f"Step: {self.current_step + 1}/{len(self.solution_path)}"
                text_surface = self.font.render(step_text, True, self.WHITE)
                text_rect = text_surface.get_rect(
                    centerx=self.window_width // 2,
                    centery=self.window_height - self.BUTTON_HEIGHT // 2 - self.BUTTON_MARGIN - 20
                )
                self.screen.blit(text_surface, text_rect)

                # Draw cost
                cost_text = f"Cost: {self.g_cost}"  # Use self.g_cost instead of self.cost
                cost_surface = self.font.render(cost_text, True, self.WHITE)
                cost_rect = cost_surface.get_rect(
                    centerx=self.window_width // 2,
                    centery=self.window_height - self.BUTTON_HEIGHT // 2 - self.BUTTON_MARGIN + 20
                )
                self.screen.blit(cost_surface, cost_rect)
            return buttons


    def run_game(self) -> None:
        """Main game loop with menu system."""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            if self.game_state == self.MENU:
                buttons = self.draw_menu()
            elif self.game_state == self.LEVEL_SELECT:
                buttons = self.draw_level_select()
            elif self.game_state == self.ALGORITHM_SELECT:
                buttons = self.draw_algorithm_select()
            elif self.game_state == self.SOLUTION:
                if self.solution_path and self.current_step < len(self.solution_path):
                    self.draw_grid(self.solution_path[self.current_step].grid)
                buttons = self.draw_solution_controls()
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    for i, button in enumerate(buttons):
                        if button.collidepoint(mouse_pos):
                            self.handle_button_click(i)
            
            clock.tick(60)
        
        pygame.quit()

    def handle_button_click(self, button_index: int) -> None:
        """Handle button clicks based on current game state."""
        if self.game_state == self.MENU:
            if button_index == 0:  # Start Game
                self.game_state = self.LEVEL_SELECT
            elif button_index == 1:  # Quit
                pygame.quit()
                sys.exit()
        
        elif self.game_state == self.LEVEL_SELECT:
            if button_index < len(self.examples):  # Level selection
                self.selected_example = button_index
                self.game_state = self.ALGORITHM_SELECT
            elif button_index == len(self.examples):  # Back button
                self.game_state = self.MENU
        
        elif self.game_state == self.ALGORITHM_SELECT:
            if button_index == 0:  # BFS
                self.selected_algorithm = "BFS"
                self.run_search()
            elif button_index in [1, 2, 3]:  # A* with different heuristics
                self.selected_algorithm = "A*"
                self.selected_heuristic = f"h{button_index}"
                self.run_search()
            elif button_index == 4:  # Back button
                self.game_state = self.LEVEL_SELECT
        
        elif self.game_state == self.SOLUTION:
            if button_index == 0 and self.current_step > 0:  # Previous
                self.current_step -= 1
            elif button_index == 1 and self.solution_path and self.current_step < len(self.solution_path) - 1:  # Next
                self.current_step += 1
            elif button_index == 2:  # Menu
                self.game_state = self.MENU
                self.solution_path = None
                self.current_step = 0

    def run_search(self) -> None:
        # Run the selected search algorithm and transition to solution state.
        initial_state = SokobanPuzzle(self.examples[self.selected_example])

        try:
            if self.selected_algorithm == "BFS":
                solution_node = self.search.BFS(initial_state)
            else:  # A*
                solution_node = self.search.astar(initial_state, self.selected_heuristic)

            if solution_node:
                self.solution_path = solution_node.getPath()
                self.current_step = 0
                self.g_cost = solution_node.g  # Access the g value from the solution node
                self.game_state = self.SOLUTION
            else:
                # You might want to show a "No solution found" message here
                self.game_state = self.MENU
        except Exception as e:
            print(f"Error during search: {e}")
            self.game_state = self.MENU

    # Keep your existing methods (_load_examples, _load_images, draw_grid)
    def _load_examples(self) -> List[List[List[str]]]:
        """Load all game examples/levels."""
        return [
            #figure 4 test examples
            [
                ['O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'S', ' ', 'B', ' ', 'O'],
                ['O', ' ', 'O', 'R', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O']    
            ],

            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
                ['O', ' ', ' ', 'O', 'O', 'O', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'O', '.', ' ', 'O'], #'.' IS PLAYER ON TARGET PLACE
                ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
                ['O', ' ', ' ', 'B', ' ', ' ', 'O', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
            ],
            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', ' ', ' ', ' ', 'O', ' ', ' ', 'O'],
                ['O', ' ', ' ', 'B', 'R', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', 'O', 'B', ' ', 'O'],
                ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
                ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                
            ],

            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
                ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
                ['O', 'O', ' ', '*', ' ', ' ', 'O'],
                ['O', ' ', 'B', 'O', 'B', ' ', 'O'],
                ['O', ' ', 'S', 'R', 'S', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'O', 'O'],
                ['O', 'O', 'O', ' ', ' ', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],

            ],

            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'S', 'O', ' ', ' ', 'O', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'B', ' ', 'O', 'O'],
                ['O', ' ', 'B', ' ', 'R', ' ', ' ', 'S', 'O'],
                ['O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'B', 'O', ' ', 'O', 'O', 'O'],
                ['O', 'O', 'O', ' ', ' ', ' ', 'S', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ],
            [     
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'S', ' ', 'O', ' ', 'R', 'O'],
                ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
                ['O', 'S', ' ', ' ', 'B', ' ', 'O'],
                ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
                ['O', 'S', ' ', 'O', ' ', ' ', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O']
            ],
            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'S', 'S', 'S', ' ', 'O', 'O', 'O'],
                ['O', ' ', 'S', ' ', 'B', ' ', ' ', 'O'],
                ['O', ' ', ' ', 'B', 'B', 'B', ' ', 'O'],
                ['O', 'O', 'O', 'O', ' ', ' ', 'R', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
            ]

        ]

    def _load_images(self) -> Dict[str, pygame.Surface]:
        """Load and scale all game images."""
        image_files = {
            self.SYMBOLS['PLAYER']: 'player.jpeg',
            self.SYMBOLS['BOX']: 'box.jpeg',
            self.SYMBOLS['WALL']: 'wall.jpeg',
            self.SYMBOLS['TARGET']: 'target.jpeg',
            self.SYMBOLS['FLOOR']: 'floor.jpeg',
            self.SYMBOLS['PLAYER_ON_TARGET']: 'player_on_target.jpeg',
            self.SYMBOLS['BOX_ON_TARGET']: 'box_on_target.jpeg'
        }
        
        images = {}
        try:
            for symbol, filename in image_files.items():
                path = os.path.join('assets', filename)
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Image file not found: {path}")
                image = pygame.image.load(path)
                images[symbol] = pygame.transform.scale(image, (self.TILE_SIZE, self.TILE_SIZE))
            return images
        except Exception as e:
            print(f"Error loading images: {e}")
            pygame.quit()
            sys.exit(1)

    def _init_display(self, grid: List[List[str]]) -> None:
        """Initialize the display with the correct size for the given grid."""
        width = len(grid[0]) * self.TILE_SIZE
        height = len(grid) * self.TILE_SIZE
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sokoban Puzzle Solver")

    def draw_grid(self, grid: List[List[str]]) -> None:
        """Draw the game grid on the screen."""
        if not self.screen:
            self._init_display(grid)
            
        self.screen.fill((0, 0, 0))  # Clear screen with black
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell in self.images:
                    self.screen.blit(
                        self.images[cell],
                        (x * self.TILE_SIZE, y * self.TILE_SIZE)
                    )
        pygame.display.flip()

    # Just remove their console print statements

def main():
    try:
        game = SokobanGame()
        game.run_game()
    except Exception as e:
        print(f"Unexpected error: {e}")
        pygame.quit()

if __name__ == "__main__":
    main()


""" import pygame
from search import Search
from node import Node
from sokoban import SokobanPuzzle
import os
from typing import Dict, List, Optional
import sys

class SokobanGame:
    # Define tile size constant
    TILE_SIZE = 40
    
    # Game state symbols
    SYMBOLS = {
        'PLAYER': 'R',
        'BOX': 'B',
        'WALL': 'O',
        'TARGET': 'S',
        'FLOOR': ' ',
        'PLAYER_ON_TARGET': '.',
        'BOX_ON_TARGET': '*'
    }

    def __init__(self):
        pygame.init()
        self.examples = self._load_examples()
        self.images = self._load_images()
        self.selected_example = 0
        self.selected_algorithm = None
        self.selected_heuristic = "h1"
        self.search = Search()
        self.screen = None

    def _load_examples(self) -> List[List[List[str]]]:
#        Load all game examples/levels.
        return [
            #figure 4 test examples
            [
                ['O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'S', ' ', 'B', ' ', 'O'],
                ['O', ' ', 'O', 'R', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O']    
            ],

            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
                ['O', ' ', ' ', 'O', 'O', 'O', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'O', '.', ' ', 'O'], #'.' IS PLAYER ON TARGET PLACE
                ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
                ['O', ' ', ' ', 'B', ' ', ' ', 'O', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
            ],
            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', ' ', ' ', ' ', 'O', ' ', ' ', 'O'],
                ['O', ' ', ' ', 'B', 'R', ' ', ' ', 'O'],
                ['O', ' ', ' ', ' ', 'O', 'B', ' ', 'O'],
                ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
                ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                
            ],

            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
                ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
                ['O', 'O', ' ', '*', ' ', ' ', 'O'],
                ['O', ' ', 'B', 'O', 'B', ' ', 'O'],
                ['O', ' ', 'S', 'R', 'S', ' ', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'O', 'O'],
                ['O', 'O', 'O', ' ', ' ', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],

            ],

            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'S', 'O', ' ', ' ', 'O', 'O'],
                ['O', ' ', ' ', ' ', ' ', 'B', ' ', 'O', 'O'],
                ['O', ' ', 'B', ' ', 'R', ' ', ' ', 'S', 'O'],
                ['O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O'],
                ['O', 'O', 'O', 'B', 'O', ' ', 'O', 'O', 'O'],
                ['O', 'O', 'O', ' ', ' ', ' ', 'S', 'O', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ],
            [     
                ['O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'S', ' ', 'O', ' ', 'R', 'O'],
                ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
                ['O', 'S', ' ', ' ', 'B', ' ', 'O'],
                ['O', ' ', ' ', 'O', 'B', ' ', 'O'],
                ['O', 'S', ' ', 'O', ' ', ' ', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O']
            ],
            [
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
                ['O', 'S', 'S', 'S', ' ', 'O', 'O', 'O'],
                ['O', ' ', 'S', ' ', 'B', ' ', ' ', 'O'],
                ['O', ' ', ' ', 'B', 'B', 'B', ' ', 'O'],
                ['O', 'O', 'O', 'O', ' ', ' ', 'R', 'O'],
                ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
            ]

        ]

    def _load_images(self) -> Dict[str, pygame.Surface]:
        #Load and scale all game images
        image_files = {
            self.SYMBOLS['PLAYER']: 'player.jpeg',
            self.SYMBOLS['BOX']: 'box.jpeg',
            self.SYMBOLS['WALL']: 'wall.jpeg',
            self.SYMBOLS['TARGET']: 'target.jpeg',
            self.SYMBOLS['FLOOR']: 'floor.jpeg',
            self.SYMBOLS['PLAYER_ON_TARGET']: 'player_on_target.jpeg',
            self.SYMBOLS['BOX_ON_TARGET']: 'box_on_target.jpeg'
        }
        
        images = {}
        try:
            for symbol, filename in image_files.items():
                path = os.path.join('assets', filename)
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Image file not found: {path}")
                image = pygame.image.load(path)
                images[symbol] = pygame.transform.scale(image, (self.TILE_SIZE, self.TILE_SIZE))
            return images
        except Exception as e:
            print(f"Error loading images: {e}")
            pygame.quit()
            sys.exit(1)

    def _init_display(self, grid: List[List[str]]) -> None:
        #Initialize the display with the correct size for the given grid
        width = len(grid[0]) * self.TILE_SIZE
        height = len(grid) * self.TILE_SIZE
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sokoban Puzzle Solver")

    def draw_grid(self, grid: List[List[str]]) -> None:
        #Draw the game grid on the screen
        if not self.screen:
            self._init_display(grid)
            
        self.screen.fill((0, 0, 0))  # Clear screen with black
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell in self.images:
                    self.screen.blit(
                        self.images[cell],
                        (x * self.TILE_SIZE, y * self.TILE_SIZE)
                    )
        pygame.display.flip()

    def select_example(self) -> None:
        #Let user select a puzzle example
        while True:
            try:
                print("\nAvailable examples:")
                for i, _ in enumerate(self.examples, 1):
                    print(f"{i}. Example {i}")
                choice = int(input(f"Select example (1-{len(self.examples)}): "))
                if 1 <= choice <= len(self.examples):
                    self.selected_example = choice - 1
                    break
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def select_algorithm(self) -> None:
        #Let user select search algorithm and heuristic
        while True:
            try:
                print("\nAvailable algorithms:")
                print("1. Breadth-First Search (BFS)")
                print("2. A* Search")
                choice = int(input("Select algorithm (1-2): "))
                
                if choice == 1:
                    self.selected_algorithm = "BFS"
                    break
                elif choice == 2:
                    self.selected_algorithm = "A*"
                    while True:
                        print("\nAvailable heuristics:")
                        print("h1: Manhattan distance")
                        print("h2: Number of misplaced boxes")
                        print("h3: Combined heuristic")
                        heuristic = input("Select heuristic (h1/h2/h3): ").lower()
                        if heuristic in ['h1', 'h2', 'h3']:
                            self.selected_heuristic = heuristic
                            break
                        print("Invalid heuristic. Please try again.")
                    break
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def run_search(self) -> Optional[List[SokobanPuzzle]]:
        #Run the selected search algorithm and return the solution path.
        initial_state = SokobanPuzzle(self.examples[self.selected_example])
        print("\nSearching for solution...")
        
        try:
            if self.selected_algorithm == "BFS":
                solution_node = self.search.BFS(initial_state)
            else:  # A*
                solution_node = self.search.astar(initial_state, self.selected_heuristic)

            if solution_node:
                path = solution_node.getPath()
                print(f"\nSolution found!")
                print(f"Steps: {len(path) - 1}")
                print(f"Cost: {solution_node.g}")
                return path
            else:
                print("\nNo solution found.")
                return None
        except Exception as e:
            print(f"\nError during search: {e}")
            return None

    def simulate_solution(self, path: List[SokobanPuzzle]) -> None:
        #Animate the solution path
        if not path:
            return

        running = True
        step = 0
        clock = pygame.time.Clock()

        while running and step < len(path):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        step += 1
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            if step < len(path):
                self.draw_grid(path[step].grid)
                clock.tick(2)  # 2 FPS for visualization
            
            pygame.display.flip()

def main():
    try:
        game = SokobanGame()
        game.select_example()
        game.select_algorithm()
        solution_path = game.run_search()
        
        if solution_path:
            game.simulate_solution(solution_path)
            
        pygame.quit()
        print("\nThanks for playing!")
        
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        pygame.quit()
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        pygame.quit()

if __name__ == "__main__":
    main() """