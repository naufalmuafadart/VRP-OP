from application.domain.repository.AlgorithmRepository import AlgorithmRepository
import datetime
import random
import numpy as np

class Individual:
    def __init__(self, size, fitness_function):
        self.size = size
        self.fitness = None
        self.fitness_function = fitness_function
        self.vector = []

    def generate_random_vector(self):
        self.vector = [round(random.random() * 10, 5) for _ in range(self.size)]
        self.fitness = self.fitness_function(self.vector)

    def set_vector(self, vector):
        self.vector = vector
        self.fitness = self.fitness_function(self.vector)

class SAAlgorithmRepository(AlgorithmRepository):
    def prepare(self, sol_size, fitness_function, is_maximizing):
        self.T = 1
        self.stopping_T = 0.2
        self.cooling_rate = 0.5
        self.sol_size = sol_size
        self.fitness_function = fitness_function
        self.is_maximizing = is_maximizing

    def is_a_better_than_b(self, a, b):
        return (self.is_maximizing and a > b) or (not self.is_maximizing and a < b)

    def run(self):
        # print('Starting SA')
        start_time = datetime.datetime.now()

        # create initial solution
        solution = Individual(self.sol_size, self.fitness_function)
        solution.generate_random_vector()

        while self.T >= self.stopping_T:
            # print('T: ', self.T)
            # create new solution
            new_solution = Individual(self.sol_size, self.fitness_function)
            new_solution.generate_random_vector()

            if self.is_a_better_than_b(solution.fitness, new_solution.fitness):
                solution = new_solution
            else:
                prob = np.exp(-np.abs(solution.fitness - new_solution.fitness)/self.T)  # probabilitas individu baru akan terpilih
                if random.random() <= prob:
                    solution.set_vector(new_solution.vector)  # ganti solusi saat ini dengan solusi baru

            self.T = self.T * self.cooling_rate

        end_time = datetime.datetime.now()
        # print('Duration, ', end_time - start_time)
        vectors = [solution.vector]
        return vectors[0]
