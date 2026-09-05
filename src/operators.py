import random


def create_random_chromosome(jobs):
    chromosome = []

    for job_id, operations in enumerate(jobs):
        chromosome.extend([job_id] * len(operations))

    random.shuffle(chromosome)

    return chromosome