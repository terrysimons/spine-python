from Bone import Bone
from Slot import Slot

class Skeleton(object):
    def __init__(self, data):
        super(Skeleton, self).__init__()
        self.data = data
        self.bones = []
        self.slots = []
        self.drawOrder = []
        self.skin = None
        self.r = 0.0
        self.g = 0.0
        self.b = 0.0
        self.a = 0.0
        self.time = 0.0
        self.flipX = False
        self.flipY = False

        if not data:
            raise Exception('data can not be null.')

        boneCount = len(data.bones)
        for i in range(boneCount):
            boneData = data.bones[i]
            bone = Bone(data=boneData)
            if boneData.parent:
                for ii in range(boneCount):
                    if data.bones[ii] == boneData.parent:
                        bone.parent = self.bones[ii]
                        break
            self.bones.append(bone)

        slotCount = len(data.slots)
        for i in range(slotCount):
            slotData = data.slots[i]
            bone = None
            for ii in range(boneCount):
                if data.bones[ii] == slotData.boneData:
                    bone = self.bones[ii]
                    break
            slot = Slot(data=slotData, skeleton=self, bone=bone)
            self.slots.append(slot)
            self.drawOrder.append(slot)
            

    
    def updateWorldTransform(self):
        for bone in self.bones:
            bone.updateWorldTransform(self.flipX, self.flipY)

    
    def setToBindPose(self):
        self.setBonesToBindPose()
        self.setSlotsToBindPose()

    
    def setBonesToBindPose(self):
        for bone in self.bones:
            bone.setToBindPose()

    
    def setSlotsToBindPose(self):
        for i in range(len(self.slots)):
            self.slots[i].setToBindPoseWithIndex(i)


    def getRootBone(self):
        if len(self.bones):
            return self.bones[0]
        return None

    
    def findBone(self, boneName):
        for i in range(len(self.bones)):
            if self.data.bones[i].name == boneName:
                return self.bones[i]
        return None

    
    def findBoneIndex(self, boneName):
        for i in range(len(self.bones)):
            if self.data.bones[i].name == boneName:
                return i
        return -1


    def findSlot(self, slotName):
        for i in range(len(self.slots)):
            if self.data.slots[i].name == slotName:
                return self.slots[i]
            return None


    def findSlotIndex(self, slotName):
        for i in range(len(self.slots)):
            if self.data.slots[i].name == slotName:
                return i
        return -1


    def setSkinByName(self, skinName):
        skin = data.findSkin(skinName)
        if not skin:
            raise Exception('Skin not found: %s' % skinName)
        self.setSkin(skin)


    def setSkinBySkin(self, newSkin):
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
            return self.skin.getAttachmentByIndex(slotIndex, attachmentName)
        return None


    def setAttachment(self, slotName, attachmentName):
        for i in range(len(self.slots)):
            slot = self.slots[i]
            if slot.data.name == slotName:
                slot.setAttachment(self.getAttachmentByIndex(i, attachmentName))
                return
        raise Exception('Slot not found: %s' % slotName)
