# ACIT4610-JSSP-GA

Job Shop Scheduling Problem using a Genetic Algorithm for ACIT4610.

The objective of the project is to minimize the makespan (Cmax) of a Job Shop Scheduling Problem (JSSP).

## Benchmark Instances

The project uses six Lawrence benchmark instances from JSPLib:

- Small: la01, la02
- Medium: la16, la17
- Large: la31, la32

The benchmark files are stored in the `data/` directory.

## Installation

Clone the repository:

```bash
git clone https://github.com/KhramtsovD/ACIT4610-JSSP-GA.git
cd ACIT4610-JSSP-GA
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Program

Run the Genetic Algorithm on the example benchmark instance:

```bash
python main.py
```

The program prints:

- GA parameters
- Best chromosome
- Operation start and finish times
- Best makespan (Cmax)

It also displays a Gantt chart of the best decoded schedule.

Run all experiments:

```bash
python experiments.py
```

The experiment script tests all six benchmark instances using three GA parameter sets and 10 independent runs for each experiment.

The results are saved in the `results/` directory.

## Chromosome Representation

The implementation uses an operation-based chromosome representation.

Each gene contains a job ID.

Example:

```text
[0, 1, 0, 1]
```

The first occurrence of a job ID represents the first operation of that job, the second occurrence represents the second operation, and so on.

For example:

```text
Job 0 Operation 0
Job 1 Operation 0
Job 0 Operation 1
Job 1 Operation 1
```

## Schedule Building Algorithm

The decoder converts each chromosome into a feasible JSSP schedule before the makespan is evaluated.

For each operation, the decoder:

1. Selects the next operation of the job.
2. Uses the machine specified by the benchmark instance.
3. Respects the precedence order of operations within the job.
4. Finds the earliest valid idle time slot on the required machine.
5. Prevents operations on the same machine from overlapping.
6. Calculates the start and finish time of the operation.

After all operations are scheduled, the makespan (Cmax) is calculated from the completion time of the final schedule.

## Genetic Algorithm

The Genetic Algorithm uses:

- Random population initialization
- Tournament selection
- Job-based crossover
- Swap mutation
- Elitism
- Makespan minimization
- A fixed number of generations as the termination condition

The crossover operator preserves the required number of occurrences of each job ID.

The swap mutation operator exchanges two positions in a chromosome without changing the number of operations belonging to each job.

## Experiment Metrics

For each experiment, the program calculates:

- Best Cmax
- Worst Cmax
- Average Cmax
- Standard deviation
- Execution time
- Convergence generation