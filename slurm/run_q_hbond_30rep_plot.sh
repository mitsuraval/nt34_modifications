#!/bin/bash
#
# Submit a SLURM job to generate replicate and mean hydrogen-bond plots
# from assembled molecular dynamics simulation data.
#
# Before running:
#   1. Modify the SLURM directives as needed for your HPC system.
#   2. Activate the appropriate Python environment.
#   3. Run this script from the directory containing
#      plot_q_hbond_reps.py.

#SBATCH --job-name=qhbond_plot
#SBATCH --output=qhbond_plot_%j.out
#SBATCH --error=qhbond_plot_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=<partition_name>
#SBATCH --mem=2G
#SBATCH --time=02:00:00

set -euo pipefail

# Activate Conda environment (adjust if necessary)
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
    conda activate rnaenv || true
fi

# Optional: load Python through your cluster's module system
# module purge
# module load python/3.12.0

# Generate replicate plots and mean hydrogen-bond trajectories
python3 plot_q_hbond_reps.py
