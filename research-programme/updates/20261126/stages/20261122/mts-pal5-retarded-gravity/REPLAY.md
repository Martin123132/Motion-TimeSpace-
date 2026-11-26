# Replaying this private calculation

Use the retained local Python 3.13 installation with NumPy and SciPy. In this directory run each item with Python's -B flag. Source guards pin the preceding bridge and the original wave and force banks. Numerical workers set BLAS/OpenMP to one thread. The owner stop files are honoured at each step. Run at most two numerical jobs at once. Keeping results is intentional; writing an existing packet requires byte equality.

1. Run controls.py for the manufactured nonlinear ±amplitude and gauge tests.
2. Run response.py with arguments 2 32 own, 2 32 cross, 2 16 own, and 3 32 own. Each generates separate calibrated predictions and current ledgers, without reading corrected trajectories.
3. Run direct_pulse.py to test the early-drive prediction against a direct, nonlinear source change. Then run pulse_memory.py and sign_contrasts.py.
4. Run compensated.py freeze **before** compensated.py run. This records all four source-only two-history predictions and pins their hashes in the later finite experiments. Run compensated.py refine after the finer response runs.
5. Run compare.py, report_numbers.py, then verify.py. The verifier reopens the saved arrays, checks the early equal-source prefix, input hashes, controls and row counts, and writes or checks the file seal. Numerical *scientific* failures remain rows in the output; they are not deleted to pass integrity validation.

Reading order: RESULTS.md, DERIVATION.md, COMPENSATED.md. Raw vector packets as well as aggregated errors are retained. No remote service, observer velocity labels, free population parameter, downloaded package or new public repository action is part of this calculation.
