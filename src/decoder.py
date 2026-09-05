def decode_schedule(jobs, chromosome, number_of_machines):
    number_of_jobs = len(jobs)

    # Which operation should be scheduled next for each job?
    next_operation = [0] * number_of_jobs

    # When is each job ready for its next operation?
    job_ready_time = [0] * number_of_jobs

    # When is each machine available?
    machine_ready_time = [0] * number_of_machines

    schedule = []

    for job_id in chromosome:
        operation_id = next_operation[job_id]

        machine_id, processing_time = jobs[job_id][operation_id]

        start_time = max(
            job_ready_time[job_id],
            machine_ready_time[machine_id]
        )

        end_time = start_time + processing_time

        schedule.append({
            "job": job_id,
            "operation": operation_id,
            "machine": machine_id,
            "start": start_time,
            "end": end_time,
            "processing_time": processing_time
        })

        job_ready_time[job_id] = end_time
        machine_ready_time[machine_id] = end_time
        next_operation[job_id] += 1

    makespan = max(job_ready_time)

    return schedule, makespan