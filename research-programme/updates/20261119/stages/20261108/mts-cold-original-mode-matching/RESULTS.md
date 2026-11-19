# Original-mode matching verified — 2026-11-08

## Advance
The original native perturbations now have explicit, tested initial coordinates in the retained physical-relative, metric-closed and phase-mean systems. This connects the next transport calculation to the original preparation instead of inventing a late cold mode. Baseline and MTS, all three wavelengths, and GR/spatial-Poisson use unchanged physical tolerances.

The physical relative phase is derived directly:

    delta = delta_rho_h/rho_h,
    W = [k²/(a*m_h*H)]*delta_theta,
    y_h = [sqrt(rho_h)*H/k]*(delta,W),
    bar_z_0 = [I+C(theta_0)]^-1 R_phys B_phys u_original.

Full derivation: DERIVATION.md. All 190 tail multipoles at each of five massive nodes are retained. The phase-dependent transformation's compact support is derived from the source structure and checked against full G192; it is not a truncated evolution.

## Preserved preparation
- Original MTS start N=-8.518454909126145; baseline -8.518454909064344.
- Original physical heavy phase -2.135154055031886 radians; initial computational carrier chart is zero. These are distinct.
- Exact initial mu=2122.173930840893; mean-background mu=2122.314934618322.
- G192 dimensions: half-k MTS/baseline 1118/1116; balanced and double-k 1064/1062.
- The existing early reference ends near N=-8.29320292518 (24685 MTS and 5402 baseline saved epochs). Cold entrance is N=-1.0140872889512205. This stage saves initial matching, not an intervening trajectory.

## Initial background shift carried explicitly
The saved invariant gives rho_mean/rho_exact=exp(-0.0006390695394492348). Its identity agrees within 7.113e-17. The resulting initial conformal-H change is -6.643866804456611e-5 and rho change -7.934896778153495e-8 in inherited conformal-density units.

Norms of bar_z_mean,0-bar_z_exact,0:
| Wavelength | GR | Spatial Poisson |
|---|---:|---:|
| half | 1.108322458423e-6 | 1.108335361842e-6 |
| balanced | 3.968784099848e-7 | 3.968791127933e-7 |
| double | 3.974294940021e-8 | 3.974296869180e-8 |

Corresponding exact mean-coordinate norms are approximately .0116530, .00492624, .00146861. These are matching errors in the retained physical norm, NOT observed spectrum residuals or fractional constraints. Baseline replacement differences are exactly zero; its independent numerical evolution error is not assumed zero.

The periodic endpoint correction is nonzero too: exact-background norm approximately 3.78237e-6, 1.69107e-6, 5.60764e-7 for GR, with separately saved Poisson values. It is kept, not absorbed into a fitted amplitude.

## Checks
- 12 model/background/wavelength preparations and 24 gravity-branch endpoints.
- Five exact symbolic density/phase identities; 12 independent model cases; 70-digit scalar differentiation for the six heavy cases.
- Native early generator absolute discrepancy <=3.311653e-8, below unchanged GATE=2e-5.
- Independent physical phase/density coordinate discrepancy <=5.998520e-12.
- Full original-coordinate reconstruction <=7.429201e-13; ALGEBRA=1e-10 unchanged.
- Phase closure relative <=8.307859e-16; derivative reconstruction <=1.568149e-14.
- 128-subset versus original 256-node mean <=2.576716e-18; initial primitive <=2.100965e-14.
- Frozen off-grid source error relative to phase variation <=2.512127e-13.
- All-phase norm bound for the computed Fourier primitive <=0.000665939126 <1, giving a positive endpoint inverse margin. This polynomial bound is not a new continuum alias-error theorem.
- All used source tables/layouts agree with prior sealed artifacts. Original trajectories agree with their accepted hashes. No existing checkpoint or physical grid was changed.

## Reuse paths
Each of half/, balanced/, double/ contains:
- preparation-01/*-{exact,mean}-prepared.npz: original raw/encoded/normalized state, complete physical and closed state, all coordinate maps.
- preparation-01/*-{exact,mean}-source.json: original parameters, source/thermal jets, layout and provenance.
- phase-matching-01/*-{exact,mean}-endpoint.npz: complete restart-ready mean coordinates, both gravity branches.
- phase-matching-01/heavy-*-primitive.npz: mean matrix, Fourier primitive and actual-phase endpoint.
- phase-matching-01/*-mean-background-endpoint-difference.npz: signed complete initial mismatch.

independent-matching/result.json and audit/result.json are the accepted checks. All eight task-owned numerical workers succeeded and exited; CLEANUP.json/closeout.json provide the final process/artifact receipts. Local only, no GitHub, compiler, app/server, subagent or process kill.

## Normalization caution
Density/phase entries in the independent report are linear transfer tangents in the retained solver's normalization. They are not finite angular excursions or a newly calibrated primordial amplitude. A tangent can exceed one radian per unit amplitude without being a finite-angle solution. No nonlinear perturbative-validity claim follows from these coordinates.

## Next physical test
Use the saved early trajectory as a controlled reference. Evolve the mean system over a bounded first early interval from these original matched states; reconstruct physical outputs with the final endpoint map, carry the signed initial background mismatch, and compare baseline/MTS and both gravity branches. Qualify time interpolation/averaging remainder before extending through the early-to-cold gap. Reuse the existing native source and restart vectors; do not rerun the original 24685/5402-point reference or launch a late unit-vector test.

