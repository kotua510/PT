import pygame
from globals import explosion_group

class Bomb(pygame.sprite.Sprite):
  def __init__(self,night_rect,night_isleft, map, night_map_rect, night_rawrect_center):
      super().__init__()
    
      pygame.sprite.Sprite.__init__(self)

      self.weapon_imgs = [
        pygame.image.load("image/my/wepon/bomb.png"),
        pygame.image.load("image/my/wepon/explosion.png"),
        pygame.image.load("image/my/wepon/knife.png")
      ]

      self.map = map
      self.night_map_rect = night_map_rect
      self.on_ground = False
      self.image = self.weapon_imgs[0] 
      self.rect = self.image.get_rect()  #まずは自分のrectを作成
      self.rect.center = night_rect   
      self.rawrect = self.image.get_rect()
      self.rawrect.center = night_rawrect_center  # その中心をnightから渡された座標にする
      self.isleft = night_isleft
      self.bomb_vx = -9 if self.isleft else 9
      self.bomb_vy = -13
      self.image = pygame.transform.flip(self.image, self.isleft, False)
      self.scroll_x = self.map.scroll_x
      self.wall_ec = False

  def update(self):

      self.hitbox = self.rawrect.inflate(20, 20)
      self.rawrect.x += self.bomb_vx  
      self.rawrect.y += self.bomb_vy
      self.bomb_vy += 1
      self.collision, self.wall = self.map.check_collision_bomb(self.rawrect)
      if self.collision == True and self.wall == False:
        self.on_ground = True
        self.wall_ec = False
      elif self.collision == True and self.wall == True:
        self.on_ground = True
        self.wall_ec = True

      scroll_x = self.map.scroll_x
      self.rect.x = int(self.rawrect.x - scroll_x)
      self.rect.y = int(self.rawrect.y)

      if self.on_ground == True:
        self.rect.y -= 13
        cx, cy = self.rect.center
        self.hitbox = self.rawrect
        night_rect = self.night_map_rect
    
        if self.wall_ec == False:
          explosion_group.add(Explosion((cx, cy), night_rect, self.map))  
          explosion_group.add(Explosion((cx - 20, cy), night_rect, self.map))  
          explosion_group.add(Explosion((cx + 20, cy), night_rect, self.map))  
          explosion_group.add(Explosion((cx, cy - 20), night_rect, self.map)) 

        if self.wall_ec == True:
          explosion_group.add(Explosion((cx, cy), night_rect, self.map))
          explosion_group.add(Explosion((cx, cy + 20), night_rect, self.map))
          explosion_group.add(Explosion((cx, cy - 20), night_rect, self.map))
        
        self.kill()
      if self.rect.y >= 600:
        self.kill()



class Explosion(pygame.sprite.Sprite):
    def __init__(self, bomb_rect, night_rect, map):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.sound = pygame.mixer.Sound("sound/my/explosion.mp3")
        self.map = map  
        self.image = pygame.image.load("image/my/wepon/explosion.png")
        self.sound.set_volume(0.2)
        self.night_rect = night_rect
        self.rect = self.image.get_rect(center=bomb_rect)
        self.explosion_sound = True
        self.life = 40  # エフェクト維持フレーム数
        # 初期位置の記録
        self.initial_x = self.rect.x
        self.initial_scroll_x = self.map.scroll_x  # 初期のスクロール量を記録

    def update(self):
        self.life -= 1
        if self.explosion_sound:
            self.sound.play()
            self.explosion_sound = False
        if self.life <= 0:
            self.kill()

        current_scroll_x = self.map.scroll_x
        if self.night_rect.x < self.map.nomove_X:
            # スクロールしていない時は位置を固定
            self.rect.x = self.initial_x
        else:
            # スクロールしている時はスクロールの伴い位置を調整
            self.rect.x = self.initial_x - (current_scroll_x - self.initial_scroll_x)