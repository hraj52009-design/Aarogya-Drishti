# AarogyaDrishti — research prototype

Brain MRI **2D image-level binary classification**, not clinical diagnosis, segmentation, tumor localization, or patient-level diagnosis. A public image-level benchmark, trained CNN checkpoint, calibration, and held-out report have been generated locally under ignored `data/` and `runs/`; these artifacts are not part of the source distribution. The result is not patient-independent or clinical validation. No verified novelty claim is made.

The local research UI uses Flask with custom HTML, CSS and JavaScript. A one-time local administrator setup protects inference and model training. Uploaded inference images are processed in memory and are not intentionally persisted. The service binds to localhost by default; do not expose it to a network or use identifiable patient data. Outputs are safety-oriented research triage findings (`SUSPICIOUS`, `NOT_SUSPICIOUS`, or `INSUFFICIENT_QUALITY`) and are never clinical diagnoses. The review-queue UI is intentionally not exposed by the application.

## Scope and source
The indexed AarogyaDrishti synopsis describes supervised brain-MRI classification, a CNN baseline, optional ResNet50/EfficientNet transfer learning, patient-aware splitting and reproducible evaluation. It explicitly describes system/evaluation contributions rather than claiming a new architecture. This implementation chooses binary labels and 2D PNG/JPEG inputs; these are implementation decisions, not proof the eventual dataset fits. It does not yet perform governed 3D NIfTI inference or segmentation. Do not relabel BraTS cases as a tumor/no-tumor cohort without valid negative data.

## Research candidate: stability-aware selective prediction
Train with optional symmetric prediction-consistency regularization under a mild gamma perturbation. At inference, compare identity, gamma 0.9, gamma 1.1 and small Gaussian blur. Combine normalized predictive entropy and between-view disagreement to flag unstable predictions for review. Temperature scaling and the review threshold use calibration data, not test data. These are established ingredients; their combination is a **candidate empirical study, not a proven first-ever invention**. Perturbations need domain review and may remove subtle findings. No guaranteed coverage or clinical error bound is claimed.

## Setup
Python 3.10+ recommended. Install a compatible torch/torchvision pair for your OS/CUDA using official PyTorch instructions, then:
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
```
ImageNet weights require internet on first use and are not medical validation. The default baseline runs without downloads; the optional public benchmark downloader runs only when explicitly invoked. CPU works for smoke tests; realistic training depends on data and hardware.

## Project layout

The project keeps the research pipeline in small, purpose-specific modules:

- `backend/` contains the Flask application and reusable research/model
  modules. The root `app.py` and module files are compatibility entry points
  for existing imports and test commands.
- `scripts/` contains the reproducible prepare/train/calibrate/evaluate,
  dataset, and validation command-line tools.
- `frontend/templates/` and `frontend/static/` contain the server-rendered
  pages and browser assets.
- `tests/` contains the regression and workflow tests.

Names are intentionally descriptive rather than tied to a specific dataset or
model vendor. Runtime outputs stay in the ignored `data/`, `runs/`, and
`instance/` directories so source code and local artifacts remain separate.

Start the local UI from the repository root with `python app.py`. Run a
research pipeline tool as a module, for example
`python -m scripts.train --help`; the root compatibility files remain
available for older automation.

## Upgrade and validation order

The real-world readiness work is intentionally staged and must not be treated
as a clinical approval:

1. Freeze the current baseline with `freeze_baseline.py`.
2. Audit the dataset and leakage with `audit_dataset.py`.
3. Require a patient-level, site-aware external manifest before model
   comparisons are used for readiness claims.
4. Compare architectures in separate, reproducible run directories.
5. Lock calibration and uncertainty thresholds using calibration data only.
6. Run external validation on a genuinely separate patient/site cohort.
7. Keep abstention and audit logging mandatory; any clinical or radiologist review process must remain external to this prototype.
8. Harden deployment only after the research evidence is complete.
9. Maintain an intended-use, risk, and clinical-evidence record.

Example foundation commands:

```powershell
.\.venv\Scripts\python.exe .\freeze_baseline.py `
  --run .\runs\public-brain-tumor-cc0\model `
  --out .\runs\public-brain-tumor-cc0\model\baseline_freeze.json

.\.venv\Scripts\python.exe .\audit_dataset.py `
  --manifest .\data\hf_brain_tumor_mri\manifest.csv `
  --out .\runs\public-brain-tumor-cc0\dataset_audit.json
