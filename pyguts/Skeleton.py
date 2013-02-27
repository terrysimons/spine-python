import spine

import pygame

class Skeleton(spine.Skeleton):
    def __init__(self, data):
        super(Skeleton, self).__init__(data=data)
        self.vertexArray = []
        self.texture = None


    def draw(self, screen, states):
        for slot in self.slots:
            if slot.attachment:
                #slot.attachment.draw(slot)
                #transformedTexture = pygame.transform.rotate(slot.attachment.texture, slot.attachment.rotation)
                transformedTexture = slot.attachment.texture
                #print("Slot: ")
                #import pprint; pprint.pprint(slot.__dict__)
                #print("Slot Bone: ")
                #import pprint; pprint.pprint(slot.bone.__dict__)
                #print("Slot Data: ")
                #import pprint; pprint.pprint(slot.data.__dict__)
                #print("Slot Attachment: ")
                #import pprint; pprint.pprint(slot.attachment.__dict__)
                screen.blit(transformedTexture, (slot.attachment.verticies[2].texCoords.x, slot.attachment.verticies[2].texCoords.y))
        #screen.blit(self.texture, (0, 0))

