#!/usr/bin/env python

import os

import pygame

import pyguts as spine

if __name__ == '__main__':
    pygame.init()

    width, height = (640, 480)

    screen = pygame.display.set_mode((width, height))
    screen.fill((0,0,0))

    atlasFile = os.path.realpath('./data/test.atlas')
    atlas = spine.Atlas(file=atlasFile)

    skeletonJson = spine.SkeletonJson(spine.AtlasAttachmentLoader(atlas))

    skeletonFile = os.path.realpath('./data/test.json')
    skeletonData = skeletonJson.readSkeletonData(skeletonFile)

    skeleton = spine.Skeleton(skeletonData=skeletonData)
    skeleton.debug = True

    skeleton.x = 320
    skeleton.y = 400
    skeleton.flipX = False
    skeleton.flipY = False
    skeleton.setToBindPose()
    skeleton.updateWorldTransform()

    clock = pygame.time.Clock()    
    clock.tick(60)
    animationTime = 0.0

    done = False

    while not done:
        clock.tick(1)
        animationTime += clock.get_time() / 1000.0                
        screen.fill((0, 0, 0))
        skeleton.draw(screen, 0)
        pygame.display.flip()
        print(skeleton.bones[0].x, skeleton.bones[0].y, skeleton.bones[0].rotation)
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
        skeleton.bones[0].rotation += 15        
pygame.quit()