```

The current public benchmark audit shows no byte or pixel duplicates and no
split-group overlap, but it has no verified `patient_id`. Therefore it remains
an image-level research benchmark and cannot support patient-independent or
clinical performance claims.

### Architecture comparison

The training interface now supports three separately reproducible 2D
architectures:

- `cnn` — small baseline
- `resnet50` — residual transfer-learning candidate
- `efficientnet_b0` — efficient convolutional transfer-learning candidate

Run a build/forward-pass comparison without downloading weights:

```powershell
.\.venv\Scripts\python.exe .\compare_architectures.py `
  --out .\runs\architecture_comparison.json
```

For a real comparison, train each architecture into a new empty run directory,
calibrate using the calibration split, and evaluate once on the locked test
split. Do not compare only accuracy: retain sensitivity, specificity,
patient-level aggregation, calibration, abstention coverage, site strata, and
false-negative review. ImageNet pretrained weights are optional and are not
medical validation.

### Calibration and uncertainty

Calibration continues to use only the reserved calibration partition. The
evaluation report now records separate normalized predictive entropy and
between-view disagreement summaries, along with retained/review counts. These
values are abstention signals for research triage; they are not disease
probabilities, diagnostic confidence, or safety guarantees.

### Patient-level external data contract

Approved external data must be imported through `patient_pipeline.py` rather
than copied into the existing image-level manifest. The minimum schema is:

```csv
path,label,patient_id,site_id,study_id,sequence
site_a/patient_001/flair.nii.gz,1,patient_001,site_a,study_001,FLAIR
```

The pipeline requires pseudonymous patient and site identifiers, stable study
identifiers, binary reference labels, and one patient per split. It rejects
patient or study leakage, mixed labels within a patient, missing files, and
cross-site patient identifiers. It creates patient-level train/validation/
calibration/test assignments and a report without exporting patient IDs:

```powershell
.\.venv\Scripts\python.exe .\patient_pipeline.py `
  --manifest .\data\external\manifest.csv `
  --out .\data\external\patient_splits.csv `
  --report .\runs\external\patient_pipeline_report.json
```

The source data must be lawfully obtained, de-identified, licensed for the
intended research use, and accompanied by provenance and labeling records.
Downloading a public collection does not by itself make it suitable for
clinical use.

### External validation gate

`external_validation.py` now records a cohort preflight in every external
report. It includes patient/site counts, class balance by patient, patients per
site, and whether every site contains both reference classes. A single-site
cohort is flagged for caution; it is not silently presented as multi-site
generalisation evidence. The report also stores the external manifest hash so
the evaluated cohort can be audited later.

## Data contract
Create an external `data/manifest.csv`, one image per row:
```csv
path,label,patient_id
images/subject001_slice01.png,0,subject001
images/subject002_slice01.png,1,subject002
```
Paths are relative to the manifest, or absolute. Labels: **0 = no_tumor; 1 = tumor**. The above rows are schema examples, not real data. Use legitimate deidentified data and stable pseudonymous subject identifiers. Do not use a filename as a patient ID unless verified. For patient-independent evaluation, provide true patient IDs so all images from each patient stay in one split. If identity is unavailable, a `group_id` can support an explicitly image-level benchmark only; it must not be described as patient-independent. The loader requires consistent labels within each group and both classes in every split. Map multiclass tumor subtypes to binary only with documented dataset semantics. Slice labels and patient labels may differ: do not automatically label every slice in a tumor patient's volume as containing tumor. Adapt the task before using such data.

Document dataset URL, version, license, consent/access restrictions, label provenance, subject count, sites and scanner sequences. PNG exports discard acquisition context. Never commit patient images or identifiers.

### Optional public image-level benchmark
`download_brain_tumor_dataset.py` downloads the public [BrainTumorMRI dataset hosted on Hugging Face](https://huggingface.co/datasets/Dharamanand/BrainTumorMRI) at a pinned revision. Its dataset card declares CC0-1.0 and publishes train/test Parquet files. The card provides limited provenance and no patient identifiers; check upstream rights/terms before reuse. This optional run is strictly **image-level**: it preserves the host's test partition, splits the host's training partition into train/validation/calibration, maps `notumor` to 0 and tumor subtypes to 1, and makes no patient-independent generalization claim. Exact/pixel duplicates are rejected; this cannot rule out near-duplicates or hidden subject overlap.

Run without Kaggle credentials:
```powershell
.\.venv\Scripts\python.exe .\download_brain_tumor_dataset.py --epochs 10 --run public-brain-tumor-cc0
```
This downloads about 158 MB and trains the CNN baseline, calibrates on its held-out calibration images, and evaluates once on the source test partition. Dataset files are kept under ignored `data/`; checkpoints and reports under ignored `runs/`. The test report is a benchmark only, not clinical performance.

## Run in order
```bash
python prepare.py --manifest data/manifest.csv --out data/splits.csv
python train.py --manifest data/splits.csv --run runs/cnn --arch cnn --epochs 20
python train.py --manifest data/splits.csv --run runs/resnet --arch resnet50 --pretrained --epochs 20
python train.py --manifest data/splits.csv --run runs/stable --arch resnet50 --pretrained --consistency 0.2 --epochs 20
python calibrate.py --run runs/stable --manifest data/splits.csv --coverage 0.9
python evaluate.py --run runs/stable --manifest data/splits.csv
python predict.py --run runs/stable --image path/to/approved_sample.png
python app.py
```
Calibrate/evaluate each baseline separately too. `--epochs 1 --arch cnn --size 64` is a smoke test, NOT a valid experiment. CLI training supports `--device cpu` or `cuda`. Defaults auto-select CUDA if available. No automatic downloads of medical data occur.

The Flask UI opens at `http://127.0.0.1:5000`. On first visit, create the administrator account in the local browser; the password is hashed in an SQLite database under the ignored `instance/` directory. The app stores a generated Flask session secret in the same directory. Back up these files securely if you need to retain the account; deleting them resets setup. There is no password recovery or multi-user account management. Inference is disabled by default. For a strictly internal, authorized research demonstration only, explicitly opt in before starting the server:
```powershell
$env:AAROGYADRISHTI_ENABLE_RESEARCH_INFERENCE = "1"
.\.venv\Scripts\python.exe .\app.py
```
This switch does not validate or authorize clinical use. Unset the variable and restart the server to disable inference.

