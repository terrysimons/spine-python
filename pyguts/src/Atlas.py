import os


import pygame


import spine

class AtlasPage(spine.AtlasPage):
    def __init__(self):
        super(AtlasPage, self).__init__()
        self.texture = None


class AtlasRegion(spine.AtlasRegion):
    def __init__(self):
        super(AtlasRegion, self).__init__()
        self.page = None


class Atlas(spine.Atlas):
    def __init__(self, file):
        super(Atlas, self).__init__()
        super(Atlas, self).loadWithFile(file)


    def newAtlasPage(self, name):
        page = AtlasPage()
        page.texture = pygame.image.load(os.path.realpath(name)).convert_alpha()
        return page


    def newAtlasRegion(self, page):
        region = AtlasRegion()
        region.page = page
        return region


    def findRegion(self, name):
        return super(Atlas, self).findRegion(name)
