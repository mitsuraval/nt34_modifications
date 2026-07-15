from itertools import chain

# ---------------------------------------------------------------------
# This script generates cpptraj input files for hydrogen-bond analysis
# of molecular dynamics trajectories and creates a SLURM submission script.
#
# Before running:
#   1. Set the paths below to your simulation directories.
#   2. Adjust the replicate range if necessary.
# ---------------------------------------------------------------------

#################
# JOB VARIABLES #
#################

start_expt = 1
end_expt = 30

# Directory containing NEUTRAL_1, NEUTRAL_2, ... NEUTRAL_30
data_dir = "/path/to/simulations/NEUTRAL_"

# Solvated topology (.prmtop) file
prmtop_path = "/path/to/topology.prmtop"

# Directory containing trajectory files
trajin_path = "/path/to/trajectories/NEUTRAL_"

# Number of nanoseconds discarded before analysis
cutoff = 20

# Simulation output frequency
frames_per_ns = 100

####################
# CALCULATE CUTOFF #
####################

stable_cutoff = str(frames_per_ns * cutoff)

###############
# WRITE FILES #
###############

outfile = open("run_cpptraj_3a_avgHbond.sh", "w")
outfile.write(
    "#!/bin/bash\n"
    "#SBATCH --job-name=\"3a_avgHbond_CPU\"\n"
    "#SBATCH --output=out_3a_avgHbond\n"
    "#SBATCH --error=err_3a_avgHbond\n"
    "#SBATCH --ntasks=1\n"
    "#SBATCH --cpus-per-task=4\n"
    "#SBATCH -N 1\n"
    "#SBATCH --partition=exx96\n"
    "#SBATCH -B 1:1:1\n\n"

    "# Environment\n"
    "export PATH=/share/apps/CENTOS7/gcc/6.5.0/bin:$PATH\n"
    "export LD_LIBRARY_PATH=/share/apps/CENTOS7/gcc/6.5.0/lib64:$LD_LIBRARY_PATH\n\n"

    "### AMBER22 ###\n"
    "source /share/apps/CENTOS7/amber/amber22/amber.sh\n\n"

    "### Run cpptraj ###\n\n"

    "for i in {" + str(start_expt) + ".." + str(end_expt) + "}; do\n"
    "    cd " + data_dir + "$i/\n"
    "    cpptraj -i cpptraj_3a_avgHbond.in\n"
    "done\n"
)
outfile.close()

for i in range(start_expt, end_expt + 1):

    outfile = open(data_dir + str(i) + "/cpptraj_3a_avgHbond.in", "w")

    outfile.write(
        "\n"
        "parm " + prmtop_path + " [modi3]\n"
        "trajin " + trajin_path + str(i) + "/mdcrd_nd_" + str(i) + " parm [modi3]\n"
        "autoimage\n\n"

        "# Anticodon position 3 / codon position 3 hydrogen bonding\n"
        "hbond nhb_AVE_408_all_425_all :408|:425 out qhbond.dat\n"
    )

    outfile.close()
