#!/usr/bin/env python3
"""
Assemble hydrogen-bond measurements from multiple molecular dynamics
simulation replicates into a single CSV file.

This script recursively searches for directories named "NEUTRAL" and combines
the q_hbond.dat outputs from replicates NEUTRAL_1 through NEUTRAL_30 into a
single table. Missing replicates are automatically padded with NaN values to
maintain a consistent output format for downstream statistical analysis and
visualization.

Output:
    q_hbond_30rep.csv

Columns:
    Frame, Time_ns, Rep01 ... Rep30

Usage:
    python assemble_all_q_hbond.py <root_directory> [--burnin N]

Requirements:
    Python 3
    pandas
"""

import os, sys, argparse, glob
import pandas as pd

def assemble_one(neutral_dir: str, burnin: int, outname: str) -> None:
    # find immediate children NEUTRAL_*
    rep_dirs = sorted(
        d for d in glob.glob(os.path.join(neutral_dir, "NEUTRAL_*"))
        if os.path.isdir(d)
    )

    if not rep_dirs:
        print(f"[skip] No NEUTRAL_* subdirs in {neutral_dir}")
        return

    dfs = []
    missing_files = []
    present_reps = set()

    # Always target Rep01..Rep30 (pad with NaN if absent)
    for rep in range(1, 31):
        rd = os.path.join(neutral_dir, f"NEUTRAL_{rep}")
        fp = os.path.join(rd, "q_hbond.dat")
        if os.path.isfile(fp):
            try:
                df = pd.read_csv(fp, sep=r"\s+", comment="#", header=None,
                                 names=["Frame", f"Rep{rep:02d}"])
                if burnin > 0:
                    df = df[df["Frame"] > burnin]
                dfs.append(df)
                present_reps.add(rep)
            except Exception as e:
                print(f"[warn] Failed to read {fp}: {e}")
                missing_files.append(fp)
        else:
            missing_files.append(fp)

    if not dfs:
        print(f"[skip] No q_hbond.dat files found under {neutral_dir}")
        return

    # Outer-merge all on Frame
    out = dfs[0]
    for df in dfs[1:]:
        out = out.merge(df, on="Frame", how="outer")

    out = out.sort_values("Frame").reset_index(drop=True)

    # Insert Time_ns after Frame (100 frames/ns)
    out.insert(1, "Time_ns", out["Frame"] / 100.0)

    # Ensure all Rep01..Rep30 columns exist (even if missing entirely)
    for rep in range(1, 31):
        col = f"Rep{rep:02d}"
        if col not in out.columns:
            out[col] = pd.Series([pd.NA] * len(out), dtype="Float64")

    # Order columns: Frame, Time_ns, Rep01..Rep30
    rep_cols = [f"Rep{r:02d}" for r in range(1, 31)]
    out = out[["Frame", "Time_ns"] + rep_cols]

    # Write in the NEUTRAL/ directory
    out_fp = os.path.join(neutral_dir, outname)
    out.to_csv(out_fp, index=False)
    print(f"[ok] Wrote {out_fp}  (present reps: {sorted(present_reps)})")

    # Brief missing report (if any)
    actually_missing = [p for p in missing_files if not os.path.isfile(p)]
    if actually_missing:
        print(
            f"[info] Missing q_hbond.dat for reps: "
            f"{[int(p.rsplit('_',1)[-1].split('/')[0]) for p in actually_missing]} in {neutral_dir}"
        )

def find_neutral_dirs(root: str):
    # Find any directory literally named "NEUTRAL"
    for dirpath, dirnames, filenames in os.walk(root):
        if os.path.basename(dirpath) == "NEUTRAL":
            yield dirpath

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".", help="Root to scan (default: .)")
    ap.add_argument("--burnin", type=int, default=0,
                    help="Drop frames <= this value")
    ap.add_argument("--outname", default="q_hbond_30rep.csv",
                    help="Output filename to create in each NEUTRAL/ directory")
    args = ap.parse_args()

    found = False
    for neutral_dir in find_neutral_dirs(args.root):
        found = True
        print(f"\n=== Processing {neutral_dir} ===")
        assemble_one(neutral_dir, burnin=args.burnin, outname=args.outname)

    if not found:
        print("[done] No NEUTRAL/ directories found under", args.root)

if __name__ == "__main__":
    main()
