import pygame
from enum import Enum, auto
import time
import math
import random 
from status import Status
import globals

pygame.init()

class Magic_man(pygame.sprite.Sprite):
  def  __init__(self, magic_man_rawrect,night,knife_rawrect,exc_rawrect,map):
    super().__init__()
    pygame.sprite.Sprite.__init__(self)


    self.image = pygame.image.load("image/stage/enemy/magic_man.png")
    self.sons = [
      pygame.mixer.Sound("sound/enemy/enemy_hit.mp3"),
      pygame.mixer.Sound("sound/enemy/ballman_attck.mp3")
    ]
    self.sound = self.sons[0]
    self.rawrect = pygame.Rect(magic_man_rawrect)
    self.rect = self.rawrect.copy()
    self.night_rawrect = night.rawrect
    self.knife_rawrect = knife_rawrect
    self.exc_rawrect = exc_rawrect
    self.map = map
    self.status = Status.NOMAL
    self.life = 3
    self.born = True
    self.Width = 900
    self.margin = 100
    self.vy = 0
    self.on_ground = False
    self.visible = False
    self.isleft = False
    self.attck_cool_time = 2500
    self.attck = True
    self.score_up = 50

  def update(self, knife_group, bomb_group,night_status):

    if night_status == Status.DEADING or night_status == Status.DEAD:
      self.kill()

    if self.status == Status.NOMAL:


        self.scroll_x = self.map.scroll_x

        global enemy_kill

        self.sound = self.sons[0]

        self.sound.set_volume(1.0)

        if self.rawrect.right > self.scroll_x - self.margin and self.rawrect.left < self.scroll_x + self.Width + self.margin:
            self.visible = True
        else:
            self.visible = False

        if not self.visible:
            return  # 表示範囲外なら停止

        self.vy += 1  
        
        self.rect.x = self.rawrect.x - self.scroll_x
        self.rect.y = self.rawrect.y
        self.hitbox = self.rawrect
        self.nowtime = pygame.time.get_ticks()

        self.rawrect.y += self.vy
        self.collision, self.line, self.sideline, self.now_tile = self.map.check_collision(self.rawrect)
        if self.collision or self.line or self.sideline:
            self.rawrect.y = (self.rawrect.y // 40 ) * 40
            if self.vy > 0:
                self.on_ground = True
                self.vy = 0
            else:
                self.vy = 1
        else:
            self.on_ground = False

        for knife in knife_group:
            if self.rawrect.colliderect(knife.rawrect):
                knife.kill()
                self.sound.play()
                if self.life > 0:
                    self.life -= (1 + globals.knife_plus)

                if self.life <= 0:
                    globals.enemy_kill += self.score_up
                    self.kill()


        for bomb in bomb_group:
            if self.hitbox.colliderect(bomb.rawrect):
              globals.enemy_kill += self.score_up
              self.kill()

        if self.attck:
          self.start_attck_time = pygame.time.get_ticks()
          self.attck = False
        
        elif not self.attck:
          self.now_attck_time = pygame.time.get_ticks()
          self.attck_time = (self.now_attck_time - self.start_attck_time) / 1000
          if self.attck_time >= 3:
              self.attck = True
              self.sound = self.sons[1]
              self.sound.play()
              magic_ball = Magic_ball(self.rawrect,self.rect, self.night_rawrect, self.map)
              globals.magic_ball_group.add(magic_ball)

        if self.rect.x + self.margin <= 0:
            self.kill()

        if self.rect.y >= 700:
          self.kill()


class Magic_ball(pygame.sprite.Sprite):
  def __init__(self, magic_man_rawrect, magic_man_rect, night_rawrect, map):
    super().__init__()
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load("image/stage/enemy/magic_ball.png")
    self.margin = 100
    self.magic_man_rect = magic_man_rect
    self.magic_man_rawrect = magic_man_rawrect
    self.rect = self.magic_man_rect.copy()
    self.rawrect = self.magic_man_rawrect.copy()
    self.night_rawrect = night_rawrect
    self.width = 900
    self.map = map
    self.rawrect = self.rawrect.inflate(-20, -20)
    self.life = pygame.time.get_ticks()

  def update(self,night_status):
    if night_status == Status.DEADING or night_status == Status.DEAD or night_status == Status.ROED  :
      self.kill()
    self.time = pygame.time.get_ticks()
    self.limit_time = (self.time - self.life) / 1000
    if self.limit_time >= 3:
      self.kill()

    self.rect.x = self.rawrect.x - self.map.scroll_x
    self.rect.y = self.rawrect.y

    target_x = self.night_rawrect.centerx
    target_y = self.night_rawrect.centery

    self.dx = target_x - self.rawrect.centerx
    self.dy = target_y - self.rawrect.centery

    distance = math.hypot(self.dx, self.dy)

    if distance == 0:
      distance = 1
    
    self.vx = (self.dx / distance) * 4
    self.vy = (self.dy / distance) * 4

    self.rawrect.x += self.vx
    self.rawrect.y += self.vy