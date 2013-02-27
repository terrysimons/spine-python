class Slot(object):
    def __init__(self, data, skeleton, bone):
        super(Slot, self).__init__()
        self.data = data
        self.skeleton = skeleton
        self.bone = bone
        self.r = 1.0
        self.g = 1.0
        self.b = 1.0
        self.a = 1.0
        self.attachment = None
        self.attachmentTime = 0.0

        if not self.data:
            raise Exception('data cannot be null.')
        if not self.skeleton:
            raise Exception('skeleton cannot be null.')
        if not self.bone:
            raise Exception('bone cannot be null.')

        self.setToBindPose()
                          
        
    def setAttachment(self, attachment):
        self.attachment = attachment


    def setAttachmentTime(self, time):
        self.attachmentTime = self.skeleton.time - time


    def getAttachmentTime(self, ):
        return self.skeleton.time - self.attachmentTime

    
    def setToBindPose(self, ):
        for slotEnumerator in enumerate(self.skeleton.data.slots):
            if self.data == slotEnumerator[1]:
                self.setToBindPoseWithIndex(slotEnumerator[0])

    def setToBindPoseWithIndex(self, slotIndex):
        self.r = self.data.r
        self.g = self.data.g
        self.b = self.data.b
        self.a = self.data.a
        self.setAttachment(self.skeleton.getAttachmentByIndex(slotIndex, self.data.attachmentName) if self.data.attachmentName else 0)
    
    
