# Local replay

Run from this directory with the retained Python 3.13, NumPy, SciPy and SymPy; use -B, serial execution, no extra workers or downloads. The physical history and upstream code are located by the earlier sealed chain. This is not a standalone public package.

Fast receipt: `python -B verify.py` verifies the existing local hashes and paired checks without launching an evolution. Before that, the original LMC retarded replay can be checked **separately** in ../mts-lmc-axisymmetric-retarded-replay-20261120 with `python -B replay.py`. The local signed-band margin verifier thereabouts does not use any matched-speed outputs.

Full speed-family replay, in order:

1. `python -B family.py prepare 5 1 2 4 8 3.125`.
2. `python -B family.py run 5 120 48 1 2 4 8 3.125`.
3. `python -B speed_collocation.py 5 120 18 1 2 4 8 3.125` and repeat with grid 160.
4. `python -B timeline.py extended` prepares and propagates q=16,32; `python -B timeline.py 2 4 8` independently checks the original endpoint files and saves partial time integrals.
5. `python -B newton_history.py`, `python -B stress_projection.py`, `python -B dust_control.py`.
6. `python -B score.py save`, `python -B curvature_test.py`, `python -B verify.py`.

Existing packets are verified rather than overwritten. Score and curvature products require the complete input set; run them only after both integrations have finished. The q32 full-duration stress comparison is an intentional recorded failure. Integrity success must not change it into a physics pass. Degrees, subdivisions and signed/host-free branches are encoded in packet names; the generated directory holds only this stage. No persistent server or job is required.
