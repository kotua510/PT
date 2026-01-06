import pygame
from enum import Enum, auto
import time
import math
import random 
from status import Status
import globals


pygame.init()

class Zombie(pygame.sprite.Sprite):
  def  __init__(self, zombie_rawrect,night,knife_rawrect,exc_rawrect,map):
    super().__init__()
    pygame.sprite.Sprite.__init__(self)

    self.imgs = [
      pygame.image.load("image/stage/enemy/zombie1.png"),
      pygame.image.load("image/stage/enemy/zombie2.png"),
    ]

    self.image = self.imgs[0]
    self.sound = pygame.mixer.Sound("sound/enemy/enemy_hit.mp3")
    self.move_index = [0,0,0,0,0,1,1,1,1,1]
    self.move_num = 0
    self.rawrect = pygame.Rect(zombie_rawrect)
    self.rect = self.rawrect.copy()
    self.night_rawrect = night.rawrect
    self.knife_rawrect = knife_rawrect
    self.exc_rawrect = exc_rawrect
    self.map = map
    self.status = Status.NOMAL
    self.vx =-4
    self.life = 2
    self.born = True
    self.Width = 900
    self.margin = 100
    self.vy = 0
    self.on_ground = False
    self.visible = False
    self.isleft = False
    self.score_up = 10

  def update(self, knife_group, bomb_group,night_status):

    if night_status == Status.DEADING or night_status == Status.DEAD or night_status == Status.ROED  :
      self.kill()

    if self.status == Status.NOMAL:


        self.scroll_x = self.map.scroll_x

        global enemy_kill

        self.sound.set_volume(1.0)
        

        # ゾンビが画面内に見えるか判定
        if self.rawrect.right > self.scroll_x - self.margin and self.rawrect.left < self.scroll_x + self.Width + self.margin:
            self.visible = True
        else:
            self.visible = False

        if not self.visible:
            return  # 表示範囲外なら動かさない

        # まずXだけ動かして、横の衝突判定
        
        #print(self.rawrect)
        #print(self.on_ground)
        self.vy += 1  # 重力加速度（下方向）
        
        self.rect.x = self.rawrect.x - self.scroll_x
        self.rect.y = self.rawrect.y
        self.image = pygame.transform.flip(self.imgs[self.move_index[self.move_num % 10]], self.isleft, False)
        self.move_num += 1
        self.hitbox = self.rawrect.inflate(20, 0)

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

        # 横の衝突判定
        self.rawrect.x += self.vx
        self.collision, self.line, self.sideline, self.now_tile = self.map.check_collision(self.rawrect)
        if self.collision:
            if self.isleft == False:
                self.rawrect.x = (self.rawrect.x // 40 + 1) * 40
                self.vx = -self.vx  # 壁で方向転換！
                self.isleft = True
            else:
                self.rawrect.x = (self.rawrect.x // 40) * 40
                self.vx = -self.vx
                self.isleft = False


        # 刃物や爆弾との衝突判定
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

        # 画面外に出たら削除
        if self.rect.x + self.margin <= 0:
            self.kill()

        if self.rect.y >= 700:
          self.kill()
          print("killed")