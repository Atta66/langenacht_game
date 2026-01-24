"""
Pathway class for generating random paths that drones must navigate through.
"""
import random
from vector2d import Vector2D
import config


class Pathway:
    """Represents a pathway with segments and gates that drones must pass through."""
    
    def __init__(self):
        """Generate a random pathway."""
        self.segments = []
        self.gates = []
        self.goal = None
        self.generate_pathway()
    
    def generate_pathway(self):
        """Generate a random pathway with gates."""
        self.segments = []
        self.gates = []
        
        # Starting position
        current_x = 100
        current_y = config.WINDOW_HEIGHT // 2
        
        # Generate segments
        for i in range(config.NUM_SEGMENTS):
            # Random offset for next segment
            offset_x = random.randint(100, config.PATHWAY_SEGMENT_LENGTH)
            offset_y = random.randint(-150, 150)
            
            next_x = current_x + offset_x
            next_y = current_y + offset_y
            
            # Keep within bounds
            next_y = max(150, min(config.WINDOW_HEIGHT - 150, next_y))
            next_x = min(config.WINDOW_WIDTH - 200, next_x)
            
            # Create gate at this position
            gate = {
                'position': Vector2D(next_x, next_y),
                'width': config.PATHWAY_WIDTH,
                'passed': False
            }
            self.gates.append(gate)
            
            # Store segment
            self.segments.append({
                'start': Vector2D(current_x, current_y),
                'end': Vector2D(next_x, next_y)
            })
            
            current_x = next_x
            current_y = next_y
        
        # Set goal at the end
        self.goal = Vector2D(current_x + 100, current_y)
    
    def get_next_gate(self):
        """Get the next gate that hasn't been passed."""
        for gate in self.gates:
            if not gate['passed']:
                return gate
        return None
    
    def check_drone_through_gate(self, drone_pos, gate):
        """Check if a drone has passed through a gate."""
        if gate is None:
            return False
        
        gate_pos = gate['position']
        width = gate['width']
        
        # Check if drone is within gate boundaries
        distance = drone_pos.distance_to(gate_pos)
        return distance < (width / 2)
    
    def reset(self):
        """Reset all gates and generate a new pathway."""
        self.generate_pathway()
