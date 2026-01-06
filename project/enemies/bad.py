import pygame
from enum import Enum, auto
import time
import math
import random 
from status import Status
import  globals

pygame.init()

class Bad(pygame.sprite.Sprite):
  def  __init__(self, bad_rawrect,night,knife_rawrect,exc_rawrect,map):
    super().__init__()
    pygame.sprite.Sprite.__init__(self)

    self.imgs = [
      pygame.image.load("image/stage/enemy/bad1.png"),
      pygame.image.load("image/stage/enemy/bad2.png"),
    ]

    self.image = self.imgs[0]
    self.sound = pygame.mixer.Sound("sound/enemy/enemy_hit.mp3")
    self.move_index = [0,0,0,0,1,1,1,1]
    self.move_num = 0
    self.rawrect = pygame.Rect(bad_rawrect)
    self.rect = self.rawrect.copy()
    self.night_rawrect = night.rawrect
    self.knife_rawrect = knife_rawrect
    self.exc_rawrect = exc_rawrect
    self.map = map
    self.status = Status.NOMAL
    self.vx = -3
    self.life = 1
    self.born = True
    self.Width = 900
    self.margin = 100
    self.score_up = 5

  def update(self, knife_group, bomb_group,night_status):

    if night_status == Status.DEADING or night_status == Status.DEAD or night_status == Status.ROED  :
      self.kill()

    if self.status == Status.NOMAL:

      self.scroll_x = self.map.scroll_x

      global enemy_kill

      self.sound.set_volume(1.0)

      if self.rawrect.right > self.scroll_x - self.margin and self.rawrect.left < self.scroll_x + self.Width + self.margin:
        self.visible = True
      else:
        self.visible = False

      if not self.visible:
        return  # 表示範囲外なら動かさない




      self.rawrect.x += self.vx
      self.rect.x = self.rawrect.x - self.scroll_x 
      self.image = self.imgs[self.move_index[self.move_num % 8]]
      self.move_num += 1
      self.hitbox = self.rawrect.inflate(20, 0)

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
          bomb.kill()

      if self.rect.x <= 0:
        self.kill()

      if self.rect.y >= 700:
          self.kill()
          print("killed")