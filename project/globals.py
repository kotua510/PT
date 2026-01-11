import pygame

pygame.init()

Width = 900
Height = 600

tile_x = 40
tile_y = 40

enemy_kill = 0

player_score = 500

boss_counter = 0

player_coin = 0

bomb_counter = 0

buy_flag = False
hint_flag = False

keep_knife_idx = 0 #これと下グローバルに移動
keep_debt_on = False
hint_first = True
debt_back = False
debt = False

h_counter_cur = 0


knife_plus = 0

out_camp = False
restart = False


window =  pygame.display.set_mode((Width, Height))




knife_group = pygame.sprite.RenderUpdates()

bomb_group = pygame.sprite.RenderUpdates()

explosion_group = pygame.sprite.LayeredUpdates()

bad_group = pygame.sprite.LayeredUpdates()

zombie_group = pygame.sprite.LayeredUpdates()

ball_group = pygame.sprite.LayeredUpdates()

magic_man_group = pygame.sprite.LayeredUpdates()

magic_ball_group = pygame.sprite.LayeredUpdates()

boss_lazer_group = pygame.sprite.LayeredUpdates()

boss_group = pygame.sprite.LayeredUpdates()

