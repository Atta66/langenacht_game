# Boids Algorithm - Mathematical Explanation

## Overview

The boids algorithm simulates flocking behavior through three fundamental rules. Each rule produces a steering force that influences the drone's movement. This document explains the mathematical implementation in detail.

## Core Concepts

### Vector Representation

Each drone has:
- **Position**: $\vec{p} = (x, y)$ - current location in 2D space
- **Velocity**: $\vec{v} = (v_x, v_y)$ - current direction and speed
- **Acceleration**: $\vec{a} = (a_x, a_y)$ - change in velocity

### Update Loop

Each frame, every drone updates its state:

$$\vec{a}_t = \sum \text{forces}$$

$$\vec{v}_{t+1} = \text{limit}(\vec{v}_t + \vec{a}_t, v_{\max})$$

$$\vec{p}_{t+1} = \vec{p}_t + \vec{v}_{t+1}$$

Where:
- $v_{\max}$ = maximum speed (prevents unrealistic acceleration)
- Forces are accumulated and applied to acceleration
- Velocity is limited to maintain realistic movement

## The Three Boids Rules

### 1. Separation (Avoidance)

**Purpose**: Prevent drones from crowding each other

**Formula**:

$$\vec{F}_{\text{sep}} = w_{\text{sep}} \cdot \text{limit}\left(\text{normalize}\left(\frac{1}{N}\sum_{i=1}^{N} \frac{\vec{p} - \vec{p}_i}{d_i^2}\right) \cdot v_{\max} - \vec{v}, f_{\max}\right)$$

**Step by Step**:

1. **Find neighbors** within perception radius $r_{\text{perception}}$:
   $$N = \{\text{drone}_i \mid d_i < r_{\text{perception}}\}$$
   
   Where: $d_i = \|\vec{p} - \vec{p}_i\|$

2. **Calculate repulsion vector** from each neighbor:
   $$\vec{d}_i = \vec{p} - \vec{p}_i$$
   
3. **Weight by inverse square distance** (closer = stronger repulsion):
   $$\vec{d}_i' = \frac{\vec{d}_i}{d_i^2}$$

4. **Average all repulsion vectors**:
   $$\vec{d}_{\text{avg}} = \frac{1}{N}\sum_{i=1}^{N} \vec{d}_i'$$

5. **Convert to steering force**:
   $$\vec{F}_{\text{desired}} = \text{normalize}(\vec{d}_{\text{avg}}) \cdot v_{\max}$$
   
   $$\vec{F}_{\text{steering}} = \vec{F}_{\text{desired}} - \vec{v}$$

6. **Limit and apply weight**:
   $$\vec{F}_{\text{sep}} = w_{\text{sep}} \cdot \text{limit}(\vec{F}_{\text{steering}}, f_{\max})$$

**Effect of weight $w_{\text{sep}}$**:
- $w_{\text{sep}} = 0$: No separation (drones cluster)
- $w_{\text{sep}} = 1.5$: Balanced spacing
- $w_{\text{sep}} = 3.0$: Strong separation (swarm breaks apart)

### 2. Alignment (Velocity Matching)

**Purpose**: Make drones move in the same direction as neighbors

**Formula**:

$$\vec{F}_{\text{ali}} = w_{\text{ali}} \cdot \text{limit}\left(\text{normalize}\left(\frac{1}{N}\sum_{i=1}^{N} \vec{v}_i\right) \cdot v_{\max} - \vec{v}, f_{\max}\right)$$

**Step by Step**:

1. **Find neighbors** within perception radius:
   $$N = \{\text{drone}_i \mid \|\vec{p} - \vec{p}_i\| < r_{\text{perception}}\}$$

2. **Average neighbor velocities**:
   $$\vec{v}_{\text{avg}} = \frac{1}{N}\sum_{i=1}^{N} \vec{v}_i$$

3. **Convert to desired velocity**:
   $$\vec{v}_{\text{desired}} = \text{normalize}(\vec{v}_{\text{avg}}) \cdot v_{\max}$$

4. **Calculate steering force** (difference from current velocity):
   $$\vec{F}_{\text{steering}} = \vec{v}_{\text{desired}} - \vec{v}$$

5. **Limit and apply weight**:
   $$\vec{F}_{\text{ali}} = w_{\text{ali}} \cdot \text{limit}(\vec{F}_{\text{steering}}, f_{\max})$$

**Effect of weight $w_{\text{ali}}$**:
- $w_{\text{ali}} = 0$: No alignment (chaotic movement)
- $w_{\text{ali}} = 1.0$: Coordinated movement
- $w_{\text{ali}} = 2.0$: Highly synchronized (rigid formation)

### 3. Cohesion (Center Seeking)

**Purpose**: Keep drones together as a group

**Formula**:

$$\vec{F}_{\text{coh}} = w_{\text{coh}} \cdot \text{limit}\left(\text{normalize}\left(\frac{1}{N}\sum_{i=1}^{N} \vec{p}_i - \vec{p}\right) \cdot v_{\max} - \vec{v}, f_{\max}\right)$$

