# Private reproducibility

Use Python 3.13 with the retained NumPy and SciPy environment. Leave the sealed packet directory intact. From this directory, python -B verify.py only reads the archive, reconstructs the signed histories and numerical budgets, reruns the one-launch constraint, checks the previous 40 file hashes and verifies this seal. It does not launch a forward evolution. Clock times, radii, field amplitudes and mass use the retained numerical units.

For a new replay use a separate empty sibling of this directory, within the same post-checkpoint-work tree. Copy only its Python and Markdown source files; the earlier frozen research siblings must be available unchanged. Generate in order, never over existing packets:

1. python -B launch.py -1, then python -B launch.py 1, then python -B launch.py freeze. This is the original prospective packet set; original forecast scores are never replaced.
2. python -B receiver.py 40 80 160; python -B score.py. These are independent free-fall evolutions (synchronous cell-centred vs polar areal node-centred), sharing only the physical launch profile and constants. No fields are initialized from evolved forecasts; the freeze is verified before any receiver run. The radius labels in the output are the areal radii at release.
3. python -B refine.py 7680; python -B assess.py 7680. If the addendum gate requires it, python -B refine.py 15360; python -B assess.py 15360. These are labelled post-forecast checks, not extra blind tests.
4. For the half-strength controls, python -B -c "from receiver import calculate, MODELS; [calculate(160,model,amplitude) for model in MODELS for amplitude in (-.5,.5)]"; then python -B assess.py physical.
5. python -B force_clock.py capture; python -B force_clock.py 15360. Only the initial physical data and the original equations enter the force replay; comparison with the opposite coordinate system uses complete histories, not an endpoint fit. python -B prepare.py solves the separate one-event launch constraints.
6. In the new directory only: python -B verify.py seal, then python -B verify.py. Saved old packets are not assumed bitwise portable across SciPy/BLAS or Python versions. The original prospective inputs, hashes, full histories, reported thresholds and units should be preserved when comparing platforms.

Full positive and negative records are stored separately. A sign suffix −1/+1 is the impulse orientation, not a choice of gravity theory. The half difference is a controlled intervention, not an observable time series from two real universes. Files named clock-transfer concern simulated changes in areal radius; frequency transfer along a photon between clocks is a different observable.

