"""
Simple 2D vector class for drone movement calculations.
"""
import math


class Vector2D:
    """A simple 2D vector class with basic operations."""
    
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        """Add two vectors."""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Subtract two vectors."""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Multiply vector by scalar."""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        """Divide vector by scalar."""
        if scalar != 0:
            return Vector2D(self.x / scalar, self.y / scalar)
        return Vector2D(0, 0)
    
    def magnitude(self):
        """Calculate the magnitude (length) of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        """Return a normalized (unit) vector."""
        mag = self.magnitude()
        if mag > 0:
            return self / mag
        return Vector2D(0, 0)
    
    def limit(self, max_value):
        """Limit the magnitude of the vector."""
        mag = self.magnitude()
        if mag > max_value:
            return self.normalize() * max_value
        return Vector2D(self.x, self.y)
    
    def distance_to(self, other):
        """Calculate distance to another vector."""
        return (self - other).magnitude()
    
    def copy(self):
        """Return a copy of this vector."""
        return Vector2D(self.x, self.y)
    
    def to_tuple(self):
        """Convert to tuple for pygame."""
        return (int(self.x), int(self.y))
