import spine

import pygame

class Skeleton(spine.Skeleton):
    def __init__(self, data):
        super(Skeleton, self).__init__(data=data)
        self.vertexArray = []
        self.texture = None


    def draw(self, screen, states):
        self.updateWorldTransform()

        debug = True
        #x = 0
        #y = 0
        #rotation = 0.0

        #for i, slot in enumerate(self.drawOrder):
        #    if slot.attachment:
        #        texture = slot.attachment.texture
        #        x = slot.bone.worldX + slot.attachment.x * slot.bone.m00 + slot.attachment.y * slot.bone.m01
        #        y = -(slot.bone.worldY + slot.attachment.x * slot.bone.m10 + slot.attachment.y * slot.bone.m11)
        #        x = x - slot.attachment.width / 2
        #        y = -y - slot.attachment.height / 2            
        #        rotation = -(slot.bone.worldRotation + slot.attachment.rotation)

        #        xScale = slot.bone.worldScaleX + slot.attachment.scaleX - 1.0
        #        yScale = slot.bone.worldScaleY + slot.attachment.scaleY - 1.0
        #        if self.flipX:
        #            xScale = -xScale
        #            rotation = -rotation
        #        if self.flipY:
        #            yScale = -yScale
        #            rotation = -rotation

        #        texture = pygame.transform.rotozoom(texture, rotation, xScale)

        #        pygame.draw.rect(texture, (0, 192, 128, 255), (0, 0, texture.get_width(), texture.get_height()), 1)                
                #screen.blit(texture, (x, y))
                
        for i, slot in enumerate(self.drawOrder):
            if not slot.attachment: 
                continue
                
            x = slot.bone.worldX + slot.attachment.x * slot.bone.m00 + slot.attachment.y * slot.bone.m01
            y = -(slot.bone.worldY + slot.attachment.x * slot.bone.m10 + slot.attachment.y * slot.bone.m11)
            x = x - slot.attachment.width / 2
            y = -y - slot.attachment.height / 2            
            rotation = -(slot.bone.worldRotation + slot.attachment.rotation)
            xScale = slot.bone.worldScaleX + slot.attachment.scaleX - 1.0
            yScale = slot.bone.worldScaleY + slot.attachment.scaleY - 1.0
            if self.flipX:
                xScale = -xScale
                rotation = -rotation
            if self.flipY:
                yScale = -yScale
                rotation = -rotation

            bone = slot.bone
            line = {}
                #lineSurface = pygame.Surface((640, 480), pygame.SRCALPHA, 32).convert_alpha()
            line['surface'] = pygame.Surface((bone.data.length, 0), pygame.SRCALPHA, 32).convert_alpha() 
            line['color'] =  pygame.Color(255, 0, 0, 128)
            line['x'] = x
            line['y'] = y
            line['rotation'] = -rotation
            if self.flipX:
                line['xScale'] = -1.0
                line['rotation'] = -line['rotation']
            else:
                line['xScale'] = 1.0
            if self.flipY:
                line['yScale'] = -1.0
                line['rotation'] = -line['rotation']
            else:
                line['yScale'] = 1.0
                
            circle = {}
                #circleSurface = pygame.Surface((640, 480), pygame.SRCALPHA, 32).convert_alpha()
            circle['surface'] = pygame.Surface((640, 480), pygame.SRCALPHA, 32).convert_alpha()
            circle['color'] = (0, 255, 0, 128)
            circle['x'] = int(x)
            circle['y'] = int(y)
            circle['rotation'] = rotation
            if self.flipX:
                circle['xScale'] = -1.0
                circle['rotation'] = -circle['rotation']
            else:
                circle['xScale'] = 1.0
            if self.flipY:
                circle['yScale'] = -1.0
                circle['rotation'] = -circle['rotation']
            else:
                circle['yScale'] = 1.0
                
            if self.slots[i].attachment:
                texture = self.slots[i].attachment.texture.convert_alpha()
                texture = pygame.transform.rotozoom(texture, rotation, xScale)
                #print("SLOT COLOR: (%s, %s, %s, %s)" % (slot.r, slot.g, slot.b, slot.a))
                texture.fill((slot.r, slot.g, slot.b, slot.a), None, pygame.BLEND_MAX)
                screen.blit(texture, (circle['x'], circle['y']))
                                   
                pygame.draw.line(line['surface'], 
                                 line['color'], 
                                 (0, 
                                  0),  
                                 (bone.data.length, 
                                  0), 1)

                    #line['surface'] = pygame.transform.rotozoom(line['surface'], 
                    #                                            line['rotation'],
                    #                                            line['xScale'])
               
            import pprint; pprint.pprint(circle)
            pygame.draw.circle(circle['surface'], circle['color'], (circle['x'], circle['y']), 3, 0)
                #circle['surface'] = pygame.transform.rotate(circle['surface'], circle['rotation'])
                
            screen.blit(line['surface'], (0,0))
            screen.blit(circle['surface'], (0,0))
                #pygame.display.flip()
                #import time; time.sleep(.5)
                
            print("lineX: %d" % line['x'])
            print("lineY: %d" % line['y'])
                
            print("circleX: %d" % circle['x'])
            print("circleY: %d" % circle['y'])

            slot = self.slots[i]
                    
            print('Bone: ')
            import pprint; pprint.pprint(slot.bone.__dict__)
            print('Bone Data: ')
            import pprint; pprint.pprint(slot.data.boneData.__dict__)
            if slot.bone.parent:
                print('Slot Parent: ')
                import pprint; pprint.pprint(slot.bone.parent.__dict__)
                print('Slot Parent Bone Data: ')
                import pprint; pprint.pprint(slot.bone.parent.data.__dict__)
                    #print('Slot Parent Bone Data: ')
                    #import pprint; pprint.pprint(slot.bone.parent.data.__dict__)
            print('Slot: ')
            import pprint; pprint.pprint(slot.__dict__)
            print('Slot Data: ')
            import pprint; pprint.pprint(slot.data.__dict__)
            if slot.attachment:
                print('Slot Attachment: ')
                import pprint; pprint.pprint(slot.attachment.__dict__)
                print('Slot Attachment Bone Data: ')
                import pprint; pprint.pprint(slot.data.boneData.__dict__)                   
                print("Attachment Name: %s" % slot.data.attachmentName)

               # while pygame.event.wait().type != pygame.KEYDOWN:
               #     for event in pygame.event.get():
               #         if event.type == pygame.KEYDOWN:
               #             if event.key == pygame.K_SPACE:
               #                 break                                                                                                 
                            #import time; time.sleep(1)

            #    transformedTexture = slot.attachment.texture

            #    slot.attachment.draw(slot)
            #    transformedTexture = pygame.transform.rotate(transformedTexture, bone.worldRotation)

            #    screen.blit(transformedTexture, (bone.worldX + slot.attachment.u2, bone.worldY + slot.attachment.v2))
                #for vertex in enumerate(self.vertexArray):
                #    if vertex[0] == 4:
                #        screen.blit(self.texture, (vertex[1].texCoords.x, vertex[1].texCoords.y))

                
        #for slot in self.slots:
        #    if slot.attachment:
                #slot.attachment.draw(slot)
        #        transformedTexture = slot.attachment.texture
                #print("Slot: ")
                #import pprint; pprint.pprint(slot.__dict__)
                #print("Slot Bone: ")
                #import pprint; pprint.pprint(slot.bone.__dict__)
                #print("Slot Data: ")
                #import pprint; pprint.pprint(slot.data.__dict__)
                #if 'left-shoulder' in slot.data.attachmentName:
                #    print("Slot Attachment: ")
                #    import pprint; pprint.pprint(slot.attachment.__dict__)
                #    for vertex in slot.attachment.verticies:
                #        import pprint; pprint.pprint(vertex.__dict__)
                #        import pprint; pprint.pprint(vertex.color.__dict__)
                #        import pprint; pprint.pprint(vertex.texCoords.__dict__)
                #            
                #    import pdb; pdb.set_trace()
