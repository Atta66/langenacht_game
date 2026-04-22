"""
Entry point for the Drone Swarm game.
Run this file to start the game.
"""
import pygame
from game import Game
from highscores import HighScoreManager
import config


def show_name_input(elapsed_time):
    """Show name input screen for high score."""
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Drone Swarm - Enter Your Name")
    clock = pygame.time.Clock()
    font_large = pygame.font.Font(None, 64)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    player_name = ""
    max_name_length = 20
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    return player_name if player_name.strip() else "Anonymous"
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.unicode.isprintable() and len(player_name) < max_name_length:
                    player_name += event.unicode
        
        screen.fill((20, 20, 30))
        
        # Title
        title = font_large.render("AWESOME RUN!", True, (100, 255, 100))
        title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 8))
        screen.blit(title, title_rect)
        
        # Time display
        time_text = font_medium.render(f"Time: {elapsed_time:.2f}s", True, (100, 200, 255))
        time_rect = time_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 3.5))
        screen.blit(time_text, time_rect)
        
        # Instructions
        instructions = font_small.render("Enter your name for the high scores:", True, (200, 200, 200))
        instructions_rect = instructions.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2.2))
        screen.blit(instructions, instructions_rect)
        
        # Name input box
        input_box = pygame.Rect(config.WINDOW_WIDTH // 4, config.WINDOW_HEIGHT // 2, config.WINDOW_WIDTH // 2, 60)
        pygame.draw.rect(screen, (100, 100, 100), input_box, 3)
        
        # Display name
        name_display = font_medium.render(player_name if player_name else "Enter name...", True, 
                                         (100, 255, 100) if player_name else (100, 100, 100))
        name_rect = name_display.get_rect(center=(input_box.centerx, input_box.centery))
        screen.blit(name_display, name_rect)
        
        # Instruction to confirm
        confirm = font_small.render("Press ENTER to confirm", True, (200, 200, 200))
        confirm_rect = confirm.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT * 0.7))
        screen.blit(confirm, confirm_rect)
        
        pygame.display.flip()
        clock.tick(60)


def show_main_menu():
    """Show main menu."""
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Drone Swarm - Main Menu")
    clock = pygame.time.Clock()
    font_large = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 32)
    
    options = ['Play', 'High Scores', 'Exit']
    selected = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = max(0, selected - 1)
                elif event.key == pygame.K_DOWN:
                    selected = min(len(options) - 1, selected + 1)
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    return options[selected]
        
        screen.fill((20, 20, 30))
        
        # Title
        title = font_large.render("DRONE SWARM", True, (100, 255, 100))
        title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 8))
        screen.blit(title, title_rect)
        
        # Menu options
        for i, option in enumerate(options):
            color = (100, 255, 100) if i == selected else (100, 100, 100)
            text = font_small.render(option, True, color)
            y = config.WINDOW_HEIGHT // 3 + i * config.WINDOW_HEIGHT // 6
            text_rect = text.get_rect(center=(config.WINDOW_WIDTH // 2, y))
            screen.blit(text, text_rect)
        
        # Instructions
        instructions = pygame.font.Font(None, 24).render("Use UP/DOWN to select, ENTER to confirm", True, (200, 200, 200))
        instructions_rect = instructions.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT * 0.95))
        screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        clock.tick(60)


