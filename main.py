from src.parser import load_jssp_instance


number_of_jobs, number_of_machines, jobs = load_jssp_instance(
    "data/la01.txt"
)

print(f"Jobs: {number_of_jobs}")
print(f"Machines: {number_of_machines}")

print("\nJob 0:")
for operation_id, operation in enumerate(jobs[0]):
    machine_id, processing_time = operation

    print(
        f"Operation {operation_id}: "
        f"Machine {machine_id}, "
        f"Processing time {processing_time}"
    )