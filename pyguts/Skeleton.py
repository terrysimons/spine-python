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
        self.debug = False
        self.images = []

    def draw(self, screen, states):
        for bone in self.bones:
            bone.updateWorldTransform(self.flipX, self.flipY)
        self.updateWorldTransform()

        screen.fill((0, 0, 0))
            
        for slot in self.drawOrder:
            if slot.attachment:
                texture = slot.attachment.texture
                if texture:
                    x = slot.bone.worldX + slot.attachment.x * slot.bone.m00 + slot.attachment.y * slot.bone.m01 
                    y = -(slot.bone.worldY + slot.attachment.x * slot.bone.m10 + slot.attachment.y * slot.bone.m11) 
                    rotation = -(slot.bone.worldRotation + slot.attachment.rotation)

                    x -= slot.attachment.width / 2
                    y -= slot.attachment.height / 2
                    x += self.x
                    y += self.y

                    xScale = slot.bone.worldScaleX + slot.attachment.scaleX - 1
                    yScale = slot.bone.worldScaleY + slot.attachment.scaleY - 1
                    if self.flipX:
                        xScale = -xScale
                        rotation = -rotation
                    if self.flipY:
                        yScale = -yScale
                        rotation = -rotation
                    #print("R: %s, G: %s, B: %s, A: %s" % (slot.r, slot.b, slot.g, slot.a))
                    #texture.fill((int(slot.r), int(slot.b), int(slot.g), int(slot.a)), None, pygame.BLEND_ADD)
                    texture = pygame.transform.rotate(texture, rotation)
                    screen.blit(texture, (x, y))        


        self.debug = True

        if self.debug:
            for bone in self.bones:

                if not bone.line:
                    bone.line = Line(bone.data.length)
                    bone.line.x = bone.worldX 
                    bone.line.y = -bone.worldY
                    bone.line.rotation = -bone.worldRotation
                    bone.line.color = (255, 0, 0)
                    pygame.draw.line(bone.line.texture, bone.line.color, (0, 0), (bone.data.length, 0), 2)

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

                startX = bone.worldX 
                startY = -bone.worldY 

                endX = startX + bone.data.length
                endY = startY

                if bone.parent:
                    if bone.parent.parent:
                        endX = startX * bone.parent.m00 + startY * bone.parent.m01 + bone.parent.worldX
                        endY = -(startX * bone.parent.m10 + startY * bone.parent.m11 + bone.parent.worldY)

                #pygame.draw.line(screen, bone.line.color, (lineX, lineY), (lineX + bone.data.length, lineY + 0), 2)
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
