class BoneData(object):
    def __init__(self, name):
        super(BoneData, self).__init__()
        self.name = name
        self.parent = None
        self.length = 0.0
        self.x = 0.0
        self.y = 0.0
        self.rotation = 0.0
        self.scaleX = 1.0
        self.scaleY = 1.0
        self.flipY = False

