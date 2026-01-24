# Drone Swarm Game - Boids Algorithm

A simulation game where you control a swarm of drones using the three boids algorithm rules: separation, alignment, and cohesion. Guide the swarm through randomly generated pathways by adjusting these parameters.

## Features

- **Boids Algorithm**: Implements the three classic boids rules for realistic swarm behavior
- **Random Pathways**: Each game generates a new random path with gates to navigate through
- **Interactive Sliders**: Real-time adjustment of separation, alignment, and cohesion parameters
- **Modular Design**: Clean, well-organized code structure for easy understanding and modification

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

```bash
python main.py
```

## How to Play

1. **Objective**: Guide the drone swarm through all the gates to reach the goal (yellow circle)
2. **Controls**:
   - **Mouse**: Drag sliders to adjust boids parameters
   - **R Key**: Generate a new random pathway
   - **SPACE Key**: Restart with the same pathway
3. **Winning**: Get 80% or more of the drones through all gates and to the goal

## Boids Algorithm Parameters

### Separation (0.0 - 3.0)
- Controls how much drones avoid crowding each other
- Higher values = drones spread out more
- Too high: swarm breaks apart
- Too low: drones collide and cluster

### Alignment (0.0 - 2.0)
- Controls how much drones match velocity with neighbors
- Higher values = drones move in same direction
- Too high: swarm becomes rigid
- Too low: chaotic individual movement

### Cohesion (0.0 - 2.0)
- Controls how much drones move toward the center of the group
- Higher values = tighter group formation
- Too high: swarm collapses into a tight ball
- Too low: swarm disperses

## Project Structure

```
langenacht_game/
│
├── main.py           # Entry point
├── game.py           # Main game loop and logic
├── drone.py          # Drone class with boids implementation
├── pathway.py        # Random pathway generation
├── ui.py             # UI components (sliders, text)
├── vector2d.py       # 2D vector mathematics
├── config.py         # All game constants and settings
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Modular Design

Each file has a specific responsibility:

- **config.py**: All configurable parameters in one place
- **vector2d.py**: Reusable vector math operations
- **drone.py**: Individual drone behavior and boids rules
- **pathway.py**: Pathway and gate generation logic
- **ui.py**: User interface components
- **game.py**: Orchestrates all components
- **main.py**: Simple entry point

## Tips for Success

1. Start with default values and make small adjustments
2. Balance is key - extreme values rarely work
3. Watch how the swarm behaves and adjust accordingly
4. Narrow passages require higher cohesion and lower separation
5. Wide open areas work with more separation

## Customization

Edit `config.py` to customize:
- Number of drones
- Pathway difficulty (width, number of segments)
- Visual appearance (colors, sizes)
- Boids parameter ranges
- Game physics (speed, force limits)

Enjoy experimenting with swarm behavior! 🚁
