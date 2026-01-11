import pygame
from enum import Enum, auto
import globals
import time
from status import Status 

pygame.init()

class Camp(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    pygame.sprite.Sprite.__init__(self)

    self.humans = [
      "青年A",
      "武器屋",
      "シスター",
      "青年B",
      "青年C",
      ""
    ]

    self.serifA = [
      "ここはキャンプだよ。 キャンプでは武器や情報を購入したりすることが",
      "できるんだぜ。 右に進むとキャンプからでることができるんだ。",
      "この世界では時間＝お金だ、所持している時間は武器屋と教会で確認できる。",
      "それじゃあ、時間に気を付けて買い物しろよ。"
    ]

    self.serifB = [
      "ここは武器屋です。 ここでは武器を購入またはあなたの武器を強化すること",
      "ができます。",
      "ご利用なさいますか？",
      "(カーソル移動:上下キー  決定:Hキー)"
    ]

    self.serifC = [
      "ここは教会です。 あなたが知りたいことにお答えしましょう。",
      "何か聞きたいことがありますか？",
      "(カーソル移動:上下キー  決定:Hキー)",
      ""
    ]

    self.serifD = [
      "知っているかい？、ステージのどこかには特別なお宝が隠されているらしい。",
      "手に入れたやつはすごい力を得るらしいぞ。 空を飛んだり、海を割るとか",
      "体が頑丈になるとか、まあどれもこれも都市伝説なんだけどな。",
      ""
    ]

    self.serifE = [
      "武器を強化すればするほど簡単にステージをクリアできるようになる。",
      "ステージをクリアしたらまた武器を強化できる。 ",
      "こうやって繰り返していくことが大事なんだなぁ。",
      ""
    ]

    self.serifF = [
      "ステージに向かいますか？",
      "(決定:Hキー)",
      "",
      ""
    ]

    self.serif_shop = [
      "ナイフ",
      "爆弾",
    ]

    self.serif_knife =[
      "  LV.1    ",
      "  LV.2    ",
      "  LV.3    ",
      "  LV.4    ",
      "  LV.MAX    "
    ]

    self.knife_place = [
      600,
      1500,
      3500,
      10000,
      ""
    ]

    self.SEs = [
      pygame.mixer.Sound("sound/camp/cursor_move.mp3"),
      pygame.mixer.Sound("sound/camp/interact.mp3"),
      pygame.mixer.Sound("sound/camp/text.mp3")
    ]

    self.treasure_hint = [
      "分かりました。 ステージ1に隠されているお宝の場所についてお教えし",
      "ましょう。 古い書物によるとお宝は大きな穴に隠されているようですね。",
      " 一見穴に見えてもお宝が隠されている場所につながっていることもある",
      "のかもしれません。"
    ]

    self.debt_text = [
      "時間を借りるのですね。 あなたに貸すことのできる時間は 500 です。",
      "返す時は+200の時間を返さなければなりません、時間を借りている間は",
      "武器の購入や強化はできません。 それでも借りるのですか? ",
      "借りるのでしたら Lキー を押して下さい"
    ]

    self.debt_end_text = [
      "了解しました。 借りた分は寄付分もしっかり返してくださいね。"
    ]

    self.debt_back_text = [
      "借りた時間を返してくれるのですか？",
      "返すのであれば Lキー を押してください。",
      "ありがとうございます、しっかりと返してもらいました。",
      "これで武器屋のご利用なども可能になりますよ。"
    ]

    self.no_weapon_text = [
      "あなた、時間を借りてるなら先にそっちを返してください。",
      "借りているものは早めに返した方がいいですよ、先代からの教えです。",
      
    ]

    self.bombs = 0


    self.font =  pygame.font.Font("C:/Windows/Fonts/msgothic.ttc", 25)
    self.enter_text = self.font.render("Enter!", False, (0,0,0))
    self.enter_text2 = self.font.render("Enter!", False, (255,255,255))

    self.key = pygame.key.get_pressed()

    self.serif = False

    self.white = (255,255,255)
    self.yellow = (255,255,0)


    self.weapon_idx = 0
    self.knife_idx = 0
    self.hint_first = globals.hint_first
    self.debt = globals.debt

    self.debt_ok = False
    self.debt_on = False
    self.debt_back = globals.debt_back

    self.prev_return = self.key[pygame.K_RETURN]

    self.knife_idx = globals.keep_knife_idx
    self.debt_on = globals.keep_debt_on


  def serif_window(self,character,target):
      
      self.character = character
      self.serif_set = target
      self.human_text1 = self.font.render(self.serif_set[0], False, (255,255,255))
      self.human_text2 = self.font.render(self.serif_set[1], False, (255,255,255))
      self.human_text3 = self.font.render(self.serif_set[2], False, (255,255,255))
      self.human_text4 = self.font.render(self.serif_set[3], False, (255,255,255))
      self.character_text = self.font.render(self.character, False, (255,255,255))

      pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
      pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))
      pygame.draw.rect(globals.window, (255,255,255),(0,194,200,50))
      pygame.draw.rect(globals.window, (0,0,0),(6,200,188,38))
      globals.window.blit(self.character_text,(10,208,150,150))

      globals.window.blit(self.human_text1,(10,20,150,150))
      globals.window.blit(self.human_text2,(10,60,150,150))
      globals.window.blit(self.human_text3,(10,100,150,150))
      globals.window.blit(self.human_text4,(10,140,150,150))



  def serif_window_shop(self,character,target,idx,score):
      self.character = character
      self.serif_set = target
      self.weapon_idx = idx
      self.score = score
      self.human_text1 = self.font.render(self.serif_set[0], False, (255,255,255))
      self.human_text2 = self.font.render(self.serif_set[1], False, (255,255,255))
      self.human_text3 = self.font.render(self.serif_set[2], False, (255,255,255))
      self.human_text4 = self.font.render(self.serif_set[3], False, (255,255,255))
      self.no_weapon_text1 = self.font.render(self.no_weapon_text[0], False, (255,255,255))
      self.no_weapon_text2 = self.font.render(self.no_weapon_text[1], False, (255,255,255))
      self.character_text = self.font.render(self.character, False, (255,255,255))
      self.score_text = self.font.render(str("所持時間:" + str(self.score)), False, (255,255,255))


      if globals.buy_flag == True:
        if self.debt_on == False:
          if self.weapon_idx == 0:
            if self.knife_idx != 4:
              self.SEs[1].play()
              if self.knife_idx == 0:
                globals.player_score -= 600
                globals.knife_plus += 0.5
                self.SEs[1].play()
              elif self.knife_idx == 1:
                globals.player_score -= 1500
                globals.knife_plus += 0.5
              elif self.knife_idx == 2:
                globals.player_score -= 3500
                globals.knife_plus += 1
              elif self.knife_idx == 3:
                globals.player_score -= 10000
                globals.knife_plus += 2
              self.knife_idx += 1


          else:
            globals.bomb_counter += 1
            globals.player_score -= 100
            self.SEs[1].play()
            self.SEs[1].set_volume(1.0)
          globals.buy_flag = False


      self.weapontexts = [
      str(self.serif_shop[0] + self.serif_knife[self.knife_idx] ),
      str(self.serif_shop[1] + "×" + str(globals.bomb_counter) + "(所持数)" )
        ]
    
      self.weapon_plecetexts = [
      str(self.knife_place[self.knife_idx]),
      str("100")
        ]


      
      if self.weapon_idx == 0:
        self.weapon_text1 = self.font.render(self.weapontexts[0], False, self.yellow)
        self.weapon_text2 = self.font.render(self.weapontexts[1], False, self.white)
        self.plece_text1 = self.font.render(self.weapon_plecetexts[0], False, self.yellow)
        self.plece_text2 = self.font.render(self.weapon_plecetexts[1], False, self.white)
      else:
        self.weapon_text1 = self.font.render(self.weapontexts[0], False, self.white)
        self.weapon_text2 = self.font.render(self.weapontexts[1], False, self.yellow)
        self.plece_text1 = self.font.render(self.weapon_plecetexts[0], False, self.white)
        self.plece_text2 = self.font.render(self.weapon_plecetexts[1], False, self.yellow)

      if self.debt_on == False:
        pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
        pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))
        pygame.draw.rect(globals.window, (255,255,255),(0,194,200,50))
        pygame.draw.rect(globals.window, (0,0,0),(6,200,188,38))
        pygame.draw.rect(globals.window, (255,255,255),(194,194,300,50))
        pygame.draw.rect(globals.window, (0,0,0),(200,200,288,38))
        globals.window.blit(self.score_text,(210,210,150,150))
        globals.window.blit(self.character_text,(10,208,150,150))

        globals.window.blit(self.human_text1,(10,20,150,150))
        globals.window.blit(self.human_text2,(10,60,150,150))
        globals.window.blit(self.human_text3,(10,100,150,150))
        globals.window.blit(self.human_text4,(10,140,150,150))

        pygame.draw.rect(globals.window, (255,255,255),(550,100,300,400))
        pygame.draw.rect(globals.window, (0,0,0),(558,108,284,384))
        globals.window.blit(self.weapon_text1,(560,110,150,150))
        globals.window.blit(self.weapon_text2,(560,150,150,150))
        globals.window.blit(self.plece_text1,(775,110,150,150))
        globals.window.blit(self.plece_text2,(800,150,150,150))

      else:
        pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
        pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))
        pygame.draw.rect(globals.window, (255,255,255),(0,194,200,50))
        pygame.draw.rect(globals.window, (0,0,0),(6,200,188,38))

        globals.window.blit(self.no_weapon_text1,(10,20,150,150))
        globals.window.blit(self.no_weapon_text2,(10,60,150,150))
        globals.window.blit(self.character_text,(10,208,150,150))



  def serif_window_church(self,character,target,idx,score):
      self.character = character
      self.serif_set = target
      self.weapon_idx = idx
      self.score = score
      self.human_text1 = self.font.render(self.serif_set[0], False, (255,255,255))
      self.human_text2 = self.font.render(self.serif_set[1], False, (255,255,255))
      self.human_text3 = self.font.render(self.serif_set[2], False, (255,255,255))
      self.human_text4 = self.font.render(self.serif_set[3], False, (255,255,255))
      self.character_text = self.font.render(self.character, False, (255,255,255))
      self.score_text = self.font.render(str("所持時間:" + str(self.score)), False, (255,255,255))

      self.hint_text1 = self.font.render(self.treasure_hint[0], False, (255,255,255))
      self.hint_text2 = self.font.render(self.treasure_hint[1], False, (255,255,255))
      self.hint_text3 = self.font.render(self.treasure_hint[2], False, (255,255,255))
      self.hint_text4 = self.font.render(self.treasure_hint[3], False, (255,255,255))

      self.debt_text1 = self.font.render(self.debt_text[0], False, (255,255,255))
      self.debt_text2 = self.font.render(self.debt_text[1], False, (255,255,255))
      self.debt_text3 = self.font.render(self.debt_text[2], False, (255,255,255))
      self.debt_text4 = self.font.render(self.debt_text[3], False, (255,255,255))



      self.debt_end_text0 = self.font.render(self.debt_end_text[0], False, (255,255,255))

      self.debt_back_text1 = self.font.render(self.debt_back_text[0], False, (255,255,255))
      self.debt_back_text2 = self.font.render(self.debt_back_text[1], False, (255,255,255))
      
      self.debt_back_text3 = self.font.render(self.debt_back_text[2], False, (255,255,255))

      self.debt_back_text4 = self.font.render(self.debt_back_text[3], False, (255,255,255))
      





      self.weapontexts = [
      str("お宝ヒント:1"),
      str("時間を借りる、返す")
        ]
    
      self.weapon_plecetexts = [
      str("2000"),
      str("")
        ]


      
      if self.weapon_idx == 0:
        self.weapon_text1 = self.font.render(self.weapontexts[0], False, self.yellow)
        self.weapon_text2 = self.font.render(self.weapontexts[1], False, self.white)
        self.plece_text1 = self.font.render(self.weapon_plecetexts[0], False, self.yellow)
        self.plece_text2 = self.font.render(self.weapon_plecetexts[1], False, self.white)
      else:
        self.weapon_text1 = self.font.render(self.weapontexts[0], False, self.white)
        self.weapon_text2 = self.font.render(self.weapontexts[1], False, self.yellow)
        self.plece_text1 = self.font.render(self.weapon_plecetexts[0], False, self.white)
        self.plece_text2 = self.font.render(self.weapon_plecetexts[1], False, self.yellow)

      if globals.hint_flag == False:
        pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
        pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))
        globals.window.blit(self.human_text1,(10,20,150,150))
        globals.window.blit(self.human_text2,(10,60,150,150))
        globals.window.blit(self.human_text3,(10,100,150,150))
        globals.window.blit(self.human_text4,(10,140,150,150))

      pygame.draw.rect(globals.window, (255,255,255),(0,194,200,50))
      pygame.draw.rect(globals.window, (0,0,0),(6,200,188,38))
      pygame.draw.rect(globals.window, (255,255,255),(194,194,300,50))
      pygame.draw.rect(globals.window, (0,0,0),(200,200,288,38))
      globals.window.blit(self.score_text,(210,210,150,150))
      globals.window.blit(self.character_text,(10,208,150,150))

      pygame.draw.rect(globals.window, (255,255,255),(550,100,300,400))
      pygame.draw.rect(globals.window, (0,0,0),(558,108,284,384))
      globals.window.blit(self.weapon_text1,(560,110,150,150))
      globals.window.blit(self.weapon_text2,(560,150,150,150))
      if self.hint_first == True:
        globals.window.blit(self.plece_text1,(775,110,150,150))
      globals.window.blit(self.plece_text2,(800,150,150,150))

      if globals.hint_flag == True:
        if self.weapon_idx == 0:
          if self.hint_first == True:
            globals.player_score -= 2000
            pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
            pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))
            
            globals.window.blit(self.hint_text1,(10,20,150,150))
            globals.window.blit(self.hint_text2,(10,60,150,150))
            globals.window.blit(self.hint_text3,(10,100,150,150))
            globals.window.blit(self.hint_text4,(10,100,150,150))
            self.hint_first = False
          else:
            pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
            pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))
            
            globals.window.blit(self.hint_text1,(10,20,150,150))
            globals.window.blit(self.hint_text2,(10,60,150,150))
            globals.window.blit(self.hint_text3,(10,100,150,150))
            globals.window.blit(self.hint_text4,(10,140,150,150))


        else:
          if self.debt == False:
            pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
            pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))
            
            globals.window.blit(self.debt_text1,(10,20,150,150))
            globals.window.blit(self.debt_text2,(10,60,150,150))
            globals.window.blit(self.debt_text3,(10,100,150,150))
            globals.window.blit(self.debt_text4,(10,140,150,150))
            self.debt_ok = True

            if self.key[pygame.K_l] and not self.prev_l:
              if self.debt_on == False:
                self.SEs[1].play()
                globals.player_score += 500
              self.debt_on = True
              self.debt_back = False
            self.prev_l = self.key[pygame.K_l]
            
            if self.debt_on == True:
              pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
              pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))

              globals.window.blit(self.debt_end_text0,(10,20,150,150))

          else:
            pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
            pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))
            
            globals.window.blit(self.debt_back_text1,(10,20,150,150))
            globals.window.blit(self.debt_back_text2,(10,60,150,150))
            
            if self.key[pygame.K_l] and not self.prev_l:
              if self.debt_on == True:
                self.SEs[1].play()
                globals.player_score -= 700
              self.debt_on = False
              self.debt_back = True
            self.prev_l = self.key[pygame.K_l]

            if self.debt_on == False:
              if self.debt_back == True:
                pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
                pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))

                globals.window.blit(self.debt_back_text3,(10,20,150,150))
                globals.window.blit(self.debt_back_text4,(10,60,150,150))


  def serif_window_campend(self,character,target):
      self.character = character
      self.serif_set = target
      self.stagetexts = [
            "ステージ1"
        ]
      self.human_text1 = self.font.render(self.serif_set[0], False, (255,255,255))
      self.human_text2 = self.font.render(self.serif_set[1], False, (255,255,255))
      self.human_text3 = self.font.render(self.serif_set[2], False, (255,255,255))
      self.human_text4 = self.font.render(self.serif_set[3], False, (255,255,255))
      self.stage_text = self.font.render(self.stagetexts[0], False, self.yellow)



      if globals.out_camp == True:
          #if self.weapon_idx == 0:
          #print("ステージ1")
          #else:

          globals.out_camp = False


      self.stagetexts = [
            "ステージ1"
        ]
      
      #if self.weapon_idx == 0:
      #else:
      pygame.draw.rect(globals.window, (255,255,255),(0,0,900,200))
      pygame.draw.rect(globals.window, (0,0,0),(6,6,888,188))

      globals.window.blit(self.human_text1,(10,20,150,150))
      globals.window.blit(self.human_text2,(10,60,150,150))
      globals.window.blit(self.human_text3,(10,100,150,150))
      globals.window.blit(self.human_text4,(10,140,150,150))

      pygame.draw.rect(globals.window, (255,255,255),(550,100,300,400))
      pygame.draw.rect(globals.window, (0,0,0),(558,108,284,384))
      globals.window.blit(self.stage_text,(560,110,150,150))



  def update(self, night_rawrect, night_weapon_idx,night_status):
    if night_status == Status.DEADING or night_status == Status.DEAD:
      globals.keep_knife_idx = self.knife_idx
      globals.keep_debt_on = self.debt_on
      globals.hint_first = self.hint_first
      globals.debt_back = self.debt_back
      globals.debt = self.debt 
    
    if night_status == Status.ROED:
      globals.keep_knife_idx = self.knife_idx
      globals.keep_debt_on = self.debt_on
      globals.hint_first = self.hint_first
      globals.debt_back = self.debt_back
      globals.debt = self.debt 



    self.night_rawrect = night_rawrect
    self.night_rawrect_x = self.night_rawrect.x

    self.enter_rect = night_rawrect.copy()
    self.enter_rect_y = self.enter_rect.y - 30

    self.weapon_idx = night_weapon_idx

    self.key = pygame.key.get_pressed()


    if self.key[pygame.K_RETURN] and not self.prev_return:  
      self.serif = True
      self.SEs[0].play()
    self.prev_return = self.key[pygame.K_RETURN]







    if 15100 <= self.night_rawrect_x <= 15150:
      globals.window.blit(self.enter_text,(310,self.enter_rect_y, 150, 150))
      if self.serif == True:
        self.serif_window(self.humans[0],self.serifA)
    
    elif 15330 <= self.night_rawrect_x <= 15390:
      globals.window.blit(self.enter_text2,(310,self.enter_rect_y, 150, 150))
      if self.serif == True:
        self.serif_window_shop(self.humans[1],self.serifB,self.weapon_idx,globals.player_score)
        

    elif 16060 <= self.night_rawrect_x <= 16100:
      globals.window.blit(self.enter_text,(310,self.enter_rect_y, 150, 150))
      if self.serif == True:
        self.serif_window_church(self.humans[2],self.serifC,self.weapon_idx,globals.player_score)

    elif 16460 <= self.night_rawrect_x <= 16500:
      globals.window.blit(self.enter_text,(310,self.enter_rect_y, 150, 150))
      if self.serif == True:
        self.serif_window(self.humans[3],self.serifD)

    elif 16545 <= self.night_rawrect_x <= 16575:
      globals.window.blit(self.enter_text,(310,self.enter_rect_y, 150, 150))
      if self.serif == True:
        self.serif_window(self.humans[4],self.serifE)

    elif 17080 <= self.night_rawrect_x:
      self.serif_window_campend(self.humans[5],self.serifF)

    else:
      self.serif = False
      globals.hint_flag = False
      self.debt_back = True
      if self.debt_ok:
        self.debt = True
      if self.debt_on == False:
        if self.debt_back == True:
          self.debt = False
          self.debt_ok = False
          self.debt_on = False
          self.debt_back = False

    if globals.out_camp == True:
      globals.restart = True


