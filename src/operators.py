import random


def create_random_chromosome(jobs):
    chromosome = []

    for job_id, operations in enumerate(jobs):
        chromosome.extend([job_id] * len(operations))

    random.shuffle(chromosome)

    return chromosome


def job_based_crossover(
    parent1,
    parent2,
    number_of_jobs
):
    """
    Create two valid child chromosomes.

    A random subset of job IDs is preserved from one parent.
    The remaining positions are filled using the order
    from the other parent.
    """

    if number_of_jobs < 2:
        return parent1.copy(), parent2.copy()

    number_selected = random.randint(
        1,
        number_of_jobs - 1
    )

    selected_jobs = set(
        random.sample(
            range(number_of_jobs),
            number_selected
        )
    )

    child1 = [None] * len(parent1)
    child2 = [None] * len(parent2)

    # Keep selected jobs from Parent 1 in Child 1.
    for index, job_id in enumerate(parent1):
        if job_id in selected_jobs:
            child1[index] = job_id

    # Keep selected jobs from Parent 2 in Child 2.
    for index, job_id in enumerate(parent2):
        if job_id in selected_jobs:
            child2[index] = job_id

    # Take the remaining jobs from the opposite parent,
    # preserving their relative order.
    remaining_from_parent2 = [
        job_id
        for job_id in parent2
        if job_id not in selected_jobs
    ]

    remaining_from_parent1 = [
        job_id
        for job_id in parent1
        if job_id not in selected_jobs
    ]

    position = 0

    for index in range(len(child1)):
        if child1[index] is None:
            child1[index] = remaining_from_parent2[position]
            position += 1

    position = 0

    for index in range(len(child2)):
        if child2[index] is None:
            child2[index] = remaining_from_parent1[position]
            position += 1

    return child1, child2


def swap_mutation(chromosome):
    """
    Mutate a chromosome by swapping two random positions.
    """

    mutated = chromosome.copy()

    if len(mutated) < 2:
        return mutated

    index1, index2 = random.sample(
        range(len(mutated)),
        2
    )

    mutated[index1], mutated[index2] = (
        mutated[index2],
        mutated[index1]
    )

    return mutated