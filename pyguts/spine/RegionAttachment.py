import math

import Attachment

class RegionAttachment(Attachment.Attachment):
    def __init__(self):
        super(RegionAttachment, self).__init__()
        self.x = 0.0
        self.y = 0.0
        self.scaleX = 1.0
        self.scaleY = 1.0
        self.rotation = 0.0
        self.width = 0.0
        self.height = 0.0
        self.offset = [0.0,
                       0.0,
                       0.0,
                       0.0,
                       0.0,
                       0.0,
                       0.0,
                       0.0]


    def updateOffset(self):
        localX2 = self.width / 2.0
        localY2 = self.height / 2.0
        localX = -localX2
        localY = -localY2
        localX *= self.scaleX
        localY *= self.scaleY
        radians = math.radians(self.rotation)
        cos = math.cos(radians)
        sin = math.sin(radians)
        localXCos = localX * cos + self.x
        localXSin = localX * sin
        localYCos = localY * cos + self.y
        localYSin = localY * sin
        localX2Cos = localX2 * cos + self.x
        localX2Sin = localX2 * sin
        localY2Cos = localY2 * cos + self.y
        localY2Sin = localY2 * sin
        self.offset[0] = localXCos - localYSin
        self.offset[1] = localYCos + localXSin
        self.offset[2] = localXCos - localY2Sin
        self.offset[3] = localY2Cos + localXSin
        self.offset[4] = localX2Cos - localY2Sin
        self.offset[5] = localY2Cos + localX2Sin
        self.offset[6] = localX2Cos - localYSin
        self.offset[7] = localYCos + localX2Sin


    def updateWorldVerticies(self, bone):
        pass

