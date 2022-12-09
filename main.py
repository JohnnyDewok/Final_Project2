import pygame
import os
import models
import random

pygame.font.init()
width, height = 1250, 650
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Earth Invader!')

background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (width, height))

def main():
    game_on = True
    game_frames = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont('courier', 25)
    level_font = pygame.font.SysFont('courier', 40)
    game_over_font = pygame.font.SysFont('courier', 70)

    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 8

    player_vel = 12
    player = models.Player(575, 475)

    clock = pygame.time.Clock()
    game_over = False
    game_over_count = 0

    def window_resize():
        win.blit(background, (0, 0))

        lives_label = main_font.render(f'Lives: {lives}', 1, (255, 255, 255))
        level_label = main_font.render(f'Level: {level}', 1, (255, 255, 255))
        enemies_label = main_font.render(f'Enemies Left: {len(enemies)}', 1, (255, 255, 255))

        win.blit(lives_label, (width - level_label.get_width() - 10, 10))
        win.blit(level_label, (10, 10))
        win.blit(enemies_label, (10, 50))
        player.draw(win)

        for enemy in enemies:
            enemy.draw(win)

        if game_over:
            game_over_label = game_over_font.render('GAME OVER', 1, (255, 255, 255))
            win.blit(game_over_label, (width / 2 - game_over_label.get_width() / 2, 350))

        pygame.display.update()

    while game_on:
        clock.tick(game_frames)
        window_resize()
        '''
        Function: to control the movement via voice and microphones.
                Reads text_files and connected MAX MSP match
        with open('text_files/left.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line == '1' and player.x - player_vel > 0:
                    player.x -= player_vel
        with open('text_files/right.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line == '1' and player.x + player_vel + player.get_width() < width:
                    player.x += player_vel
        with open('text_files/forward.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line == '1' and player.y - player_vel > 0:
                    player.y -= player_vel
        with open('text_files/back.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line == '1' and player.y + player_vel + player.get_height() + 15 < height:
                    player.y += player_vel'''

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()

        if keys[pygame.K_a] and player.x - player_vel > 0:
           player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < width:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < height:
            player.y += player_vel

        if len(enemies) == 0:
            level += 1
            wave_length += 10
            for i in range(wave_length):
                enemy = models.Enemy(random.randrange(50, width - 100), random.randrange(-1500, -100),
                                     random.choice(['red', 'yellow', 'grey']))
                enemies.append(enemy)

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 2 * game_frames) == 1:
                enemy.shoot()
            elif models.collide(enemy, player):
                player.health -= 50
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > height:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        if lives <= 0 or player.health <= 0:
            game_over = True
            game_over_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

        if game_over_count > game_frames * 1:
            game_on = False
        else:
            continue


def menu():
    title_font = pygame.font.SysFont('courier', 40)
    rules_font = pygame.font.SysFont('courier',20)
    game_on = True

    while game_on:
        win.blit(background, (0, 0))
        rules_label_1 = rules_font.render('Welcome Cadet, Earth has come under fire from', 1, (255, 255, 255))
        win.blit(rules_label_1, (100, 150))
        rules_label_2 = title_font.render('THE UNKNOWN...', 1, (255, 255, 255))
        win.blit(rules_label_2, (200, 175))
        rules_label_3 = rules_font.render('To combat this threat, we have placed you in charge of your very own Phoenix class starship', 1, (255, 255, 255))
        win.blit(rules_label_3, (100, 250))
        rules_label_4 = rules_font.render('"W" ----- UP', 1, (255, 255, 255))
        win.blit(rules_label_4, (150, 275))
        rules_label_5 = rules_font.render('"S" ----- DOWN', 1, (255, 255, 255))
        win.blit(rules_label_5, (150, 300))
        rules_label_6 = rules_font.render('"A" ----- LEFT', 1, (255, 255, 255))
        win.blit(rules_label_6, (150, 323))
        rules_label_7 = rules_font.render('"D" ----- RIGHT', 1, (255, 255, 255))
        win.blit(rules_label_7, (150, 350))
        rules_label_8 = rules_font.render('"SPACE" - SHOOT', 1, (255, 255, 255))
        win.blit(rules_label_8, (150, 375))
        title_label = title_font.render('Press the SPACE BAR if you are ready ...', 1, (255, 255, 255))
        win.blit(title_label, (width / 2 - title_label.get_width() / 2, 550))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            if event.type == pygame.KEYDOWN:
                main()

    pygame.quit()


menu()
