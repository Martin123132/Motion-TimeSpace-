> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Local reproduction

Keep this directory beside the pinned [signed Newtonian comparison](../mts-newton-cloud-clock/RESULTS.md) and its unchanged parent inputs. Use the retained Python 3.13, NumPy, SciPy, SymPy and local MTS environment. All commands are local finite jobs, each with one numerical thread and no downloads. Existing generated results compare bytes rather than being overwritten. The checks include failing scientific gates; a verified release is not an assertion they all pass.

1. Independent controls: `python -B fixtures.py`, `python -B fixtures.py stagger`, `python -B instrument.py`, `python -B exact_dust.py`, `python -B cold.py stagger`.
2. The signed point solver is `python -B evolve.py GRID STEPS PROJECT METHOD [EDGE [NATIVE]]`; defaults are EDGE=6 and NATIVE=5. The finite-width solver is `python -B window.py GRID STEPS PROJECT METHOD [NATIVE]`. The release configurations are identified in [the campaign runner](evidence-001.zip) (archive member: `replay.py`). Every group includes the six combinations of host and pressure switch.
3. Newtonian detectors: `python -B window_newton.py 5 8`, `python -B window_newton.py 4 4`. These integrate each physical aperture rather than substituting its midpoint; all three archived point readings are compared exactly in the same invocation. The separate local Newtonian part is from `newton_local.py`.
4. Independent source splits: `python -B source_budget.py 120 96 5` gives intrinsic/extrinsic, kinetic, stress and rest contributions. Adding a final `1` produces the real-wave amplitude/phase split. `python -B stress_forecast.py 5 8` predicts those terms from the Newtonian clock and formation equations. Mesh 4 checks are included in the runner.
5. Use `python -B replay.py sample` for the lightweight representative comparison; `python -B replay.py all` for a serial campaign from existing inputs. Use `python -B verify.py` for the sealed data and gate check. No scheduler, server, or continuing worker is required.

Neither the Galactic force-band comparison nor the late-time cosmology fits were rerun or recalibrated here; this calculation concerns the prepared early cloud only.
