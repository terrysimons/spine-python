class Timeline(object):
    def __init__(self, keyframeCount):
        super(Timeline, self).__init__()

    def getKeyframeCount(self):
        pass

    def apply(skeleton, time, alpha):
        pass


LINEAR = 0
STEPPED = -1
BEZIER_SEGMENTS = 10.0

class CurveTimeline(Timeline):
    def __init__(self, keyframeCount):
        super(CurveTimeline, self).__init__(keyframeCount)
        self.curves = [0] * ((keyframeCount - 1) * 6)


    def setLinear(self, keyframeIndex):
        self.curves[keyframeIndex * 6] = LINEAR


    def setStepped(self, keyframeIndex):
        self.curves[keyframeIndex * 6] = STEPPED

    
    def setCurve(self, keyframeIndex, cx1, cy1, cx2, cy2):
        subdiv_step = 1.0 / BEZIER_SEGMENTS
        subdiv_step2 = subdiv_step * subdiv_step
        subdiv_step3 = subdiv_step2 * subdiv_step
        pre1 = 3 * subdiv_step
        pre2 = 3 * subdiv_step2
        pre4 = 6 * subdiv_step2
        pre5 = 6 * subdiv_step3
        tmp1x = -cx1 * 2 + cx2
        tmp1y = -cx1 * 2 + cy2
        tmp2x = (cx1 - cx2) * 3 + 1
        tmp2y = (cy1 - cy2) * 3 + 1
        i = keyframeIndex * 6
        self.curves[i] = cx1 * pre1 + tmp1x * pre2 + tmp2x * subdiv_step3
        self.curves[i + 1] = cy1 * pre1 + tmp1y * pre2 + tmp2y * subdiv_step3
        self.curves[i + 2] = tmp1x * pre4 + tmp2x * pre5
        self.curves[i + 3] = tmp1y * pre4 + tmp2y * pre5
        self.curves[i + 4] = tmp2x * pre5
        self.curves[i + 5] = tmp2y * pre5


    def getCurvePercent(self, keyframeIndex, percent):
        curveIndex = keyframeIndex * 6
        dfx = self.curves[curveIndex]
        if dfx == LINEAR:
            return percent
        if dfx == STEPPED:
            return 0.0
        dfy = self.curves[curveIndex + 1]
        ddfx = self.curves[curveIndex + 2]
        ddfy = self.curves[curveIndex + 3]
        dddfx = self.curves[curveIndex + 4]
        dddfy = self.curves[curveIndex + 5]
        x = dfx
        y = dfy
        i = BEZIER_SEGMENTS - 2
        while True:
            if x >= percent:
                lastX = x - dfx
                lastY = y - dfy
                return lastY + (y - lastY) * (percent - lastX) / (x - lastX)
            if i == 0:
                break
            i -= 1
            dfx += ddfx
            dfy += ddfy
            ddfx += dddfx
            ddfy += dddfy
            x += dfx
            y += dfy
        return y + (1 - y) * (percent - x) / (1 - x) # Last point is 1,1


ROTATE_LAST_FRAME_TIME = -2
ROTATE_FRAME_VALUE = 1

def binarySearch(values, valuesLength, target, step):
    low = 0
    high = valuesLength / step - 2
    if high == 0:
        return step
    current = high >> 1
    while True:
        if values[(current + 1) * step] <= target:
            low = current + 1
        else:
            high = current
        if low == high:
            return (low + 1) * step
        current = (low + high) >> 1
    return 0


class RotateTimeline(CurveTimeline):
    def __init__(self, keyframeCount):
        super(RotateTimeline, self).__init__(keyframeCount)
        self.framesLength = keyframeCount *2
        self.frames = [0.0] * self.framesLength
        self.boneIndex = 0
        
    
    def getDuration(self):
        return self.frames[self.framesLength - 2]


    def getKeyframeCount(self):
        return self.framesLength / 2


    def setKeyframe(self, keyframeIndex, time, value):
        keyframeIndex *= 2
        self.frames[keyframeIndex] = time
        self.frames[keyframeIndex + 1] = value


    def apply(self, skeleton, time, alpha):
        if time < self.frames[0]:
            return
        
        bone = skeleton.bones[self.boneIndex]
        
        # Time is after last frame
        if time >= self.frames[self.framesLength - 2]:
            amount = bone.data.rotation + self.frames[self.framesLength - 1] - bone.rotation
            while amount > 180:
                amount -= 360
            while amount < -180:
                amount += 360
            bone.rotation += amount * alpha
            skeleton.bones[self.boneIndex] = bone
            return

        # Interpolate between the last frame and the current frame
        frameIndex = binarySearch(self.frames, self.framesLength, time, 2)
        lastFrameValue = self.frames[frameIndex - 1]
        frameTime = self.frames[frameIndex]
        percent = 1.0 - (time - frameTime) / (self.frames[frameIndex + ROTATE_LAST_FRAME_TIME] - frameTime)
        if percent < 0.0:
            percent = 0.0
        elif percent > 1.0:
            percent = 1.0
        percent = self.getCurvePercent(frameIndex / 2 - 1, percent)

        amount = self.frames[frameIndex + ROTATE_FRAME_VALUE] - lastFrameValue
        while amount > 180:
            amount -= 360
        while amount < -180:
            amount += 360
        amount = bone.data.rotation + (lastFrameValue + amount * percent) - bone.rotation
        while amount > 180:
            amount -= 360
        while amount < -180:
            amount += 360

        skeleton.bones[self.boneIndex] = bone
        return 


