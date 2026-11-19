# Complete coupled restart and physical continuation — 17 November 2026

## Advance

Saved the complete coupled dynamical state, proved fresh-process restart
fidelity, and continued baseline and MTS through native-clock epochs2925–2932.
No new force law, coefficient, fit, bank, native DLL, grid, or tolerance was used.

This is a physical continuation of the retained one-mode cosmological evolution,
not another re-scoring of the same saved output window. It does not extend the
902 shifted preparation projections: those require additional supported history
and a separate uncertainty calculation.

## Exact preservation and restart

Both full replays reproduce all24 earlier output arrays bitwise exactly.
They now additionally retain full normalized states at29,766 existing query
times:385 variables for baseline and393 for MTS, plus allocated native
seed/old/change vectors, physical backgrounds, integrated work, normalization
vectors, active layout, seed cache/mask and source manifests.

The original934 native state/derivative/cache/readout rows are identical inside
the942-row capture. All retained regime signatures remain unchanged. Fortran
owners contain process-local pointers; these are rebuilt from the same binary,
parameters and tables, not falsely advertised as portable serialized pointers.
The saved dynamical state is then loaded into that verified owner.

Fresh processes restart at2916 and reproduce37 overlapping queries through2924.
Initial derivatives and metric packets reload bitwise exactly.

| Restart comparison | Baseline | MTS |
|---|---:|---:|
| Worst full native-state difference / frozen component units | 1.73195e-13 | 1.53977e-12 |
| Worst native-velocity output difference / original output norm | 9.22119e-12 | 1.56974e-12 |
| Required full-output tolerance | 2e-5 | 2e-5 |

Both pass. The baseline's much smaller native correction-relative restart
comparison remains unresolved (2.84392e-3 versus2e-5). Aggregate native
correction normalization is not the same as velocity/spectrum precision:
its largest MTS component is a slow-scalar derivative of order1e-16, with an
old normalization6.72285e-17. An order-unity ratio there does not mean an
order-unity baryon velocity, metric change, or loss of perturbative smallness.
Earlier observable correction-relative failures are not promoted.

## New physical interval

Both models advance approximately0.009859 Mpc of conformal time, from
z_scale4409.34384 to4408.78858, at the existing k=5 Mpc^-1. Original clock
indices, starting state and32/64 maximum-step settings are preserved.

| New-interval check | Baseline | MTS |
|---|---:|---:|
| Coherent velocity32/64 difference / original norm | 1.19885e-11 | 1.56974e-12 |
| Coherent spatial trace residual / frozen norm | 4.41497e-8 | 4.47153e-8 |
| Coherent shear residual / frozen norm | 4.41497e-8 | 4.54465e-8 |
| Coherent density-exchange residual / old source norm | 1.62716e-15 | 4.64835e-11 |
| Coherent current-exchange residual / old source norm | exactly zero, zero baseline current | 9.85111e-13 |
| MTS pressure32/64 difference / old pressure norm | structural zero for cold source | 3.31652e-15 |

All these checks pass2e-5 without subtracting the finite-neutrino remainder.
Photon density, native Weyl, relative density and velocity-slip refinements,
metric eta/density/Friedmann constraints, and old/correction exchange checks
also pass. Cold source pressure zero is structural, not an accuracy measurement
of a nonzero pressure. These are finite-step checks, not rigorous error bounds.

The MTS native baryon-velocity repair changes from approximately-1.012812e-7
at2924 to+2.195255e-7 at2932. The final correction is3.17125e-5 of the
original MTS velocity amplitude. This sign change is resolved in the tested
outputs. It is coherent-versus-original MTS, NOT MTS-versus-LambdaCDM, and it
must not be relabelled as a new observed cosmological signal. A constant repair
offset would misrepresent the actual evolution. The baseline correction stays
at unresolved rounding-level values.

The old projected preparation-pressure budget87.5966% remains an earlier-window
result; it is not silently applied to this new pointwise trajectory or a sky
spectrum. Quantum measure, complete line-of-sight observables and galaxy
occupation are separate questions.

## Reusable restart files

- cold-extension-64-terminal.npz
- heavy-extension-64-terminal.npz

These include the full state at2932. The earlier epoch2916/2924 checkpoints,
complete-history files and state-manifest.json are preserved. Use run_checked.py
for fresh-process tests; it verifies immutable state hashes in addition to the
source manifest. Future code must save new outputs separately rather than
overwrite this stage or infer missing hierarchy entries as zero.

## Next physically motivated window

The retained mass and endpoint scale give a local principal frequency
sqrt(k^2+a^2 m_h^2)=34.3574731 Mpc^-1 and period0.182876817 Mpc.
This is the Klein–Gordon principal part, not the full forced-system eigenmode.

The first native clock AFTER that duration is3039, but the original output grid
jumps there: it would span4.32345 local periods, not one. This was caught before
any future response was inspected. next-window-grid-check.json supersedes the
initial endpoint proposal in next-window.json. The recommended endpoint is3038,
the last existing native clock before the target:106 new epochs,0.130515 Mpc,
about0.714 local periods. This is not a claim to have tested a complete cycle.
No grid was altered and no future fit/performance was used to choose it.

## Verification and cleanup

41 consolidated checks pass, including all physical/full-output restart gates,
independent process identities, exact state reloads and native owner releases.
The separate tiny baseline response gate remains false. All580 frozen inputs
and14 immutable state/wrapper files are unchanged. Single numerical worker,
one thread, below-normal priority; no GitHub, other-chat process, browser,
scheduler or service changes. Final cleanup and artifact seal are in closeout.json.

Protocol, CONTRACT.md, the per-case full/restart results, extension-score.json,
verification.json and both terminal checkpoints are authoritative. All source
paths are recorded in protocol.json, inputs.json and state-manifest.json.

