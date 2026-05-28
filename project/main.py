import pygame
from hud import Hud
from map import Map
from camp import Camp
from my_night import My_night
from weapons.bomb import Bomb
from weapons.knife import Knife
from enemies.bad import Bad
from enemies.ball import Ball
from enemies.fall_boll import Fall_Ball
from enemies.boss import Boss
from enemies.boss2 import Boss2
from enemies.boss3 import Boss3
from enemies.boss_nom import Boss_nom
from enemies.boss2_nom import Boss2_nom
from enemies.magic_man import Magic_man
from enemies.zombie import Zombie
import globals
from status import Status
from opening import Opening


pygame.init()

def init():

  group = pygame.sprite.RenderUpdates()
  map =Map()
  camp = Camp()
  hud = Hud(map.clock_counter, map.bomb_get)
  night = My_night(map, globals.window,globals.player_score, globals.bad_group, globals.zombie_group, globals.ball_group,globals.fall_ball_group, globals.magic_man_group, globals.magic_ball_group,globals.boss_group,globals.boss_lazer_group,globals.boss_ball_night_group,globals.boss_ball_ran_group,globals.boss_ball_ran_nom_group,globals.boss_ball_night_nom_group,globals.boss_lazer_nom_group,globals.boss_nom_group,globals.boss2_nom_group)
  group.add(night)

  return group, night, map, hud, camp

def opening():
  pygame.init()
  pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
  pygame.mixer.set_num_channels(128)

  title_BGM = pygame.mixer.Sound("sound/stage/title.mp3")
  opening_bool = True
  opening = Opening()
  title_BGM.set_volume(0.2)
  title_BGM.play(-1)

  while opening_bool:
    opening.update()
    action = pygame.key.get_pressed()
    if action[pygame.K_RETURN]:
          opening_bool = False
          title_BGM.stop()
          
    for e in pygame.event.get():
            if e.type == pygame.QUIT:
                opening_bool = False
                pygame.quit()

def clear_enemy_groups():
  globals.bad_group.empty()
  globals.zombie_group.empty()
  globals.ball_group.empty()
  globals.fall_ball_group.empty()
  globals.magic_man_group.empty()
  globals.magic_ball_group.empty()
  globals.boss_group.empty()
  globals.boss_lazer_group.empty()
  globals.boss_ball_night_group.empty()
  globals.boss_nom_group.empty()
  globals.boss2_nom_group.empty()

