import Timeline

class Animation(object):
    def __init__(self, name, timelines, duration):
        if not timelines: 
            raise Exception('Timelines cannot be None.')
        self.name = name
        self.timelines = timelines
        self.duration = duration


    def mix(self, skeleton, time, loop, alpha):
        if not skeleton:
            raise Exception('Skeleton cannot be None.')

        if loop and duration:
            time = time % duration
        if loop and self.duration:
            time = time % self.duration

        for timeline in self.timelines:
            timeline.apply(skeleton, time, alpha)


    def apply(self, skeleton, time, loop):
        if not skeleton:
            raise Exception('Skeleton cannot be None.')
        
        if loop and self.duration:
            time = time % self.duration

        for timeline in self.timelines:
            timeline.apply(skeleton, time, 1)



