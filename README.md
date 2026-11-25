# Low-Cost Wearable for Activity Monitoring

**How many sensors, where, and how fast?** · FENG 497 · Group 61

We look for the smallest, cheapest and most energy-efficient IMU setup that still recognises daily activities accurately. From the public PAMAP2 dataset we build 126 sensor configurations (7 placements × 6 sampling rates × 3 channel sets) and score each one on:

| Score | Measure | Work package |
|---|---|---|
| Accuracy | macro F1, Random Forest, leave-one-subject-out | WP5 |
| Battery life | days, datasheet-based power model | WP4 |
| Cost | hardware cost per kit | WP7 |

The configurations that no other setup beats on all three form the **Pareto front**. An interactive dashboard (WP6) recommends a setup for a given budget and battery life.

## Repository structure

```
├── src/g61/       # project code (Python package)
├── notebooks/     # base notebooks from the supervisor + experiments
├── dashboard/     # Streamlit dashboard (WP6)
├── tests/         # tests (run with pytest)
├── data/          # PAMAP2 is downloaded here (not in git)
├── outputs/       # generated tables and figures (not in git)
├── requirements.txt
└── pyproject.toml
```

## Setup

```bash
git clone https://github.com/Ezgiercin/FENG497_Group61.git
cd FENG497_Group61
pip install -r requirements.txt
pip install -e .
```

## How we work

1. Do not push directly to `main`. Create a branch for your work package
2. Open a **Pull Request** into `main`, one other member reviews it before merging.
3. Do not edit the base notebooks in `notebooks/`. Work on a copy (e.g. `notebooks/wp5_ezgi.ipynb`).
4. Do not commit data or outputs, the pipeline recreates them.


## Data

Reiss A., *PAMAP2 Physical Activity Monitoring*, UCI Machine Learning Repository, 2012, doi:10.24432/C5NW2H, CC BY 4.0.