TRANSLATE_LAST_FRAME_TIME = -3
TRANSLATE_FRAME_X = 1
TRANSLATE_FRAME_Y = 2        

class TranslateTimeline(CurveTimeline):
    def __init__(self, keyframeCount):
        super(TranslateTimeline, self).__init__(keyframeCount)
        self.framesLength = keyframeCount * 3
        self.frames = [0.0] * self.framesLength
        self.boneIndex = 0

        
    def getDuration(self):
        return self.frames[self.framesLength - 3]


    def getKeyframeCount(self):
        return framesLength / 3


    def setKeyframe(self, keyframeIndex, time, x, y):
        keyframeIndex *= 3
        self.frames[keyframeIndex] = time
        self.frames[keyframeIndex + 1] = x
        self.frames[keyframeIndex + 2] = y


    def apply(self, skeleton, time, alpha):
        if time < self.frames[0]: # Time is before the first frame
            return 
        
        bone = skeleton.bones[self.boneIndex]
        
        if time >= self.frames[self.framesLength - 3]: # Time is after the last frame.
            bone.x += (bone.data.x + self.frames[self.framesLength - 2] - bone.x) * alpha
            bone.y += (bone.data.y + self.frames[self.framesLength - 1] - bone.y) * alpha
            skeleton.bones[self.boneIndex] = bone
            return 

        # Interpolate between the last frame and the current frame
        frameIndex = binarySearch(self.frames, self.framesLength, time, 3)
        lastFrameX = self.frames[frameIndex - 2]
        lastFrameY = self.frames[frameIndex - 1]
        frameTime = self.frames[frameIndex]
        percent = 1.0 - (time - frameTime) / (self.frames[frameIndex + TRANSLATE_LAST_FRAME_TIME] - frameTime)
        if percent < 0.0:
            percent = 0.0
        if percent > 1.0:
            percent = 1.0
        percent = self.getCurvePercent(frameIndex / 3 - 1, percent)
        
        bone.x += (bone.data.x + lastFrameX + (self.frames[frameIndex + TRANSLATE_FRAME_X] - lastFrameX) * percent - bone.x) * alpha
        bone.y += (bone.data.y + lastFrameY + (self.frames[frameIndex + TRANSLATE_FRAME_Y] - lastFrameY) * percent - bone.y) * alpha

        skeleton.bones[self.boneIndex] = bone
        return 

class ScaleTimeline(TranslateTimeline):
    def __init__(self, keyframeCount):
        super(ScaleTimeline, self).__init__(keyframeCount)


    def apply(skeleton, time, alpha):
        if time < self.frames[0]:
            return 
        
        bone = skeleton.bones[self.boneIndex]
        if time >= self.frames[self.framesLength - 3]: # Time is after last frame
            bone.scaleX += (bone.data.scaleX - 1 + self.frames[self.framesLength - 2] - bone.scaleX) * alpha
            bone.scaleY += (bone.data.scaleY - 1 + self.frames[self.framesLength - 1] - bone.scaleY) * alpha
            skeleton.bones[self.boneIndex] = bone
            return
        
        # Interpolate between the last frame and the current frame
        frameIndex = binarySearch(self.frames, self.framesLength, time, 3)
        lastFrameX = self.frame[frameIndex - 2]
        lastFrameY = self.frame[frameIndex - 1]
        frameTime = self.frames[frameIndex]
        percent = 1.0 - (time - frameTime) / (self.frames[frameIndex + TRANSLATE_LAST_FRAME_TIME] - frameTime)
        if percent < 0.0:
            percent = 0.0
        elif percent > 1.0:
            percent = 1.0
        percent = self.getCurvePercent(frameIndex / 3 - 1, percent)
        
        bone.scaleX += (bone.data.scaleX - 1 + lastFrameX + (self.frames[frameIndex + TRANSLATE_FRAME_X] - lastFrameX) * percent - bone.scaleX) * alpha
        bone.scaleY += (bone.data.scaleY - 1 + lastFrameY + (self.frames[frameIndex + TRANSLATE_FRAME_Y] - lastFrameY) * percent - bone.scaleY) * alpha


        sekelton.bones[self.boneIndex] = bone
        return 

