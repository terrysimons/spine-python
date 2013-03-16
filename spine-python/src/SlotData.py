class SlotData(object):
    def __init__(self, name, boneData):
        super(SlotData, self).__init__()
        if not name:
            raise Exception('Name cannot be None.')

        if not boneData:
            raise Exception('boneData cannot be None.')

        self.name = name
        self.boneData = boneData
        self.r = 255
        self.g = 255
        self.b = 255
        self.a = 255
        self.attachmentName = None


    def setColor(r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