def main():
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.set_num_channels(128)
  clock = pygame.time.Clock()

  group, night, map, hud, camp = init()
  clear_enemy_groups()
  running = True
  weapon_cooltime = False
  attck_cooltime_start = 0
  global knife
  knife_rawrect = globals.knife_group.sprites()[0].rawrect if globals.knife_group else pygame.Rect(0, 0, 0, 0)
  bomb_rawrect = globals.bomb_group.sprites()[0].rawrect if globals.bomb_group else pygame.Rect(0, 0, 0, 0)

  bad_positions = [
    (1400, 330),(1460, 330),(2010,400),(2270,350),(2250,380),(2290,320),(4260,180),(4300,140),(4340,220),
    (6200,140),(6250,180),(8650,320),(8700,450),(12180,350),(12280, 380),(12320,450)
    ]
  
  zombie_positions = [
    (1050, 480), (1100, 480),(2150,480),(2200,480),(2250,480),(6250,280),(6300,280),(9700,480),(9800,480),
    (12800,200),(12880,200)
    ]

  ball_positions = [
      (1300, 440),(7200,440),(7300,440),(7780,350),(7880,300),(7980,210)
    ]
  
  magic_man_positions = [
    (4960,200),(5160, 160),(8400, 480),(9800,480),(10320,480),(10480,320),(10649,200)
    ]

  for pos in bad_positions:
        bad = Bad((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
        globals.bad_group.add(bad, layer=2)

  for pos in zombie_positions:
        zombie = Zombie((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
        globals.zombie_group.add(zombie, layer=2)

  for pos in ball_positions:
        ball = Ball((pos[0], pos[1], 80, 80), night, knife_rawrect, bomb_rawrect, map)
        globals.ball_group.add(ball, layer=2)
        
  for pos in magic_man_positions:
        magic_man = Magic_man((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
        globals.magic_man_group.add(magic_man, layer=2)

  boss = Boss((14280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
  globals.boss_group.add(boss)

  while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        weapon_now_time = pygame.time.get_ticks()
        action = pygame.key.get_pressed()

        globals.window.fill((144, 215, 236))
        if night.status == Status.DEADING:
          pygame.display.flip
          continue

        if night.status == Status.DEAD:
          globals.deaded = True
          globals.player_score = hud.keep_time
          globals.player_coin = map.keep_coin
          globals.boss_start = False
          group, night, map, hud, camp = init()
          clear_enemy_groups()
          globals.player_deaded = True
          globals.boss_nom_dead = False
          globals.boss_nom2_dead = False
          globals.score_dis = False
          if globals.treasure_get_now1 == True:
            globals.treasure_get1 = False
          if globals.treasure_get_now2 == True:
            globals.treasure_get2 = False
          
          if  globals.stage_num == 0:
            bad_positions = [
    (1400, 330),(1460, 330),(2010,400),(2270,350),(2250,380),(2290,320),(4260,180),(4300,140),(4340,220),
    (6200,140),(6250,180),(8650,320),(8700,450),(12180,350),(12280, 380),(12320,450)
    ]
  
            zombie_positions = [
    (1050, 480), (1100, 480),(2150,480),(2200,480),(2250,480),(6250,280),(6300,280),(9700,480),(9800,480),
    (12800,200),(12880,200)
    ]

            ball_positions = [
      (1300, 440),(7200,440),(7300,440),(7780,350),(7880,300),(7980,210)
    ]

            fall_ball_positions = []
  
            magic_man_positions = [
    (4960,200),(5160, 160),(8400, 480),(9800,480),(10320,480),(10480,320),(10649,200)
    ]

            boss = Boss((14280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss_group.add(boss)
          
          elif globals.stage_num == 1:
            bad_positions = [
    (1660, 280),(1700, 350),(2400,350),(4000,280),(5800,280),(5900,300)
    ]
  
            zombie_positions = [
    (6200, 280), (6270, 280)
    ]


            fall_ball_positions = [
      (2880, 0),(3640,0),(4300,0),(4780,0),(5625,0),(6280,0),(6680,0),(7710,0),
      (7780,0),(8180,0),(9080,0),(10050,0),(10220,0),(11000,0),(11400,0),(11800,0),
      (6480,0),(7880,0),(8080,0),(11200,0),(11600,0),(7980,0)
    ]

            ball_positions = []

  
            magic_man_positions = [
    (5180,400),
    ]

            boss = Boss2((14280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss_group.add(boss)

          elif globals.stage_num == 2:
            clear_enemy_groups()
            bad_positions = []
            zombie_positions = []
            ball_positions = []
            fall_ball_positions = []
            magic_man_positions = []
            boss_nom = Boss_nom((3240, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss_nom_group.add(boss_nom)
            boss2_nom = Boss2_nom((6600, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss2_nom_group.add(boss2_nom)
            boss = Boss3((13280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss_group.add(boss)

          for pos in bad_positions:
            bad = Bad((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
            globals.bad_group.add(bad, layer=2)


          for pos in zombie_positions:
            zombie = Zombie((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
            globals.zombie_group.add(zombie, layer=2)

          for pos in ball_positions:
            ball = Ball((pos[0], pos[1], 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.ball_group.add(ball, layer=2)

          for pos in fall_ball_positions:
            fall_ball = Fall_Ball((pos[0], pos[1], 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.fall_ball_group.add(fall_ball, layer=2)


          for pos in magic_man_positions:
            magic_man = Magic_man((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
            globals.magic_man_group.add(magic_man, layer=2)

          pygame.display.flip()
          continue

        if night.status == Status.ROED:
          globals.deaded = False
          globals.boss_start = False
          group, night, map, hud, camp = init()
          clear_enemy_groups()
          globals.player_coin = 0
          globals.boss_nom_dead = False
          globals.boss_nom2_dead = False
          globals.score_dis = False
          globals.treasure_get_now1 = False
          globals.treasure_get_now2 = False
          if globals.treasure_get1 == True:
            globals.treasure_up = 10

          if globals.stage_num == 0:
            bad_positions = [
    (1400, 330),(1460, 330),(2010,400),(2270,350),(2250,380),(2290,320),(4260,180),(4300,140),(4340,220),
    (6200,140),(6250,180),(8650,320),(8700,450),(12180,350),(12280, 380),(12320,450)
    ]
  
            zombie_positions = [
    (1050, 480), (1100, 480),(2150,480),(2200,480),(2250,480),(6250,280),(6300,280),(9700,480),(9800,480),
    (12800,200),(12880,200)
    ]

            ball_positions = [
      (1300, 440),(7200,440),(7300,440),(7780,350),(7880,300),(7980,210)
    ]

            fall_ball_positions = []
  
            magic_man_positions = [
    (4960,200),(5160, 160),(8400, 480),(9800,480),(10320,480),(10480,320),(10649,200)
    ]

            boss = Boss((14280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss_group.add(boss)

          elif globals.stage_num == 1:
            bad_positions = [
    (1660, 280),(1700, 350),(2400,350),(4000,280),(5800,280),(5900,300)
    ]
  
            zombie_positions = [
    (6200, 280), (6270, 280)
    ]


            fall_ball_positions = [
      (2880, 0),(3640,0),(4300,0),(4780,0),(5625,0),(6280,0),(6680,0),(7710,0),
      (7780,0),(8180,0),(9080,0),(10050,0),(10220,0),(11000,0),(11400,0),(11800,0),
      (6480,0),(7880,0),(8080,0),(11200,0),(11600,0),(7980,0)
    ]

            ball_positions = []

  
            magic_man_positions = [
    (5180,400),
    ]

            boss = Boss2((14280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss_group.add(boss)
          elif globals.stage_num == 2:
            clear_enemy_groups()
            bad_positions = []
            zombie_positions = []
            ball_positions = []
            fall_ball_positions = []
            magic_man_positions = []
            boss_nom = Boss_nom((3240, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss_nom_group.add(boss_nom)
            boss2_nom = Boss2_nom((6600, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss2_nom_group.add(boss2_nom)
            boss = Boss3((14280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.boss_group.add(boss)


          for pos in bad_positions:
            bad = Bad((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
            globals.bad_group.add(bad, layer=2)


          for pos in zombie_positions:
            zombie = Zombie((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
            globals.zombie_group.add(zombie, layer=2)

          for pos in ball_positions:
            ball = Ball((pos[0], pos[1], 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.ball_group.add(ball, layer=2)

          for pos in fall_ball_positions:
            fall_ball = Fall_Ball((pos[0], pos[1], 80, 80), night, knife_rawrect, bomb_rawrect, map)
            globals.fall_ball_group.add(fall_ball, layer=2)


          for pos in magic_man_positions:
            magic_man = Magic_man((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
            globals.magic_man_group.add(magic_man, layer=2)


          pygame.display.flip()
          continue

        map.update(night.rawrect.center,boss.dead,night.status)

        if weapon_cooltime:
            attck_cooltime = (weapon_now_time - attck_cooltime_start) / 1000
            if attck_cooltime >= 0.15:
                weapon_cooltime = False

        if not weapon_cooltime:
            if action[pygame.K_j]:
              if globals.score_dis == False:
                if len(globals.knife_group) < 3:
                    knife = Knife(night.rect.center, night.isleft, map,night.rawrect.center)
                    globals.knife_group.add(knife)
                    weapon_cooltime = True
                    attck_cooltime_start = weapon_now_time

            if action[pygame.K_k]:
              if globals.score_dis == False:
                if map.bomb_get == True:
                  if globals.bomb_counter > 0:
                    bomb = Bomb(night.rect.center, night.isleft, map, night.rect, night.rawrect.center)
                    globals.bomb_group.add(bomb)
                    weapon_cooltime = True
                    attck_cooltime_start = weapon_now_time
                    globals.bomb_counter -= 1
        
        
        knife_rawrect = globals.knife_group.sprites()[0].rawrect if globals.knife_group else pygame.Rect(0, 0, 0, 0)
        # スクロール量を更新
        map.update_scroll(night.rawrect)


        group.update(globals.player_score,hud.deadflug)
        globals.knife_group.update()
        globals.bomb_group.update()
        globals.explosion_group.update()
        hud.update(map.clock_counter, map.bomb_get, night.damage,boss.dead,night.status)
        globals.bad_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.zombie_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.ball_group.update(globals.knife_group,night.status)
        globals.fall_ball_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.magic_man_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.magic_ball_group.update(night.status)
        globals.boss_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.boss_lazer_group.update(night.status,boss.live)
        globals.boss_ball_night_group.update(globals.knife_group,night.status,boss.live)
        globals.boss_ball_ran_group.update(globals.knife_group,night.status,boss.live)
        globals.boss_nom_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.boss2_nom_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.boss_lazer_nom_group.update(night.status,boss.live)
        globals.boss_ball_night_nom_group.update(globals.knife_group,night.status)
        globals.boss_ball_ran_nom_group.update(globals.knife_group,night.status)


        globals.knife_group.draw(globals.window)
        globals.bomb_group.draw(globals.window)
        globals.explosion_group.draw(globals.window)
        map.draw(globals.window, night.rawrect)
        hud.draw(globals.window)
        group.draw(globals.window)

        camp.update(night.rawrect,night.weapon_idx,night.stage_idx,night.end_idx,night.status)

        for bad in globals.bad_group:
          if bad.visible:
            globals.window.blit(bad.image, bad.rect)
            

        for zombie in globals.zombie_group:
          if zombie.visible:
            globals.window.blit(zombie.image, zombie.rect)

        for ball in globals.ball_group:
          if ball.visible:
            globals.window.blit(ball.image, ball.rect)

        for fall_ball in globals.fall_ball_group:
          if fall_ball.visible:
            globals.window.blit(fall_ball.image, fall_ball.rect)
            

        for magic_man in globals.magic_man_group:
          if magic_man.visible:
            globals.window.blit(magic_man.image, magic_man.rect)

        for magic_ball in globals.magic_ball_group:
          globals.window.blit(magic_ball.image, magic_ball.rect)
        
        for boss in globals.boss_group:
          globals.window.blit(boss.image, boss.rect)

        for boss_lazer in globals.boss_lazer_group:
          globals.window.blit(boss_lazer.image, boss_lazer.rect)

        for boss_ball_night in globals.boss_ball_night_group:
          globals.window.blit(boss_ball_night.image, boss_ball_night.rect)

        for boss_ball_ran in globals.boss_ball_ran_group:
          globals.window.blit(boss_ball_ran.image, boss_ball_ran.rect)

        for boss_nom in globals.boss_nom_group:
          globals.window.blit(boss_nom.image, boss_nom.rect)

        for boss2_nom in globals.boss2_nom_group:
          globals.window.blit(boss2_nom.image, boss2_nom.rect)

        for boss_lazer_nom in globals.boss_lazer_nom_group:
          globals.window.blit(boss_lazer_nom.image, boss_lazer_nom.rect)

        for boss_ball_nom_night in globals.boss_ball_night_nom_group:
          globals.window.blit(boss_ball_nom_night.image, boss_ball_nom_night.rect)

        for boss_ball_ran_nom in globals.boss_ball_ran_nom_group:
          globals.window.blit(boss_ball_ran_nom.image, boss_ball_ran_nom.rect)

        pygame.display.flip()
        clock.tick(60)

  pygame.quit()

opening()

main()