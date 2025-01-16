import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    game_active = True

    try:
        pygame.mixer.music.load("assets/background_music.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    except:
        print("Could not load background music")

    try:
        explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
    except:
        print("Could not load explosion sound")
        explosion_sound = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
        if game_active:
            for obj in updatable:
                obj.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    lives -= 1
                    if lives <= 0:
                        game_active = False
                    else:
                        player.reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        
                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        if explosion_sound:
                            explosion_sound.play()
                        asteroid.split()
                        score += 100

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        if not game_active:
            game_over_text = font.render('GAME OVER', True, (255, 0, 0))
            final_score_text = font.render(f'Final Score: {score}', True, (255, 255, 255))
            restart_text = font.render('Press R to Restart', True, (255, 255, 255))
            
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50))
            screen.blit(final_score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                score = 0
                lives = 3
                game_active = True
                player.reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                for asteroid in asteroids:
                    asteroid.kill()

        pygame.display.flip()
        dt = clock.tick(60) / 1000 

if __name__ == "__main__":
    main()