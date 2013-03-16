import Enum

AttachmentType = Enum.enum(region=0, 
                           regionSequence=1)

class AttachmentLoader(object):
    def __init__(self):
        super(AttachmentLoader, self).__init__()

    def newAttachment(type, name):
        pass

