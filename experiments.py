import csv
import random
import statistics
import time
from pathlib import Path

from src.parser import load_jssp_instance
from src.ga import run_genetic_algorithm


RESULTS_DIR = Path("results")

SUMMARY_FILE = RESULTS_DIR / "experiment_summary.csv"
RUNS_FILE = RESULTS_DIR / "run_results.csv"


instances = [
    {
        "name": "la01",
        "category": "Small",
        "path": "data/la01.txt"
    },
    {
        "name": "la02",
        "category": "Small",
        "path": "data/la02.txt"
    },
    {
        "name": "la16",
        "category": "Medium",
        "path": "data/la16.txt"
    },
    {
        "name": "la17",
        "category": "Medium",
        "path": "data/la17.txt"
    },
    {
        "name": "la31",
        "category": "Large",
        "path": "data/la31.txt"
    },
    {
        "name": "la32",
        "category": "Large",
        "path": "data/la32.txt"
    }
]


parameter_sets = [
    {
        "name": "Set A",
        "population_size": 30,
        "generations": 100,
        "crossover_probability": 0.7,
        "mutation_probability": 0.05
    },
    {
        "name": "Set B",
        "population_size": 50,
        "generations": 200,
        "crossover_probability": 0.8,
        "mutation_probability": 0.10
    },
    {
        "name": "Set C",
        "population_size": 100,
        "generations": 300,
        "crossover_probability": 0.9,
        "mutation_probability": 0.20
    }
]


def find_convergence_generation(best_history):
    """
    Return the first generation where the final best Cmax
    was reached.
    """

    final_best = best_history[-1]

    for generation, makespan in enumerate(best_history):
        if makespan == final_best:
            return generation

    return len(best_history) - 1


def save_csv(file_path, rows, fieldnames):
    """
    Save a list of dictionaries to a CSV file.
    """

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)


def run_experiment(
    instance,
    parameters,
    runs
):
    _, number_of_machines, jobs = (
        load_jssp_instance(instance["path"])
    )

    makespans = []
    execution_times = []
    convergence_generations = []

    run_results = []

    for run_number in range(1, runs + 1):
        # Use a reproducible seed.
        seed = run_number
        random.seed(seed)

        start_time = time.perf_counter()

        _, best_makespan, best_history = (
            run_genetic_algorithm(
                jobs,
                number_of_machines,
                parameters["population_size"],
                parameters["generations"],
                parameters[
                    "crossover_probability"
                ],
                parameters[
                    "mutation_probability"
                ]
            )
        )

        execution_time = (
            time.perf_counter() - start_time
        )

        convergence_generation = (
            find_convergence_generation(
                best_history
            )
        )

        makespans.append(best_makespan)
        execution_times.append(
            execution_time
        )
        convergence_generations.append(
            convergence_generation
        )

        run_results.append({
            "instance": instance["name"],
            "category": instance["category"],
            "parameter_set": parameters["name"],
            "run": run_number,
            "seed": seed,
            "best_cmax": best_makespan,
            "execution_time": round(
                execution_time,
                4
            ),
            "convergence_generation":
                convergence_generation
        })

    summary = {
        "instance": instance["name"],
        "category": instance["category"],
        "parameter_set": parameters["name"],
        "runs": runs,
        "population_size":
            parameters["population_size"],
        "generations":
            parameters["generations"],
        "crossover_probability":
            parameters["crossover_probability"],
        "mutation_probability":
            parameters["mutation_probability"],
        "best_cmax": min(makespans),
        "worst_cmax": max(makespans),
        "average_cmax": round(
            statistics.mean(makespans),
            2
        ),
        "standard_deviation": round(
            statistics.stdev(makespans),
            2
        ),
        "average_execution_time": round(
            statistics.mean(execution_times),
            4
        ),
        "average_convergence_generation": round(
            statistics.mean(
                convergence_generations
            ),
            2
        )
    }

    return summary, run_results


def main():
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    all_summaries = []
    all_run_results = []

    runs = 10

    total_experiments = (
        len(instances)
        * len(parameter_sets)
    )

    experiment_number = 0

    for instance in instances:
        for parameters in parameter_sets:
            experiment_number += 1

            print("\n" + "=" * 60)

            print(
                f"Experiment "
                f"{experiment_number}/"
                f"{total_experiments}"
            )

            print(
                f"Instance: "
                f"{instance['name']} "
                f"({instance['category']})"
            )

            print(
                f"Parameter Set: "
                f"{parameters['name']}"
            )

            print(
                f"Population: "
                f"{parameters['population_size']}"
            )

            print(
                f"Generations: "
                f"{parameters['generations']}"
            )

            print("Running...")

            summary, run_results = (
                run_experiment(
                    instance,
                    parameters,
                    runs
                )
            )

            all_summaries.append(summary)
            all_run_results.extend(
                run_results
            )

            print(
                f"Best Cmax: "
                f"{summary['best_cmax']}"
            )

            print(
                f"Average Cmax: "
                f"{summary['average_cmax']}"
            )

            print(
                f"Std Dev: "
                f"{summary['standard_deviation']}"
            )

            print(
                f"Average Time: "
                f"{summary['average_execution_time']}s"
            )

            # Save after every experiment so completed
            # results are not lost.
            save_csv(
                SUMMARY_FILE,
                all_summaries,
                [
                    "instance",
                    "category",
                    "parameter_set",
                    "runs",
                    "population_size",
                    "generations",
                    "crossover_probability",
                    "mutation_probability",
                    "best_cmax",
                    "worst_cmax",
                    "average_cmax",
                    "standard_deviation",
                    "average_execution_time",
                    "average_convergence_generation"
                ]
            )

            save_csv(
                RUNS_FILE,
                all_run_results,
                [
                    "instance",
                    "category",
                    "parameter_set",
                    "run",
                    "seed",
                    "best_cmax",
                    "execution_time",
                    "convergence_generation"
                ]
            )

    print("\n" + "=" * 60)
    print("All experiments completed.")

    print(
        f"Summary saved to: "
        f"{SUMMARY_FILE}"
    )

    print(
        f"Individual runs saved to: "
        f"{RUNS_FILE}"
    )


if __name__ == "__main__":
    main()