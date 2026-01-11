import pygame
from enum import Enum, auto
import time
import math
import random 
import globals
from status import Status

pygame.init()

class Hud(pygame.sprite.Sprite, ):
  def __init__(self, map_clock_counter, map_treasure_get, map_bomb_get):
    super().__init__()
    pygame.sprite.Sprite.__init__(self)

    self.imgs = [
      pygame.image.load("image/HUD/hp_bar.png"),
      pygame.image.load("image/HUD/hp_memory.png"),
      pygame.image.load("image/HUD/time_frame.png"),
      pygame.image.load("image/my/wepon/bomb.png"),
      pygame.image.load("image/stage/gimmick/clock.png"),
      pygame.image.load("image/stage/gimmick/treasure.png"),
      pygame.image.load("image/my/wepon/bomb_no.png"),
    ]
    globals.bomb_counter

    self.hp_bar_image = self.imgs[0]
    self.hp_memory_image = self.imgs[1]
    self.time_frame_image = self.imgs[2]
    self.weapon_image = self.imgs[6]
    self.clock_image = self.imgs[4]
    self.treasure_image = self.imgs[5]
    self.treasure_get = map_treasure_get
    self.bomb_get = map_bomb_get
    self.life = 38  

    self.hp_bar_rect = pygame.Rect(-30, 20, 150, 150)
    self.hp_memory_rect = pygame.Rect(-30, 20, 150, 150)
    self.weapon_rect = pygame.Rect(65, 30, 150, 150)
    self.weapon_text_rect = pygame.Rect(98, 35, 150, 150)
    self.clock_rect = pygame.Rect(60, 65, 150, 150)
    self.clock_text_rect = pygame.Rect(98, 78, 150, 150)
    self.treasure_rect = pygame.Rect(63, 110, 150, 150)
    self.time_rect = pygame.Rect(780, 0, 150, 150)
    self.time_text_rect = pygame.Rect(807, 42, 150, 150)

    self.enemy_text_rect = pygame.Rect(330, 100, 150,150)
    self.enemy_score_text_rect = pygame.Rect(510, 100, 150,150)
    self.coin_score_rect = pygame.Rect(330, 170, 150,150)
    self.coin_score_text_rect = pygame.Rect(510, 170, 150,150)
    self.time_score_text_rect = pygame.Rect(330, 240, 150,150)
    self.time_score_num_rect = pygame.Rect(510, 240, 150,150)
    self.time_score_high_rect = pygame.Rect(620,310, 150, 150)
    self.total_text_rect = pygame.Rect(330, 310, 150,150)
    self.total_score_text_rect = pygame.Rect(510, 310, 150,150)

    self.font = pygame.font.SysFont("叛逆明朝",30)
    self.score_font = pygame.font.SysFont("叛逆明朝",50)
    self.bomb_num = f"×{globals.bomb_counter}"
    self.bomb_text = self.font.render( self.bomb_num , False, (255, 255, 255))  # 白色の文字
    self.clock_counter = map_clock_counter
    self.clock_num = f"×{self.clock_counter}"
    self.clock_text = self.font.render(self.clock_num, False, (255, 255, 255) )

    self.enemy_str = "ENEMY"
    self.enemy_int = "100"
    self.coin_str = "CLOCKS"
    self.coin_int = "50"
    self.time_str = "TIME"
    self.time_int = "259"
    self.score_high_str = "BEST SCORE!!!"
    self.total_str = "TOTAL"
    self.total_int = "359"

    self.score_up = True

    self.enemy_str_text = self.score_font.render(self.enemy_str, False, (255, 255, 255))
    self.coin_str_text = self.score_font.render(self.coin_str, False, (255, 255, 255))
    self.time_str_text = self.score_font.render(self.time_str, False, (255, 255, 255))
    self.score_high_text =self.score_font.render(self.score_high_str, False, (255, 255, 255))
    self.total_str_text = self.score_font.render(self.total_str, False, (255, 255, 255))


    self.current_time = pygame.time.get_ticks()
    self.base_time = self.current_time 
    self.keep_time = globals.player_score
    self.last_time = 0

    self.high_score = 600
    self.now_time = 0

    self.wallno = False
    self.score = 0

    self.score_dis = False
    self.first_score = True

    self.first_camp = True
    
    self.camp_BGM= pygame.mixer.Sound("sound/camp/camp_BGM.mp3")
    self.time_score_base = 500
    self.time_spemd = 0
    self.deadflug = False


  def update(self,map_clock_counter, map_treasure_get, map_bomb_get, night_damage,boss_dead, treasure_up,night_status):
    if night_status == Status.ROED:
      self.camp_BGM.stop()

    if night_status == Status.NOMAL:
      if (self.life <= 0):
        self.deadflug = True
      self.boss_dead = boss_dead
      self.score = globals.player_score
      self.coins = globals.player_coin
      self.life = self.life - night_damage + treasure_up
      night_damage = 0
      treasure_up = 0
      if self.bomb_get == True:
        self.weapon_image = self.imgs[3]
      self.clock_counter = map_clock_counter
      self.treasure_get = map_treasure_get
      self.bomb_get = map_bomb_get
      self.bomb_num = f"×{globals.bomb_counter}"
      self.bomb_text = self.font.render( self.bomb_num , False, (255, 255, 255))
      self.clock_num = f"×{self.clock_counter}"
      self.clock_text = self.font.render(self.clock_num, False, (255, 255, 255) )
      self.current_time = pygame.time.get_ticks()
      self.limit_time = (self.current_time - self.base_time) / 1000  # 経過時間（秒）
      self.limit_time = int(self.limit_time)
      if self.boss_dead:
        self.now_time = self.limit_time
      else:
        if self.limit_time != self.last_time:
          self.last_time = self.limit_time
          if globals.player_score > 0:
            globals.player_score -= 1
            self.time_spemd += 1
          else:
            globals.player_score = 0


      globals.window.fill((144, 215, 236))

      self.time_text = self.font.render( str(globals.player_score), False, (255, 255, 255))



  def draw(self, win):

    

    self.coin_text = self.score_font.render(str(self.coins), False, (255, 255, 255))
    self.enemy_int_text = self.score_font.render(str(globals.enemy_kill), False, (255, 255, 255))
    self.total_int = int(globals.enemy_kill) + int(self.coins) + int(self.time_score_base - self.time_spemd)
    self.total_int_text = self.score_font.render(str(self.total_int), False, (255, 255, 255))
    self.time_int_text = self.score_font.render(str(self.time_score_base - self.time_spemd), False, (255, 255, 255))
    self.time_str_text = self.score_font.render("TIME", False, (255, 255, 255))

    win.blit(self.hp_bar_image, self.hp_bar_rect)
    win.blit(self.weapon_image, self.weapon_rect)
    if self.bomb_get == True: 
      win.blit(self.bomb_text, self.weapon_text_rect)
    win.blit(self.time_frame_image, self.time_rect)
    win.blit(self.time_text, self.time_text_rect)
    win.blit(self.clock_image, self.clock_rect)
    win.blit(self.clock_text, self.clock_text_rect)
    if self.treasure_get == True:
      win.blit(self.treasure_image, self.treasure_rect)

    base_y = self.hp_memory_rect.y
    for i in range(self.life):
        temp_rect = self.hp_memory_rect.copy()
        temp_rect.y = base_y - (4 * i)
        win.blit(self.hp_memory_image, temp_rect)
    
    if self.boss_dead == True:
      if self.score_up == True:
        globals.player_score += globals.enemy_kill + globals.player_coin + (self.time_score_base - self.time_spemd)
        self.score_up = False

      
      if self.first_score == True:
        self.score_start_time = pygame.time.get_ticks()
        self.first_score = False
        self.score_dis = True
      if self.score_dis == True:
        win.blit(self.enemy_str_text, self.enemy_text_rect)
        win.blit(self.enemy_int_text, self.enemy_score_text_rect)
        win.blit(self.coin_str_text, self.coin_score_rect)
        win.blit(self.coin_text, self.coin_score_text_rect)
        win.blit(self.time_str_text, self.time_score_text_rect)
        win.blit(self.time_int_text, self.time_score_num_rect)
        win.blit(self.total_str_text, self.total_text_rect)
        win.blit(self.total_int_text, self.total_score_text_rect)
        if self.high_score <= self.total_int:
          win.blit(self.score_high_text, self.time_score_high_rect)
      
      self.score_current_time = pygame.time.get_ticks()
      self.score_spend_time = (self.score_current_time - self.score_start_time)  # 経過時間（秒）
      self.score_spend_time = int(self.score_spend_time)
      if self.score_spend_time >= 16800:
        self.score_dis = False
        if self.first_camp == True:
          self.camp_BGM.set_volume(0.2)
          self.camp_BGM.play(-1)
          self.first_camp = False
