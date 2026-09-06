# A Risk-Aware Predictive Maintenance Decision Framework

> An independent study linking statistical process control, nonlinear failure prediction, and constrained operating decisions

**Doyun Shin · Department of Industrial Engineering, Gachon University**  
Independent undergraduate research manuscript · 2026

[Read the English paper](papers/read-en.md) · [한국어 논문](papers/read-ko.md) · [Download English PDF](papers/risk-aware-predictive-maintenance-en.pdf) · [Companion code](https://github.com/doyunsin883-debug/risk-aware-predictive-maintenance) · [한국어 README](README.md)

![Conceptual view of process monitoring, failure-risk prediction, and constrained operating decisions](assets/figures/research-hero.jpg)

## The study in three questions

1. **SQC:** Is the process behaving differently from its baseline?
2. **ML:** Is that state likely to lead to an actual machine failure?
3. **Optimization:** Given the estimated risk, how should the machine be operated while preserving productivity?

In short, **SQC explains process state, ML estimates failure risk, and optimization turns prediction into a candidate action.**

## Start here

| Goal | Recommended route |
|---|---|
| Read the full manuscript on any device | [English mobile reader](papers/read-en.md) |
| Download the publication-quality file | [English PDF](papers/risk-aware-predictive-maintenance-en.pdf) |
| Inspect the research logic and decisions | [Research-flow guide](docs/RESEARCH_FLOW_KO.md) |
| Review the headline numbers | [Results at a glance](docs/RESULTS_AT_A_GLANCE.md) |
| Reproduce the analysis | [Companion code repository](https://github.com/doyunsin883-debug/risk-aware-predictive-maintenance) |

## End-to-end design

```mermaid
flowchart LR
    A["AI4I 2020<br/>10,000 observations"] --> B["EDA and data audit"]
    B --> C["Sequential split<br/>70% · 15% · 15%"]
    C --> D["SQC<br/>I-MR charts and drift"]
    D --> E["Feature design<br/>raw + engineered + SPC"]
    E --> F["Model comparison<br/>LR · RF · GB"]
    F --> G["Validation threshold<br/>0.65"]
    G --> H["Held-out test"]
    H --> I["Constrained search<br/>risk under productivity"]
    I --> J["Operating candidate"]
```

The sequence matters. Control-chart alarms were not relabeled as failures. Models and the operating threshold were selected on the validation block, while the final block remained untouched until the held-out evaluation.

## Data and evaluation protocol

- 10,000 observations and **339 failures (3.39%)**
- 27 consistency exceptions between the aggregate failure label and component failure modes
- Observation-order split: 7,000 training, 1,500 validation, and 1,500 test rows
- Failure counts: 278, 32, and 29, respectively
- Evaluation centered on recall and PR-AUC rather than accuracy alone

The final Gradient Boosting model, selected with a validation threshold of 0.65, achieved the following held-out results:

| Metric | Test result |
|---|---:|
| Accuracy | 0.9833 |
| Precision | 0.5526 |
| Recall | 0.7241 |
| F1-score | 0.6269 |
| ROC-AUC | 0.9615 |
| PR-AUC | 0.7463 |

It detected **21 of 29** failures, with 17 false alarms and 8 missed failures.

## What the negative results taught us

Torque and mechanical-power I-MR alarms were rare but risk-enriched. In contrast, the temperature-difference alarm fired on 96.13% of the validation block yet produced a risk lift of only 0.98 because the process mean had shifted. It was therefore treated as a **drift indicator**, not a failure predictor.

Adding binary SPC alarm flags to continuous sensor and engineered features did not improve PR-AUC. Their feature importance was near zero. This is operationally useful: SQC retained strong value for diagnosis and communication, but contributed little incremental ranking information after the continuous variables were already present.

## From prediction to a bounded decision

The study searched a 60×60 RPM–torque grid under a mechanical-power constraint. Of 3,600 candidates, 1,999 were feasible. A representative candidate was approximately **1,768 rpm, 41.45 Nm, and 7.68 kW**, with a model score of **1.3046%**.

This point is conditional on the observed data, fixed contextual variables, the fitted model, and the chosen grid. It is not presented as a universal causal optimum. Likewise, the score change near 202.7 minutes of tool wear is a tree-model policy boundary, not a physical law requiring replacement at exactly 203 minutes.

## Two core repositories, one study

| Repository | Role |
|---|---|
| **This repository — Paper** | Manuscripts, argument, reading guides, and research interpretation |
| **[Companion Code](https://github.com/doyunsin883-debug/risk-aware-predictive-maintenance)** | Notebooks, data, model artifacts, figures, and reproducibility instructions |

Read the argument here, then use the companion repository to trace each reported number to its analysis stage.

## Citation

> Shin, D. (2026). *A Risk-Aware Predictive Maintenance Decision Framework: From Statistical Process Control and Nonlinear Failure Prediction to Constrained Operating Decisions*. Independent undergraduate research manuscript, Department of Industrial Engineering, Gachon University.

Machine-readable metadata is available in [CITATION.cff](CITATION.cff).

## Scope and AI disclosure

This is an unpublished, non-peer-reviewed independent manuscript based on the public synthetic AI4I 2020 dataset. Deployment would require timestamped plant data, external validation, cost-calibrated thresholds, and review of physical and safety constraints.

Generative AI was used as an assistive tool for **analysis-code implementation and debugging**. During repository publication, it also assisted with document organization and language review. The author remains responsible for the research question, interpretation, numerical verification, claims, and conclusions.

---

© 2026 Doyun Shin. See [RIGHTS.md](RIGHTS.md) for reuse terms.
