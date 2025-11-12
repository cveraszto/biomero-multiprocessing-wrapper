# BIOMERO Parallel Wrapper

A lightweight Python wrapper that automatically parallelizes BIOMERO Python processing jobs across all available CPU cores on a compute node.
This approach is primarily beneficial for **Python versions before 3.13**, which still include the **Global Interpreter Lock (GIL)**.
Starting with **Python 3.13+ (No-GIL mode)**, true multi-core parallel execution will be possible without workarounds like `multiprocessing`.


## Features

- Automatically detects available CPU cores.
- Splits image datasets into parallel chunks.
- Runs user-defined Python processing functions (`main(image)`).
- Designed to integrate with BIOMERO workflows or run standalone.

## Installation

Clone and install locally:

```bash
git clone https://github.com/<your-username>/biomero-parallel-wrapper.git
cd biomero-parallel-wrapper
pip install -e .

## Notes

The wrapper uses Python’s built-in multiprocessing library.

For integration with BIOMERO, it should be placed next to user code in a Docker or SLURM environment.

Requires Python 3.7+.


## Author

Created by cveraszto.