#!/usr/bin/env python

import pygame

pygame.init()

width, height = (640, 480)

screen = pygame.display.set_mode((width, height))
screen.fill((0,0,0))
pygame.draw.circle(screen, (0, 255, 0), (0, 0), 20, 0)
pygame.display.flip()
import time; time.sleep(5)
