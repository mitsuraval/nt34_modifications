# nt34_modifications

Analysis scripts accompanying the manuscript:

**Anticodon nucleotide modifications affect translational tuning by the ribosomal CAR surface**

## Overview

This repository contains the computational analysis scripts used to investigate how post-transcriptional modifications of tRNA nucleotide 34 influence hydrogen bonding, base stacking, and communication between the ribosomal A site and the adjacent CAR interaction surface.

The workflow was developed for molecular dynamics simulations of ribosomal decoding-center subsystems performed using the AMBER molecular simulation package and analyzed with cpptraj and Python.

---

## Workflow

The analysis pipeline consists of four major steps:

1. Generate cpptraj input files for hydrogen-bond analysis.
2. Run hydrogen-bond analysis on all molecular dynamics simulation replicates.
3. Assemble replicate outputs into combined datasets.
4. Generate summary statistics and visualization of hydrogen-bond dynamics.

---

## Repository contents

### `make_cpptraj_3a_avgHbond.py`

Generates cpptraj input files and SLURM submission scripts for hydrogen-bond analysis of molecular dynamics trajectories. One cpptraj input file is created for each simulation replicate.

---

### `assemble_all_q_hbond.py`

Collects hydrogen-bond output files from all simulation replicates and combines them into a single CSV dataset for downstream statistical analysis.

Output:

- `q_hbond_30rep.csv`

---

### `plot_q_hbond_reps.py`

Plots hydrogen-bond trajectories for all replicates and calculates the mean hydrogen-bond profile across simulations.

Outputs:

- `q_hbond_30rep_plot.png`
- `q_hbond_30rep_mean.csv`

---

### `assemble_all_q.sh`

Example SLURM submission script for assembling hydrogen-bond data across all simulation directories.

---

### `run_q_hbond_30rep_plot.sh`

Example SLURM submission script for generating replicate plots and mean hydrogen-bond trajectories.

---

## Software requirements

- Python 3.12
- pandas
- NumPy
- matplotlib
- AMBER22
- cpptraj

---

## Data

The scripts are designed to analyze molecular dynamics trajectories of ribosomal decoding-center subsystems generated with AMBER22. Simulation trajectories are not included in this repository because of their size.

---

## Citation

If you use these scripts in your work, please cite:

> Raval M., Weir M.P.
> *Anticodon nucleotide modifications affect translational tuning by the ribosomal CAR surface.*

---

## License

This repository is distributed under the MIT License.
