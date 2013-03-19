from Bone import Bone
from Slot import Slot

class Skeleton(object):
    def __init__(self, skeletonData):
        super(Skeleton, self).__init__()
        self.data = skeletonData
        self.skin = None
        self.r = 1.0
        self.g = 1.0
        self.b = 1.0
        self.a = 1.0
        self.time = 0.0
        self.bones = []
        self.slots = []
        self.drawOrder = []
        self.flipX = False
        self.flipY = False

        if not self.data:
            raise Exception('skeletonData can not be null.')

        boneCount = len(self.data.bones)
        self.bones = [None] * boneCount
        for i in range(boneCount):
            boneData = self.data.bones[i]
            bone = Bone(data=boneData)
            if boneData.parent:
                for ii in range(boneCount):
                    if self.data.bones[ii] == boneData.parent:
                        bone.parent = self.bones[ii]
                        break
            self.bones[i] = bone

        slotCount = len(self.data.slots)
        self.slots = [None] * slotCount
        for i in range(slotCount):
            slotData = self.data.slots[i]
            bone = None
            for ii in range(boneCount):
                if self.data.bones[ii] == slotData.boneData:
                    bone = self.bones[ii]
                    break
            slot = Slot(slotData=slotData, skeleton=self, bone=bone)
            self.slots[i] = slot
            self.drawOrder.append(slot)
    
    
    def updateWorldTransform(self):
        for i, bone in enumerate(self.bones):
            self.bones[i].updateWorldTransform(self.flipX, self.flipY)

    
    def setToBindPose(self):
        self.setBonesToBindPose()
        self.setSlotsToBindPose()

    
    def setBonesToBindPose(self):
        for i, bone in enumerate(self.bones):
            self.bones[i].setToBindPose()

    
    def setSlotsToBindPose(self):
        for i, bone in enumerate(self.slots):
            self.slots[i].setToBindPoseWithIndex(i)


    def getRootBone(self):
        if len(self.bones):
            return self.bones[0]
        return None


    def setRootBone(self, bone):
        if len(self.bones):
            self.bones[0] = bone
    
    
    def findBone(self, boneName):
        for i, bone in enumerate(self.bones):
            if self.data.bones[i].name == boneName:
                return self.bones[i]
        return None

    
    def findBoneIndex(self, boneName):
        for i, bone in enumerate(self.bones):
            if self.data.bones[i].name == boneName:
                return i
        return -1


    def findSlot(self, slotName):
        for i, slot in enumerate(self.slots):
            if self.data.slots[i].name == slotName:
                return self.slots[i]
        return None


    def findSlotIndex(self, slotName):
        for i, slot in enumerate(self.slots):
            if self.data.slots[i].name == slotName:
                return i
        return -1


    def setSkin(self, skinName):
        skin = self.data.findSkin(skinName)
        if not skin:
            raise Exception('Skin not found: %s' % skinName)
        self.setSkinToSkin(skin)


    def setSkinToSkin(self, newSkin):
        if self.skin and newSkin:
            newSkin.attachAll(self, self.skin)
        self.skin = newSkin


    def getAttachmentByName(self, slotName, attachmentName):
        return self.getAttachmentByIndex(self.data.findSlotIndex(slotName), attachmentName)


    def getAttachmentByIndex(self, slotIndex, attachmentName):
        if self.data.defaultSkin:
            attachment = self.data.defaultSkin.getAttachment(slotIndex, attachmentName)
            if attachment:
                return attachment
        if self.skin:
            return self.skin.getAttachment(slotIndex, attachmentName)
        return None


    def setAttachment(self, slotName, attachmentName):
        for i in range(len(self.slots)):
            if self.slots[i].data.name == slotName:
                self.slots[i].setAttachment(self.getAttachmentByIndex(i, attachmentName))
                return
        raise Exception('Slot not found: %s' % slotName)


    def update(self, delta):
        self.time += delta

    
