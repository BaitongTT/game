import pygame
import pygame_button
import test_game_page_1
import test_game_page_2
import test_game_page_3

pygame.init()

def run_game(loop_game, game, screen, clock):
    return loop_game.game_loop(game, screen, clock)

def main():
    game = None
    #framerate
    clock = pygame.time.Clock()
    FPS = 70
    clock.tick(FPS)

    pygame.display.set_caption('Trick or Treat' )
    screen = pygame.display.set_mode((720, 400))
    width, length = screen.get_size() #get the windows size
    #print(width, length) to get 1536, 864
    screen.fill((0, 0, 0))
    
    game = run_game(test_game_page_1, game, screen, clock)
    
    if game == 1:
        game = run_game(test_game_page_2, game, screen, clock)
        
        pygame.quit()
        
        
        
if __name__ == "__main__":
    main()