def show_high_scores_menu():
    """Show high scores menu with all 3 categories in columns."""
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Drone Swarm - High Scores")
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 48)
    font_category = pygame.font.Font(None, 36)
    font_score = pygame.font.Font(None, 24)
    font_small = pygame.font.Font(None, 20)
    
    high_score_manager = HighScoreManager()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    pygame.quit()
                    return
                elif event.key == pygame.K_c:
                    # Clear scores
                    high_score_manager.clear_scores()
        
        screen.fill((20, 20, 30))
        
        # Title
        title = font_title.render("HIGH SCORES - TOP 20", True, (100, 255, 100))
        title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT * 0.05))
        screen.blit(title, title_rect)
        
        # Display 3 columns: Easy, Medium, Hard
        col_width = config.WINDOW_WIDTH // 3
        columns = [
            ('easy', col_width // 2, (100, 200, 100)),
            ('medium', col_width + col_width // 2, (200, 200, 100)),
            ('hard', 2 * col_width + col_width // 2, (200, 100, 100))
        ]
        
        for difficulty, x_pos, color in columns:
            # Category header
            header = font_category.render(difficulty.upper(), True, color)
            screen.blit(header, (x_pos - 40, config.WINDOW_HEIGHT * 0.1))
            
            # Get scores for this difficulty
            scores = high_score_manager.get_top_scores(limit=20, difficulty=difficulty)
            
            if scores:
                y_offset = config.WINDOW_HEIGHT * 0.16
                for i, score in enumerate(scores, 1):
                    player_name = score.get('player', 'Anon')[:8]  # Truncate to 8 chars
                    score_text = font_score.render(
                        f"{i:2d}. {player_name:8s} {score['time']:5.1f}s",
                        True,
                        color
                    )
                    screen.blit(score_text, (x_pos - 60, y_offset))
                    y_offset += 26
            else:
                no_scores = font_score.render("No scores yet", True, (100, 100, 100))
                screen.blit(no_scores, (x_pos - 40, config.WINDOW_HEIGHT * 0.2))
        
        # Instructions
        instructions = font_small.render("Press ESC to go back | C to clear all scores", True, (200, 200, 200))
        instructions_rect = instructions.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT * 0.95))
        screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        clock.tick(60)
def show_difficulty_menu():
    """Show difficulty selection menu."""
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Drone Swarm - Select Difficulty")
    clock = pygame.time.Clock()
    font_large = pygame.font.Font(None, 64)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    difficulties = ['easy', 'medium', 'hard']
    selected = 1  # Start with medium
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = max(0, selected - 1)
                elif event.key == pygame.K_RIGHT:
                    selected = min(len(difficulties) - 1, selected + 1)
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    return difficulties[selected]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None
        
        screen.fill((20, 20, 30))
        
        # Title
        title = font_large.render("SELECT DIFFICULTY", True, (255, 255, 255))
        title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 8))
        screen.blit(title, title_rect)
        
        # Difficulty buttons
        for i, difficulty in enumerate(difficulties):
            diff_config = pygame.font.Font(None, 32).render(
                {
                    'easy': 'EASY (20 drones, 5 gates, wide passages)',
                    'medium': 'MEDIUM (30 drones, 5 gates, balanced)',
                    'hard': 'HARD (15 drones, 7 gates, narrow passages)'
                }[difficulty],
                True,
                (100, 255, 100) if i == selected else (100, 100, 100)
            )
            y = config.WINDOW_HEIGHT // 3 + i * config.WINDOW_HEIGHT // 6
            screen.blit(diff_config, (config.WINDOW_WIDTH // 6, y))
        
        # Instructions
        instructions = font_small.render("Use LEFT/RIGHT arrows to select, ENTER to start, ESC to go back", True, (200, 200, 200))
        instructions_rect = instructions.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT * 0.9))
        screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        clock.tick(60)


def main():
    """Start the game."""
    while True:
        choice = show_main_menu()
        
        if choice == 'Play':
            while True:
                difficulty = show_difficulty_menu()
                if difficulty:
                    game = Game(difficulty=difficulty)
                    game.run()
                    
                    # If game was won, show name input, save score, and show high scores
                    if game.game_won:
                        player_name = show_name_input(game.elapsed_time)
                        if player_name:
                            game.high_score_manager.add_score(difficulty, game.elapsed_time, player_name)
                            # Show high scores after saving
                            show_high_scores_menu()
                    
                    # If user didn't press M to return to menu, break back to main menu
                    if not game.return_to_menu:
                        break
                else:
                    # User pressed ESC, go back to main menu
                    break
        
        elif choice == 'High Scores':
            show_high_scores_menu()
        
        else:
            # Exit selected or window closed
            break


if __name__ == "__main__":
    main()
