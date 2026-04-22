# Drone Swarm Game - Boids Algorithm

A simulation game where you control a swarm of drones using the three boids algorithm rules: separation, alignment, and cohesion. Guide the swarm through randomly generated pathways by adjusting these parameters.

## Features

- **Boids Algorithm**: Implements the three classic boids rules for realistic swarm behavior
- **Random Pathways**: Each game generates a new random path with gates to navigate through
- **Interactive Sliders**: Real-time adjustment of separation, alignment, and cohesion parameters
- **Timer & High Scores**: Track your best times across 3 difficulty levels
- **Persistent Leaderboard**: Top 20 scores saved and loaded automatically
- **3 Difficulty Levels**: Easy, Medium, and Hard with unique challenges
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

1. **Main Menu**: Launch the game to see the main menu (Play, High Scores, Exit)
2. **Difficulty Selection**: Choose from Easy, Medium, or Hard before each game
3. **Objective**: Guide the drone swarm through all the gates to reach the goal (yellow circle)
4. **Timer**: Your completion time is displayed at the top center of the screen
5. **Controls**:
   - **Mouse**: Drag sliders to adjust boids parameters
   - **R Key**: Generate a new random pathway
   - **SPACE Key**: Restart with the same pathway
   - **M Key**: Return to main menu during gameplay
6. **Winning**: 
   - Get the required percentage of drones through all gates and to the goal (varies by difficulty)
   - Timer freezes when you reach the goal
   - **Name Entry Screen appears automatically** - enter your name to save your score
   - High scores display with all 3 difficulty categories shown side-by-side

## Difficulty Levels

### Easy 🟢
- **40 drones** - More drones but not too easy
- **4 gates** - Moderate pathway length
- **Wide passages** - 170px gate width for learning
- **Relaxed controls** - Wider slider ranges:
  - Separation: 0.0 - 3.5
  - Alignment: 0.0 - 2.5
  - Cohesion: 0.0 - 2.5
- **Good guidance** - Drones pulled toward gates (seek_weight: 0.6)
- **70% threshold** - 70% of drones must reach goal
- **Perfect for**: Learning the game mechanics

### Medium 🟡 (Default)
- **30 drones** - Balanced challenge
- **5 gates** - Standard pathway complexity
- **Standard passages** - 150px gate width
- **Standard controls** - Default slider ranges:
  - Separation: 0.0 - 3.0
  - Alignment: 0.0 - 2.0
  - Cohesion: 0.0 - 2.0
- **Moderate guidance** - Moderate pulling toward gates (seek_weight: 0.5)
- **Standard threshold** - 80% of drones must reach goal
- **Perfect for**: Main gameplay experience

### Hard 🔴
- **15 drones** - Few drones, every one counts!
- **7 gates** - Long, challenging pathway
- **Narrow passages** - 80px gate width, requires tight control
- **Restricted controls** - Limited slider ranges:
  - Separation: 0.0 - 2.0
  - Alignment: 0.0 - 1.5
  - Cohesion: 0.0 - 1.5
- **Weak guidance** - Drones barely guided toward gates (seek_weight: 0.2)
- **High threshold** - 90% of drones must reach goal (almost all!)
- **Perfect for**: Experienced players seeking a real challenge

## Boids Algorithm Parameters

### Separation (varies by difficulty)
- Controls how much drones avoid crowding each other
- Higher values = drones spread out more
- Too high: swarm breaks apart
- Too low: drones collide and cluster

### Alignment (varies by difficulty)
- Controls how much drones match velocity with neighbors
- Higher values = drones move in same direction
- Too high: swarm becomes rigid
- Too low: chaotic individual movement

### Cohesion (varies by difficulty)
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

## High Scores & Leaderboard

- **Automatic Name Prompt**: When you win, the name input screen appears automatically
- **3-Column Display**: View Easy, Medium, and Hard scores side-by-side
- **Top 20 Per Category**: Each difficulty tracks its own top 20 fastest times
- **Player Names**: Each score displays the player's name for recognition
- **After Name Entry**: High scores screen is shown automatically with your score displayed
- **File Storage**: Scores are saved in `highscores.json` in the game directory
- **Persistent**: Scores persist between game sessions - compete to beat your own records!
- **Clear Scores**: Press 'C' while viewing high scores to clear all scores

## Tips for Success

1. Start with default values and make small adjustments
2. Balance is key - extreme values rarely work
3. Watch how the swarm behaves and adjust accordingly
4. Narrow passages require higher cohesion and lower separation
5. Wide open areas work with more separation
6. Try different difficulties to compete for the fastest times!

## Customization

Edit `config.py` to customize:
- Number of drones
- Pathway difficulty (width, number of segments)
- Visual appearance (colors, sizes)
- Boids parameter ranges
- Game physics (speed, force limits)

Enjoy experimenting with swarm behavior! 🚁
