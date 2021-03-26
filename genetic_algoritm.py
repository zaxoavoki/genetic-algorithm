import random
import copy
from helpers import *
from config import *
from components.individual import Individual
from components.path import Path
from components.segment import Segment


def generate_random_segments(path):
    if path.xs == path.xe and path.ys == path.ye: return []

    x, y = path.xs, path.ys
    prev_direction = None
    segments = []

    for i in range(random.randint(2, MAX_SEGMENTS)):
        if x == path.xe and y == path.ye: return segments

        directions = ['U', 'D', 'L', 'R']
        # Remove previous and same direction
        if prev_direction: 
            directions.remove(prev_direction)
            directions.remove(opposite_direction(prev_direction))
        
        direction = random.choice(directions)
        distance = random.randint(1, MAX_SEGMENT_DIS)

        segment = Segment(direction, distance)
        segments.append(segment)

        if direction == 'U': y -= distance
        if direction == 'D': y += distance
        if direction == 'R': x += distance
        if direction == 'L': x -= distance

        prev_direction = direction

    # Here we need to find closest way to the end point
    # Also we have previous direction, so we cant move there
    # In this place x, y can not be equal the end point
    directions = ['U', 'D', 'L', 'R']
    directions.remove(prev_direction)
    directions.remove(opposite_direction(prev_direction))

    direction = random.choice(directions)
    distance = random.randint(1, MAX_SEGMENT_DIS)
    additional_direction = False

    if prev_direction in 'UD' and x == path.xe:
        segments.append(Segment(direction, distance))
        x += distance * (1 if direction == 'R' else -1)
        additional_direction = True
    elif prev_direction in 'LR' and y == path.ye:
        segments.append(Segment(direction, distance))
        y += distance * (1 if direction == 'D' else -1)
        additional_direction = True

    # Here we know we need to connect with two segments
    # thats why lets first find direction to 
    h_distance = path.xe - x
    v_distance = path.ye - y
    с1 = Segment('R' if h_distance > 0 else 'L', abs(h_distance))
    с2 = Segment('D' if v_distance > 0 else 'U', abs(v_distance))

    if not additional_direction: direction = prev_direction
    if direction in 'UD': 
        segments.append(с1)
        segments.append(с2)
    elif direction in 'LR': 
        segments.append(с2)
        segments.append(с1)

    return segments


def initial_population(coordinates: list) -> list:
    population = []
    for _ in range(POPULATION_SIZE):
        individual = Individual()
        for [x, y, xe, ye] in coordinates:
            path = Path(x, y, xe, ye)
            path.segments = generate_random_segments(path)
            individual.paths.append(path)
        population.append(individual)
    return population


def fitness_proportionate_selection(array: list, k=1) -> Individual:
    return min(random.choices(array, [1 / ind.fitness_score for ind in array], k=k), key=lambda x: x.fitness_score)


def tournament_selection(array: list, k=1) -> Individual:
    return min(random.sample(array, k=k), key=lambda ind: ind.fitness_score)


def single_point_crossover(parent1: Individual, parent2: Individual) -> Individual:
    if random.random() > CROSSOVER_CHANCE:  
        return copy.deepcopy(parent1 if random.random() > 0.5 else parent2)

    pivot = random.randint(1, len(parent1.paths))
    child = Individual()
    
    child.paths = copy.deepcopy(parent1.paths[:pivot]) + copy.deepcopy(parent1.paths[pivot:])
    return child

  
def mutate(ind: Individual) -> None:
    if random.random() > MUTATION_CHANCE: return

    for path in ind.paths: 
        segment = random.choice(path.segments)
        idx = path.segments.index(segment)

        # Path B
        if random.random() > 1 - MUTATION_VARIANT_B_CHANCE:
            if segment.distance > MUTATION_SEGMENT_PIVOT:
                pivot = random.randint(1, segment.distance)
                segment.distance -= pivot
                path.segments.insert(idx + 1, Segment(segment.direction, pivot))
                idx += 1
                segment = path.segments[idx]

        # Path A
        if segment.direction in 'UD':
            _dir = 'L' if random.random() >= 0.5 else 'R'
            _again_dir = 'R' if _dir == 'L' else 'L'
            _dirs = 'UD'
        else:
            _dir = 'D' if random.random() >= 0.5 else 'U'
            _again_dir = 'U' if _dir == 'D' else 'D'
            _dirs = 'LR'

        if idx > 0 and path.segments[idx - 1].direction not in _dirs:
            path.segments[idx - 1].distance += MUTATION_SEGMENT_DISTANCE * (-1 if path.segments[idx - 1].direction == _again_dir else 1)
            if path.segments[idx - 1].distance == 0:
                path.segments.pop(idx - 1)
                idx -= 1
        else:
            path.segments.insert(idx, Segment(_dir, MUTATION_SEGMENT_DISTANCE))
            idx += 1

        if idx < len(path.segments) - 1 and path.segments[idx + 1].direction not in _dirs:
            path.segments[idx + 1].distance += MUTATION_SEGMENT_DISTANCE * (-1 if path.segments[idx + 1].direction == _dir else 1)
            if path.segments[idx + 1].distance == 0: 
                path.segments.pop(idx + 1)
        else: path.segments.insert(idx + 1, Segment(_again_dir, MUTATION_SEGMENT_DISTANCE))


        i = 0
        while True:
            if i >= len(path.segments): break

            if path.segments[i].distance == 0:
                path.segments.pop(i)
                continue

            if i > 0 and path.segments[i - 1].direction == path.segments[i].direction:
                path.segments[i - 1].distance += path.segments[i].distance
                path.segments.pop(i)
                continue

            if i > 0 and path.segments[i].direction == opposite_direction(path.segments[i - 1].direction):
                if path.segments[i - 1].distance < path.segments[i].distance:
                    path.segments[i - 1].direction = path.segments[i].direction
                    path.segments[i - 1].distance = path.segments[i].distance - path.segments[i - 1].distance
                elif path.segments[i - 1].distance > path.segments[i].distance:
                    path.segments[i - 1].distance -= path.segments[i].distance
                else:
                    path.segments.pop(i)
                    i -= 1
                path.segments.pop(i)
                i -=1 

            i += 1