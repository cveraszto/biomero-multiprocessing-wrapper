# BIOMERO Parallel Wrapper

- A lightweight Python wrapper that automatically parallelizes BIOMERO Python processing jobs across all available CPU cores on a compute node.
- This approach is primarily beneficial for **Python versions before 3.13**, which still include the **Global Interpreter Lock (GIL)**.
- Starting with **Python 3.13+ (No-GIL mode)**, true multi-core parallel execution will be possible without workarounds like `multiprocessing`.
- You can also read the tutorial Notebook for more info.

## Features

- Automatically detects available CPU cores.
- Splits image datasets into parallel chunks.
- Runs user-defined Python processing functions (`main(image)`).
- Designed to integrate with BIOMERO workflows or run standalone.

## Installation

Clone and install locally:

```bash
# Clone the repository
git clone https://github.com/cveraszto/biomero-multiprocessing-wrapper.git

# Change into the project directory
cd biomero-multiprocessing-wrapper

# Install the package locally in editable mode
pip install -e .
```

## Recommended Project Structure

/app/
 ├── biomero/           ← BIOMERO library (mounted or installed)
 ├── biomero_parallel_wrapper.py
 ├── user_code/
 │    └── e.g. my_processing.py
 └── Dockerfile

## Usage

Run your processing script with the wrapper:

```bash
python biomero_parallel_wrapper.py user_code/my_processing.py 123
```

- `user_code/my_processing.py` → your script to process
- `123` → an example argument (replace with what your script expects)

## Notes

The wrapper uses Python’s built-in multiprocessing library.

For integration with BIOMERO, it should be placed next to user code in a Docker or SLURM environment.

Requires Python 3.7+.


## Author

Created by cveraszto.