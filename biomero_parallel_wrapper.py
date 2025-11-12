#!/usr/bin/env python3
"""
BIOMERO Parallel Wrapper
------------------------
Automatically parallelize user-provided Python code across all CPU cores
within a single SLURM compute node.

Usage:
    biomero-wrapper path/to/user_script.py <dataset_id>

Assumptions:
    - The user script defines a function `main(image)` that processes one image.
"""

import os
import sys
import importlib.util
from multiprocessing import Pool, cpu_count

# ---- BIOMERO imports ----
try:
    from biomero.database import get_dataset_images
except ImportError:
    raise ImportError("This wrapper must run inside a BIOMERO environment.")


def load_user_module(script_path):
    """Dynamically load a user script as a Python module."""
    spec = importlib.util.spec_from_file_location("user_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_chunk(chunk, user_main):
    """Run user_main() sequentially on each image in a chunk (per process)."""
    results = []
    for image in chunk:
        try:
            results.append(user_main(image))
        except Exception as e:
            print(f"[ERROR] Failed processing {image}: {e}", flush=True)
    return results


def parallel_run(script_path, dataset_id):
    """
    Automatically parallelize user code across all CPU cores.

    Args:
        script_path (str): Path to user-provided Python script.
        dataset_id (int | str): OMERO dataset ID to process.
    """
    # Load user script dynamically
    module = load_user_module(script_path)
    if not hasattr(module, "main"):
        raise AttributeError("User script must define a `main(image)` function.")
    user_main = module.main

    # Retrieve dataset images from BIOMERO
    images = get_dataset_images(dataset_id)
    if not images:
        raise ValueError(f"No images found for dataset {dataset_id}")
    print(f"Found {len(images)} images in dataset {dataset_id}")

    # Detect CPUs
    num_cpus = cpu_count()
    print(f"Using {num_cpus} CPU cores")

    # Split dataset into chunks for each core
    chunk_size = max(1, len(images) // num_cpus)
    image_chunks = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]

    # Parallel execution
    print("Starting parallel processing...")
    with Pool(processes=num_cpus) as pool:
        results = pool.starmap(run_chunk, [(chunk, user_main) for chunk in image_chunks])

    # Flatten and return all results
    flattened = [item for sublist in results for item in sublist]
    print("All images processed successfully.")
    return flattened


def main():
    """Entry point for command-line execution."""
    if len(sys.argv) < 3:
        print("Usage: biomero-wrapper path/to/user_script.py <dataset_id>")
        sys.exit(1)

    user_script = sys.argv[1]
    dataset_id = sys.argv[2]
    parallel_run(user_script, dataset_id)


if __name__ == "__main__":
    main()