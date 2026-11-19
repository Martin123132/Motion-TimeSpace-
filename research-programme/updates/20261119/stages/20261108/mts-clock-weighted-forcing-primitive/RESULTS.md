# Clock-weighted response completed and verified

2026-11-08. Local completion of the previously safe-partial stage after an app restart. The four pending controls were first launches, not reruns. All earlier evidence remains intact. The broader MTS programme remains active.

## Physical and mathematical advance

The complete saved forcing is represented as f(N,theta)=sum_j B_j(theta) F_j(N). The derived clock-weighted primitive obeys

    Omega partial_theta J = f - fbar
    mean_clock J = 0
    delta = eta + J
    eta_N = M eta + fbar + M J - J_N.

This retains every original real Fourier term, including both Nyquist components, both normal-form and coordinate-map forcing, and the full G192 hierarchy. The required initial offset eta(initial)=-J(initial) preserves the original zero local increment on top of the inherited physical state. It is not a late preparation or a replacement theory.

Differentiating the clock-weighted normalization derives the mean correction

    mean_clock(M J - J_N) = -mean_clock((Omega_N/Omega) J).

The mean drive therefore need not equal fbar alone. DERIVATION.md and MOVING-CLOCK-MEAN.md contain the construction and its precise derivative scope. No coefficient was fitted to the reference discrepancy.

## Completed comparison matrix

All eighteen response jobs are accepted: three wavenumbers, baseline/MTS, fine/time-coarse/auxiliary-kernel-coarse. Each job retains both GR and spatial-Poisson branches. All five postprocessing steps are complete for each wavenumber.

The full audit independently verifies:
- 54 paired source/derivative validation records.
- 36 branch-level response regressions from eighteen response jobs.
- 120 physical channel comparisons, each over the original five probe epochs.
- 240 propagated physical control records.
- 36 oscillatory residual groups, covering both forcing components and branches at three epochs per wavenumber.
- 37 accepted result reports, their dependencies, frozen sources, original seals and the unchanged safe-partial artifact set.

ALGEBRA remains 1e-10; the numerical gate remains 2e-5. The response uses the original DOP853 rtol=2e-12 and atol=2e-14 with 4096/2048 step caps. The auxiliary kernel control uses65/33 nodes; it does NOT change the original nine forcing epochs, physical grids, thermal/scattering bank or histories.

## Direct-response agreement

| Comparison against retained direct response | Largest relative difference |
| --- | ---: |
| MTS fine, relative to the small correction | 7.718329358746032e-13 |
| MTS auxiliary-kernel coarse, relative to correction | 6.589792037088034e-13 |
| MTS time coarse, relative to correction | 2.3251658902677814e-12 |
| Separate forcing-component regression, all MTS jobs | 2.325569473603737e-12 |
| MTS difference relative to leading physical state, all jobs | 4.643812750206321e-19 |
| Baseline time coarse, relative to correction | 1.6612602243085326e-12 |

Baseline fine and auxiliary-kernel-coarse arrays reproduce their retained fine response exactly in these tests. This does not imply that the baseline's underlying physical solution has no numerical error. Corrections are assessed separately from the large state so that small-scale error is not hidden by normalization.

## Original physical readouts remain within the unchanged gate

These errors compare each model/branch to ITS OWN original full-equation reference, not MTS against baseline and not GR against Poisson. No new observational fit is performed.

| Wavenumber family | MTS GR | MTS spatial-Poisson | Baseline GR | Baseline spatial-Poisson |
| --- | ---: | ---: | ---: | ---: |
| half | 2.072881286154049e-6 | 2.0672307489057578e-6 | 2.2403788482234975e-10 | 9.87363816903019e-11 |
| balanced | 1.7126491898336047e-6 | 1.7127709207944389e-6 | 9.721170556465998e-11 | 1.9865195364880394e-10 |
| double | 2.0290360211662155e-6 | 2.028980654866233e-6 | 2.5725274419107975e-10 | 2.5731217641337553e-10 |

Each number is the largest of ten channel-normalized discrepancies over the fixed five epochs. The largest MTS channel is Q in all six entries. Representation-control differences propagated into physical readouts are at most1.1641771849088964e-18 for MTS and1.478837947875238e-39 for baseline.

## Oscillatory reduction, measured without discarding the residual

The ratios below compare clock-weighted RMS of the remaining oscillating part of M J-J_N to the original oscillating forcing. They cover nine sampled source locations per row: three epochs for each of three wavenumbers.

| Component / branch | Minimum ratio | Maximum ratio |
| --- | ---: | ---: |
| normal-form / GR | 0.00843116890661742 | 0.039339144700373106 |
| normal-form / spatial-Poisson | 0.050756804548695356 | 0.17365412706960093 |
| coordinate-map / GR | 0.0006604971168209069 | 0.0010447060591473542 |
| coordinate-map / spatial-Poisson | 0.0006628489626086826 | 0.0010436028537502352 |

Thus normal-form oscillation is reduced by approximately96.1–99.2percent in GR and82.6–94.9percent in spatial-Poisson; map forcing is reduced by approximately99.895–99.934percent. These are finite-domain forcing measurements, not observed cosmological improvement, uniform operator bounds or runtime speedups. All residual terms were retained during every response solve. The derived moving-clock mean identity agrees to5.961498227789101e-16 under its residual normalization.

The smallest fixed-N all-phase clock lower bound at the65 tested kernel nodes is2765.526062747708. The largest primitive/normalization identity residual is1.5763824704287567e-15. These fixed-N phase bounds do not by themselves enclose every intervening N.

## Error budget carried forward

The transformation's excellent agreement is a representation test. It does not remove the inherited nine-versus-five forcing-history uncertainty (about7.995e-5 relative to the small direct correction in the completed parent), the first-response omission R_total delta, background/source reconstruction uncertainty, or inherited interval error. Numerical physical-scale controls and continuum enclosures are distinct.

F_j,N is the exact derivative of the complete retained forcing interpolant. An independently derived microscopic operator derivative at every N has not been silently substituted. The next physical task is a source-conditioned accumulated-response bound using the original preparation and endpoint maps, before accepting a slow-only evolution or transporting it farther.

## Crash recovery, execution and receipts

The original SAFE-CHECKPOINT-01.json SHA256 is0109780b97f4d9435574e8f136e820d281c0bffa0e2a531c260e83a08c29cbbd. Its261 artifacts were checked before resuming and again by the full audit. The original no-start marker remains: it records an intentional earlier four-hour handover and was resolved by one first launch after that marker.

New resume_window_02.py/run_window_02.ps1 renew only the temporal guard in memory within the recorded22:21–02:10UTC window. Every original owner-hold clause and scientific source byte remains unchanged. Both launcher and target hashes are recorded. The original auditor draft is preserved; audit_primitive_stage_v2.py is the accepted full auditor, recognizing the documented safe handover without deleting it.

All39 numerical-process receipts in this stage terminate successfully, including the29 previously completed workers and ten continuation invocations. CLEANUP.json and closeout.json are produced only after verification that those exact identities have exited and all audited artifacts remain unchanged. No process was killed, no compiler/app/server/subagent was started, and no GitHub action or other-chat modification occurred.

Authoritative machine-readable result: audit/result.json. Final immutable manifest: closeout.json. Read NEXT.md for the next calculation, not NEXT-SAFE-01.md, which is retained historical evidence.
