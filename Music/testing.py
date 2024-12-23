import pygame
import sys

# Initialize pygame
pygame.init()

# Screen settings
WINDOW_WIDTH = pygame.display.Info().current_w  # Initial window width
WINDOW_HEIGHT = pygame.display.Info().current_h  # Initial window height
WINDOW_TITLE = "Music Player"

# Create a windowed mode display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Fullscreen toggle state
fullscreen = False

def toggle_fullscreen():
    global fullscreen, screen
    if fullscreen:
        # Switch to windowed mode
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        fullscreen = False
    else:
        # Switch to fullscreen mode
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        fullscreen = True

def main():     
    global fullscreen
    angle = 0
    clock = pygame.time.Clock()
    record = pygame.image.load("C:\\Users\\sakth\\OneDrive\\Documents\\python projects\\J.A.R.V.I.S\\Image assets\\record.png").convert_alpha()
    background = pygame.image.load("C:\\Users\\sakth\\OneDrive\\Documents\\python projects\\J.A.R.V.I.S\\Image assets\\background.jpg").convert()

    # Center the record on the screen
    record_rect = record.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    toggle_fullscreen()
                
        # Draw background
        screen.blit(background, (0, 0))
        
        # Rotate the record
        rotated_record = pygame.transform.rotate(record, angle)
        rotated_record_rect = rotated_record.get_rect(center=record_rect.center)

        # Draw rotated record
        screen.blit(rotated_record, rotated_record_rect.topleft)

        pygame.display.flip()
        
        # Update angle
        angle -= 1
        angle %= 360 
      
        clock.tick(110)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
