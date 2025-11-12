import os
import sys
import importlib.util
from multiprocessing import Pool, cpu_count

# ---- BIOMERO imports ----
try:
    from biomero.database import get_dataset_images
except ImportError:
    raise ImportError("This wrapper must run inside a BIOMERO-like environment.")


def load_user_module(script_path):
    """Load user script dynamically as a module."""
    spec = importlib.util.spec_from_file_location("user_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_chunk(chunk, script_path):
    """Each worker loads the user script locally to avoid pickling errors."""
    module = load_user_module(script_path)
    if not hasattr(module, "main"):
        raise AttributeError("User script must define a `main(image)` function.")
    user_main = module.main

    results = []
    for image in chunk:
        try:
            results.append(user_main(image))
        except Exception as e:
            print(f"[ERROR] Failed processing image: {e}", flush=True)
    return results


def parallel_run(script_path, dataset_id):
    """Parallelize user code on all CPU cores."""
    images = get_dataset_images(dataset_id)
    if not images:
        raise ValueError(f"No images found for dataset {dataset_id}")
    print(f"Found {len(images)} images in dataset {dataset_id}")

    num_cpus = cpu_count()
    print(f"Using {num_cpus} CPU cores")

    chunk_size = max(1, len(images) // num_cpus)
    image_chunks = [images[i:i + chunk_size] for i in range(0, len(images), chunk_size)]

    print("Starting parallel processing...")
    with Pool(processes=num_cpus) as pool:
        results = pool.starmap(run_chunk, [(chunk, script_path) for chunk in image_chunks])

    flattened = [item for sublist in results for item in sublist]
    print("All images processed successfully.")
    return flattened


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python biomero_parallel_wrapper.py path/to/user_script.py <dataset_id>")
        sys.exit(1)

    user_script = sys.argv[1]
    dataset_id = sys.argv[2]
    parallel_run(user_script, dataset_id)