After signing in, open **Model setup** and provide the full local path to a CSV manifest with `path,label,patient_id` columns for patient-wise evaluation. Use `group_id` only when subject identity is unavailable and the resulting study is explicitly image-level. The workflow validates the manifest, creates group-wise splits, trains a CNN or ResNet50 (random initialization), calibrates the checkpoint, and evaluates once on the held-out test split. Outputs are saved under `runs/<run-name>/model/`; only runs with `best.pt`, matching `calibration.json`, and `test_report.json` appear in the image-analysis model selector. The dataset and images are not bundled or uploaded by this UI; provide an authorized deidentified dataset. Training can take a long time and needs enough independent groups in both classes for stratification. Do not use test results to retune settings.

The UI validates PNG/JPEG uploads, dimensions and size; uploaded images are not intentionally written by the app. POST routes require a CSRF token, passwords must be at least 12 characters, and a run can only be started once under a new safe run name. Keep the default localhost binding. This is a local research prototype, not production-hardened or clinically validated.

Inference applies a conservative, calibration-recorded suspicious threshold, rejects very low-contrast or non-grayscale-domain inputs, and writes a metadata-only audit trail to `instance/inference_audit.jsonl`. The `/api/patient-summary` endpoint can conservatively aggregate multiple image predictions using a pseudonymous patient ID; it does not replace complete-study clinical review. External validation reports are generated with `external_validation.py` and require a separate patient/site-labelled cohort.

The phase-two `/api/validate-study` endpoint validates DICOM and NIfTI containers in memory, rejects selected identifying DICOM tags, and reports dimensions/shape without storing source bytes. It deliberately returns `inference_ready: false`: container validation is not a clinical study adapter, and DICOM/NIfTI inference must not be enabled by treating a volume as an arbitrary 2D image. Install `pydicom` and `nibabel` from `requirements.txt` before using this endpoint.

The research workspace also provides **Study workflow**, **Review queue**, and **Monitoring** pages. Study workflow aggregates authorized PNG/JPEG research slices conservatively and creates a mandatory radiologist-review item. The image-analysis result panel exposes quality/domain heuristics, the calibrated suspicious threshold, and an optional gradient-based sensitivity map. The map is exploratory only: it is not a lesion segmentation, localization result, or causal explanation. Model registry and monitoring endpoints expose checkpoint hashes, provenance metadata, inference counts, and insufficient-quality counts for local audit; these pages do not establish model performance or clinical safety.

Evaluation reports now include fixed-threshold operating points (sensitivity, specificity, false-negative and false-positive counts), prevalence-aware PPV/NPV estimates, reliability-curve bins, Brier score and ECE. These are descriptive validation statistics; confidence intervals remain cohort-dependent and do not establish clinical performance. Existing checkpoints must be evaluated into a new report directory or a new run because held-out reports are intentionally immutable.

### External patient-grouped validation groundwork
`external_validation.py` provides a separate, one-time evaluation path for a **frozen** checkpoint and calibration on a held-out external cohort. It does not train, recalibrate, or select thresholds from the external data. The external CSV must contain `path,label,patient_id,site_id`; IDs must be stable pseudonyms, both reference-label classes must be present, and every image must be a readable 2D PNG/JPEG. Patient IDs must not overlap the model-development cohort. The command rejects training runs whose groups are image IDs rather than patient IDs, and audits exact/pixel-identical duplicate images against the development cohort.

