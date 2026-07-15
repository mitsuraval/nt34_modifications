# nt34_modifications

Analysis scripts associated with the manuscript

**Anticodon nucleotide modifications affect translational tuning by the ribosomal CAR surface**

These scripts automate the analysis of molecular dynamics simulations investigating how tRNA nucleotide-34 modifications influence A-site codon recognition, CAR-site interactions, and translational tuning.

---

## Overview

The workflow consists of four major stages:

1. Generate cpptraj input files for hydrogen-bond analysis
2. Run hydrogen-bond analysis on all molecular dynamics replicates
3. Assemble replicate outputs into combined datasets
4. Visualize and summarize hydrogen-bond dynamics

---

## Repository contents

### Hydrogen-bond analysis

#### `make_cpptraj_3a_avgHbond.py`

Generates cpptraj input files and a SLURM submission script for hydrogen-bond analysis of molecular dynamics trajectories. The script automatically creates one cpptraj input file for each simulation replicate and measures hydrogen bonding between the third nucleotide of the A-site codon and the third nucleotide of the tRNA anticodon.

---

#### `assemble_all_q_hbond.py`

Collects hydrogen-bond measurements from all replicate simulations into a single CSV file. Missing replicates are automatically padded with NaN values, allowing consistent downstream analysis.


