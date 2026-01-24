"""
Main game class that manages the game loop and coordinates all components.
"""
import pygame
import random
from drone import Drone
from pathway import Pathway
from ui import UI
from vector2d import Vector2D
import config


class Game:
    """Main game class."""
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("Drone Swarm - Boids Algorithm")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize components
        self.ui = UI()
        self.pathway = Pathway()
        self.drones = []
        self.spawn_drones()
        
        # Game state
        self.current_gate_index = 0
        self.drones_at_goal = 0
        self.game_won = False
        
        # Font for messages
        self.big_font = pygame.font.Font(None, 48)
    
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
            
            # Handle UI events
            self.ui.handle_event(event)
    
    def update(self):
        """Update game state."""
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
            seek_force = drone.seek(target, weight=0.5)
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
        
        # Draw win message
        if self.game_won:
            text = self.big_font.render("SUCCESS! Press R for new pathway", True, (100, 255, 100))
            text_rect = text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2))
            pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(20, 20))
            self.screen.blit(text, text_rect)
        
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
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(config.FPS)
        
        pygame.quit()
