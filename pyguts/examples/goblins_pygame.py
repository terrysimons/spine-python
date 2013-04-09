#!/usr/bin/env python

import os

import pygame

import pyguts as spine

if __name__ == '__main__':
    pygame.init()

    width, height = (640, 480)

    screen = pygame.display.set_mode((width, height))
    screen.fill((0,0,0))
    caption = 'PyGuts - A Pygame front-end based on the python-spine Runtime'
    pygame.display.set_caption(caption, 'Spine Runtime')

    atlas = spine.Atlas(file='./data/goblins.atlas')
    skeletonJson = spine.SkeletonJson(spine.AtlasAttachmentLoader(atlas))
    skeletonData = skeletonJson.readSkeletonDataFile('./data/goblins.json')
    walkAnimation = skeletonData.findAnimation('walk')

    goblin = spine.Skeleton(skeletonData=skeletonData)
    goblin.debug = True

    goblin.setSkin('goblin')
    goblin.setToBindPose()
    goblin.x = 120
    goblin.y = 400
    goblin.flipX = False
    goblin.flipY = False
    goblin.updateWorldTransform()

    goblingirl = spine.Skeleton(skeletonData=skeletonData)
    goblingirl.debug = True

    goblingirl.setSkin('goblingirl')
    goblingirl.setToBindPose()
    goblingirl.x = 420
    goblingirl.y = 400
    goblingirl.flipX = False
    goblingirl.flipY = False
    goblingirl.updateWorldTransform()

    clock = pygame.time.Clock()    
    animationTime = 0.0

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    done = True
        clock.tick(0)
        animationTime += clock.get_time() / 1000.0
        walkAnimation.apply(skeleton=goblin,
                            time=animationTime,
                            loop=True)
        walkAnimation.apply(skeleton=goblingirl,
                            time=animationTime,
                            loop=True)
        goblin.updateWorldTransform()
        goblingirl.updateWorldTransform()
        screen.fill((0, 0, 0))
        goblin.draw(screen, 0)
        goblingirl.draw(screen, 0)
        pygame.display.set_caption('%s  %.2f' % (caption, clock.get_fps()), 'Spine Runtime')
        pygame.display.flip()
pygame.quit()
