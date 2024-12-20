# High-Throughput QC Input Generator

## Overview

This Python scripts facilitate the generation of input files for high-throughput quantum chemistry (QC) calculations using software like [**ORCA**](https://www.faccts.de/orca/), [**Gaussian**](https://gaussian.com/), and [**MobCal-MPI**](https://github.com/HopkinsLaboratory/MobCal-MPI). It is particularly suited for automating large-scale computational workflows.

## Features

- Each script processes an ensemble of conformers (e.g., typically obtained from [**CREST**](https://github.com/crest-lab/crest)) alongside user-provided "base" input files specifying QC parameters.
- Generates a **"ready-to-submit"** set of input files, each with a unique name and, where applicable (e.g., Gaussian), a unique identifier for checkpoint files or a base name (for ORCA).
- Supports high-throughput benchmarking studies, such as optimization of full ensemble of conformers, testing multiple **DFT methods** or climbing the **"Jacob's ladder"** of computational accuracy.

## Example Use Case

- **Input**: 10 conformers and 10 DFT methods.
- **Output**: 10 × 10 = 100 unique input files, ready for submission.

## Benefits

This tool streamlines the setup for:
- **Benchmarking studies** to compare multiple DFT methods.
- Large-scale conformer optimizations using various QC methods.
- Automated workflows for evaluating improvements in accuracy.

## Getting Started

Examples of input files and a tested ensemble are included to help you get started quickly.

## License

This project is licensed under the [MIT License](LICENSE).

