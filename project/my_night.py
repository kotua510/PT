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



  def __init__(self,map,window,time_limit,bad_group, zombie_group, ball_group,fall_ball_group,magic_man_group, magic_ball_group, boss_group,boss_lazer_group, boss_ball_night_group, boss_ball_ran_group, boss_nom_group,boss_lazer_nom_group, boss_ball_night_nom_group, boss_ball_ran_nom_group,boss2_nom_group):

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
    self.stage_idx = 0
    self.end_idx = 0

    self.h_in = False

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
    self.endfont = pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", 35)  
    self.over_text = self.font.render( "GAME OVER" , False, (255, 255, 255))
    self.over_text_rect = (220, 160)
    self.endtexts1 =[
      "1000時間をあなたは姫に与えました",
      "姫とあなたはわずかな時間でしたが幸せに",
      "過ごしました"
    ]
    self.endtexts2 =[
      "10000時間をあなたは姫に与えました",
      "姫とあなたはそれからの時間を共に",
      "そしてしあわせに過ごしました"
    ]
    self.endtexts3 =[
      "あなたは時間を姫に与えませんでした",
      "あなたはその後姫を見殺しにしたとして",
      "一生その身を追われることになりました"
    ]
    self.end_text1 = self.endfont.render( "" , False, (255, 255, 255))
    self.end_text2 = self.endfont.render( "" , False, (255, 255, 255))
    self.end_text3 = self.endfont.render( "" , False, (255, 255, 255))
    self.end_text4 = self.font.render( "" , False, (255, 255, 255))
    self.over_text_out_rect = (220, 160)
    self.end_text_rect4 = (280, 450)
    self.end_text_rect1 = (80, 100)
    self.end_text_rect2 = (80, 150)
    self.end_text_rect3 = (80, 200)

    self.bad_group = bad_group
    self.zombie_group = zombie_group
    self.ball_group = ball_group
    self.fall_ball_group = fall_ball_group
    self.magic_man_group = magic_man_group
    self.magic_ball_group = magic_ball_group
    self.boss_group = boss_group
    self.boss_lazer_group = boss_lazer_group
    self.boss_ball_night_group = boss_ball_night_group
    self.boss_ball_ran_group = boss_ball_ran_group
    self.boss_nom_group = boss_nom_group
    self.boss2_nom_group = boss2_nom_group
    self.boss_lazer_nom_group = boss_lazer_nom_group
    self.boss_ball_night_nom_group = boss_ball_night_nom_group
    self.boss_ball_ran_nom_group = boss_ball_ran_nom_group
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

  
  def ending(self):
    if globals.end_num == -1 :
      return
    pygame.mixer.music.stop()
    if globals.end_num == 0:
      self.end_text1 = self.endfont.render( self.endtexts1[0] , False, (255, 255, 255))
      self.end_text2 = self.endfont.render( self.endtexts1[1] , False, (255, 255, 255))
      self.end_text3 = self.endfont.render( self.endtexts1[2] , False, (255, 255, 255))
      self.end_text4 = self.font.render( "Good End" , False, (255, 255, 255))
    if globals.end_num == 1:
      self.end_text1 = self.endfont.render( self.endtexts2[0] , False, (255, 255, 255))
      self.end_text2 = self.endfont.render( self.endtexts2[1] , False, (255, 255, 255))
      self.end_text3 = self.endfont.render( self.endtexts2[2] , False, (255, 255, 255))
      self.end_text4 = self.font.render( "The End" , False, (255, 255, 255))
    if globals.end_num == 2:
      self.end_text1 = self.endfont.render( self.endtexts3[0] , False, (255, 255, 255))
      self.end_text2 = self.endfont.render( self.endtexts3[1] , False, (255, 255, 255))
      self.end_text3 = self.endfont.render( self.endtexts3[2] , False, (255, 255, 255))
      self.end_text4 = self.font.render( "Bad End" , False, (255, 255, 255))

    time.sleep(2)
    self.win.fill((0, 0, 0))
    self.rawrect = pygame.Rect(14000, 200, 40, 40) 
    self.win.blit(self.end_text1, self.end_text_rect1)
    self.win.blit(self.end_text2, self.end_text_rect2)
    self.win.blit(self.end_text3, self.end_text_rect3)
    self.win.blit(self.end_text4, self.end_text_rect4)
    pygame.display.update()
    time.sleep(15)
    self.status = Status.DEAD


  def update(self,time_limit,player_dead):
    if globals.treasure_get2 == True:
      globals.treasure_knife = 1
    self.h_in = False
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

    if self.status == Status.END:
      self.ending()

    if self.status == Status.NOMAL:

      self.rere = self.rawrect.y
      action = pygame.key.get_pressed()

      if globals.ending_true == True:
        globals.ending_true = False
        self.status = Status.END

    # 移動処理
      if globals.score_dis == False:
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

        if action[pygame.K_h]:  
          self.h_in = True
          if not self.prev_h:
            if 15330 <= self.rawrect.x <= 15390:
              globals.buy_flag = True

            elif 16060 <= self.rawrect.x <= 16100:
              self.inter_se.play()
              globals.hint_flag = True

            elif 15545 <= self.rawrect.x <= 15575:
              self.inter_se.play()
              globals.end_true = True

            elif 17080 <= self.rawrect.x:
              self.inter_se.play()
              globals.out_camp = True
              self.status = Status.ROED
              

            
        self.prev_h = action[pygame.K_h]

        if action[pygame.K_UP] and not self.prev_up:  
          if self.h_in == False:
            self.weapon_idx = 1 - self.weapon_idx
            if self.end_idx != 0:
              self.end_idx = self.end_idx - 1
            else:
              self.end_idx = 2
            if globals.stage1_clear == True and globals.stage2_clear == False:
              self.stage_idx = 1 - self.stage_idx
            elif globals.stage1_clear == True and globals.stage2_clear == True:
              if self.stage_idx != 0:
                self.stage_idx = self.stage_idx - 1
              else:
                self.stage_idx = 2

            if globals.hints_idx != 0:
              globals.hints_idx = globals.hints_idx - 1
            else:
              globals.hints_idx = 2
            self.cursor_SE.play()
        self.prev_up = action[pygame.K_UP]
      
        if action[pygame.K_DOWN] and not self.prev_down:  
          if self.h_in == False:
            self.weapon_idx = 1 - self.weapon_idx
            if self.end_idx != 2:
                self.end_idx = self.end_idx + 1
            else:
                self.end_idx = 0
            if globals.stage1_clear == True and globals.stage2_clear == False:
              self.stage_idx = 1 - self.stage_idx
            elif globals.stage1_clear == True and globals.stage2_clear == True:
              if self.stage_idx != 2:
                self.stage_idx = self.stage_idx + 1
              else:
                self.stage_idx = 0

            if globals.hints_idx != 2:
              globals.hints_idx = globals.hints_idx + 1
            else:
              globals.hints_idx = 0
            self.cursor_SE.play()
        self.prev_down = action[pygame.K_DOWN]



        

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

      for fall_ball in self.fall_ball_group:
        if self.rawrect.colliderect(fall_ball.rawrect):
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

      for boss_ball_night in self.boss_ball_night_group:
        if self.rawrect.colliderect(boss_ball_night.rawrect):
          if not self.invincible:
            self.damage = 6
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()

      for boss_ball_ran in self.boss_ball_ran_group:
        if self.rawrect.colliderect(boss_ball_ran.rawrect):
          if not self.invincible:
            self.damage = 6
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()

      for boss_ball_ran_nom in self.boss_ball_ran_nom_group:
        if self.rawrect.colliderect(boss_ball_ran_nom.rawrect):
          if not self.invincible:
            self.damage = 6
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()

      for boss_ball_night_nom in self.boss_ball_night_nom_group:
        if self.rawrect.colliderect(boss_ball_night_nom.rawrect):
          if not self.invincible:
            self.damage = 6
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()

      for boss_nom in self.boss_nom_group:
        if self.rawrect.colliderect(boss_nom.rawrect):
          if not self.invincible:
            self.damage = 4
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()
          
      for boss_lazer_nom in self.boss_lazer_nom_group:
        if self.rawrect.colliderect(boss_lazer_nom.rawrect):
          if not self.invincible:
            self.damage = 6
            self.invincible = True
            self.invincible_start_time = pygame.time.get_ticks()
            self.sound = self.night_mucs[1]
            self.sound.play()

      for boss2_nom in self.boss2_nom_group:
        if self.rawrect.colliderect(boss2_nom.rawrect):
          if not self.invincible:
            self.damage = 4
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
      if globals.score_dis == False:
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
          globals.boss_start = True
          globals.fall_ball_group.empty()
          self.boss_BGM = True