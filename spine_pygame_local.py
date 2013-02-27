#!/usr/bin/env python

import os

import pygame

import pyguts as spine

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    width, height = (640, 480)

    font = pygame.font.SysFont('None', 24, True, False)
    screen = pygame.display.set_mode((width, height))
    screen.fill((0,0,0))
    caption = 'PyGuts - A Pygame front-end based on the python-spine Runtime'
    pygame.display.set_caption(caption, 'Spine Runtime')

    atlasFile = os.path.realpath('./data/spineboy.atlas')
    atlas = spine.Atlas(file=atlasFile)

    skeletonJson = spine.SkeletonJson(spine.AtlasAttachmentLoader(atlas))

    skeletonFile = os.path.realpath('./data/spineboy-skeleton.json')
    skeletonData = skeletonJson.readSkeletonData(skeletonFile)

    animationFile = os.path.realpath('./data/spineboy-walk.json')
    animation = skeletonJson.readAnimation(file=animationFile, 
                                           skeletonData=skeletonData)

    skeleton = spine.Skeleton(data=skeletonData)

    skeleton.flipX = False
    skeleton.flipY = False
    skeleton.setToBindPose()
    skeleton.getRootBone().x = 0.0
    skeleton.getRootBone().y = 0.0
    skeleton.getRootBone().x = 200.0
    skeleton.getRootBone().y = 420.0
    skeleton.updateWorldTransform()

    clock = pygame.time.Clock()    
    animationTime = 0.0

    done = False

    while not done:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        animationTime += clock.get_time() / 1000.0                
        animation.apply(skeleton=skeleton,
                        time=animationTime,
                        loop=True)
        skeleton.updateWorldTransform()
        skeleton.draw(screen, 0)
        pygame.display.flip()
pygame.quit()
