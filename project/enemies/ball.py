import pygame
from enum import Enum, auto
import time
import math
import random
from status import Status
import globals

pygame.init()

class Ball(pygame.sprite.Sprite):
  def  __init__(self, ball_rawrect,night,knife_rawrect,exc_rawrect,map):
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
    self.rawrect = pygame.Rect(ball_rawrect)
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


  def update(self, knife_group, bomb_group,night_status):

    if night_status == Status.DEADING or night_status == Status.DEAD or night_status == Status.ROED  :
      self.kill()

    if self.status == Status.NOMAL:


        self.scroll_x = self.map.scroll_x

        global enemy_kill


        self.foot_rawrect = pygame.Rect(self.rawrect.x, self.rawrect.bottom, self.rawrect.width, 1)
        self.right_rawrect = pygame.Rect(self.rawrect.right, self.rawrect.top, 1, self.rawrect.height)
        self.left_rawrect = pygame.Rect(self.rawrect.left - 1, self.rawrect.top, 1, self.rawrect.height)


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
        self.image = pygame.transform.flip(self.imgs[self.move_index[self.move_num % 40]], self.isleft, False)
        self.move_num += 1
        self.hitbox = self.rawrect.inflate(0, 0)

        # 縦方向の当たり判定（地面に埋まらない版）
        # 縦方向の当たり判定
        # 移動前の位置を保存
        old_bottom = self.rawrect.bottom

# 移動
        self.rawrect.y += self.vy

# 当たり判定
        self.foot_collision, self.foot_line, self.foot_sideline, self.foot_now_tile = self.map.check_collision(self.foot_rawrect)

        if self.foot_collision or self.foot_line or self.foot_sideline:
          if self.vy > 0:
        # 落下なら、移動前の bottom に戻して、ぴったり床に乗る
            self.rawrect.bottom = (old_bottom // 40) * 40
            self.on_ground = True
            self.vy = 0
          else:
            self.rawrect.top = (self.rawrect.top // 40 + 1) * 40
            self.vy = 1
        else:
          self.on_ground = False




        # 横の衝突判定
        self.rawrect.x += self.vx
        self.right_collision, self.right_line, self.right_sideline, self.right_now_tile = self.map.check_collision(self.left_rawrect)
        if self.right_collision:
            if self.isleft == False:
                self.rawrect.x = (self.rawrect.x // 40 + 1) * 40
                self.vx = -self.vx  # 壁で方向転換！
                self.isleft = True
        

        self.left_collision, self.left_line, self.left_sideline, self.left_now_tile = self.map.check_collision(self.right_rawrect)
        if self.left_collision:
            if self.isleft == True:
                self.rawrect.x = (self.rawrect.x // 40) * 40
                self.vx = -self.vx
                self.isleft = False

        # 刃物や爆弾との衝突判定
        for knife in knife_group:
            if self.rawrect.colliderect(knife.rawrect):
                knife.kill()
                if self.life > 0:
                    self.life -= (1 + globals.knife_plus)

                if self.life <= 0:
                    globals.enemy_kill += self.score_up
                    self.kill()


        # 画面外に出たら削除
        if self.rect.x + self.margin <= 0:
            self.kill()

        if self.rect.y >= 700:
          self.kill()
          print("killed")