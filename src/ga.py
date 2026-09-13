import random

from src.operators import (
    create_random_chromosome,
    job_based_crossover,
    swap_mutation
)
from src.decoder import decode_schedule


def create_population(jobs, population_size):
    population = []

    for _ in range(population_size):
        chromosome = create_random_chromosome(jobs)
        population.append(chromosome)

    return population


def evaluate_population(
    population,
    jobs,
    number_of_machines
):
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


def tournament_selection(
    evaluated_population,
    tournament_size=3
):
    competitors = random.sample(
        evaluated_population,
        tournament_size
    )

    winner = min(
        competitors,
        key=lambda individual: individual["makespan"]
    )

    return winner["chromosome"].copy()


def create_next_generation(
    evaluated_population,
    jobs,
    crossover_probability,
    mutation_probability,
    elitism_count=1
):
    population_size = len(evaluated_population)
    number_of_jobs = len(jobs)

    new_population = []

    # Sort population from best to worst.
    sorted_population = sorted(
        evaluated_population,
        key=lambda individual: individual["makespan"]
    )

    # Elitism: keep the best chromosome(s).
    for individual in sorted_population[:elitism_count]:
        new_population.append(
            individual["chromosome"].copy()
        )

    # Create offspring until the new population is full.
    while len(new_population) < population_size:
        parent1 = tournament_selection(
            evaluated_population
        )

        parent2 = tournament_selection(
            evaluated_population
        )

        # Apply crossover according to its probability.
        if random.random() < crossover_probability:
            child1, child2 = job_based_crossover(
                parent1,
                parent2,
                number_of_jobs
            )
        else:
            child1 = parent1.copy()
            child2 = parent2.copy()

        # Apply mutation independently to each child.
        if random.random() < mutation_probability:
            child1 = swap_mutation(child1)

        if random.random() < mutation_probability:
            child2 = swap_mutation(child2)

        new_population.append(child1)

        if len(new_population) < population_size:
            new_population.append(child2)

    return new_population


def run_genetic_algorithm(
    jobs,
    number_of_machines,
    population_size,
    generations,
    crossover_probability,
    mutation_probability
):
    # Create the initial population.
    population = create_population(
        jobs,
        population_size
    )

    # Evaluate Generation 0.
    evaluated_population = evaluate_population(
        population,
        jobs,
        number_of_machines
    )

    best_individual = min(
        evaluated_population,
        key=lambda individual: individual["makespan"]
    )

    best_chromosome = (
        best_individual["chromosome"].copy()
    )

    best_makespan = best_individual["makespan"]

    # Store the best Cmax found after each generation.
    best_history = [best_makespan]

    # Evolutionary loop.
    for generation in range(1, generations + 1):
        population = create_next_generation(
            evaluated_population,
            jobs,
            crossover_probability,
            mutation_probability
        )

        evaluated_population = evaluate_population(
            population,
            jobs,
            number_of_machines
        )

        current_best = min(
            evaluated_population,
            key=lambda individual: individual["makespan"]
        )

        if current_best["makespan"] < best_makespan:
            best_makespan = current_best["makespan"]

            best_chromosome = (
                current_best["chromosome"].copy()
            )

        best_history.append(best_makespan)

    return (
        best_chromosome,
        best_makespan,
        best_history
    )