class SkeletonData(object):
    def __init__(self):
        super(SkeletonData, self).__init__()
        self.bones = []
        self.slots = []
        self.skins = []
        self.animations = []
        self.defaultSkin = None

        
    def findBone(self, boneName):
        for i, bone in enumerate(self.bones):
            if bone.name == boneName:
                return bone
        return None


    def findBoneIndex(self, boneName):
        for i, bone in enumerate(self.bones):
            if bone.name == boneName:
                return i
        return -1


    def findSlot(self, slotName):
        for i, slot in enumerate(self.slots):
            if slot.name == slotName:
                return slot
        return None

    
    def findSlotIndex(self, slotName):
        for i, slot in enumerate(self.slots):
            if slot.name == slotName:
                return i
        return -1


    def findSkin(self, skinName):
        for i, skin in enumerate(self.skins):
            if skin.name == skinName:
                return skin
        return None
    

    def findAnimation(self, animationName):
        for i, animation in enumerate(self.animations):
            if animation.name == animationName:
                return animation
        return None
