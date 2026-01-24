# Boids Algorithm - Mathematical Explanation

## Overview

The boids algorithm simulates flocking behavior through three fundamental rules. Each rule produces a steering force that influences the drone's movement. This document explains the mathematical implementation in detail.

## Core Concepts

### Vector Representation

Each drone has:
- **Position**: **p** = (x, y) - current location in 2D space
- **Velocity**: **v** = (vₓ, vᵧ) - current direction and speed
- **Acceleration**: **a** = (aₓ, aᵧ) - change in velocity

### Update Loop

Each frame, every drone updates its state:

```
acceleration(t) = Σ forces

velocity(t+1) = limit(velocity(t) + acceleration(t), max_speed)

position(t+1) = position(t) + velocity(t+1)
```

Where:
- `max_speed` = maximum speed (prevents unrealistic acceleration)
- Forces are accumulated and applied to acceleration
- Velocity is limited to maintain realistic movement

## The Three Boids Rules

### 1. Separation (Avoidance)

**Purpose**: Prevent drones from crowding each other

**Formula Overview**:
```
F_separation = weight_sep × limit(normalize(avg_repulsion) × max_speed - velocity, max_force)
```

**Step by Step**:

1. **Find neighbors** within perception radius (50 pixels):
   ```
   Neighbors = {drone_i | distance(drone, drone_i) < perception_radius}
   ```
   
   Where distance is: `distance = √((x₁-x₂)² + (y₁-y₂)²)`

2. **Calculate repulsion vector** from each neighbor:
   ```
   diff = my_position - neighbor_position
   ```
   
3. **Weight by inverse square distance** (closer = stronger repulsion):
   ```
   weighted_diff = diff / (distance²)
   ```
   
   This means:
   - Distance = 10 → weight = 1/100 = 0.01
   - Distance = 5 → weight = 1/25 = 0.04 (4× stronger!)
   - Closer drones push away much harder

4. **Average all repulsion vectors**:
   ```
   avg_repulsion = sum(all weighted_diffs) / count(neighbors)
   ```

5. **Convert to steering force**:
   ```
   desired_velocity = normalize(avg_repulsion) × max_speed
   steering_force = desired_velocity - current_velocity
   ```

6. **Limit and apply weight**:
   ```
   F_separation = weight_sep × limit(steering_force, max_force)
   ```

**Effect of weight_sep**:
- `weight_sep = 0`: No separation → drones cluster and collide
- `weight_sep = 1.5`: Balanced spacing → natural flock
- `weight_sep = 3.0`: Strong separation → swarm breaks apart

### 2. Alignment (Velocity Matching)

**Purpose**: Make drones move in the same direction as neighbors

**Formula Overview**:
```
F_alignment = weight_ali × limit(normalize(avg_velocity) × max_speed - velocity, max_force)
```

**Step by Step**:

1. **Find neighbors** within perception radius:
   ```
   Neighbors = {drone_i | distance(drone, drone_i) < perception_radius}
   ```

2. **Average neighbor velocities**:
   ```
   avg_velocity = sum(all neighbor velocities) / count(neighbors)
   ```
   
   Example:
   - Neighbor 1 velocity: (3, 1)
   - Neighbor 2 velocity: (2, 2)
   - Neighbor 3 velocity: (4, 0)
   - Average: ((3+2+4)/3, (1+2+0)/3) = (3, 1)

3. **Convert to desired velocity**:
   ```
   desired_velocity = normalize(avg_velocity) × max_speed
   ```
   
   This makes the drone want to match the group's direction at full speed

4. **Calculate steering force** (difference from current velocity):
   ```
   steering_force = desired_velocity - current_velocity
   ```

5. **Limit and apply weight**:
   ```
   F_alignment = weight_ali × limit(steering_force, max_force)
   ```

**Effect of weight_ali**:
- `weight_ali = 0`: No alignment → chaotic, independent movement
- `weight_ali = 1.0`: Coordinated movement → flies like a flock
- `weight_ali = 2.0`: Highly synchronized → rigid formation, turns as one

### 3. Cohesion (Center Seeking)

**Purpose**: Keep drones together as a group

**Formula Overview**:
```
F_cohesion = weight_coh × limit(normalize(center - position) × max_speed - velocity, max_force)
```

**Step by Step**:

1. **Find neighbors** within perception radius:
   ```
   Neighbors = {drone_i | distance(drone, drone_i) < perception_radius}
   ```

