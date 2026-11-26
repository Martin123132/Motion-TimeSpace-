# Replay locally, with no fits or external contact

Use the retained Python 3.13, NumPy, SciPy; PyMuPDF and requests are required only for re-extracting source curves. Run in this directory with one numerical thread. No service or background process is needed.

1. `python -B verify.py` checks the parent seal, source normalization, isospin factors, analytic scalar moment, six independent complex-amplitude checks, the wrong-pole control, spacelike stress, energy slices and the 101 saved product rows. No output file is modified.
2. `python -B elastic.py` recomputes `moments.json` and `products.csv` from the six CSV source curves, offline. `python -B verify.py --receipt` writes `checks.json`.
3. Optional source recovery: `python -B source_curves.py` retrieves versioned scientific figures, checks their bytes against the pinned hashes and compares each exported curve byte for byte if present. No papers are stored or reposted. The two sources are [Dai–Pennington v2, Fig. 3](https://arxiv.org/abs/1404.7524v2) and [Cao et al. v2, supplementary Omnès graph and main pion form factors](https://arxiv.org/abs/2411.13398v2). The signed equation, crossing model and physical subtraction constants are from [García-Martín–Moussallam](https://arxiv.org/abs/1006.5373v1). The raw-source figure is preferred over tracing pixels. These are reconstructions, not raw collision events; energies along a drawn line are not independent statistical observations.

Read the sign convention, retained contributions, cutoff prescriptions and limits in [the derivation](DERIVATION.md), not from the scalar column of a CSV alone. No edits to original photographs, archives, galaxy files or past research checkpoints are needed.
