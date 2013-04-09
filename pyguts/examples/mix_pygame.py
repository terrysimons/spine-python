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

    atlas = spine.Atlas(file='./data/spineboy.atlas')
    skeletonJson = spine.SkeletonJson(spine.AtlasAttachmentLoader(atlas))
    skeletonData = skeletonJson.readSkeletonDataFile(file='./data/spineboy.json')
    walkAnimation = skeletonData.findAnimation('walk')
    jumpAnimation = skeletonData.findAnimation('jump')

    skeleton = spine.Skeleton(skeletonData=skeletonData)
    skeleton.debug = True

    skeleton.setToBindPose()
    skeleton.x = -50
    skeleton.y = 400
    skeleton.flipX = False
    skeleton.flipY = False
    skeleton.updateWorldTransform()    

    clock = pygame.time.Clock()    
    animationTime = 0.0

    done = False

    time = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    done = True
        clock.tick(60.0)

        delta = clock.get_time() * 1.0

        time += delta / 1000.00

        jump = jumpAnimation.duration
        beforeJump = 1.0
        blendIn = 0.4
        blendOut = 0.4
        blendOutStart = beforeJump + jump - blendOut
        total = 3.75

        root = skeleton.bones[0]
        speed = 180.0

        if time > beforeJump + blendIn and time < blendOutStart:
            speed = 360.0

        root.x = root.x + speed * delta / 1000.00
        
        screen.fill((0, 0, 0))

        if time > total:
            # restart
            time = 0.0
            root.x = -50.0
        elif time > beforeJump + jump:
            # just walk after jump
            walkAnimation.apply(skeleton, time, True)
        elif time > blendOutStart:
            # blend out jump
            walkAnimation.apply(skeleton, time, True)
            jumpAnimation.mix(skeleton, time - beforeJump, False, 1.0 - (time - blendOutStart) / blendOut)
        elif time > beforeJump + blendIn:
            # just jump
            jumpAnimation.apply(skeleton, time - beforeJump, False)
        elif time > beforeJump:
            # blend in jump
            walkAnimation.apply(skeleton, time, True)
            jumpAnimation.mix(skeleton, time - beforeJump, False, (time - beforeJump) / blendIn)
        else:
            # just walk before jump
            walkAnimation.apply(skeleton, time, True)

        skeleton.updateWorldTransform()
        skeleton.update(clock.get_time())
        skeleton.draw(screen, 0)
        pygame.display.set_caption('%s  %.2f' % (caption, clock.get_fps()), 'Spine Runtime')
        pygame.display.flip()
pygame.quit()
