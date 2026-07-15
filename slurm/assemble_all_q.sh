#!/bin/bash

# ----------------------------------------------------------------------
# Create and submit a SLURM job for assembling hydrogen-bond data from
# multiple molecular dynamics simulation replicates.
#
# Before running:
#   1. Set PROJECT_DIR to the directory containing the NEUTRAL folders.
#   2. Modify the SLURM directives if required for your HPC system.
# ----------------------------------------------------------------------

cat > assemble_q_all.sbatch <<'SLURM'
#!/bin/bash
#SBATCH --job-name=qhbond_all
#SBATCH --output=qhbond_all_%j.out
#SBATCH --error=qhbond_all_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=<partition_name>
#SBATCH --mem=2G
#SBATCH --time=02:00:00

# Activate Python environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate rnaenv

# Optional: load Python through your cluster's module system
module purge
module load python/3.12.0

# Root directory containing the NEUTRAL simulation folders
PROJECT_DIR="/path/to/project"

cd "${PROJECT_DIR}"

python3 assemble_all_q_hbond.py . --burnin 0
SLURM

# Submit the job
sbatch assemble_q_all.sbatch
