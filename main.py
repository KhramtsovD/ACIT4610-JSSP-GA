from src.parser import load_jssp_instance
from src.decoder import decode_schedule


number_of_jobs, number_of_machines, jobs = load_jssp_instance(
    "data/la01.txt"
)

print(f"Jobs: {number_of_jobs}")
print(f"Machines: {number_of_machines}")


# Create a simple valid chromosome.
# Each job appears once for every operation it has.
chromosome = []

for operation_id in range(number_of_machines):
    for job_id in range(number_of_jobs):
        chromosome.append(job_id)


schedule, makespan = decode_schedule(
    jobs,
    chromosome,
    number_of_machines
)


print(f"\nChromosome length: {len(chromosome)}")
print(f"Makespan Cmax: {makespan}")


print("\nFirst 10 scheduled operations:")

for operation in schedule[:10]:
    print(
        f"Job {operation['job']} "
        f"Operation {operation['operation']} "
        f"Machine {operation['machine']} "
        f"Start {operation['start']} "
        f"End {operation['end']}"
    )