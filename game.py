"""
Main game class that manages the game loop and coordinates all components.
"""
import pygame
import random
from drone import Drone
from pathway import Pathway
from ui import UI
from vector2d import Vector2D
from highscores import HighScoreManager
import config


class Game:
    """Main game class."""
    
    def __init__(self, difficulty='medium'):
        """Initialize the game with a specific difficulty level."""
        pygame.init()
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Drone Swarm - Boids Algorithm")
        self.clock = pygame.time.Clock()
        self.running = True
        self.return_to_menu = False
        
        # Set difficulty parameters
        self.difficulty = difficulty
        self.difficulty_config = config.DIFFICULTY_LEVELS[difficulty]
        self.apply_difficulty_config()
        
        # Initialize components
        self.ui = UI(self.difficulty_config)
        self.pathway = Pathway(self.difficulty_config)
        self.drones = []
        self.spawn_drones()
        
        # Game state
        self.current_gate_index = 0
        self.drones_at_goal = 0
        self.game_won = False
        
        # Timer
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0.0
        
        # High scores
        self.high_score_manager = HighScoreManager()
        
        # Font for messages
        self.big_font = pygame.font.Font(None, 48)
        self.timer_font = pygame.font.Font(None, 36)
    
    def apply_difficulty_config(self):
        """Apply difficulty-specific configuration."""
        config.NUM_DRONES = self.difficulty_config['num_drones']
        config.NUM_SEGMENTS = self.difficulty_config['num_segments']
        config.PATHWAY_WIDTH = self.difficulty_config['pathway_width']
        config.SEPARATION_RANGE = self.difficulty_config['separation_range']
        config.ALIGNMENT_RANGE = self.difficulty_config['alignment_range']
        config.COHESION_RANGE = self.difficulty_config['cohesion_range']
        config.SUCCESS_THRESHOLD = self.difficulty_config['success_threshold']
        self.seek_weight = self.difficulty_config['seek_weight']
    
    def spawn_drones(self):
        """Spawn drones at the starting position."""
        self.drones = []
        start_x = 50
        start_y = config.WINDOW_HEIGHT // 2
        
        for _ in range(config.NUM_DRONES):
            # Spawn in a small area
            x = start_x + random.randint(-20, 20)
            y = start_y + random.randint(-20, 20)
            self.drones.append(Drone(x, y))
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset with new pathway
                    self.reset_game(new_pathway=True)
                elif event.key == pygame.K_SPACE:
                    # Restart with same pathway
                    self.reset_game(new_pathway=False)
                elif event.key == pygame.K_m:
                    # Return to menu
                    self.return_to_menu = True
                    self.running = False
            
            # Handle UI events
            self.ui.handle_event(event)
    
    def update(self):
        """Update game state."""
        # Update timer only if game is not won
        if not self.game_won:
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
        
        if self.game_won:
            return
        
        # Get boids parameters from sliders
        params = self.ui.get_values()
        
        # Get current target (next gate or goal)
        current_gate = self.pathway.get_next_gate()
        if current_gate is not None:
            target = current_gate['position']
        else:
            target = self.pathway.goal
        
        # Update each drone
        for drone in self.drones:
            # Apply boids rules
            drone.flock(
                self.drones,
                params['separation'],
                params['alignment'],
                params['cohesion']
            )
            
            # Seek target
            seek_force = drone.seek(target, weight=self.seek_weight)
            drone.apply_force(seek_force)
            
            # Update position
            drone.update()
        
        # Check gate progress
        if current_gate is not None:
            drones_through = 0
            for drone in self.drones:
                if self.pathway.check_drone_through_gate(drone.position, current_gate):
                    drones_through += 1
            
            # If enough drones passed, mark gate as passed
            if drones_through >= len(self.drones) * config.SUCCESS_THRESHOLD:
                current_gate['passed'] = True
                self.current_gate_index += 1
        
        # Check if drones reached goal
        else:
            self.drones_at_goal = 0
            for drone in self.drones:
                if drone.position.distance_to(self.pathway.goal) < config.GOAL_RADIUS:
                    self.drones_at_goal += 1
            
            # Win condition
            if self.drones_at_goal >= len(self.drones) * config.SUCCESS_THRESHOLD:
                self.game_won = True
    
    def draw(self):
        """Draw everything on the screen."""
        self.screen.fill(config.BACKGROUND_COLOR)
        
        # Draw pathway segments
        for segment in self.pathway.segments:
            pygame.draw.line(
                self.screen,
                config.PATHWAY_COLOR,
                segment['start'].to_tuple(),
                segment['end'].to_tuple(),
                config.PATHWAY_WIDTH
            )
        
        # Draw gates
        for i, gate in enumerate(self.pathway.gates):
            color = config.GATE_COLOR if gate['passed'] else (100, 100, 100)
            pos = gate['position'].to_tuple()
            width = gate['width']
            
            # Draw gate as a circle
            pygame.draw.circle(self.screen, color, pos, width // 2, config.GATE_THICKNESS)
            
            # Draw gate number
            text = self.ui.font.render(str(i + 1), True, color)
            self.screen.blit(text, (pos[0] - 10, pos[1] - 10))
        
        # Draw goal
        pygame.draw.circle(
            self.screen,
            config.GOAL_COLOR,
            self.pathway.goal.to_tuple(),
            config.GOAL_RADIUS
        )
        
        # Draw drones
        for drone in self.drones:
            pygame.draw.circle(
                self.screen,
                config.DRONE_COLOR,
                drone.position.to_tuple(),
                config.DRONE_SIZE
            )
            
            # Draw direction indicator
            direction = drone.velocity.normalize() * 10
            end_pos = drone.position + direction
            pygame.draw.line(
                self.screen,
                config.DRONE_COLOR,
                drone.position.to_tuple(),
                end_pos.to_tuple(),
                2
            )
        
        # Draw UI
        self.ui.draw(self.screen)
        self.ui.draw_instructions(self.screen)
        
        # Draw timer at top center
        timer_text = self.timer_font.render(
            f"Time: {self.elapsed_time:.2f}s", 
            True, 
            (100, 255, 100)
        )
        timer_rect = timer_text.get_rect(center=(config.WINDOW_WIDTH // 2, 30))
        self.screen.blit(timer_text, timer_rect)
        
        # Draw difficulty level
        difficulty_text = self.ui.font.render(
            f"Difficulty: {self.difficulty_config['name'].upper()}", 
            True, 
            (200, 200, 100)
        )
        self.screen.blit(difficulty_text, (config.WINDOW_WIDTH - 350, 20))
        
        # Draw win message
        if self.game_won:
            # Don't save score automatically - show name input first
            text = self.big_font.render("SUCCESS!", True, (100, 255, 100))
            time_text = self.big_font.render(f"Time: {self.elapsed_time:.2f}s", True, (100, 200, 255))
            instruction = self.ui.font.render("Press R for new pathway | M to menu", True, (200, 200, 200))
            
            y_center = config.WINDOW_HEIGHT // 2
            text_rect = text.get_rect(center=(config.WINDOW_WIDTH // 2, y_center - 40))
            time_rect = time_text.get_rect(center=(config.WINDOW_WIDTH // 2, y_center + 20))
            instr_rect = instruction.get_rect(center=(config.WINDOW_WIDTH // 2, y_center + 80))
            
            pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(40, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), time_rect.inflate(40, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), instr_rect.inflate(40, 20))
            
            self.screen.blit(text, text_rect)
            self.screen.blit(time_text, time_rect)
            self.screen.blit(instruction, instr_rect)
        
        pygame.display.flip()
    
    def reset_game(self, new_pathway=True):
        """Reset the game."""
        if new_pathway:
            self.pathway.reset()
        else:
            # Reset gate states
            for gate in self.pathway.gates:
                gate['passed'] = False
        
        self.spawn_drones()
        self.current_gate_index = 0
        self.drones_at_goal = 0
        self.game_won = False
        self.score_saved = False
        self.start_time = pygame.time.get_ticks()
        self.ui.reset_sliders()
    
    def run(self):
        """Main game loop."""
        show_name_screen_timer = None  # Timer to delay name input screen
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            # If game was just won, wait a moment then exit to show name input
            if self.game_won and show_name_screen_timer is None:
                show_name_screen_timer = pygame.time.get_ticks()
            
            # After 1 second of winning, exit the game loop
            if show_name_screen_timer and (pygame.time.get_ticks() - show_name_screen_timer) > 1000:
                self.running = False
            
            self.clock.tick(config.FPS)
        
        pygame.quit()