2. **Calculate center of mass** of neighbors:
   ```
   center_x = sum(all neighbor x positions) / count(neighbors)
   center_y = sum(all neighbor y positions) / count(neighbors)
   center = (center_x, center_y)
   ```
   
   Example:
   - Neighbor at (100, 50)
   - Neighbor at (120, 60)
   - Neighbor at (110, 70)
   - Center: ((100+120+110)/3, (50+60+70)/3) = (110, 60)

3. **Calculate direction to center**:
   ```
   direction_to_center = center - my_position
   ```
   
   If I'm at (90, 50) and center is (110, 60):
   - direction = (110-90, 60-50) = (20, 10)
   - This points toward the group!

4. **Convert to desired velocity**:
   ```
   desired_velocity = normalize(direction_to_center) × max_speed
   ```

5. **Calculate steering force**:
   ```
   steering_force = desired_velocity - current_velocity
   ```

6. **Limit and apply weight**:
   ```
   F_cohesion = weight_coh × limit(steering_force, max_force)
   ```

**Effect of weight_coh**:
- `weight_coh = 0`: No cohesion → swarm disperses, drones fly apart
- `weight_coh = 1.0`: Maintains group → stays together while moving
- `weight_coh = 2.0`: Tight clustering → may collapse into a dense ball

## Combining the Forces

### Force Accumulation

All forces are combined through simple vector addition:

```
F_total = F_separation + F_alignment + F_cohesion + F_seek
```

Where `F_seek` is the force guiding drones toward the target gate.

**Example calculation for one drone**:
```
F_separation = (2.0, -1.0)   // Push away from neighbors
F_alignment  = (3.0,  1.5)   // Match neighbor directions
F_cohesion   = (-0.5, 0.5)   // Pull toward group center
F_seek       = (1.0,  2.0)   // Head to goal

F_total = (2.0 + 3.0 + (-0.5) + 1.0, -1.0 + 1.5 + 0.5 + 2.0)
        = (5.5, 3.0)

This becomes the drone's acceleration!
```

### Seek Force (Target Following)

**Formula Overview**:
```
F_seek = weight_seek × limit(normalize(target - position) × max_speed - velocity, max_force)
```

This steers the drone toward the next gate or goal.

**How it works**:
1. Calculate direction to target: `target - my_position`
2. Make it a desired velocity: `normalize(direction) × max_speed`
3. Calculate needed steering: `desired - current_velocity`
4. Limit and apply weight: `weight × limit(steering, max_force)`

## Helper Functions

### Normalize

Convert a vector to unit length (magnitude = 1):

```python
def normalize(vector):
    magnitude = sqrt(vector.x² + vector.y²)
    if magnitude > 0:
        return (vector.x / magnitude, vector.y / magnitude)
    return (0, 0)
```

**Example**:
```
vector = (3, 4)
magnitude = √(3² + 4²) = √(9 + 16) = √25 = 5
normalized = (3/5, 4/5) = (0.6, 0.8)
new magnitude = √(0.6² + 0.8²) = √(0.36 + 0.64) = √1 = 1 ✓
```

### Limit

Cap a vector's magnitude to a maximum value:

```python
def limit(vector, max_value):
    magnitude = sqrt(vector.x² + vector.y²)
    if magnitude > max_value:
        return normalize(vector) × max_value
    return vector
```

**Example**:
```
vector = (6, 8), magnitude = 10
max_value = 4
Result: normalize(6, 8) × 4 = (0.6, 0.8) × 4 = (2.4, 3.2)
New magnitude = 4 ✓
```

### Distance

Euclidean distance between two points:

```python
def distance(point1, point2):
    dx = point1.x - point2.x
    dy = point1.y - point2.y
    return sqrt(dx² + dy²)
```

**Example**:
```
point1 = (100, 50)
point2 = (130, 90)
distance = √((100-130)² + (50-90)²)
         = √((-30)² + (-40)²)
         = √(900 + 1600)
         = √2500
         = 50 pixels
```

## Constants Used

| Constant | Value | Description |
|----------|-------|-------------|
| `MAX_SPEED` | 4.0 | Maximum velocity magnitude (pixels/frame) |
| `MAX_FORCE` | 0.1 | Maximum steering force (prevents sharp turns) |
| `PERCEPTION_RADIUS` | 50 | Neighbor detection range (pixels) |
| `weight_separation` | 0.0 - 3.0 | User-adjustable slider |
| `weight_alignment` | 0.0 - 2.0 | User-adjustable slider |
| `weight_cohesion` | 0.0 - 2.0 | User-adjustable slider |
| `weight_seek` | 0.5 | Fixed weight for target seeking |

## Interaction Between Rules

### Balance Dynamics

