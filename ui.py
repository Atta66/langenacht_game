"""
UI components for the game, including sliders for adjusting boids parameters.
"""
import pygame
import config


class Slider:
    """A slider UI element for adjusting values."""
    
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        """Initialize a slider."""
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        
        # Calculate handle position
        self.handle_radius = height
        self.update_handle_position()
    
    def update_handle_position(self):
        """Update handle position based on current value."""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.rect.x + int(ratio * self.rect.width)
    
    def handle_event(self, event):
        """Handle mouse events for the slider."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            handle_rect = pygame.Rect(
                self.handle_x - self.handle_radius,
                self.rect.y - self.handle_radius // 2,
                self.handle_radius * 2,
                self.rect.height + self.handle_radius
            )
            if handle_rect.collidepoint(mouse_pos):
                self.dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = pygame.mouse.get_pos()[0]
            # Constrain to slider bounds
            mouse_x = max(self.rect.x, min(self.rect.x + self.rect.width, mouse_x))
            # Calculate value
            ratio = (mouse_x - self.rect.x) / self.rect.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            self.update_handle_position()
    
    def draw(self, surface, font):
        """Draw the slider on the surface."""
        # Draw label
        label_text = font.render(f"{self.label}: {self.value:.2f}", True, config.TEXT_COLOR)
        surface.blit(label_text, (self.rect.x, self.rect.y - 25))
        
        # Draw slider bar
        pygame.draw.rect(surface, config.SLIDER_COLOR, self.rect)
        
        # Draw handle
        pygame.draw.circle(
            surface,
            config.SLIDER_HANDLE_COLOR,
            (self.handle_x, self.rect.y + self.rect.height // 2),
            self.handle_radius
        )


class UI:
    """Manages all UI elements."""
    
    def __init__(self, difficulty_config=None):
        """Initialize UI with sliders."""
        pygame.font.init()
        self.font = pygame.font.Font(None, config.FONT_SIZE)
        
        # Use difficulty config if provided
        if difficulty_config is None:
            difficulty_config = config.DIFFICULTY_LEVELS['medium']
        
        # Create sliders
        self.separation_slider = Slider(
            config.SLIDER_X,
            config.SLIDER_Y_START,
            config.SLIDER_WIDTH,
            config.SLIDER_HEIGHT,
            difficulty_config['separation_range'][0],
            difficulty_config['separation_range'][1],
            config.DEFAULT_SEPARATION,
            "Separation"
        )
        
        self.alignment_slider = Slider(
            config.SLIDER_X,
            config.SLIDER_Y_START + config.SLIDER_SPACING,
            config.SLIDER_WIDTH,
            config.SLIDER_HEIGHT,
            difficulty_config['alignment_range'][0],
            difficulty_config['alignment_range'][1],
            config.DEFAULT_ALIGNMENT,
            "Alignment"
        )
        
        self.cohesion_slider = Slider(
            config.SLIDER_X,
            config.SLIDER_Y_START + config.SLIDER_SPACING * 2,
            config.SLIDER_WIDTH,
            config.SLIDER_HEIGHT,
            difficulty_config['cohesion_range'][0],
            difficulty_config['cohesion_range'][1],
            config.DEFAULT_COHESION,
            "Cohesion"
        )
        
        self.sliders = [
            self.separation_slider,
            self.alignment_slider,
            self.cohesion_slider
        ]
    
    def handle_event(self, event):
        """Handle events for all UI elements."""
        for slider in self.sliders:
            slider.handle_event(event)
    
    def draw(self, surface):
        """Draw all UI elements."""
        for slider in self.sliders:
            slider.draw(surface, self.font)
        
        # Draw slider descriptions
        self.draw_slider_descriptions(surface)
    
    def draw_slider_descriptions(self, surface):
        """Draw helpful descriptions next to sliders."""
        small_font = pygame.font.Font(None, 22)
        
        # Descriptions for each slider
        descriptions = {
            'separation': 'Drones either ignore or avoid nearby drones',
            'alignment': 'Nearby drones move in sync & parallel',
            'cohesion': 'Drones move towards the center of nearby drones'
        }
        
        # Colors for descriptions
        colors = {
            'separation': (150, 100, 100),
            'alignment': (100, 150, 100),
            'cohesion': (100, 100, 150)
        }
        
        # Draw descriptions next to sliders
        sliders_info = [
            ('separation', self.separation_slider, config.SLIDER_Y_START),
            ('alignment', self.alignment_slider, config.SLIDER_Y_START + config.SLIDER_SPACING),
            ('cohesion', self.cohesion_slider, config.SLIDER_Y_START + config.SLIDER_SPACING * 2)
        ]
        
        for key, slider, y_pos in sliders_info:
            desc_text = small_font.render(descriptions[key], True, colors[key])
            surface.blit(desc_text, (config.SLIDER_X + config.SLIDER_WIDTH + 40, y_pos - 5))
            
            # Draw current value
            value_text = small_font.render(f"({slider.value:.1f})", True, colors[key])
            surface.blit(value_text, (config.SLIDER_X + config.SLIDER_WIDTH + 40, y_pos + 18))
    
    def get_values(self):
        """Get current values from sliders."""
        return {
            'separation': self.separation_slider.value,
            'alignment': self.alignment_slider.value,
            'cohesion': self.cohesion_slider.value
        }
    
    def reset_sliders(self):
        """Reset all sliders to default values."""
        self.separation_slider.value = config.DEFAULT_SEPARATION
        self.separation_slider.update_handle_position()
        
        self.alignment_slider.value = config.DEFAULT_ALIGNMENT
        self.alignment_slider.update_handle_position()
        
        self.cohesion_slider.value = config.DEFAULT_COHESION
        self.cohesion_slider.update_handle_position()
    
    def draw_instructions(self, surface):
        """Draw instructions and game info."""
        small_font = pygame.font.Font(None, 26)
        tiny_font = pygame.font.Font(None, 22)
        
        # Main instructions
        instructions = [
            "🎮 Adjust sliders to guide the swarm through gates to the goal",
            "⌨️ R: new pathway | SPACE: restart | M: menu"
        ]
        
        y_offset = config.WINDOW_HEIGHT - 110
        for instruction in instructions:
            text = small_font.render(instruction, True, config.TEXT_COLOR)
            surface.blit(text, (config.SLIDER_X, y_offset))
            y_offset += 30
        
        # Quick tips
        tip_text = tiny_font.render("💡 Tip: Balance all 3 sliders for best results", True, (150, 150, 100))
        surface.blit(tip_text, (config.SLIDER_X, config.WINDOW_HEIGHT - 35))
