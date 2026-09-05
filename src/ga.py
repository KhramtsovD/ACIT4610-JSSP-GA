from src.operators import create_random_chromosome
from src.decoder import decode_schedule


def create_population(jobs, population_size):
    population = []

    for _ in range(population_size):
        chromosome = create_random_chromosome(jobs)
        population.append(chromosome)

    return population


def evaluate_population(population, jobs, number_of_machines):
    evaluated_population = []

    for chromosome in population:
        schedule, makespan = decode_schedule(
            jobs,
            chromosome,
            number_of_machines
        )

        evaluated_population.append({
            "chromosome": chromosome,
            "makespan": makespan
        })

    return evaluated_population