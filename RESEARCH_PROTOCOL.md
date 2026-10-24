# Proposed study — results pending

Working title: **Stability-Aware Selective Prediction for Reproducible Brain-MRI Image Classification**. Novelty is not established. Search and review relevant medical-imaging, selective-classification, consistency-regularization and test-time-augmentation literature before positioning contributions. No fabricated bibliography is supplied.

Research question: Does gamma-consistency training plus perturbation-stability scoring improve the error/coverage tradeoff relative to calibrated confidence-only selection under a fixed subject-independent protocol?

| Experiment | Training | Calibration/inference |
|---|---|---|
| A | Small CNN, consistency 0 | Identity, temperature, entropy |
| B | Pretrained ResNet50, consistency 0 | Identity, temperature, entropy |
| C | Same ResNet50 as B | Four views, temperature, entropy |
| D | Same ResNet50 as B | Four views, temperature, entropy plus disagreement |
| E | ResNet50, consistency 0.2 | Four views, temperature, entropy plus disagreement |
| F | Same weights as E | Four views, temperature disabled, combined score |

For identity use `calibrate.py --single-view --alpha 1`; for entropy-only use `--alpha 1`; combined defaults to `--alpha 0.5`; temperature ablation uses `--no-temperature`. For inference-only ablations copy an uncalibrated training run into separate directories BEFORE calibration. Do not reuse calibration JSON across different checkpoints. Calibration includes empirical quantile selection and may overfit small cohorts; report sample size and uncertainty. No distribution-free guarantee is implemented.

For each preplanned training seed, run B and E with the same seed, split, initialization scheme, optimizer settings and training budget. Use validation only to choose consistency weight and other settings; record all attempts. CNN vs ResNet assesses model family differences, NOT isolated consistency benefit. Run at least three training seeds if feasible and keep the patient split fixed for these comparisons. Site-separated external validation is valuable but is not implemented by the internal-manifest evaluation command; create a separately governed external protocol rather than relabeling internal test data.

| Evidence to report | Current status |
|---|---|
| Dataset provenance, license, true patient counts, scanner/site context | Not supplied |
| Exact and near-duplicate audit | Exact checks implemented; human near-duplicate audit required |
| Full-cohort macro-F1, sensitivity, specificity, AUROC, average precision | To be measured |
| Calibration NLL, Brier and ECE | To be measured |
| Actual coverage and retained-subset errors at calibration-fixed threshold | To be measured |
| Coverage separately for tumor and no-tumor groups | To be measured |
| Patient-cluster confidence intervals | Implemented; not run |
| Paired improvement intervals between methods | Not implemented; needed for inferential comparison |
| Latency, memory and model size | Manual benchmark required |
| External validation and expert review | Not performed |

Risk/coverage curves are descriptive, not permission to optimize on test data. Rejection can hide hard positive cases: always report class-specific coverage, number referred, retained errors and full-cohort performance. Compare achieved coverage, not just requested calibration coverage. Scores are model probabilities, not individual disease risks. Model flags are not clinical quality judgments.

## Paper structure
| Section | Required content |
|---|---|
| Abstract | Task, actual cohort, protocol, measured findings and limitations; fill after experiments |
| Introduction | Brain-MRI classification scope and motivation for uncertainty-aware review |
| Related work | Verified sources, existing approaches, honest distinction from prior methods |
| Methods | Binary-label semantics, patient splits, architecture, preprocessing, consistency objective, view definitions, score and calibration |
| Experiments | Baselines, preplanned ablations, seeds, hardware, versions and frozen test protocol |
| Results | Actual metrics with uncertainty; no placeholder values presented as findings |
| Discussion | Errors, coverage tradeoffs, nuisance transformations, shortcut learning and dataset shift |
| Limitations and ethics | Image-level scope, dataset bias, data access, no clinical validation and no novelty guarantee |
| Reproducibility | Code revision, dependency lockfile, configs and governed data manifest |

Suggested abstract skeleton: We investigate [question] on [dataset/version] containing [independent patients/images]. We compare [preplanned baselines] using [split protocol]. The proposed configuration achieves [measured result with interval] at [actual coverage], compared with [baseline]. Limitations include [observed limits]. The system is an academic prototype and is not validated for clinical use.
