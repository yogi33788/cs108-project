import numpy as np 
import pygame,sys

# Base class defintion
# and some attributes described very frequently in the pygames

class Base:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.gameover = False
        self.gamewinner = None
        self.player = 1
        self.animate = False
        self.base_width = 800
        self.base_height = 800

  

        