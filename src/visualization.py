import matplotlib.pyplot as plt


def plot_gantt(
    schedule,
    number_of_machines,
    title="JSSP Gantt Chart"
):
    """
    Display a Gantt chart for a decoded JSSP schedule.
    """

    fig, ax = plt.subplots(figsize=(12, 6))

    for operation in schedule:
        machine_id = operation["machine"]
        job_id = operation["job"]
        operation_id = operation["operation"]

        start_time = operation["start"]
        processing_time = operation["processing_time"]

        ax.barh(
            machine_id,
            processing_time,
            left=start_time
        )

        ax.text(
            start_time + processing_time / 2,
            machine_id,
            f"J{job_id}O{operation_id}",
            ha="center",
            va="center",
            fontsize=8
        )

    ax.set_yticks(
        range(number_of_machines)
    )

    ax.set_yticklabels(
        [
            f"Machine {machine_id}"
            for machine_id in range(number_of_machines)
        ]
    )

    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")
    ax.set_title(title)

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.4
    )

    plt.tight_layout()
    plt.show()