# Final source-tail investigation — 2026-11-17

## Status and authority

Completed a private continuation experiment, a separately isolated arithmetic repair attempt, an independent inherited-defect propagation and a photon/baryon momentum-exchange derivation. No public changes, fitted parameters, altered bank/grids/normalizations or relaxed tolerances.

Last accepted physical state remains epoch3940 in ../mts-physical-time-window-20261117 (authority closeout SHA2569d5ade4b714a5c6226f8efa914e0547ee3c2cb1e90c5cd30363399237c8f42bc).
The original4249 candidate and separately replayed4249 candidate remain RAW-GATE FAILED. They are useful verified evidence, NOT new accepted continuation states. No4250..4252 integration was launched. The prepared clocks for those endpoints are not completed work.

## Completed numerical experiment

Both baseline and MTS evolved3940..4249 at32/64 maximum-step resolutions, preserving309 original intervals, background knots, all accumulated native/K/error/h/f/probes/work and the original934 normalization. MTS has1307 saved samples. The original physical, signed precision, defect-accounting, work controls, physical-work budget and inverse-safety checks pass. Maximum inverse expression0.2658397810049486<1.

The split-state check fails: maximum normalized defect3.140658577649447e-8, scale208.95404699129287, relative1.503037927655126e-10 versus unchanged1e-10. Original artifact verification passes201 checks. This is a failure of an auxiliary decomposition check, not an observed-data discrepancy.

## Derived arithmetic repair: correct but insufficient

For photon and E-polarization ell3..44, (A1-A0)u=-Delta(chi)u. With d=(a1-a0)/a0, Delta(chi)=-chi0*d*(2+d)/(1+d)^2. This removes subtraction of nearly equal streaming derivatives without changing the mathematical operator.

92 saved-state checks pass, including80-digit coefficient checks, native-operator agreement and exact unmodified physical RHS/readouts. Isolated replay changes only84 rows in the total/inherited/generated auxiliary error and signed-probe derivatives. Both unchanged cold controls are reused with hashes; MTS32/64 are recomputed from the accepted3940 state. No inherited error is reset.

Repaired raw split relative1.510070107211475e-10 still FAILS. Physical outputs agree with the original candidate within the unchanged2e-5 comparisons, and145 independent technical checks pass. The repair is NOT accepted as a sufficient remedy. Both sides of its RHS-diagnostic representation switch are saved in photon-difference-replay-v2/join-32.json and join-64.json.

## Cause tested from the equations

Since e'=Ae-r, h'=Ah and f'=Af-r, the existing defect d=e-h-f obeys d'=Ad. A saved nonzero d(t0) must propagate; demanding a later zero without accounting for it is not the exact inherited identity.

We independently evolved this nonzero defect and the existing background equations, without interpolating a target discrepancy into a forcing term or rerunning the physical matter solution. Original units, knots and tolerances remain. Each32/64 restart seed was separately evolved at both maximum-step resolutions; this distinguishes numerical refinement from different initial seeds.

For the64 seed:
- saved initial defect maximum6.888072334731987e-9;
- observed later maximum3.1553526014249655e-8;
- predicted inherited maximum3.15537034263242e-8;
- maximum remaining discrepancy across all saved times/components8.331734650152817e-11, approximately0.2641% of the observed maximum;
- remaining discrepancy/original split scale3.987352611791147e-13, below the unchanged1e-10 comparison;
- same-seed refinement5.4527218274952535e-15 relative to the predicted defect amplitude.

The32 seed independently gives remaining discrepancy3.573368102515561e-13 on the original scale and same-seed refinement9.328050234721103e-15. All33 technical checks pass, including exact background-RHS checks at9 points per seed. This supports inherited amplification as the dominant cause on this interval. It is a numerical verification, not a certified continuum bound. Neither raw failed gate is retroactively turned into a pass.

## New photon/baryon exchange result, using ACCEPTED history only

Using only the accepted history through3940, derive
J=(4/3)B_gamma*chi*(v_b-3q_gamma/4),
where B_gamma=kappa_grav*a^2*rho_gamma and native J has units Mpc^-3.

Within the retained fixed-ionization branch, B_gamma and chi each scale as a^-2. Thus A=(4/3)B_gamma*chi scales as a^-4, and the exact finite response is
Delta J=A0[(1+alpha)^-4 Delta s+((1+alpha)^-4-1)s0].
The coefficient difference is evaluated without near-equal subtraction. The existing gravitational and scattering constants are retained inputs, not newly derived constants.

14 exact rational identities and36 independent native-RHS checks pass, including equal/opposite photon/baryon exchange. Readout replay is exact. MTS parent final coherent-minus-original Delta J=9.909432197219827e-15 in native units; the parent/approximate comparison including numerical allowance is9.727487168856106e-7 relative, below2e-5. Parent response own precision4.90084641308192e-7 passes.

The cold baseline tiny response precision0.010815779264211718 FAILS the2e-5 requirement and remains unresolved. Do not substitute zero, call this an MTS-minus-baseline detection, or infer an energy-heating/spectral-distortion prediction. This is a momentum-exchange bridge on the retained background, with the quantum measure separate.

## Implementation receipts

A first repair launch failed while serializing initial diagnostic arrays, BEFORE integration. A second scoring invocation selected an older same-named score_live module after inherited path changes, AFTER both complete physical replays. Both errors, failure receipts and original sources are preserved. JSON serialization was fixed in a distinct output version; scoring now resolves the exact stage module by absolute path. No physical calculation was discarded or rerun to hide a failed result.

See verification.json; repair-probe-result.json; photon-difference-replay-v2/verification.json; split-defect-transport/result.json; accepted-photon-exchange/result.json and verification.json. closeout.json and cleanup.json supply integrity and ownership receipts.

