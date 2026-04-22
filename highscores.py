"""
High scores management system.
Saves and loads high scores from a JSON file.
"""
import json
import os
from pathlib import Path


class HighScoreManager:
    """Manages high scores storage and retrieval."""
    
    def __init__(self, filename="highscores.json"):
        """Initialize high score manager."""
        self.filename = filename
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Load high scores from file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    scores = data.get('scores', [])
                    # Ensure all scores have a player name (for backwards compatibility)
                    for score in scores:
                        if 'player' not in score:
                            score['player'] = 'Anonymous'
                    return scores
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_scores(self):
        """Save high scores to file."""
        with open(self.filename, 'w') as f:
            json.dump({'scores': self.scores}, f, indent=2)
    
    def add_score(self, difficulty, time_elapsed, player_name="Anonymous"):
        """
        Add a new score to the high scores list.
        Keeps top 20 scores per difficulty level.
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
            time_elapsed: Time in seconds (float)
            player_name: Name of the player
        
        Returns:
            rank: The rank of the new score (1 is best), or None if not in top 20
        """
        new_score = {
            'difficulty': difficulty,
            'time': round(time_elapsed, 2),
            'player': player_name,
        }
        
        self.scores.append(new_score)
        # Sort by difficulty, then by time (ascending - faster is better)
        self.scores.sort(key=lambda x: (x['difficulty'], x['time']))
        
        # Keep only top 20 per difficulty level
        difficulty_counts = {'easy': 0, 'medium': 0, 'hard': 0}
        filtered_scores = []
        for score in self.scores:
            diff = score['difficulty']
            if difficulty_counts[diff] < 20:
                filtered_scores.append(score)
                difficulty_counts[diff] += 1
        
        self.scores = filtered_scores
        self.save_scores()
        
        # Find rank of the new score within its difficulty
        difficulty_scores = [s for s in self.scores if s['difficulty'] == difficulty]
        for i, score in enumerate(difficulty_scores):
            if score['time'] == new_score['time'] and score['player'] == new_score['player']:
                return i + 1
        
        return None
    
    def get_top_scores(self, limit=20, difficulty=None):
        """Get top scores, optionally filtered by difficulty."""
        if difficulty:
            scores = [s for s in self.scores if s['difficulty'] == difficulty]
        else:
            scores = self.scores
        return scores[:limit]
    
    def clear_scores(self):
        """Clear all high scores."""
        self.scores = []
        self.save_scores()
    
    def get_scores_by_difficulty(self, difficulty):
        """Get scores for a specific difficulty."""
        return [s for s in self.scores if s['difficulty'] == difficulty]
