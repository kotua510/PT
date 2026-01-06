import pygame
from globals import window

pygame.init()

class Opening(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()


    self.image = pygame.image.load("image/stage/gimmick/cloud_title.png")

    window.fill((144, 215, 236))

    self.cloud1_rect = pygame.Rect(100,30,40,40)
    self.cloud2_rect = pygame.Rect(700,70,40,40)
    self.title_rect = pygame.Rect(180, 150, 40, 40)
    self.title_flame_rect = pygame.Rect(170, 150, 40, 40)
    self.enter_rect = pygame.Rect(300, 350, 40, 40)
    self.enter_flame_rect = pygame.Rect(294, 350, 40, 40)
    self.title_font = pygame.font.SysFont("叛逆明朝",150)
    self.title_flame_font = pygame.font.SysFont("叛逆明朝",152)
    self.enter_font = pygame.font.SysFont("叛逆明朝",60)
    self.enter_flame_font = pygame.font.SysFont("叛逆明朝",63)
    self.title_text = f"time striker"
    self.enter_text = f"press Enter"
    self.title_flame = self.title_flame_font.render(self.title_text, False, (0,0,0))
    self.enter_flame = self.enter_flame_font.render(self.enter_text, False, (0,0,0))
    self.title = self.title_font.render(self.title_text, False, (255,255,255))
    self.enter = self.enter_font.render(self.enter_text, False, (255,255,255))
    clock = pygame.time.Clock()
    
    opening = True

  def update(self):

        window.fill((144, 215, 236))
        window.blit(self.image, self.cloud1_rect)
        window.blit(self.image, self.cloud2_rect)
        window.blit(self.title_flame, self.title_flame_rect)
        window.blit(self.title, self.title_rect)
        window.blit(self.enter_flame, self.enter_flame_rect)
        window.blit(self.enter, self.enter_rect)


        pygame.display.flip()

  
