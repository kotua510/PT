import pygame
from enum import Enum, auto
import time
import math
import random 
from status import Status
import globals

pygame.init()


class My_night(pygame.sprite.Sprite):
  anime_walk_index = [0,0,0,1,1,1]



  def __init__(self,map,window,time_limit,bad_group, zombie_group, ball_group,magic_man_group, magic_ball_group, boss_group,boss_lazer_group):

    super().__init__()
    pygame.sprite.Sprite.__init__(self)

    pygame.mixer.init()

    self.BGM = ["sound/stage/stage_BGM.mp3",
                "sound/enemy/boss_BGM.mp3",
                "sound/camp/camp_BGM.mp3"
      ]
    if globals.deaded == True:
      self.music = self.BGM[2]
    else:
      self.music = self.BGM[0]
    self.isleft = False
    self.anime_walk_index = [0,0,0,0,1,1,1,1]
    self.now_rect = []
    self.walk_index = 0
    self.on_ground = True
    self.wepon_draw = False
    globals.player_deaded = False
    self.map = map
    self.vy = 0
    self.wepon_x = 0
    self.wepon_y = 0
    self.wepon_vx = 0
    self.collision = False
    self.line_move = True
    self.line = False
    self.sideline = False
    self.now_tile = 3
    self.wepon_add_index = 0
    self.attck_bool = False
    self.attck_cooltime_bool = False
    self.attck_bomb_bool = False
    self.win = window
    self.status = Status.NOMAL
    self.time_limit = time_limit
    pygame.mixer.music.load(self.music)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    self.boss_BGM = False

    self.weapon_idx = 0

    self.night_imgs = [
      pygame.image.load("image/my/night/night.png"),
      pygame.image.load("image/my/night/night_jump_run1.png"),
      pygame.image.load("image/my/night/night_run2.png"),
      pygame.image.load("image/my/night/night_throw.png")
    ]
    

    self.night_mucs = [
      pygame.mixer.Sound("sound/my/my_attck.mp3"),
      pygame.mixer.Sound("sound/my/my_hit.mp3"),
      pygame.mixer.Sound("sound/stage/gameover.wav"),
    ]


    self.image = self.night_imgs[0]

    self.sound = self.night_mucs[0]
    
    if globals.deaded == True:
      self.rawrect = pygame.Rect(15050, 400, 40, 40) 
    else:
      self.rawrect = pygame.Rect(200, 200, 40, 40) 
    self.rect = self.rawrect

    self.font = pygame.font.Font(None, 100)  
    self.font_out = pygame.font.Font(None, 108)  
    self.over_text = self.font.render( "GAME OVER" , False, (255, 255, 255))
    self.over_text_out_rect = (220, 160)
    self.over_text_rect = (220, 160)

    self.bad_group = bad_group
    self.zombie_group = zombie_group
    self.ball_group = ball_group
    self.magic_man_group = magic_man_group
    self.magic_ball_group = magic_ball_group
    self.boss_group = boss_group
    self.boss_lazer_group = boss_lazer_group
    self.damage = 0 
    self.invincible = False
    self.invincible_start_time = 0 
    self.invincible_duration = 1000
    self.deadflug = False
    self.inter_se = pygame.mixer.Sound("sound/camp/interact.mp3")

    self.prev_h = False

    globals.buy_flag = False
    self.cursor_SE = pygame.mixer.Sound("sound/camp/cursor_move.mp3")

  def right(self):
    if self.on_ground == True:
      if self.attck_bool == False:
        self.rawrect.x +=5 
        self.isleft = False
        self.walk_index += 1
    else:
      self.rawrect.x +=5 
      self.isleft = False
      self.walk_index += 5
    self.collision, self.line, self.sideline ,self.now_tile = self.map.check_collision(self.rawrect)
    if self.collision == True and self.sideline == True:
        self.rawrect.x = (self.rawrect.x // 40 ) * 40
        self.rawrect.x -= 5
    elif self.collision == True and self.line == False and self.sideline == False :
      self.rawrect.x = (self.rawrect.x // 40 ) * 40


  def left(self):
    if self.on_ground == True:
      if self.attck_bool == False:
        self.rawrect.x -= 5
        self.isleft = True
        self.walk_index += 1
    else:
      self.rawrect.x -= 5
      self.isleft = True
      self.walk_index += 1
    self.collision, self.line, self.sideline , self.now_tile = self.map.check_collision(self.rawrect)
    if self.collision == True and self.sideline == True:
        self.rawrect.x = (self.rawrect.x // 40 + 1) * 40
        self.rawrect.x += 5
    elif self.collision == True and self.line == False and self.sideline == False :
      self.rawrect.x = (self.rawrect.x // 40 + 1 ) * 40



  def jump(self):
      if self.on_ground:
        self.vy -= 18 
        self.on_ground = False

  def attck(self):
    current_time = pygame.time.get_ticks()
    if not self.attck_cooltime_bool:  # クールタイム中でない場合
            self.sound = self.night_mucs[0]
            self.sound.play()
            self.attck_cooltime_bool = True
            self.attck_bool = True
            self.attck_cooltime_start = current_time  # クールタイム開始時間を記録
            self.start_attck_time = current_time  # 攻撃開始時間を記録

    # クールタイム解除処理
    if self.attck_cooltime_bool:
        attck_cooltime = (current_time - self.attck_cooltime_start) / 1000  # 経過時間（秒）
        if attck_cooltime >= 0.1:
            self.attck_cooltime_bool = False  # クールタイム終了

  def attck_bomb(self):
    current_time = pygame.time.get_ticks()

    if not self.attck_cooltime_bool:  # クールタイム中でない場合
            self.sound = self.night_mucs[0]
            self.sound.play()
            self.attck_cooltime_bool = True
            self.attck_bool = True
            self.attck_cooltime_start = current_time  # クールタイム開始時間を記録
            self.start_attck_time = current_time  # 攻撃開始時間を記録

    # クールタイム解除処理
    if self.attck_cooltime_bool:
        attck_cooltime = (current_time - self.attck_cooltime_start) / 1000  # 経過時間（秒）
        if attck_cooltime >= 0.1:
            self.attck_cooltime_bool = False  # クールタイム終了

  def deading(self):
    pygame.mixer.music.stop()
    time.sleep(0.5)
    self.win.fill((0, 0, 0))
    self.rawrect = pygame.Rect(14000, 200, 40, 40) 
    self.sound = self.night_mucs[2]
    self.win.blit(self.over_text, self.over_text_rect)
    self.sound.play()
    pygame.display.update()
    time.sleep(8.5)
    self.status = Status.DEAD

  



  def update(self,time_limit,score_dis,player_dead):
    self.deadflug = player_dead
    if self.rawrect.x > 17080:
      self.rawrect.x = 17080
    self.sound.set_volume(0.3)
    self.check_x =self.rawrect.x // 40 
    self.check_y = self.rawrect.y // 40
    
    self.damage = 0
    self.time_limit = time_limit
    if self.time_limit <= 0 or self.deadflug == True:
      self.status = Status.DEADING




    if self.rect.y >= 800:
        self.status = Status.DEADING



    if self.status == Status.DEADING:
      self.deading()

    if self.status == Status.NOMAL:

      self.rere = self.rawrect.y
      self.score_dis = score_dis
      action = pygame.key.get_pressed()

    # 移動処理
      if self.score_dis == False:
        if self.line_move == True:
          if action[pygame.K_d]:
            self.right()
        if action[pygame.K_j]:  
            self.attck()
        if self.line_move == True:
          if action[pygame.K_a]:
            self.left()
        if action[pygame.K_SPACE]:
            self.jump()
        if action[pygame.K_k]:
            self.attck_bomb()

        if action[pygame.K_UP] and not self.prev_up:  
          self.weapon_idx = 1 - self.weapon_idx
          self.cursor_SE.play()
        self.prev_up = action[pygame.K_UP]
      
        if action[pygame.K_DOWN] and not self.prev_down:  
            self.weapon_idx = 1 - self.weapon_idx
            self.cursor_SE.play()
        self.prev_down = action[pygame.K_DOWN]

        if action[pygame.K_h] and not self.prev_h:  

            if 15330 <= self.rawrect.x <= 15390:
              globals.buy_flag = True

            elif 16060 <= self.rawrect.x <= 16100:
              self.inter_se.play()
              globals.hint_flag = True

            elif 17080 <= self.rawrect.x:
              self.inter_se.play()
              globals.out_camp = True
              self.status = Status.ROED
              

            
        self.prev_h = action[pygame.K_h]

        

    # 重力処理

      self.vy += 1
      self.rawrect.y += self.vy
    

      self.collision, self.line, self.sideline , self.now_tile = self.map.check_collision(self.rawrect)
      if self.collision == True and self.line == False and self.sideline == False :
          self.rawrect.y = (self.rawrect.y // 40 + (1 if self.vy < 0 else 0)) * 40
          if self.vy > 0:
              self.on_ground = True
              self.vy = 0
          else:
              self.vy = 1
      elif self.collision == True and self.line == True:
        if self.vy > 0:
              self.rawrect.y = (self.rawrect.y // 40 + (1 if self.vy < 0 else 0)) * 40
              self.on_ground = True
              self.vy = 0
              self.line_move = True
        else:
              self.vy = -15
              self.line_move = False


      for bad in self.bad_group:
        if self.rawrect.colliderect(bad.rawrect):
          if not self.invincible:
            self.damage = 3
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()
      
      
      for zombie in self.zombie_group:
        if self.rawrect.colliderect(zombie.rawrect):
          if not self.invincible:
            self.damage = 4
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()

      for ball in self.ball_group:
        if self.rawrect.colliderect(ball.rawrect):
          if not self.invincible:
            self.damage = 7
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()
      

      for magic_man in self.magic_man_group:
        if self.rawrect.colliderect(magic_man.rawrect):
          if not self.invincible:
            self.damage = 3
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()

      for magic_ball in self.magic_ball_group:
        if self.rawrect.colliderect(magic_ball.rawrect):
          if not self.invincible:
            self.damage = 2
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()



      for boss in self.boss_group:
        if self.rawrect.colliderect(boss.rawrect):
          if not self.invincible:
            self.damage = 4
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()
          
      for boss_lazer in self.boss_lazer_group:
        if self.rawrect.colliderect(boss_lazer.rawrect):
          if not self.invincible:
            self.damage = 6
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()




      if self.invincible:
        now = pygame.time.get_ticks()
        if now - self.invincible_start_time > self.invincible_duration:
          self.invincible = False


    # 攻撃クールタイム処理
      if self.attck_bool:
          self.now_attck_time = pygame.time.get_ticks()
          self.throw_time = (self.now_attck_time - self.start_attck_time) / 1000
          if self.throw_time >= 0.05:
              self.attck_bool = False



    # アニメーション処理
      if self.score_dis == False:
        if not any(action) and self.on_ground:
          self.image = pygame.transform.flip(self.night_imgs[0], self.isleft, False)
        elif self.attck_bool:
          self.image = pygame.transform.flip(self.night_imgs[3], self.isleft, False)
        elif not self.on_ground:
          self.image = pygame.transform.flip(self.night_imgs[1], self.isleft, False)
        elif (action[pygame.K_a] or action[pygame.K_d]) and self.on_ground:
          self.image = pygame.transform.flip(self.night_imgs[self.anime_walk_index[self.walk_index % 8]], self.isleft, False)
      else:
        self.image = pygame.transform.flip(self.night_imgs[0], self.isleft, False)

      if self.invincible and (pygame.time.get_ticks() // 100 % 2 == 0):
        self.image.set_alpha(10)
      else:
        self.image.set_alpha(255)

      self.rect = pygame.Rect(self.map.get_drawx(self.rawrect), self.rawrect.y, self.rawrect.width, self.rawrect.height)

      if self.rawrect.x >= 13650 and not self.boss_BGM and globals.deaded == False:
          pygame.mixer.music.stop() 
          pygame.mixer.music.load(self.BGM[1])
          pygame.mixer.music.set_volume(0.3)
          pygame.mixer.music.play(-1)
          self.boss_BGM = True