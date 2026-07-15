#!/usr/bin/env python3
"""
Generate replicate and mean hydrogen-bond plots from assembled molecular
dynamics simulation data.

This script recursively searches for files named `q_hbond_30rep.csv`,
plots the hydrogen-bond trajectories of all available simulation replicates,
computes the mean hydrogen-bond profile, and saves both a publication-quality
figure and the corresponding mean values.

Outputs (written to the same directory as the input CSV):
    q_hbond_30rep_plot.png
    q_hbond_30rep_mean.csv

Usage:
    python plot_q_hbond_reps.py

Requirements:
    Python 3
    pandas
    NumPy
    matplotlib
"""

import os, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_one(csv_path):
    out_dir = os.path.dirname(csv_path)
    df = pd.read_csv(csv_path)

    # Be tolerant to column names/case
    first_col = df.columns[0]
    if first_col.lower() != "frame":
        df = df.rename(columns={first_col: "Frame"})

    # Ensure numeric
    df["Frame"] = pd.to_numeric(df["Frame"], errors="coerce")
    rep_cols = [c for c in df.columns if c != "Frame"]
    df[rep_cols] = df[rep_cols].apply(pd.to_numeric, errors="coerce")

    # Sort by frame and drop rows with NaN frame
    df = df.dropna(subset=["Frame"]).sort_values("Frame").reset_index(drop=True)

    # Compute average across available replicates per frame
    df["MeanHBond"] = df[rep_cols].mean(axis=1, skipna=True)

    # Derive a title from the directory structure
    parts = os.path.normpath(csv_path).split(os.sep)
    title_bits = []
    if "NEUTRAL" in parts:
        i = parts.index("NEUTRAL")
        if i - 1 >= 0:
            title_bits.append(parts[i - 1])
        title_bits.append(parts[i])
    else:
        title_bits.append(os.path.basename(out_dir))
    title = " / ".join(title_bits) + " — q_hbond"

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot individual replicates
    for c in rep_cols:
        ax.plot(df["Frame"], df[c], alpha=0.25, linewidth=0.8)

    # Plot mean trajectory
    ax.plot(df["Frame"], df["MeanHBond"], linewidth=2.5)

    ax.set_xlabel("Frame")
    ax.set_ylabel("H-bond (binary)")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)

    png_path = os.path.join(out_dir, "q_hbond_30rep_plot.png")
    fig.tight_layout()
    fig.savefig(png_path, dpi=300)
    plt.close(fig)

    mean_csv = os.path.join(out_dir, "q_hbond_30rep_mean.csv")
    df[["Frame", "MeanHBond"]].to_csv(mean_csv, index=False)

    print(f"Saved: {png_path}")
    print(f"Saved: {mean_csv}")

def main():
    files = glob.glob("**/q_hbond_30rep.csv", recursive=True)

    if not files:
        print("No q_hbond_30rep.csv files found under the current directory.")
        return

    print(f"Found {len(files)} file(s).")

    for f in files:
        try:
            print(f"Processing: {f}")
            plot_one(f)
        except Exception as e:
            print(f"Skipped {f}: {e}")

if __name__ == "__main__":
    main()