**Step by Step**:

1. **Find neighbors** within perception radius:
   $$N = \{\text{drone}_i \mid \|\vec{p} - \vec{p}_i\| < r_{\text{perception}}\}$$

2. **Calculate center of mass** of neighbors:
   $$\vec{p}_{\text{center}} = \frac{1}{N}\sum_{i=1}^{N} \vec{p}_i$$

3. **Calculate direction to center**:
   $$\vec{d}_{\text{center}} = \vec{p}_{\text{center}} - \vec{p}$$

4. **Convert to desired velocity**:
   $$\vec{v}_{\text{desired}} = \text{normalize}(\vec{d}_{\text{center}}) \cdot v_{\max}$$

5. **Calculate steering force**:
   $$\vec{F}_{\text{steering}} = \vec{v}_{\text{desired}} - \vec{v}$$

6. **Limit and apply weight**:
   $$\vec{F}_{\text{coh}} = w_{\text{coh}} \cdot \text{limit}(\vec{F}_{\text{steering}}, f_{\max})$$

**Effect of weight $w_{\text{coh}}$**:
- $w_{\text{coh}} = 0$: No cohesion (swarm disperses)
- $w_{\text{coh}} = 1.0$: Maintains group
- $w_{\text{coh}} = 2.0$: Tight clustering (may be too dense)

## Combining the Forces

### Force Accumulation

All forces are combined through simple vector addition:

$$\vec{F}_{\text{total}} = \vec{F}_{\text{sep}} + \vec{F}_{\text{ali}} + \vec{F}_{\text{coh}} + \vec{F}_{\text{seek}}$$

Where $\vec{F}_{\text{seek}}$ is the force guiding drones toward the target gate.

### Seek Force (Target Following)

**Formula**:

$$\vec{F}_{\text{seek}} = w_{\text{seek}} \cdot \text{limit}\left(\text{normalize}(\vec{p}_{\text{target}} - \vec{p}) \cdot v_{\max} - \vec{v}, f_{\max}\right)$$

This steers the drone toward the next gate or goal.

## Helper Functions

### Normalize

Convert a vector to unit length (magnitude = 1):

$$\text{normalize}(\vec{v}) = \frac{\vec{v}}{\|\vec{v}\|}$$

Where: $\|\vec{v}\| = \sqrt{v_x^2 + v_y^2}$

### Limit

Cap a vector's magnitude to a maximum value:

$$\text{limit}(\vec{v}, m) = \begin{cases}
\vec{v} & \text{if } \|\vec{v}\| \leq m \\
\text{normalize}(\vec{v}) \cdot m & \text{if } \|\vec{v}\| > m
\end{cases}$$

### Distance

Euclidean distance between two points:

$$d(\vec{p}_1, \vec{p}_2) = \|\vec{p}_1 - \vec{p}_2\| = \sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$$

## Constants Used

| Constant | Symbol | Value | Description |
|----------|--------|-------|-------------|
| Max Speed | $v_{\max}$ | 4.0 | Maximum velocity magnitude |
| Max Force | $f_{\max}$ | 0.1 | Maximum steering force |
| Perception Radius | $r_{\text{perception}}$ | 50 | Neighbor detection range |
| Separation Weight | $w_{\text{sep}}$ | 0.0 - 3.0 | User-adjustable slider |
| Alignment Weight | $w_{\text{ali}}$ | 0.0 - 2.0 | User-adjustable slider |
| Cohesion Weight | $w_{\text{coh}}$ | 0.0 - 2.0 | User-adjustable slider |
| Seek Weight | $w_{\text{seek}}$ | 0.5 | Fixed weight for target seeking |

## Interaction Between Rules

### Balance Dynamics

The three rules create competing forces:

1. **Separation pushes apart** ↔ **Cohesion pulls together**
2. **Alignment synchronizes** → Creates coherent movement
3. **Seek guides** → Provides goal-directed behavior

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

Each drone only considers neighbors within $r_{\text{perception}}$:

$$\text{Neighbors}(\text{drone}) = \{\text{drone}_i \mid d(\text{drone}, \text{drone}_i) < r_{\text{perception}}\}$$

This creates **emergent global behavior** from **local interactions**.

### Steering Behavior

All forces use the same steering pattern:

$$\vec{F}_{\text{steering}} = \vec{v}_{\text{desired}} - \vec{v}_{\text{current}}$$

This creates smooth, realistic turns rather than instant direction changes.

### Force Limitation

By limiting forces to $f_{\max}$, we ensure:
- Smooth acceleration
- No instantaneous changes
- Realistic physics
- Stable simulation

## Implementation Notes

### Computational Complexity

For $N$ drones:
- **Naive approach**: $O(N^2)$ - check every drone against every other
- **Optimization possible**: Spatial partitioning (quadtree) → $O(N \log N)$

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
