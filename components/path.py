import helpers


class Path:
    def __init__(self, xs=0, ys=0, xe=0, ye=0):
        self.xs = xs
        self.ys = ys
        self.xe = xe
        self.ye = ye
        self.segments = []
        self.color = helpers.get_random_hex_color()


    def __str__(self):
        return self.color + '\n(%s, %s); (%s, %s);\n' % (self.xs, self.ys, self.xe, self.ye) + '\t'.join(str(i) for i in self.segments)