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
    
    def __init__(self):
        """Initialize UI with sliders."""
        pygame.font.init()
        self.font = pygame.font.Font(None, config.FONT_SIZE)
        
        # Create sliders
        self.separation_slider = Slider(
            config.SLIDER_X,
            config.SLIDER_Y_START,
            config.SLIDER_WIDTH,
            config.SLIDER_HEIGHT,
            config.SEPARATION_RANGE[0],
            config.SEPARATION_RANGE[1],
            config.DEFAULT_SEPARATION,
            "Separation"
        )
        
        self.alignment_slider = Slider(
            config.SLIDER_X,
            config.SLIDER_Y_START + config.SLIDER_SPACING,
            config.SLIDER_WIDTH,
            config.SLIDER_HEIGHT,
            config.ALIGNMENT_RANGE[0],
            config.ALIGNMENT_RANGE[1],
            config.DEFAULT_ALIGNMENT,
            "Alignment"
        )
        
        self.cohesion_slider = Slider(
            config.SLIDER_X,
            config.SLIDER_Y_START + config.SLIDER_SPACING * 2,
            config.SLIDER_WIDTH,
            config.SLIDER_HEIGHT,
            config.COHESION_RANGE[0],
            config.COHESION_RANGE[1],
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
    
    def get_values(self):
        """Get current values from sliders."""
        return {
            'separation': self.separation_slider.value,
            'alignment': self.alignment_slider.value,
            'cohesion': self.cohesion_slider.value
        }
    
    def draw_instructions(self, surface):
        """Draw instructions and game info."""
        instructions = [
            "Adjust sliders to help drones navigate through gates",
            "Press R to reset pathway",
            "Press SPACE to restart with same pathway"
        ]
        
        y_offset = config.WINDOW_HEIGHT - 100
        for instruction in instructions:
            text = self.font.render(instruction, True, config.TEXT_COLOR)
            surface.blit(text, (config.SLIDER_X, y_offset))
            y_offset += 25
