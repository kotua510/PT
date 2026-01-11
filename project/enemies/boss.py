import pygame
from enum import Enum, auto
import time
import math
import random 
from status import Status
import globals

pygame.init()


class Boss(pygame.sprite.Sprite):
  def  __init__(self, boss_rawrect,night,knife_rawrect,exc_rawrect,map):
    super().__init__()
    pygame.sprite.Sprite.__init__(self)

    self.imgs = [
      pygame.image.load("image/stage/enemy/boss1_1.png"),
      pygame.image.load("image/stage/enemy/boss1_2.png"),
    ]

    self.sous = [
      pygame.mixer.Sound("sound/enemy/enemy_hit.mp3"),
      pygame.mixer.Sound("sound/enemy/boss_attck.mp3")
    ]

    self.image = self.imgs[0]
    self.sound = self.sous[0]
    self.sound = pygame.mixer.Sound("sound/enemy/enemy_hit.mp3")
    self.move_index = [0,0,0,0,0,1,1,1,1,1]
    self.move_num = 0
    self.rawrect = pygame.Rect(boss_rawrect)
    self.rect = self.rawrect.copy()
    self.night_rawrect = night.rawrect
    self.knife_rawrect = knife_rawrect
    self.exc_rawrect = exc_rawrect
    self.map = map
    self.status = Status.NOMAL
    self.vx = -4
    self.life = 70
    self.born = True
    self.Width = 900
    self.margin = 100
    self.vy = 0
    self.on_ground = False
    self.visible = False
    self.isleft = False
    self.first = True
    self.select_move = True
    self.move_time = 1
    self.trun = True
    self.trun_limit_time = 0
    self.trun_limit_time_dec = 0
    self.trun_on = 0
    self.attck = True
    self.attck_limi = [0.5,1]
    self.dead = False
    self.win_se = pygame.mixer.Sound("sound/stage/win_BGM.mp3")
    self.boss_dead_se = pygame.mixer.Sound("sound/enemy/boss_dead.mp3")
    self.score_up = 200
    self.live = True




  def update(self, knife_group, bomb_group,night_status):
    if night_status == Status.DEADING or night_status == Status.DEAD or night_status == Status.ROED  :
      self.kill()

    if self.status == Status.NOMAL:


        self.scroll_x = self.map.scroll_x

        self.sound.set_volume(1.0)

        global enemy_kill

        self.nowtime = pygame.time.get_ticks()

        self.trun_box = self.rawrect.inflate(240,0)


        self.foot_rawrect = pygame.Rect(self.rawrect.x, self.rawrect.bottom, self.rawrect.width, 1)
        self.right_rawrect = pygame.Rect(self.rawrect.right, self.rawrect.top, 1, self.rawrect.height)
        self.left_rawrect = pygame.Rect(self.rawrect.left - 1, self.rawrect.top, 1, self.rawrect.height)


        if self.first:
          if self.rawrect.right > self.scroll_x - self.margin and self.rawrect.left < self.scroll_x + self.Width + self.margin:
            self.visible = True
            self.first = False
          else:
            self.visible = False

        if not self.visible:
            return  # 表示範囲外なら停止

        self.vy += 1 

        
        self.rect.x = self.rawrect.x - self.scroll_x
        self.rect.y = self.rawrect.y
        self.image = pygame.transform.flip(self.imgs[self.move_index[self.move_num % 10]], self.isleft, False)
        self.move_num += 1
        self.hitbox = self.rawrect.inflate(0, 0)

        old_bottom = self.rawrect.bottom

        self.rawrect.y += self.vy

        self.foot_collision, self.foot_line, self.foot_sideline, self.foot_now_tile = self.map.check_collision(self.foot_rawrect)
        if self.foot_collision or self.foot_line or self.foot_sideline:
          if self.vy > 0:
            self.rawrect.bottom = (old_bottom // 40) * 40
            self.on_ground = True
            self.vy = 0
          else:
            self.rawrect.top = (self.rawrect.top // 40 + 1) * 40
            self.vy = 1
        else:
          self.on_ground = False




        self.rawrect.x += self.vx

        self.right_rawrect = pygame.Rect(self.rawrect.right, self.rawrect.top, 1, self.rawrect.height)
        self.left_rawrect = pygame.Rect(self.rawrect.left - 1, self.rawrect.top, 1, self.rawrect.height)



        self.right_collision, self.right_line, self.right_sideline, self.right_now_tile = self.map.check_collision(self.left_rawrect)

        if self.right_collision:
            if self.isleft == False:
                self.rawrect.x = (self.rawrect.x // 40 + 1) * 40
                self.vx = -self.vx  
                self.isleft = True
                self.trun_limit_time = self.nowtime

        self.left_collision, self.left_line, self.left_sideline, self.left_now_tile = self.map.check_collision(self.right_rawrect)
        if self.left_collision:
            if self.isleft == True:
                self.rawrect.x = (self.rawrect.x // 40) * 40
                self.vx = -self.vx
                self.isleft = False
                self.trun_limit_time = self.nowtime


        if 13750 < self.rawrect.x < 14000:
          self.trun_right = True
        else:
          self.trun_right = False


        for knife in knife_group:
            if self.rawrect.colliderect(knife.rawrect):
                knife.kill()
                self.life -= 1 + globals.knife_plus
                self.sound = self.sous[0]
                self.sound.play()

        for bomb in bomb_group:
            if self.rawrect.colliderect(bomb.rawrect):
                self.life -= 3

        if  self.trun:
          self.start_trun_time = pygame.time.get_ticks()
          self.trun = False
        
        elif not self.trun:
          self.now_trun_time = pygame.time.get_ticks()
          self.trun_time = (self.now_trun_time - self.start_trun_time) / 1000
          if self.trun_time >= 1:
              self.trun_on = random.randint(0, 1)
              self.trun = True


        if self.select_move:
          self.start_select_time = pygame.time.get_ticks()
          self.select_move = False
          self.move_time = random.randint(1,2)
        
        elif not self.select_move:
          self.now_select_time = pygame.time.get_ticks()
          self.select_time = (self.now_select_time - self.start_select_time) / 1000
          if self.select_time >= self.move_time:
            if  self.trun_right:
              if self.trun_on == 0:
                self.vx = -self.vx
                self.isleft = not self.isleft
              if self.vx > 0:
                self.vx = random.randint(4, 10)
                self.isleft = True
              else:
                self.vx = random.randint(4, 10)
                self.vx = -self.vx
                self.isleft = False
            self.select_move = True

        if self.attck:
          self.start_attck_time = pygame.time.get_ticks()
          self.attck_limi_time = random.choice([2000,2500,3000])
          self.attck = False
        
        elif not self.attck:
          self.now_attck_time = pygame.time.get_ticks()
          self.attck_time = (self.now_attck_time - self.start_attck_time) 
          if self.attck_time >= self.attck_limi_time:
              self.attck = True
              self.sound = self.sous[1]
              self.sound.play()
              boss_lazer = Boss_lazer(self.rawrect,self.rect, self.night_rawrect, self.map)
              globals.boss_lazer_group.add(boss_lazer)


        if self.life <= 0:
          self.kill()
          self.live = False
          globals.enemy_kill += self.score_up
          self.dead = True
          pygame.mixer.music.stop()
          self.boss_dead_se.set_volume(1.0)
          self.boss_dead_se.play()
          time.sleep(2.5)
          self.win_se.play()


        if self.rect.y >= 700:
          self.kill()

class Boss_lazer(pygame.sprite.Sprite):
  def __init__(self, boss_rawrect, boss_rect, night_rawrect, map):
    super().__init__()
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load("image/stage/enemy/boss_attck.png")
    self.trans_image = self.image
    self.margin = 100
    self.boss_rect = boss_rect
    self.boss_rawrect = boss_rawrect
    self.rect = self.boss_rect.copy()
    self.rawrect = self.boss_rawrect.copy()
    self.night_rawrect = night_rawrect
    self.width = 900
    self.map = map
    



    target_x = self.night_rawrect.centerx
    target_y = self.night_rawrect.centery

    self.dx = target_x - self.rawrect.centerx
    self.dy = target_y - self.rawrect.centery

    distance = math.hypot(self.dx, self.dy)

    if distance == 0:
      distance = 1
    
    self.vx = (self.dx / distance) * 7
    self.vy = (self.dy / distance) * 7

  def update(self,night_status,boss_live):

    if night_status == Status.DEADING or night_status == Status.DEAD or night_status == Status.ROED or boss_live == False:
      self.kill()

    if self.vx >= 0:
      self.isleft = True
    else:
      self.isleft = False

    self.image = pygame.transform.flip(self.trans_image, self.isleft, False)

    self.rawrect.x += self.vx
    self.rawrect.y += self.vy

    self.rect.x = self.rawrect.x - self.map.scroll_x
    self.rect.y = self.rawrect.y
