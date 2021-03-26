import random
import time
import statistics
import matplotlib.pyplot as plt
from PIL import Image
from config import *
from genetic_algoritm import *
from helpers import *
from gui import *


if __name__ == '__main__':
    # Seed random to test algorithm
    # random.seed(129)

    random_algorithm_dict = {
        'best': [],
        'worst': [],
        'std': [],
        'avg': []
    }
    genetic_algorithm_dict = {
        'best': [],
        'worst': [],
        'avg': [],
        'std': [],
    }

    # Read file and get size of the map
    (field_width, field_height), coordinates = read_data(FILENAME)

    # Set field width and height to make fitness calculations correct
    Individual.f_width = field_width
    Individual.f_height = field_height

    x_axis = EPOCHES // 2
    exec_start_time = time.time()
    epoches_exec_time = None

    g_population = initial_population(coordinates)

    for ind in g_population:
        ind.calculate_fitness_score()

    for j in range(EPOCHES):
        if TURN_ON_RANDOM_ALGORITHM:
            r_population = initial_population(coordinates)
            for ind in r_population:
                ind.calculate_fitness_score()

        if TURN_ON_GENETIC_ALGORITHM:
            new_population = []

            for i in range(len(g_population)):
                a = tournament_selection(g_population, k=SELECTION_SIZE) if SELECTION_TYPE_PARENT1 == 1 else fitness_proportionate_selection(g_population, k=SELECTION_SIZE)
                b = tournament_selection(g_population, k=SELECTION_SIZE) if SELECTION_TYPE_PARENT1 == 1 else fitness_proportionate_selection(g_population, k=SELECTION_SIZE)
                
                child = single_point_crossover(a, b)
                mutate(child)

                child.calculate_fitness_score()
                new_population.append(child)

            g_population = list(new_population)
            new_population = []

        if j % (EPOCHES // x_axis) == 0:
            if TURN_ON_RANDOM_ALGORITHM:
                random_algorithm_dict['avg'].append(sum(x.fitness_score for x in r_population) / POPULATION_SIZE)
                random_algorithm_dict['best'].append(min(x.fitness_score for x in r_population))
                random_algorithm_dict['worst'].append(max(x.fitness_score for x in r_population))
                random_algorithm_dict['std'].append(statistics.stdev(x.fitness_score for x in r_population))

            if TURN_ON_GENETIC_ALGORITHM:
                genetic_algorithm_dict['avg'].append(sum(x.fitness_score for x in g_population) / POPULATION_SIZE)
                genetic_algorithm_dict['best'].append(min(x.fitness_score for x in g_population))
                genetic_algorithm_dict['worst'].append(max(x.fitness_score for x in g_population))
                genetic_algorithm_dict['std'].append(statistics.stdev(x.fitness_score for x in g_population))

        if j % (EPOCHES // 10) == 0: 
            if epoches_exec_time is None:
                epoches_exec_time = exec_start_time
            print('Epoch: ', j, 'Time: ', time.time() - epoches_exec_time)
            epoches_exec_time = time.time()

    # Print time execution
    print('Time: ', time.time() - exec_start_time)

    # Draw plots with analysis
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 10))

    x_axis = list(x * EPOCHES // x_axis for x in range(x_axis))
    if TURN_ON_RANDOM_ALGORITHM:
        ax1.set_title('Random algorithm')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Random score')
        ax1.plot(x_axis, random_algorithm_dict['best'], color='green', label='Best')
        ax1.plot(x_axis, random_algorithm_dict['worst'], color='red', label='Worst')
        ax1.plot(x_axis, random_algorithm_dict['avg'], color='blue', label='Average')
        ax1.legend()

    if TURN_ON_GENETIC_ALGORITHM:
        ax2.set_title('Genetic algorithm')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Fitness score')
        ax2.plot(x_axis, genetic_algorithm_dict['best'], color='green', label='Best')
        ax2.plot(x_axis, genetic_algorithm_dict['worst'], color='red', label='Worst')
        ax2.plot(x_axis, genetic_algorithm_dict['avg'], color='blue', label='Average')
        ax2.legend()

    plt.savefig('model.png')
    plt.show()

    gui = GUI(field_width, field_height)
    gui.draw_field()
    gui.draw_individual(min(g_population, key=lambda x: x.fitness_score))
    gui.draw_coords(coordinates)

    
    for i, ind in enumerate(g_population):
        gui.w.delete('all')

        gui.draw_field()
        gui.draw_individual(ind)
        gui.draw_coords(coordinates)

        if SAVE_IMAGES:
            filename = f'models/{i}_ind'
            # FIXME: Remove .ps files
            gui.w.postscript(file=filename + '.ps', colormode='color')
            img = Image.open(filename + '.ps')
            img.save(filename + '.png', 'png')

    gui.root.mainloop()