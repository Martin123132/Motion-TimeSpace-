# Offline replay, source inputs and evidence limits

Python 3.13 on Windows x64 with NumPy/SciPy. Use the same pinned sibling directories as the four-pion photon stage, including its previously tested single-threaded angular sum. The new scattering angular integral is analytic and implemented in Python; there is no new binary to build, new calibration, Monte Carlo seed for integration or network dependency. Controls use a fixed seed for permutation choices. The central pulsar transfer is read from the pinned archived CSV independently of the pion code.

Run from this directory, with OPENBLAS_NUM_THREADS=1, MKL_NUM_THREADS=1, OMP_NUM_THREADS=1, sequentially:
1. `python -B calculate.py` — rebuild the projected six-leg source, primary Table I comparison, threshold/elastic checks, 16 energy/refinement rows and diagnostics.
2. `python -B disperse.py` — 26 quadrature rows across energy and phase-space refinements, subthreshold shifts, signed window budgets and finite differences.
3. `python -B same_window.py` — uses the saved sources to integrate the same-window response both ways around the principal value. No new scattering evolution.
4. `python -B reciprocal.py` — separately use the complete crossed amplitude, original explicit charge amplitudes and reversed angular integration for the imaginary-product cancellation.
5. `python -B parent_readout.py` — convert the specified direct and two feedback allocations using the already computed central orbital ray.
6. `python -B verify.py` — check stage inputs, row counts, hashes and control ranges. Do not reseal on a changed result. Previous stages are read only. No persistent process is needed.

The detailed primary source is [Bijnens & Husek, Phys. Rev. D 104, 054046 (2021)](https://doi.org/10.1103/PhysRevD.104.054046); their LO six-pion amplitude is imported and independently evaluated, not claimed as an MTS invention. The projection onto the saved production sources and signed finite-window tests are local calculations. Signs refer to the Born-normalized convention set by the previous photon stage. The four-body state uses degenerate charged/neutral masses and the leading effective action; higher chiral orders, electromagnetic final-state effects, higher-energy spectral weight and local parent matching are not uncertainties measured by a replay.

