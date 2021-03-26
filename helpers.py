from random import randint
from shapely.geometry import LineString


def read_data(filename: str) -> (list, list):
    with open('./data/' + filename) as f:
        size = list(map(int, f.readline().split(';')))
        coordinates = [list(map(int, i.split(';'))) for i in f.readlines()]
        return size, coordinates


def line_intersect(x1, y1, x2, y2, x3, y3, x4, y4) -> bool:
    return LineString([(x1, y1), (x2, y2)]).intersects(LineString([(x3, y3), (x4, y4)]))


def get_random_hex_color():
    return '#%06X' % randint(0, 256 ** 3 - 1)


def against_direction(key: str) -> str:
    return { 'R': 'L', 'L': 'R', 'U': 'D', 'D': 'U' }.get(key)