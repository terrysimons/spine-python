#!/usr/bin/env python

import os

import pygame

if __name__ == '__main__':
    pygame.init()

    width, height = (640, 480)

    screen = pygame.display.set_mode((width, height))
    screen.fill((0,0,0))

    clock = pygame.time.Clock()    

    done = False


    slot = {}
    slot['x'] = 320
    slot['y'] = 240

    bone = {}
    bone['x'] = 320
    bone['y'] = 240
    bone['xScale'] = 1.0
    bone['yScale'] = 1.0
    bone['rotation'] = 0.0
    bone['length'] = 100
    bone['color'] = [255.0, 192.0, 0.0, 255.0]
    bone['surface'] = pygame.Surface((bone['length'], 1), pygame.SRCALPHA, 32).convert_alpha()

    pygame.draw.line(bone['surface'], 
                     bone['color'], 
                     (0, 0), 
                     (bone['length'], 0), 1)
        
    while not done:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0, 255), (320 - bone['length'], 240 - bone['length'], bone['length'] * 2, bone['length'] * 2), 1)
        
        offset = bone['length'] / 2

        lineTexture = bone['surface'].copy()
        
        lineTexture = pygame.transform.rotozoom(lineTexture, -bone['rotation'], bone['xScale'])
        
        pygame.draw.circle(screen, (255, 0, 0, 255), (320, 240), 3, 0)
        
        #screen.blit(lineTexture, (bone['x'], bone['y']))

        import time; time.sleep(0.1)
        print('%s, %s, %s' % (bone['x'], bone['y'], bone['rotation']))
        bone['rotation'] += 1

        pygame.display.flip()
pygame.quit()
