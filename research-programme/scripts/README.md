# Scripts

These scripts were used to generate and validate many of the checkpoint artifacts.

Most scripts are research utilities rather than a single polished package. They are included for auditability and reproducibility of the public workbench.

## Basic Dependencies

The common numerical scripts use:

- Python 3.11+
- `numpy`
- `scipy`
- `matplotlib` for plotting branches

Some CMB-oriented scripts additionally require `camb`.

## Data Note

Large datasets are not committed. Scripts that reference local datasets should be treated as workflow records unless the corresponding public data are downloaded separately.