Before collecting or evaluating any clinical cohort, obtain institutional data-access, privacy, ethics and governance approvals; define intended use, population, image-level reference standard and analysis plan; and have qualified reviewers adjudicate labels. Keep external labels locked until protocol and model are frozen. Near-duplicate, site, scanner, subgroup, temporal and acquisition-protocol audits still require governed data and human review. This tool produces research metrics only; it is not a regulatory submission, clinical study approval, clinical validation, or permission to use predictions in care.

Example, using a genuinely independent and approved external cohort:
```powershell
.\.venv\Scripts\python.exe .\external_validation.py `
  --run .\runs\patient-grouped-model\model `
  --training-manifest .\data\development-splits.csv `
  --external-manifest .\data\approved-external-cohort.csv `
  --output .\runs\patient-grouped-model\external-site-a
```
The output directory is write-once and contains aggregate metrics, patient-cluster bootstrap intervals, and pseudonymous site strata; raw paths, patient IDs, and image predictions are not exported. A failed eligibility or overlap check must be resolved through the data/protocol owners, not bypassed.

Splits are approximately 60% train, 15% validation, 10% calibration, 15% test by group. Approximate image proportions can differ. Small cohorts can fail stratification; collect adequate independent patients for patient-level claims instead of bypassing safeguards. Tune model hyperparameters on validation only, freeze the study protocol, then calibrate and evaluate once. Do not repeatedly choose settings based on test reports.

## Outputs and limitations
Training saves best validation-loss weights, history and experiment provenance. Calibration saves temperature and empirical stability-score threshold. Evaluation saves full-cohort and retained-subset metrics, coverage, confusion matrix, group-cluster bootstrap intervals and threshold-sweep risk/coverage data. Intervals are image-metric intervals resampled by group, not patient-level diagnostic performance when group identity is unavailable. Skipped single-class bootstrap resamples are reported. No Grad-CAM implementation is included; explanation heatmaps would not establish localization accuracy.

The UI only displays research labels and review flags. It cannot verify that an arbitrary uploaded image is a brain MRI, detect all out-of-distribution inputs, or assess clinical image quality. PIL corruption checks are not clinical quality control. No image or prediction is intentionally persisted by the UI; hosting infrastructure may log requests. Do not deploy with identifiable patient information.

### Local authentication
Local signup is intended for controlled research use only. New accounts require a username and a confirmed password of at least 12 characters using at least three character types (lowercase, uppercase, number, or symbol); passwords must not match the username. These checks improve local account hygiene but are not a substitute for an approved identity provider, email verification, administrator approval, rate limiting, or production-grade account recovery. The password-reset flow is restricted to local requests and is not available as networked account recovery. The review-queue UI and route are disabled; any reviewer workflow must be implemented separately with an approved role and assignment process.

The first local setup account is an administrator. Accounts created through signup are research users. Both roles use the same login page, but administrators can manage research model setup, monitoring, review operations, and local user roles; research users can access image analysis, study workflow, and review workflow only. The administrator user-management screen prevents removing the last administrator.

## Deployment readiness
**This project is not ready for patient care or clinical deployment.** The available benchmark has no patient identifiers, so its 1,030-image held-out result is not a patient-independent validation and is not eligible for the external clinical-validation groundwork command. On that image-level test set, accuracy was 85.9% and specificity was 61.1% (112 false positives among 288 no-tumor images). These results do not establish clinical safety, utility, or performance at another site.

Before any clinical use, define and approve the intended use and target population; acquire legally governed, representative patient-level data with clinically adjudicated labels; perform leakage-controlled external and subgroup validation across sites, scanners, and populations; and complete prospective workflow/human-factors evaluation, clinical safety review, and applicable regulatory/privacy approvals. Add validated image/modality and out-of-distribution checks, calibrated uncertainty and safe failure behavior, and a clinician-controlled workflow. Do not use the current public image-level checkpoint to guide care.

For a future approved service, set `AAROGYADRISHTI_ENV=production`, enable `AAROGYADRISHTI_SECURE_COOKIES=1`, and run behind TLS using a production WSGI server and reverse proxy; the application refuses to start its Flask development server in production mode and refuses production configuration without secure cookies. Add managed identity, role-based access, rate limits, audit and retention controls, encrypted storage, operational monitoring, backup/restore, and model versioning/rollback. The current local account database and in-process training job are prototype features, not a production operations platform.
