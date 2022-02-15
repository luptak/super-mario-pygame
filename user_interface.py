import pygame

class UI:
    def __init__(self,surface,font):
        self.surface = surface
        self.currentTime = 0
        self.font = font

    def draw(self):
        self.displayText()

    def displayText(self):
        self.timeTextSurf = self.font.render("TIME",False,(255,255,255))
        self.timeTextRect = self.timeTextSurf.get_rect(center = (600,45))
        self.surface.blit(self.timeTextSurf,self.timeTextRect)

        self.worldTextSurf = self.font.render("WORLD",False,(255,255,255))
        self.worldTextRect = self.worldTextSurf.get_rect(center = (400,45))
        self.surface.blit(self.worldTextSurf,self.worldTextRect)

        self.marioSurf = self.font.render("MARIO",False,(255,255,255))
        self.marioRect = self.marioSurf.get_rect(center = (100,45))
        self.surface.blit(self.marioSurf,self.marioRect)

    def displayTime(self, currentTime):
        self.timeSurf = self.font.render(f"{int(currentTime)}",False,(255,255,255))
        self.timeRect = self.timeSurf.get_rect(center = (600,75))
        self.surface.blit(self.timeSurf,self.timeRect)

    def displayLevel(self,level):
        self.worldSurf = self.font.render(f"1-{level+1}",False,(255,255,255))
        self.worldRect = self.worldSurf.get_rect(center = (400,75))
        self.surface.blit(self.worldSurf,self.worldRect)

    def displayScore(self,score):
        self.worldSurf = self.font.render(f"{score:06}",False,(255,255,255))
        self.worldRect = self.worldSurf.get_rect(center = (100,75))
        self.surface.blit(self.worldSurf,self.worldRect)