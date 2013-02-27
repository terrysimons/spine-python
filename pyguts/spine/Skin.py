class Key(object):
    def __init__(self, slotIndex, name):
        super(Key, self).__init__()
        self.slotIndex = slotIndex
        self.name = name
    
    def __lt__(self, key):
        if self.slotIndex == key.slotIndex:
            return self.name < key.name
        return self.slotIndex < key.slotIndex

    def __hash__(self):
        return hash((self.slotIndex, self.name))

    def __eq__(self, other):
        return (self.slotIndex, self.name) == (other.slotIndex, other.name)


class Skin(object):
    def __init__(self, name):
        self.name = name
        self.attachments = {}


    def addAttachment(self, slotIndex, name, attachment):
        key = Key(slotIndex=slotIndex, name=name)
        self.attachments[key] = attachment

    
    def getAttachment(self, slotIndex, name):
        key = Key(slotIndex=slotIndex, name=name)
        if key in self.attachments:
            return self.attachments[key]
        return None

            
    def attachAll(self, skeleton, oldSkin):
        for key, attachment in self.attachments.iteritems():
            slot = skeleton.slots[key.slotIndex]
            print("NB: This might not work right.")
            if slot.attachment == attachment:
                newAttachment = self.getAttachment(key.slotIndex, key.name)
                if newAttachment:
                    slot.setAttachment(newAttachment)
            
