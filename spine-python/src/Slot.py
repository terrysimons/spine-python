class Slot(object):
    def __init__(self, slotData, skeleton, bone):
        super(Slot, self).__init__()
        if not slotData:
            raise Exception('slotData cannot be None.')
        if not skeleton:
            raise Exception('skeleton cannot be None.')
        if not bone:
            raise Exception('bone cannot be None.')
        self.data = slotData
        self.skeleton = skeleton
        self.bone = bone
        self.r = 255
        self.g = 255
        self.b = 255
        self.a = 255
        self.attachment = None
        self.attachmentTime = 0.0
        self.setToBindPose()


    def setColor(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
                          
        
    def setAttachment(self, attachment):
        self.attachment = attachment
        self.attachmentTime = self.skeleton.time


    def setAttachmentTime(self, time):
        self.attachmentTime = self.skeleton.time - time


    def getAttachmentTime(self):
        return self.skeleton.time - self.attachmentTime

    
    def setToBindPose(self):
        for i, slot in enumerate(self.skeleton.data.slots):
            if self.data == slot:
                self.setToBindPoseWithIndex(i)


    def setToBindPoseWithIndex(self, slotIndex):
        self.setColor(self.data.r, self.data.g, self.data.b, self.data.a)
        self.setAttachment(self.skeleton.getAttachmentByIndex(slotIndex, self.data.attachmentName) if self.data.attachmentName else None)
    
    
