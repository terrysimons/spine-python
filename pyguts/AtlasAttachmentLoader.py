import spine

import RegionAttachment

class AtlasAttachmentLoader(spine.AttachmentLoader.AttachmentLoader):
    def __init__(self, atlas):
        self.atlas = atlas
        
    def newAttachment(self, type, name):
        if type == spine.AttachmentLoader.AttachmentType.region:
            region = self.atlas.findRegion(name)
            if not region:
                raise Exception("Atlas region not found: %s" % name)
            return RegionAttachment.RegionAttachment(region)
        else:
            raise Exception('Unknown attachment type: %s' % type)

    