The three rules create competing forces:

1. **Separation pushes apart** ↔ **Cohesion pulls together**
   - Too much separation → swarm spreads out and disconnects
   - Too much cohesion → swarm collapses into a tight ball
   - Balance needed for natural spacing

2. **Alignment synchronizes** → Creates coherent movement
   - Helps the swarm move as one unit
   - Enables coordinated turns through gates
   - Too much = rigid formation, too little = chaos

3. **Seek guides** → Provides goal-directed behavior
   - Pulls the swarm toward the target
   - Competes with separation (which might push away from target)
   - Works with cohesion (keeps everyone heading to target together)

### Emergent Behavior

Different weight combinations produce different behaviors:

| Separation | Alignment | Cohesion | Behavior |
|------------|-----------|----------|----------|
| High | Low | Low | Dispersed, chaotic |
| Low | High | High | Tight, synchronized ball |
| Balanced | Balanced | Balanced | Natural flock behavior |
| Medium | High | Low | Parallel streams |
| Low | Low | High | Clustered, unstable |

### Navigation Challenge

To navigate through gates successfully:
- **Narrow passages**: Need higher cohesion (stay together) and lower separation (allow clustering)
- **Tight turns**: Need higher alignment (turn together) and moderate cohesion
- **Wide spaces**: Can increase separation without losing formation
- **All cases**: Balance is critical - extreme values usually fail

## Mathematical Properties

### Locality

Each drone only considers neighbors within perception radius:

```
Neighbors(drone) = {drone_i | distance(drone, drone_i) < PERCEPTION_RADIUS}
```

This creates **emergent global behavior** from **local interactions**.

**What this means**:
- No central controller
- Each drone follows simple rules
- Complex flock behavior emerges naturally
- Like real birds or fish!

### Steering Behavior

All forces use the same steering pattern:

```
steering_force = desired_velocity - current_velocity
```

This creates smooth, realistic turns rather than instant direction changes.

**Why this works**:
- If you want to go right but you're going left, the steering force points right
- The bigger the difference, the stronger the turn
- Creates natural, physics-based movement

### Force Limitation

By limiting forces to `MAX_FORCE`, we ensure:
- **Smooth acceleration**: Drones can't instantly change direction
- **No instantaneous changes**: Realistic physics
- **Stable simulation**: Prevents numerical explosions
- **Predictable behavior**: Makes tuning easier

## Implementation Notes

### Computational Complexity

For N drones:
- **Naive approach**: O(N²) - check every drone against every other
  - 30 drones = 30 × 29 = 870 comparisons per frame
  - 60 FPS = 52,200 comparisons per second
  
- **Optimization possible**: Spatial partitioning (quadtree) → O(N log N)
  - Only check drones in nearby cells
  - Much faster for large swarms (100+ drones)

Current implementation uses naive approach (sufficient for 30 drones).

### Numerical Stability

Important checks:
- Avoid division by zero in normalize: check if $\|\vec{v}\| > 0$
- Avoid division by zero in distance weighting: check if $d > 0$
- Limit extreme forces to prevent instability

## Experimentation Guide

### Finding Good Parameters

1. **Start with defaults**: sep=1.5, ali=1.0, coh=1.0
2. **Observe behavior**: Is swarm too loose? Too tight? Chaotic?
3. **Adjust one at a time**: See isolated effects
4. **Find balance**: All three must work together

### Common Problems and Solutions

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Swarm breaks apart | Separation too high | Decrease separation |
| Drones collide | Separation too low | Increase separation |
| Chaotic movement | Alignment too low | Increase alignment |
| Can't turn | Alignment too high | Decrease alignment |
| Swarm disperses | Cohesion too low | Increase cohesion |
| Dense clustering | Cohesion too high | Decrease cohesion |

### Advanced Tuning

Consider the pathway characteristics:
- **Pathway width** ↔ Separation tolerance
- **Turn sharpness** ↔ Alignment need
- **Gate spacing** ↔ Cohesion requirement

---

## Further Reading

- **Original Paper**: Reynolds, C. W. (1987). "Flocks, herds and schools: A distributed behavioral model"
- **Steering Behaviors**: Reynolds' autonomous character paper
- **Game AI**: "Programming Game AI by Example" by Mat Buckland

## Code Reference

See these files for implementation:
- `drone.py` - Lines 28-95: Three boids rules implementation
- `vector2d.py` - Vector mathematics utilities
- `config.py` - All constants and parameters

---

*Understanding these formulas will help you predict how parameter changes affect swarm behavior and successfully navigate the challenges!*
