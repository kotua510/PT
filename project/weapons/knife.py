import pygame
from enum import Enum, auto
import time
import math
import random 
from globals import Width

class Knife(pygame.sprite.Sprite):#後でknifeにする
  def __init__(self,night_rect,night_isleft,map, night_rawrect_center):
    super().__init__()
    
    pygame.sprite.Sprite.__init__(self)
    
    self.weapon_imgs = [
      pygame.image.load("image/my/wepon/bomb.png"),
      pygame.image.load("image/my/wepon/explosion.png"),
      pygame.image.load("image/my/wepon/knife.png")
    ]

    self.image = self.weapon_imgs[2] 
    self.rect = self.image.get_rect()  # ← まずは自分の rect を作る
    self.rect.center = night_rect
    self.rawrect = self.image.get_rect()
    self.rawrect.center = night_rawrect_center
    self.isleft = night_isleft
    self.image = pygame.transform.flip(self.image, self.isleft, False)
    self.map = map
    self.scroll_x = self.map.scroll_x



  def update(self):
    


    self.knife_vx = -8 if self.isleft else 8
    action = pygame.key.get_pressed()
    if action[pygame.K_d]:
      self.knife_vx = -6 if self.isleft else 10
    if action[pygame.K_a]:
      self.knife_vx = -10 if self.isleft else 6

    self.rawrect.x += self.knife_vx

    # スクロール量取得
    scroll_x = self.map.scroll_x

    # 描画用の座標に変換
    self.rect.x = self.rawrect.x - scroll_x

    # 当たり判定はワールド座標の rawrect を使う！
    self.collision = self.map.check_collision_knife(self.rawrect)

    if self.rect.left > Width or self.rect.left < 0:  # 画面の右端（例: 横幅800）
            self.kill()
    
    if self.collision == True:
      self.kill()