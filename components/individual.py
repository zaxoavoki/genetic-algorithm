import helpers
from config import *

class Individual:
    f_width = 0
    f_height = 0

    def __init__(self):
        self.paths = []


    def __str__(self):
        return '\n'.join(str(i) for i in self.paths)


    def calculate_fitness_score(self):
        summary_distance = 0
        summary_segments = 0
        crossouts = 0
        summary_distance_outside = 0
        summary_segments_outside = 0
        
        lines = []
        for path in self.paths:
            summary_segments += len(path.segments)

            x, y = path.xs, path.ys
            for seg in path.segments:
                summary_distance += seg.distance 

                xe, ye = x, y
                if seg.direction == 'U': ye -= seg.distance
                if seg.direction == 'D': ye += seg.distance
                if seg.direction == 'L': xe -= seg.distance
                if seg.direction == 'R': xe += seg.distance
                lines.append([x, y, xe, ye, path])

                for i in range(seg.distance):
                    if x <= 0 or y <= 0 or x > self.f_width or y > self.f_height: summary_distance_outside += 1
                    if seg.direction == 'U': y -= 1
                    if seg.direction == 'D': y += 1
                    if seg.direction == 'L': x -= 1
                    if seg.direction == 'R': x += 1
                
                if x <= 0 or x > self.f_width or y <= 0 or y >= self.f_height: summary_segments_outside += 1
                else:
                    if seg.direction == 'D' and y - seg.distance <= 0: summary_segments_outside += 1
                    if seg.direction == 'U' and y + seg.distance > self.f_height: summary_segments_outside += 1
                    if seg.direction == 'R' and x - seg.distance <= 0: summary_segments_outside += 1
                    if seg.direction == 'L' and x + seg.distance > self.f_width: summary_segments_outside += 1

        for i in range(len(lines) - 1):
            for j in range(i + 1, len(lines)):
                if helpers.line_intersect(*lines[i][:-1], *lines[j][:-1]):
                    crossouts += 1

        summary_distance_outside += 1 if summary_distance_outside != 0 else 0
        self.fitness_score = sum([a * b for a, b in zip([crossouts, summary_distance, summary_segments, summary_segments_outside, summary_distance_outside], COST_FUNCTION_WEIGHTS)])
        return self.fitness_score