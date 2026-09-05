def load_jssp_instance(file_path):
    """
    Read a JSPLib Job Shop Scheduling instance.

    Returns:
        number_of_jobs
        number_of_machines
        jobs

    Each operation is stored as:
        (machine_id, processing_time)
    """

    with open(file_path, "r") as file:
        lines = [
            line.strip()
            for line in file
            if line.strip()
        ]

    # First line: number of jobs and machines
    number_of_jobs, number_of_machines = map(
        int,
        lines[0].split()
    )

    jobs = []

    # Each following line describes one job
    for job_id in range(number_of_jobs):
        values = list(
            map(int, lines[job_id + 1].split())
        )

        expected_values = number_of_machines * 2

        if len(values) != expected_values:
            raise ValueError(
                f"Job {job_id}: expected {expected_values} values, "
                f"but found {len(values)}"
            )

        operations = []

        # Read values in pairs:
        # machine, processing_time
        for i in range(0, len(values), 2):
            machine_id = values[i]
            processing_time = values[i + 1]

            operations.append(
                (machine_id, processing_time)
            )

        jobs.append(operations)

    return number_of_jobs, number_of_machines, jobs