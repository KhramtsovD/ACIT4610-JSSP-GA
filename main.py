from src.parser import load_jssp_instance
from src.decoder import decode_schedule
from src.ga import run_genetic_algorithm
from src.visualization import plot_gantt


# Load JSSP instance.
number_of_jobs, number_of_machines, jobs = load_jssp_instance(
    "data/la01.txt"
)

print(f"Jobs: {number_of_jobs}")
print(f"Machines: {number_of_machines}")


# GA parameters.
population_size = 50
generations = 200
crossover_probability = 0.8
mutation_probability = 0.1


print("\nGA parameters:")
print(f"Population size: {population_size}")
print(f"Generations: {generations}")
print(f"Crossover probability: {crossover_probability}")
print(f"Mutation probability: {mutation_probability}")


# Run the Genetic Algorithm.
best_chromosome, best_makespan, best_history = (
    run_genetic_algorithm(
        jobs,
        number_of_machines,
        population_size,
        generations,
        crossover_probability,
        mutation_probability
    )
)


# Decode the best chromosome.
best_schedule, _ = decode_schedule(
    jobs,
    best_chromosome,
    number_of_machines
)


print("\nResults:")
print(f"Initial best Cmax: {best_history[0]}")
print(f"Final best Cmax: {best_makespan}")

print(
    f"Improvement: "
    f"{best_history[0] - best_makespan}"
)


print("\nBest chromosome:")
print(best_chromosome)


print("\nBest schedule:")

for operation in best_schedule:
    print(
        f"Job {operation['job']} "
        f"Operation {operation['operation']} "
        f"Machine {operation['machine']} "
        f"Start {operation['start']} "
        f"End {operation['end']}"
    )


# Display Gantt chart.
plot_gantt(
    best_schedule,
    number_of_machines,
    title=f"la01 - Best Schedule - Cmax {best_makespan}"
)