import pygame

pygame.init()

Width = 900
Height = 600

tile_x = 40
tile_y = 40

enemy_kill = 0
player_score = 500
treasure_get1 = False
treasure_get2 = False
treasure_get_now1 = False
treasure_get_now2 = False
treasure_knife = 0
treasure_up = 0
princess_true = False
player_coin = 0
bomb_counter = 0
boss_counter = 0
boss_start = False

score_dis = False
player_deaded = False

buy_flag = False
hint_flag = False
hints_idx = 0
hint1_first = True
hint2_first = True
debt_back = False
debt = False

keep_knife_idx = 0 
keep_debt_on = False
h_counter_cur = 0
deaded = False
ending_true = False

knife_plus = 0
out_camp = False
restart = False

stage_num = 0
stage1_clear = False
stage2_clear = False
boss_nom_dead = False
boss_nom2_dead = False

end_true = False
end_num = -1


window =  pygame.display.set_mode((Width, Height))
knife_group = pygame.sprite.RenderUpdates()
bomb_group = pygame.sprite.RenderUpdates()
explosion_group = pygame.sprite.LayeredUpdates()
bad_group = pygame.sprite.LayeredUpdates()
zombie_group = pygame.sprite.LayeredUpdates()
ball_group = pygame.sprite.LayeredUpdates()
fall_ball_group = pygame.sprite.LayeredUpdates()
magic_man_group = pygame.sprite.LayeredUpdates()
magic_ball_group = pygame.sprite.LayeredUpdates()
boss_lazer_group = pygame.sprite.LayeredUpdates()
boss_ball_night_group = pygame.sprite.LayeredUpdates()
boss_ball_ran_group = pygame.sprite.LayeredUpdates()
boss_lazer_nom_group = pygame.sprite.LayeredUpdates()
boss_ball_night_nom_group = pygame.sprite.LayeredUpdates()
boss_ball_ran_nom_group = pygame.sprite.LayeredUpdates()
boss_group = pygame.sprite.LayeredUpdates()
boss_nom_group = pygame.sprite.LayeredUpdates()
boss2_nom_group = pygame.sprite.LayeredUpdates()