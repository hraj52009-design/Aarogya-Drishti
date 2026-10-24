# Public BrainTumorMRI dataset attribution and limitations

- Host: Hugging Face Datasets
- Dataset ID: `Dharamanand/BrainTumorMRI`
- Dataset card: https://huggingface.co/datasets/Dharamanand/BrainTumorMRI
- Revision used by the downloader: `247d8e19a2b0c3337c0e16d00efeb7094a3ebe57`
- License declared in the host dataset card: CC0-1.0
- Host card describes four labels: glioma, meningioma, no tumor, pituitary; 5,969 training and 1,054 test examples.

The card does not adequately document the underlying source dataset or upstream rights, and does not provide patient identifiers. Verify those matters before publication or redistribution. This project maps the three tumor labels to binary label 1 and `notumor` to label 0, uses the hosted test partition as a held-out test set, and splits only the hosted training partition into train/validation/calibration sets. Exact and pixel-identical duplicates are collapsed within the test set, and matching training examples are removed to prevent image leakage; the counts are recorded in `dataset-attribution.json`. Each image is assigned an image-specific group identifier only to prevent the local evaluator from implying a patient cluster. Metrics are image-level and do not demonstrate patient-independent generalization, clinical validity, or performance outside this benchmark.

The downloader pins the host revision and verifies the Parquet files against the SHA-256 values reported by the host's file metadata. Dataset files, extracted images, manifests, and run artifacts are ignored by source control.
