import itertools, collections
import os


from .. import Enum

formatNames = ('Alpha', 
               'Intensity',
               'LuminanceAlpha',
               'RGB565',
               'RGBA4444',
               'RGB888',
               'RGBA8888')

textureFiltureNames = ('Nearest',
                       'Linear',
                       'MipMap', 
                       'MipMapNearestNearest', 
                       'MipMapLinearNearest',
                       'MipMapNearestLinear', 
                       'MipMapLinearLinear')

class AtlasPage(object):
    def __init__(self):
        super(AtlasPage, self).__init__()
        self.name = None
        self.format = None
        self.minFilter = None
        self.magFilter = None
        self.uWrap = None
        self.vWrap = None


class AtlasRegion(object):
    def __init__(self):
        super(AtlasRegion, self).__init__()
        self.name = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.offsetX = 0.0
        self.offsetY = 0.0
        self.originalWidth = 0
        self.originalHeight = 0
        self.index = 0
        self.rotate = False
        self.flip = False
        self.splits = []
        self.pads = []


Format = Enum.enum(alpha=0,
                   intensity=1,
                   luminanceAlpha=2,
                   rgb565=3,
                   rgba4444=4,
                   rgb888=5,
                   rgba8888=6)


TextureFilter = Enum.enum(nearest=0,
                          linear=1,
                          mipMap=2,
                          mipMapNearestNearest=3,
                          mipMapLinearNearest=4,
                          mipMapNearestLinear=5,
                          mipMapLinearLinear=6)


TextureWrap = Enum.enum(mirroredRepeat=0,
                        clampToEdge=1,
                        repeat=2)


class Atlas(object):
    def __init__(self):
        super(Atlas, self).__init__()
        self.pages = []
        self.regions = []


    def loadWithFile(self, file):
        if not file:
            raise Exception('input cannot be null.')

        text = None

        with open(os.path.realpath(file), 'r') as fh:
            text = fh.readlines()
        self.load(text)

    def load(self, text):
        page = None
        region = None
        _page = None
        _region = {}


        for line in text:
            value = line.strip().rstrip()
            if len(value) == 0:
                _page = {}
                page = None
            if not page:
                if not ':' in value:
                    value = value.strip().rstrip()
                    _page['name'] = value
                else:
                    (key, value) = value.split(':')
                    key = key.strip().rstrip()
                    value = value.strip().rstrip()
                    if ',' in value:
                        value = value.split(',')
                        _page[key] = [x.strip().rstrip() for x in value]                    
                    else:
                        if value == 'false':
                            value = False
                        elif value == 'true':
                            value = True
                        _page[key] = value
                    if key == 'repeat':
                        page = self.newAtlasPage(_page['name'])
                        page.format = _page['format']
                        page.minFilter = _page['filter'][0]
                        page.magFilter = _page['filter'][1]
                        if _page['repeat'] == 'x':
                            page.uWrap = TextureWrap.repeat
                            page.vWrap = TextureWrap.clampToEdge
                        elif _page['repeat'] == 'y':
                            page.uWrap = TextureWrap.clampToEdge
                            page.vWrap = TextureWrap.repeat
                        elif _page['repeat'] == 'xy':
                            page.uWrap = TextureWrap.repeat
                            page.vWrap = TextureWrap.repeat
                        self.pages.append(page)
            else:
                if not ':' in value:
                    value = value.strip().rstrip()
                    _region['name'] = value
                else:
                    (key, value) = value.split(':')
                    key = key.strip().rstrip()
                    value = value.strip().rstrip()
                    if ',' in value:
                        value = value.split(',')
                        _region[key] = [int(x.strip().rstrip()) for x in value]
                    else:
                        if value == 'false':
                            value = False
                        elif value == 'true':
                            value = True
                        _region[key] = value
                    if key == 'index':
                        region = self.newAtlasRegion(page)
                        region.name = _region['name']
                        region.x = _region['xy'][0]
                        region.y = _region['xy'][1]
                        region.width = _region['size'][0]
                        region.height = _region['size'][1]
                        if 'split' in _region:
                            region.splits.append(_region['split'][0])
                            region.splits.append(_region['split'][1])
                            region.splits.append(_region['split'][2])
                            region.splits.append(_region['split'][3])
                            if 'pad' in _region:
                                region.pads.append(_region['pad'][0])
                                region.pads.append(_region['pad'][1])
                                region.pads.append(_region['pad'][2])
                                region.pads.append(_region['pad'][3])
                        region.originalWidth = _region['orig'][0]
                        region.originalHeight = _region['orig'][1]
                        region.offsetX = _region['offset'][0]
                        region.offsetY = _region['offset'][1]
                        region.index = int(_region['index'])
                        self.regions.append(region)
                        _region = {}
                        continue

    
    def findRegion(self, name):
        for region in self.regions:
            if region.name == name:
                return region
        return None

    
    def newAtlasPage(self, name):
        pass


    def newAtlasRegion(self, page):
        pass


