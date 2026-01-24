"""
Drone class implementing the boids algorithm.
Each drone follows three rules: separation, alignment, and cohesion.
"""
import random
from vector2d import Vector2D
import config


class Drone:
    """A single drone that follows boids rules."""
    
    def __init__(self, x, y):
        """Initialize a drone with position and random velocity."""
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ).normalize() * 2
        self.acceleration = Vector2D(0, 0)
    
    def apply_force(self, force):
        """Apply a force to the drone's acceleration."""
        self.acceleration = self.acceleration + force
    
    def update(self):
        """Update drone position based on velocity and acceleration."""
        self.velocity = self.velocity + self.acceleration
        self.velocity = self.velocity.limit(config.MAX_SPEED)
        self.position = self.position + self.velocity
        self.acceleration = Vector2D(0, 0)
    
    def separation(self, drones, weight):
        """
        Separation: steer to avoid crowding local flockmates.
        Drones try to keep distance from nearby drones.
        """
        steering = Vector2D(0, 0)
        total = 0
        
        for other in drones:
            distance = self.position.distance_to(other.position)
            if other != self and distance < config.PERCEPTION_RADIUS:
                diff = self.position - other.position
                diff = diff / (distance ** 2)  # Weight by distance
                steering = steering + diff
                total += 1
        
        if total > 0:
            steering = steering / total
            steering = steering.normalize() * config.MAX_SPEED
            steering = steering - self.velocity
            steering = steering.limit(config.MAX_FORCE)
        
        return steering * weight
    
    def alignment(self, drones, weight):
        """
        Alignment: steer towards the average heading of local flockmates.
        Drones try to match velocity with nearby drones.
        """
        steering = Vector2D(0, 0)
        total = 0
        
        for other in drones:
            distance = self.position.distance_to(other.position)
            if other != self and distance < config.PERCEPTION_RADIUS:
                steering = steering + other.velocity
                total += 1
        
        if total > 0:
            steering = steering / total
            steering = steering.normalize() * config.MAX_SPEED
            steering = steering - self.velocity
            steering = steering.limit(config.MAX_FORCE)
        
        return steering * weight
    
    def cohesion(self, drones, weight):
        """
        Cohesion: steer to move towards the average position of local flockmates.
        Drones try to move towards the center of nearby drones.
        """
        steering = Vector2D(0, 0)
        total = 0
        
        for other in drones:
            distance = self.position.distance_to(other.position)
            if other != self and distance < config.PERCEPTION_RADIUS:
                steering = steering + other.position
                total += 1
        
        if total > 0:
            steering = steering / total
            steering = steering - self.position
            steering = steering.normalize() * config.MAX_SPEED
            steering = steering - self.velocity
            steering = steering.limit(config.MAX_FORCE)
        
        return steering * weight
    
    def seek(self, target, weight=1.0):
        """
        Seek: steer towards a target position.
        Used to guide drones through the pathway.
        """
        desired = target - self.position
        desired = desired.normalize() * config.MAX_SPEED
        steering = desired - self.velocity
        steering = steering.limit(config.MAX_FORCE)
        return steering * weight
    
    def flock(self, drones, sep_weight, ali_weight, coh_weight):
        """
        Apply all three boids rules to the drone.
        Returns the combined force from all rules.
        """
        separation_force = self.separation(drones, sep_weight)
        alignment_force = self.alignment(drones, ali_weight)
        cohesion_force = self.cohesion(drones, coh_weight)
        
        self.apply_force(separation_force)
        self.apply_force(alignment_force)
        self.apply_force(cohesion_force)
