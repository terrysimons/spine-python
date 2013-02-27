import math

import Timeline

class Animation(object):
    def __init__(self, timelines, duration):
        self.timelines = timelines
        self.duration = duration

    def apply(self, skeleton, time, loop):
        if not skeleton:
            raise Exception('skeleton cannot be null.')
        
        if loop and self.duration:
            time = math.fmod(time, self.duration)

        for timeline in self.timelines:
            timeline.apply(skeleton, time, 1)



