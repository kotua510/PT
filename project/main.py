import pygame
from enum import Enum, auto
import time
import math
import random 
from hud import Hud
from map import Map
from camp import Camp
from my_night import My_night
from weapons.bomb import Bomb
from weapons.knife import Knife
from enemies.bad import Bad
from enemies.ball import Ball
from enemies.boss import Boss
from enemies.magic_man import Magic_man
from enemies.zombie import Zombie
import globals
from status import Status
from opening import Opening
#todo ,一回につき300+時計追加、150以下は禁止, 死んだときに敵をinit(), 自分を殺す,ボスへの爆弾のダメージを低下、bomb_counetを下げる
#爆弾の問題は現状解決不可、いったんとったら爆弾を打てるitemを設置、スタートから飛び降りる形式にすることによって隠すことにする


globals.bomb_counter = 150     

pygame.init()

def init():

  group = pygame.sprite.RenderUpdates()

  map =Map()

  camp = Camp()

  hud = Hud(map.clock_counter, map.treasure_get, map.bomb_get)

  night = My_night(map, globals.window,globals.player_score, globals.bad_group, globals.zombie_group, globals.ball_group, globals.magic_man_group, globals.magic_ball_group,globals.boss_group,globals.boss_lazer_group)
  


  group.add(night)

  return group, night, map, hud, camp


def opening():
  pygame.init()

  #pygame.mixer.init()
  pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

  pygame.mixer.set_num_channels(64)

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





def main():
  pygame.init()
  #画面を作成する

  pygame.mixer.init()

  pygame.mixer.set_num_channels(128)

  clock = pygame.time.Clock()


  group, night, map, hud, camp = init()
  running = True
  weapon_cooltime = False
  attck_cooltime_start = 0
  global knife
  keep_bomb = globals.bomb_counter
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
        # DEADING中は描画処理をスキップ
          pygame.display.flip()
          continue

        if night.status == Status.DEAD:
          globals.player_score = hud.keep_time
          globals.player_coin = map.keep_coin
          globals.bomb_counter = keep_bomb
          group, night, map, hud, camp = init()
          keep_bomb = globals.bomb_counter

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

          boss = Boss((14280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
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


          for pos in magic_man_positions:
            magic_man = Magic_man((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
            globals.magic_man_group.add(magic_man, layer=2)

          boss = Boss((14280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
          globals.boss_group.add(boss)

          pygame.display.flip()
          continue
##############################################

        if night.status == Status.ROED:
          group, night, map, hud, camp = init()
          globals.player_coin = 0
          

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

          boss = Boss((14280, 440, 80, 80), night, knife_rawrect, bomb_rawrect, map)
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


          for pos in magic_man_positions:
            magic_man = Magic_man((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
            globals.magic_man_group.add(magic_man, layer=2)



          pygame.display.flip()
          continue

        map.update(night.rawrect.center,boss.dead,hud.score_dis)
        score_dis = hud.score_dis




        if weapon_cooltime:
            attck_cooltime = (weapon_now_time - attck_cooltime_start) / 1000
            if attck_cooltime >= 0.15:
                weapon_cooltime = False

        if not weapon_cooltime:  # クールタイムが終わってたら攻撃できる
            if action[pygame.K_j]:
              if score_dis == False:
                if len(globals.knife_group) < 3:
                    knife = Knife(night.rect.center, night.isleft, map,night.rawrect.center)
                    globals.knife_group.add(knife)
                    weapon_cooltime = True
                    attck_cooltime_start = weapon_now_time

            if action[pygame.K_k]:
              if score_dis == False:
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


        group.update(globals.player_score,hud.score_dis,hud.deadflug)
        globals.knife_group.update()
        globals.bomb_group.update()
        globals.explosion_group.update()
        hud.update(map.clock_counter, map.treasure_get, map.bomb_get, night.damage,boss.dead,map.treasure_up,night.status)
        globals.bad_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.zombie_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.ball_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.magic_man_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.magic_ball_group.update(night.status)
        globals.boss_group.update(globals.knife_group, globals.bomb_group,night.status)
        globals.boss_lazer_group.update(night.status,boss.live)


        globals.knife_group.draw(globals.window)
        globals.bomb_group.draw(globals.window)
        globals.explosion_group.draw(globals.window)
        map.draw(globals.window, night.rawrect)
        hud.draw(globals.window)
        group.draw(globals.window)

        camp.update(night.rawrect,night.weapon_idx,night.status)

        for bad in globals.bad_group:
          if bad.visible:
            globals.window.blit(bad.image, bad.rect)
            

        for zombie in globals.zombie_group:
          if zombie.visible:
            globals.window.blit(zombie.image, zombie.rect)

        for ball in globals.ball_group:
          if ball.visible:
            globals.window.blit(ball.image, ball.rect)
            

        for magic_man in globals.magic_man_group:
          if magic_man.visible:
            globals.window.blit(magic_man.image, magic_man.rect)

        for magic_ball in globals.magic_ball_group:
          globals.window.blit(magic_ball.image, magic_ball.rect)
        
        for boss in globals.boss_group:
          globals.window.blit(boss.image, boss.rect)

        for boss_lazer in globals.boss_lazer_group:
          globals.window.blit(boss_lazer.image, boss_lazer.rect)

        pygame.display.flip()
        clock.tick(60)

  pygame.quit()

opening()

main()