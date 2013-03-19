import math

import spine

import pygame

class Circle(object):
    def __init__(self, x, y, r):
        super(Circle, self).__init__()
        self.x = x
        self.y = y
        self.r = r
        self.color = (0, 255, 0, 255)


class Line(object):
    def __init__(self, length):
        super(Line, self).__init__()
        self.x = 0.0
        self.y = 0.0
        self.x1 = 0.0
        self.x2 = 0.0
        self.length = length
        self.rotation = 0.0
        self.color = (255, 0, 0, 255)
        self.texture = pygame.Surface((640, 480), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.texture, (255, 255, 0, 64), (0, 0, self.texture.get_width(), self.texture.get_height()), 1)


    def rotate(self):
        return pygame.transform.rotozoom(self.texture, self.rotation, self.xScale)


class Skeleton(spine.Skeleton):
    def __init__(self, skeletonData):
        super(Skeleton, self).__init__(skeletonData=skeletonData)
        self.x = 0
        self.y = 0
        self.texture = None
        self.debug = True
        self.images = []

    def draw(self, screen, states):
        x = 0
        y = 0

        for slot in self.drawOrder:
            if slot.attachment:
                texture = slot.attachment.texture.copy()
                if texture:
                    x = slot.bone.worldX + slot.attachment.x  * slot.bone.m00 + slot.attachment.y * slot.bone.m01
                    y = -(slot.bone.worldY + slot.attachment.x * slot.bone.m10 + slot.attachment.y * slot.bone.m11)
                    rotation = -(slot.bone.worldRotation + slot.attachment.rotation)
                    xScale = slot.bone.worldScaleX + slot.attachment.scaleX - 1
                    yScale = slot.bone.worldScaleY + slot.attachment.scaleY - 1

                    x += self.x
                    y += self.y

                    if self.flipX:
                        xScale = -xScale
                        rotation = -rotation
                    if self.flipY:
                        yScale = -yScale
                        rotation = -rotation

                    flipX = False
                    flipY = False

                    if xScale < 0:
                        flipX = True
                        #xScale = int(math.abs(xScale))
                    if yScale < 0:
                        flipY = True
                        #yScale = int(math.abs(yScale))

                    
                    texture.fill((slot.r, slot.g, slot.b, slot.a), None, pygame.BLEND_RGBA_MULT)

                    center = texture.get_rect().center                    
                    texture = pygame.transform.flip(texture, flipX, flipY)
                    #texture = pygame.transform.smoothscale(texture, (int(math.fabs(xScale)), int(math.fabs(yScale))))
                    texture = pygame.transform.rotozoom(texture, -rotation, 1)

                    # Center image
                    x = x - texture.get_width() / 2
                    y = y - texture.get_height() / 2
                    screen.blit(texture, (x, y))

        if self.debug:
            for bone in self.bones:

                if not bone.line:
                    bone.line = Line(bone.data.length)
                bone.line.x = bone.worldX + self.x
                bone.line.y = -bone.worldY + self.y
                bone.line.rotation = -bone.worldRotation
                bone.line.color = (255, 0, 0)

                if self.flipX:
                    bone.line.xScale = -1
                    bone.line.rotation = -bone.line.rotation
                else:
                    bone.line.xScale = 1
                if self.flipY:
                    bone.line.yScale = -1
                    bone.line.rotation = -bone.line.rotation
                else:
                    bone.line.yScale = 1

                bone.line.x1 = bone.line.x + math.cos(math.radians(bone.line.rotation)) * bone.line.length
                bone.line.y1 = bone.line.y + math.sin(math.radians(bone.line.rotation)) * bone.line.length

                pygame.draw.line(screen, bone.line.color, (bone.line.x, bone.line.y), (bone.line.x1, bone.line.y1))

                if not bone.circle:
                    bone.circle = Circle(0, 0, 3)
                bone.circle.x = int(bone.worldX) + self.x
                bone.circle.y = -int(bone.worldY) + self.y
                bone.circle.color = (0, 255, 0)
                    
                if 'top left' in bone.data.name:
                    bone.circle.color = (255, 0, 0)
                if 'top right' in bone.data.name:
                    bone.circle.color = (255, 140, 0)
                if 'bottom right' in bone.data.name:
                    bone.circle.color = (255, 255, 0)
                if 'bottom left' in bone.data.name:
                    bone.circle.color = (199, 21, 133)

                pygame.draw.circle(screen, 
                                   bone.circle.color,
                                   (bone.circle.x, bone.circle.y),
                                   bone.circle.r,
                                   0)
