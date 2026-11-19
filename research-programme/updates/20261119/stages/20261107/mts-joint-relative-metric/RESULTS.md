# Joint relative-phase/metric stage: local result

Completed2026-11-07. Parent:
../mts-relative-phase-perturbations-20261107/RESULTS.md.
Same retained action, physical parameters, source bank and tolerance gates.

## The advance

The relative-phase transformation now includes gravity and the remaining
matter as one coupled system. With metric u=L_h y+L_r r and y=Tz+Vu,
we solve (I-VL_h)y=Tz+V L_r r and derive the full transformed generator.
Metric derivatives follow the coupled equations; they are not discarded
or assumed to be a slow externally imposed signal.

The new feedback inverse is uniformly well conditioned on the saved
cold interval. The bound applies to every scalar phase and any nonnegative
external quadrature enthalpy consistent with the stated positive branch.

| Inherited k label | GR bound on norm(V L_h) | Spatial-Poisson bound |
|---|---:|---:|
| half | 2.464498223e-11 | 1.234380304e-11 |
| balanced | 1.553218911e-12 | 7.819567911e-13 |
| double | 1.008461849e-13 | 5.178569801e-14 |

These are bounds on the additional coordinate-inversion correction,
NOT evidence that gravitational coupling or gravitational growth is tiny.
The full metric/matter feedback stays in the generator.

## Native and saved-history checks

- All six native model/wavenumber cases pass for GR and spatial Poisson.
  There are612 full-vector comparisons including the retained G192 hierarchy.
- Worst native generator discrepancy:6.972465731e-8, below unchanged2e-5.
- Worst algebra/roundtrip check in the native qualification:5.594525446e-12,
  below unchanged1e-10.
- Inverse-derivative refinement:1.406387368e-8; independent product-rule
  discrepancy:5.771237103e-9. Both pass the original numerical gate.
- Native tail agreement:2.606443594e-14. Native baryon pressure, radiation
  closures, current, shear and quadrature enthalpy defect remain present.
- Twelve existing prepared histories were transported at156 selected
  epochs, including every initial/final endpoint. Maximum saved physical
  readout discrepancy:2.647489325e-8; state roundtrip:2.971680234e-13.
- 8,640 phase/positive-enthalpy fixtures check the implementation of the
  analytic cold bound; they are not used to infer its supremum.

Native generator errors use the maximum absolute component difference
divided by the larger maximum component of the compared vectors. Saved
physical-readout errors use each observable's maximum saved amplitude
across its13 selected epochs. No denominator is fitted to the outcome.

The native checks use the owned EARLY resolved histories. The cold inverse
bound uses the accepted LATE mean background and its tube. These are
distinct pieces of evidence: we did not generate a late microscopic phase
or a new late coupled trajectory.

## Failure preserved, not hidden

native-half-01 exited before the first joint coefficient test because
the reused canonical extractor expected the adapter name check_parent.
IMPORT-DIAGNOSIS.md records the cause. The failed receipts/context remain
in half/ and native-half-01.* and are not accepted scientific output.
run_native_v2.py supplies the existing input-check function under that
name and writes to separate *-qualified folders. Physics and tolerances
are unchanged. Every accepted native and history run then passes.

## Evidence and reuse

- summary/result.json: phase-uniform inverse bounds and fixture results.
- half-qualified/, balanced-qualified/, double-qualified/: native coupled
  generator, metric, stress, derivative and G192 checks.
- half-histories/, balanced-histories/, double-histories/: small transported
  packets, source hashes, original prepared endpoints and readout comparisons.
- audit/result.json: independent recomputation of saved readout errors,
  source integrity, syntax checks, acceptance summary and excluded failure.
- DERIVATION.md, joint_math.py and native_joint.py: exact transformation,
  assumptions and its native implementation.
- CLEANUP.json and closeout.json: final owned-process exits and artifact seal.

Only one numerical worker/thread ran at a time. Native context creation
replays its retained prefix to verify the saved preparation, but no new
background or late perturbation solve was launched. No subagents, GitHub
actions, original checkpoint edits or bank/grid/tolerance changes.

## Next

Derive the phase-averaged COUPLED growth equations from this explicit
generator, keeping the correlations with gravity and other matter, and
bound their remainder. Transport the existing early preparation rather
than assigning a late initial mode. Then use that controlled evolution
for matched GR/spatial-Poisson histories on the unchanged cold interval.
