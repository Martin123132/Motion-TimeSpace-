> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Reproduce the transfer

From this stage run `python -B verify.py` with one numerical thread (set OPENBLAS_NUM_THREADS, MKL_NUM_THREADS and OMP_NUM_THREADS to 1). Uses the previously retained NumPy/SciPy environment and sibling checkpoints. The verifier first verifies the preceding seal, regenerates both sets of integrals, angular bounds, disk controls and all four numeric outputs, then checks every file against this stage's seal. Does not write to upstream stages or require network access. No external numerical service, fit, observing-data change or worker to resume.

Upstream pion inputs (not bundled here) · static optical normalization (not bundled here) · binary scale only (not bundled here). External analytic control: [Bellazzini, Isabella, Lewandowski and Sgarlata, v3](https://arxiv.org/abs/2108.05896v3), eikonal amplitude and Fourier prescription; scalar-loop appendix. Inspected arXiv TeX file TimeDelay_v3.tex SHA-256 3b6f28fea9761dae1a4ab2fef2df18dc486a4f55496d7fa74f3c95898cd4f2f7; equations used are specified in [the derivation](DERIVATION.md). No external code copied.
