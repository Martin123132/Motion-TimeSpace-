# Local reproduction and stop point

Use the retained Python environment (NumPy and SciPy), the unmodified sibling primordial-patch stage, and its upstream research inputs. All commands start in this folder. Run serially, with Python's `-B` switch; source.py limits numerical libraries to one thread. Placing STOP-REQUESTED here stops the next guarded batch. Nothing needs to be fetched or fitted. Do not rerun full evolutions merely to check saved bytes.

**Integrity:** `python -B verify.py` checks the pinned predecessor and all sealed local files, final branches, positive original masses, signed folding, two-time replay and interference, source/force tests and local balances. File names with `from0.600000` / `from0.400000` refer to continued segments. Their JSON `origin_events` marks the first negative label seen *in that segment*, **not a second first crossing**. The corresponding earlier non-continued restart contains the actual first-crossing bracket.

**Examples of how the saved run was generated.** In a fresh reproduction folder preserving the same relative layout and upstream inputs, the gravity and wave grids are specified in comoving Mpc and the evolution rate is steps per unit log(a). Heavy/cold use their own prepared restart:
    
    python -B evolve.py heavy --spacing .00625 --steps 2048 --stop .60 --action
    python -B evolve.py heavy --spacing .00625 --steps 2048 --action --continued restart-heavy-h0.00625-n2048-L24-to0.600000-sine-action
    python -B evolve.py cold --spacing .00625 --steps 2048 --stop .40 --action
    python -B evolve.py cold --spacing .00625 --steps 2048 --action --continued restart-cold-h0.00625-n2048-L24-to0.400000-sine-action
    python -B evolve.py heavy --steps 2048 --action --split 2 --keep-knots
    python -B evolve.py cold --steps 2048 --action --split 2 --keep-knots

The 40-Mpc pair changes `--box 40`; the fine continued pair uses spacing .003125 and 4096 for the final segment; the finest pair .0015625 and 8192. The end is set by the predecessor. Uniform-volume gravity, cubic-density and earlier overlap diagnostics are separately named. The seed is a conditional coherent spherical cosmological realization, not an empirically measured Galactic state.

**Readout:** `checks.py` and `binding_checks.py` exercise manufactured and gravity-variation controls. `binding.py <restart stem>` evaluates energy on positive classical sheets and frozen wave capacity. For a heavy restart run `population.py <restart stem>` to extract the negative-wave occupations, then `weak_operator.py <restart stem>` for the independent spatial weak balance. `hilbert.py <restart stem>` evaluates either branch; `hilbert_check.py` reconstructs the real scalar cycle on the split final sample. `tagged.py heavy split` and `tagged.py cold split` start at a common 0.65; replace split by matched or fine for separate refinement tests. Changing a model, epoch, potential or boundary requires a new experiment, not silently replacing a sealed file.

**Next meaningful diagnostic:** compare the time-dependent negative-subspace transfer and outward flux at fixed preparation on the two gravity meshes before quoting a population fraction. The original LMC task is separately reproducible, without running the spherical formation extensions: from the sibling `mts-lmc-axisymmetric-retarded-replay-20261120` run `python -B replay.py` then `python -B density_to_bands.py`.
