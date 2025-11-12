setup(
    name="biomero-wrapper",
    version="0.1",
    py_modules=["biomero_parallel_wrapper"],
    entry_points={
        "console_scripts": [
            "biomero-wrapper = biomero_parallel_wrapper:main",
        ],
    },
)