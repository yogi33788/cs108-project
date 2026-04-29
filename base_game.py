import numpy as np 
import pygame,sys

class Base:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.gameover = False
        self.gamewinner = None
        self.player = 1
        self.animate = False
