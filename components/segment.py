class Segment:
    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance


    def __str__(self):
        return '[%s, %s]' % (self.direction, self.distance)
