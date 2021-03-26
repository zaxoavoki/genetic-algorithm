from config import *
import tkinter as tk
from components.individual import *


class GUI:
    def __init__(self, f_width, f_height):
        self.C_WIDTH = f_width * LINE_DIS
        self.C_HEIGHT = f_height * LINE_DIS

        self.root = tk.Tk()

        self.root.title('Genetic Algorithm')
        self.root.resizable(False, False)

        self.w = tk.Canvas(self.root, width=self.C_WIDTH, height=self.C_HEIGHT, bg="#505050")
        self.w.pack()
        self.root.update()


    def draw_individual(self, ind: Individual) -> None:
        # Draw individual by drawing all segments for ecah path
        offset = LINE_DIS / 2
        for path in ind.paths:
            x, y = path.xs * LINE_DIS, path.ys * LINE_DIS
            for segment in path.segments:
                x_gap, y_gap = 0, 0
                if segment.direction in ('U', 'D'): y_gap = LINE_DIS
                if segment.direction in ('L', 'R'): x_gap = LINE_DIS
                
                x_sign, y_sign = 1, 1
                if segment.direction == 'U': y_sign = -1
                if segment.direction == 'L': x_sign = -1

                for i in range(segment.distance):
                    self.w.create_line(x - offset, y - offset, x + x_gap * x_sign - offset, y - offset + y_sign * y_gap, fill=path.color)
                    if segment.direction == 'U': y -= LINE_DIS
                    if segment.direction == 'D': y += LINE_DIS
                    if segment.direction == 'L': x -= LINE_DIS
                    if segment.direction == 'R': x += LINE_DIS


    def draw_field(self) -> None:
        # Draw background dots
        for x in range(0, self.C_WIDTH, LINE_DIS):
            for y in range(0, self.C_HEIGHT, LINE_DIS):
                self.draw_rect(x, y, x + LINE_DIS, y + LINE_DIS, _offset=2)


    def draw_rect(self, x1, y1, x2, y2, _offset=2, color='#bbb') -> None:
        # Helper function to draw a circle
        offset = LINE_DIS / _offset
        self.w.create_oval(x1 + offset, y1 + offset, x2 - offset, y2 - offset, fill=color, outline='')


    def draw_coords(self, coordinates) -> None:
        # Draw points by their coordinates
        for x in coordinates:
            x = list(map(lambda e: (e - 1) * LINE_DIS, x))
            self.draw_rect(x[0], x[1], x[0] + LINE_DIS, x[1] + LINE_DIS, _offset=3, color='#aaa')
            self.draw_rect(x[2], x[3], x[2] + LINE_DIS, x[3] + LINE_DIS, _offset=3, color='#aaa')