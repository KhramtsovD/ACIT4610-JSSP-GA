def find_earliest_start(
    machine_schedule,
    job_ready_time,
    processing_time
):
    """
    Find the earliest feasible start time for an operation.

    The operation must:
    - start after its previous job operation has finished
    - not overlap with operations already scheduled on the machine
    """

    start_time = job_ready_time

    for scheduled_operation in machine_schedule:
        # Check whether the operation fits before
        # the next scheduled operation.
        if (
            start_time + processing_time
            <= scheduled_operation["start"]
        ):
            return start_time

        # Otherwise move past this scheduled operation.
        start_time = max(
            start_time,
            scheduled_operation["end"]
        )

    return start_time


def decode_schedule(jobs, chromosome, number_of_machines):
    number_of_jobs = len(jobs)

    # Next unscheduled operation for every job.
    next_operation = [0] * number_of_jobs

    # Earliest time each job can continue.
    job_ready_time = [0] * number_of_jobs

    # Operations already placed on every machine.
    machine_schedules = [
        []
        for _ in range(number_of_machines)
    ]

    schedule = []

    for job_id in chromosome:
        operation_id = next_operation[job_id]

        machine_id, processing_time = (
            jobs[job_id][operation_id]
        )

        start_time = find_earliest_start(
            machine_schedules[machine_id],
            job_ready_time[job_id],
            processing_time
        )

        end_time = start_time + processing_time

        operation = {
            "job": job_id,
            "operation": operation_id,
            "machine": machine_id,
            "start": start_time,
            "end": end_time,
            "processing_time": processing_time
        }

        schedule.append(operation)

        machine_schedules[machine_id].append(operation)

        machine_schedules[machine_id].sort(
            key=lambda item: item["start"]
        )

        job_ready_time[job_id] = end_time

        next_operation[job_id] += 1

    makespan = max(job_ready_time)

    return schedule, makespan