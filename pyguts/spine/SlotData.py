class SlotData(object):
    def __init__(self, name, boneData):
        super(SlotData, self).__init__()
        self.name = name
        self.boneData = boneData
        self.r = 1.0
        self.g = 1.0
        self.b = 1.0
        self.a = 1.0
        self.attachmentName = None
