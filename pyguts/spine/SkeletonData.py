class SkeletonData(object):
    def __init__(self):
        super(SkeletonData, self).__init__()
        self.bones = []
        self.slots = []
        self.skins = []
        self.defaultSkin = None

        
    def findBone(self, boneName):
        for i in range(len(self.bones)):
            if self.bones[i].name == boneName:
                return self.bones[i]
        return None


    def findBoneIndex(self, boneName):
        for i in range(len(self.bones)):
            if self.bones[i].name == boneName:
                return i
        return -1


    def findSlot(self, slotName):
        for i in range(len(self.slots)):
            if self.slots[i].name == slotName:
                return self.slots[i]
        return None

    
    def findSlotIndex(self, slotName):
        for i in range(len(self.slots)):
            if self.slots[i].name == slotName:
                return i
        return -1


    def findSkin(self, skinName):
        for i in range(len(self.skins)):
            if self.skins[i].name == skinName:
                return skins[i]
        return None
    