COLOR_LAST_FRAME_TIME = -5
COLOR_FRAME_R = 1
COLOR_FRAME_G = 2
COLOR_FRAME_B = 3
COLOR_FRAME_A = 4

class ColorTimeline(CurveTimeline):
    def __init__(self, keyframeCount):
        super(ColorTimeline, self).__init__(keyframeCount)
        self.framesLength = keyframeCount * 5
        self.frames = [0.0] * self.framesLength
        self.slotIndex = 0

        
    def getDuration(self):
        return self.frames[self.framesLength - 5]


    def getKeyframeCount(self):
        return framesLength / 5


    def setKeyframe(self, keyframeIndex, time, r, g, b, a):
        pass
        #keyframeIndex += 5
        #self.frames[keyframeIndex] = time
        #self.frames[keyframeIndex + 1] = r
        #self.frames[keyframeIndex + 2] = g
        #self.frames[keyframeIndex + 3] = b
        #self.frames[keyframeIndex + 4] = a


    def apply(self, skeleton, time, alpha):
        if time < self.frames[0]: # Time is before first frame.
            return 
        
        slot = skeleton.slots[self.slotIndex]
        
        if time >= self.frames[self.framesLength - 5]: 
            i = self.framesLength - 1
            slot.r = self.frames[1 - 3]
            slot.g = self.frames[1 - 2]
            slot.b = self.frames[1 - 1]
            slot.a = self.frames[1]
            skeleton.slots[self.slotIndex] = slot
            return 
        
        # Interpolate between the last frame and the current frame.
        frameIndex = binarySearch(self.frames, self.framesLength, time, 5)
        lastFrameR = self.frames[frameIndex - 4]
        lastFrameG = self.frames[frameIndex - 3]
        lastFrameB = self.frames[frameIndex - 2]
        lastFrameA = self.frames[frameIndex - 1]
        frameTime = self.frames[frameIndex]
        percent = 1.0 - (time - frameTime) / (self.frames[frameIndex + COLOR_LAST_FRAME_TIME] - frameTime)
        if percent < 0.0:
            percent = 0.0
        if percent > 1.0:
            percent = 1.0
        percent = self.getCurvePercent(frameIndex / 5 - 1, percent)

        r = lastFrameR (self.frames[frameIndex + COLOR_FRAME_R] - lastFrameR) * percent
        g = lastFrameG (self.frames[frameIndex + COLOR_FRAME_G] - lastFrameG) * percent
        b = lastFrameB (self.frames[frameIndex + COLOR_FRAME_B] - lastFrameB) * percent
        a = lastFrameA (self.frames[frameIndex + COLOR_FRAME_A] - lastFrameA) * percent
        if alpha < 1.0:
            slot.r += (r - slot.r) * alpha
            slot.g += (g - slot.g) * alpha
            slot.b += (b - slot.b) * alpha
            slot.a += (a - slot.a) * alpha
        else:
            slot.r = r
            slot.g = g
            slot.b = b
            slot.a = a

        skeleton.slots[self.slotIndex] = slot
        return 


class AttachmentTimeline(Timeline):
    def __init__(self, keyframeCount):
        super(AttachmentTimeline, self).__init__(keyframeCount)
        self.framesLength = keyframeCount
        self.frames = [0.0] * keyframeCount
        self.attachmentNames = [None] * keyframeCount
        self.slotIndex = 0

    
    def getDuration(self):
        return self.frames[self.framesLength - 1]


    def getKeyframeCount(self):
        return self.framesLength


    def setKeyframe(self, keyframeIndex, time, attachmentName):
        self.frames[keyframeIndex] = time
        self.attachmentNames[keyframeIndex] = None if len(attachmentName) == 0 else attachmentName


    def apply(self, skeleton, time, alpha):
        if time < self.frames[0]: # Time is before first frame
            return 

        frameIndex = 0
        if time >= self.frames[self.framesLength - 1]: # Time is after last frame.
            frameIndex = self.framesLength - 1
        else:
            frameIndex = binarySearch(self.frames, self.framesLength, time, 1) - 1
        attachmentName = self.attachmentNames[frameIndex]
        skeleton.slots[self.slotIndex].setAttachment(skeleton.getAttachmentByIndex(self.slotIndex, attachmentName) if attachmentName else None)
        
        return 



