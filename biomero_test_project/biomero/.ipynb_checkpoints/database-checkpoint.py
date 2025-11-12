import numpy as np

def get_dataset_images(dataset_id):
    """
    Mock dataset generator for testing BIOMERO wrapper.
    Each 'image' is a X byY NumPy array with random black & white pixels (0 or 255).
    """
    print(f"[DEBUG] Generating dataset {dataset_id}...")
    num_images = 10  # adjust to 90 or any number you want
    dataset = []

    for i in range(num_images):
        image = np.random.choice([0, 255], size=(500, 500), p=[0.5, 0.5]).astype(np.uint8)
        dataset.append(image)

    return dataset