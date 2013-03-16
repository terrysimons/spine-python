import math

class Bone(object):
    def __init__(self, data):
        super(Bone, self).__init__()
        self.data = data
        self.parent = None
        self.x = data.x
        self.y = data.y
        self.rotation = data.rotation
        self.scaleX = data.scaleX
        self.scaleY = data.scaleY
        self.m00 = 0.0
        self.m01 = 0.0
        self.m10 = 0.0
        self.m11 = 0.0
        self.worldX = 0.0
        self.worldY = 0.0
        self.worldRotation = 0.0
        self.worldScaleX = 0.0
        self.worldScaleY = 0.0
        self.line = None
        self.circle = None
        

    def setToBindPose(self):
        self.x = self.data.x
        self.y = self.data.y
        self.rotation = self.data.rotation
        self.scaleX = self.data.scaleX
        self.scaleY = self.data.scaleY


    def updateWorldTransform(self, flipX, flipY):
        if self.parent:
            self.worldX = self.x * self.parent.m00 + self.y * self.parent.m01 + self.parent.worldX 
            self.worldY = self.x * self.parent.m10 + self.y * self.parent.m11 + self.parent.worldY
            self.worldScaleX = self.parent.worldScaleX * self.scaleX
            self.worldScaleY = self.parent.worldScaleY * self.scaleY
            self.worldRotation = self.parent.worldRotation + self.rotation
        else:
            self.worldX = self.x
            self.worldY = self.y
            self.worldScaleX = self.scaleX
            self.worldScaleY = self.scaleY
            self.worldRotation = self.rotation

        radians = math.radians(self.worldRotation)
        cos = math.cos(radians)
        sin = math.sin(radians)
        self.m00 = cos * self.worldScaleX
        self.m10 = sin * self.worldScaleX
        self.m01 = -sin * self.worldScaleY
        self.m11 = cos * self.worldScaleY

        if flipX:
            self.m00 = -self.m00 
            self.m01 = -self.m01 
        if flipY:
            self.m10 = -self.m10 
            self.m11 = -self.m11 
        # The C++ runtime has this, but Corona doesn't.
        #if self.data.flipY:
        #    self.m10 = -self.m10 if self.m10 != 0.0 else 0.0
        #    self.m11 = -self.m11 if self.m11 != 0.0 else 0.0
        
