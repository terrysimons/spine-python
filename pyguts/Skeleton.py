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
        self.length = length
        self.rotation = 0.0
        self.color = (255, 0, 0, 255)
        self.texture = pygame.Surface((640, 480), pygame.SRCALPHA, 32)
        #self.texture = pygame.Surface((300, 300), pygame.SRCALPHA, 32)
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
        for bone in self.bones:
            bone.updateWorldTransform(self.flipX, self.flipY)

        x = 0
        y = 0

        for slot in self.drawOrder:
            if slot.attachment:
                texture = slot.attachment.texture
                if texture:
                    x = slot.bone.worldX + slot.attachment.x * slot.bone.m00 + slot.attachment.y * slot.bone.m01
                    y = -(slot.bone.worldY + slot.attachment.x * slot.bone.m10 + slot.attachment.y * slot.bone.m11)
                    rotation = -(slot.bone.worldRotation + slot.attachment.rotation)
                    xScale = slot.bone.worldScaleX + slot.attachment.scaleX - 1
                    yScale = slot.bone.worldScaleY + slot.attachment.scaleY - 1

                    x += self.x
                    y += self.y

                    # Center image.
                    x -= slot.attachment.offset.center[0]
                    y -= slot.attachment.offset.center[1]

                    if self.flipX:
                        xScale = -xScale
                        rotation = -rotation
                    if self.flipY:
                        yScale = -yScale
                        rotation = -rotation
                    avgScale = (xScale + yScale) / 2
                    
                    #texture.fill((slot.r, slot.g, slot.b, slot.a), None, pygame.BLEND_MAX)
                    
                    texture = pygame.transform.rotozoom(texture, rotation, 1)
                    screen.blit(texture, (x, y))        


        self.debug = True

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

                lineX = bone.line.x + bone.data.length * bone.m00 + bone.y * bone.m01
                lineY = -(bone.line.y + bone.data.length * bone.m01 + bone.y * bone.m11)
            
                #pygame.draw.line(screen, bone.line.color, (bone.line.x, bone.line.y), (lineX, lineY), 2)
                #pygame.draw.line(screen, bone.line.color, (startX + self.x, startY + self.y), (endX + self.x, endY + self.y), 2)

                #screen.blit(bone.line.texture, (bone.worldX + self.x, -bone.worldY + self.y))
                #screen.blit(bone.line.rotate(), (bone.worldX + self.x - 320, -bone.worldY + self.y - 240))
                #screen.blit(bone.line.rotate(), (bone.worldX + self.x, -bone.worldY + self.y))
                #screen.blit(bone.line.rotate(), (bone.worldX + self.x / 2, -bone.worldY + self.y))
                #screen.blit(bone.line.rotate(), (bone.worldX + self.x / 2, -bone.worldY + self.y))
                #screen.blit(bone.line.rotate(), (bone.worldX * bone.m00 + self.x, -bone.worldY * bone.m01 + self.y))
                            
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

                print('Bone Name: %s' % bone.data.name)
                import pprint; pprint.pprint(bone.__dict__)
                import pprint; pprint.pprint(bone.data.__dict__)
                    
                fontDebug = False

                if fontDebug:
                    pygame.font.init()
                    myfont = pygame.font.SysFont(None, 12)
                    nameTexture = myfont.render(bone.data.name, 0, (255, 255, 255))
                    posTexture = myfont.render('x: %s, y: %s' % (bone.circle.x, bone.circle.y), 0, (255, 255, 255))
                    screen.blit(nameTexture, (bone.circle.x - 200, bone.circle.y - 10))
                    screen.blit(posTexture, (bone.circle.x - 200, bone.circle.y + 10))
                    pygame.display.flip()
                    
        #print(self.bones[0].x, self.bones[0].y, self.bones[0].rotation)                    
        #while (pygame.event.wait().type != pygame.KEYDOWN): pass
        #self.bones[0].rotation += 15
