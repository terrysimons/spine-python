import spine

import pygame

class Skeleton(spine.Skeleton):
    def __init__(self, data):
        super(Skeleton, self).__init__(data=data)
        self.vertexArray = []
        self.texture = None


    def draw(self, screen, states):
        self.updateWorldTransform()
        
