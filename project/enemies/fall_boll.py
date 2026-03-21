import pygame
from enum import Enum, auto
import time
import math
import random
from status import Status
import globals

pygame.init()

class Fall_Ball(pygame.sprite.Sprite):
  def  __init__(self, fall_ball_rawrect,night,knife_rawrect,exc_rawrect,map):
    super().__init__()
    pygame.sprite.Sprite.__init__(self)

    self.imgs = [
      pygame.image.load("image/stage/enemy/ball1.png"),
      pygame.image.load("image/stage/enemy/ball2.png"),
      pygame.image.load("image/stage/enemy/ball3.png"),
      pygame.image.load("image/stage/enemy/ball4.png"),
    ]

    self.image = self.imgs[0]
    self.sound = pygame.mixer.Sound("sound/enemy/enemy_hit.mp3")
    self.move_index = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3]
    self.move_num = 0
    self.rawrect = pygame.Rect(fall_ball_rawrect)
    self.rawrect_origin = self.rawrect.copy()
    self.rect = self.rawrect.copy()
    self.night_rawrect = night.rawrect
    self.knife_rawrect = knife_rawrect
    self.exc_rawrect = exc_rawrect
    self.map = map
    self.status = Status.NOMAL
    self.vx = -4
    self.life = 100
    self.born = True
    self.Width = 900
    self.margin = 100
    self.vy = 0
    self.on_ground = False
    self.visible = False
    self.isleft = False
    self.score_up = 100
    self.vyadd = 0


  def update(self, knife_group,bomb_group,night_status):

    if night_status == Status.DEADING or night_status == Status.DEAD or night_status == Status.ROED or night_status == Status.END or night_status == Status.RESET  :
      self.kill()

    if self.status == Status.NOMAL:


        self.scroll_x = self.map.scroll_x

        global enemy_kill


        self.foot_rawrect = pygame.Rect(self.rawrect.x, self.rawrect.bottom, self.rawrect.width, 1)
        self.right_rawrect = pygame.Rect(self.rawrect.right, self.rawrect.top, 1, self.rawrect.height)
        self.left_rawrect = pygame.Rect(self.rawrect.left - 1, self.rawrect.top, 1, self.rawrect.height)


        if self.rawrect.right > self.scroll_x - self.margin and self.rawrect.left < self.scroll_x + self.Width + self.margin:
            self.visible = True
        else:
            self.visible = False

        if not self.visible:
            return  # 表示範囲外なら停止


        self.vyadd += 1
        if self.vyadd >= 3:
          self.vy += 1
          self.vyadd = 0
        
        self.rect.x = self.rawrect.x - self.scroll_x
        self.rect.y = self.rawrect.y
        self.image = pygame.transform.flip(self.imgs[self.move_index[self.move_num % 40]], self.isleft, False)
        self.move_num += 1
        self.hitbox = self.rawrect.inflate(0, 0)

        old_bottom = self.rawrect.bottom

        self.rawrect.y += self.vy
        self.rect.y = self.rawrect.y


        # 武器との衝突判定
        for knife in knife_group:
            if self.rawrect.colliderect(knife.rawrect):
                knife.kill()
                if self.life > 0:
                    self.life -= (1 + globals.knife_plus + globals.treasure_knife)

                if self.life <= 0:
                    globals.enemy_kill += self.score_up
                    self.kill()



        if self.rect.y >= 700:
          self.rawrect = self.rawrect_origin.copy()
          self.rect = self.rawrect.copy()
          self.vy = 0