# Joint field-space and Gram refinement of the frozen candidate

Private continuation of `DERIVATION-20260920-complete-frozen-candidate-and-source-response.md`.

Status: COMPLETE for two joint spatial refinements, all-mode homogeneous response comparisons, and arithmetic controls. This is still the homogeneous scalar block on the prescribed original physical metric. The source reaction is an endpoint diagnostic, not an evolved source force. No original live action or earlier physical discrepancy is replaced.

## 1. The discriminating question

The preceding primary and alternative MTS extensions produced almost identical bulk field responses but a0.706588% difference in the final source diagnostic. Their arithmetic agreed much more closely than that. We now test whether the difference shrinks when the entire spatial approximation is refined, rather than choosing the extension that happens to look closer to the reference.

Both MTS rules and the reference receive the same spatial hierarchy, initial physical fields, time interval, arithmetic tests and backwards recovery. Each branch retains its own original saved physical metric. This is a numerical consistency comparison, not model selection against observations.

## 2. Refinement that does not discard or change the initial field

Every cell of the saved common P2 mesh is bisected. The fixed reference source anchor remains a cell boundary with the original constrained field value. All other endpoints and midpoints supply the refined free field variables. The Gram knots are the refined free nodes, using the previously defined primary or alternative nonuniform action.

| Level | Field variables | P2 cells | Gram knots |
|---|---:|---:|---:|
|0, previous result |1,094 |547 |1,094 |
|1 |2,188 |1,094 |2,188 |
|2 |4,376 |2,188 |4,376 |

These are not the earlier2,187/4,373-knot tests of a fixed field space. The field space itself now refines, and each newly added field degree of freedom is evolved. Every cell shrinks, not just cells beside the source.

Let E_l embed the original P2 space into refined level l by exact rational polynomial evaluation, and R_l evaluate the refined field at the original degrees of freedom. The checks establish

    R_l E_l = I

exactly, and verify exact preservation of the unweighted mass and gradient forms for independent rational fields. Initial displacement and velocity are embedded, not re-fitted or re-sampled from a different continuum profile. Recovering the actual saved initial fields changes them by less than1e-55 in the64-digit assembly.

Integration boundaries are the union of the original physical-geometry cuts and ALL exact rational child-cell boundaries. New midpoints can require more binary digits than a binary64 coordinate retains. Therefore the cell lengths, local polynomial coordinates and integration measures are kept rational/decimal rather than rounding boundaries back onto another cell. Physical metric evaluation still uses the original binary64 functions; this does not create additional physical precision.

## 3. Assembly and source derivatives

Mass M, gradient G, transport B, field source-inertia C, and all four physical-X derivatives are recomputed on the refined space. The metric profile, physical source position, source speed, dust inertia and dust drive reproduce the preceding values exactly. Gram factors are evaluated through the established local derivative-atom formulation, with the same hinge compensation and positive coefficient sampler. No high-frequency modes are deleted.

For each of the eight bulk matrices A, two independent consistency checks are applied:

    A_l(order32) versus A_l(order64),
    E_l^T A_l(order64) E_l versus A_0(order64).

The largest normalized entry change is7.57e-15 for quadrature and6.82e-15 for the pullback, below the unchanged3e-10 assembly gate. Normalization is by max(1, largest comparator entry). This is not a force-error bound. The Gram matrix is deliberately NOT required to preserve the old numerical energy: the question is precisely how the refinement-dependent Gram extension behaves as resolution changes.

All required matrices are symmetric; positive mass pivots, direct-versus-assembled positive Gram energy and the unchanged mass-solve gate pass. Assembly takes119.22seconds on one actual single-core worker.

### Unfiltered computed frequency bounds

| Level | Reference | Primary | Alternative |
|---|---:|---:|---:|
|1 |3.97462e6 |5.80453e6 |5.89279e6 |
|2 |7.94913e6 |1.15029e7 |1.16441e7 |

For the original T=4e-5 coordinate-time interval, these require40/59/59 and80/116/117 scaled substeps respectively. They use the previous row-dominance bound with all modes retained, not outward-rounded certification. Coordinates and time retain the parent's normalization; neither seconds nor hertz is assigned here.

## 4. What is evolved and what is only measured

Each case solves

    u_dot = v, v_dot = -M_l^-1 K_l u

with frozen matrices. It does not evolve X, the saved nonzero source speed, or the metric. The full prescribed-background Schur source reaction from the preceding derivation is evaluated at the initial and final fields using those frozen source parameters. This is not the moving-source linearized operator or a coupled source/gravity trajectory.

Both32digits/Taylor48 and48digits/Taylor64 are run. Every48-digit endpoint is propagated backwards over the full interval. The predeclared gates remain: relative frozen-energy drift1e-20/1e-34; phase arithmetic refinement1e-20; source-diagnostic arithmetic refinement1e-19; backwards phase recovery1e-32. Spatial disagreement is a measured scientific result, not a reason to relax a gate or discard a run.

Adjacent endpoint fields are compared by exact embedding of the coarser P2 field into the finer space and use the finer phase-energy norm. The source diagnostic is compared both across spatial levels and between numerical extensions. Absolute differences are retained alongside relative ones because the diagnostic involves cancellations and a possibly small denominator.

### Results: the extension ambiguity decreases

| Field variables | Primary final diagnostic | Alternative final diagnostic | Absolute extension gap | Gap / primary magnitude |
|---|---:|---:|---:|---:|
|1,094 | -5.70999472e-8 | -5.66964859e-8 |4.03461e-10 |0.706588% |
|2,188 | -5.69634829e-8 | -5.70483644e-8 |8.48816e-11 |0.149011% |
|4,376 | -5.76719435e-8 | -5.76787097e-8 |6.76616e-12 |0.0117321% |

The absolute and relative extension differences both decrease at each refinement: roughly60-fold overall. The signed alternative-minus-primary gap changes sign on the first refinement, so these are not monotone upper/lower brackets. The corresponding relative phase-energy differences decrease4.90316e-10 ->1.66156e-10 ->5.85399e-11. Neither extension was selected, fitted, or discarded.

### But the diagnostic itself is not yet spatially qualified

| Branch | Final diagnostic at1,094 | At2,188 | At4,376 | Relative change0->1 | Relative change1->2 |
|---|---:|---:|---:|---:|---:|
| Reference | -5.66495464e-8 | -5.73755600e-8 | -5.77151304e-8 |1.26537% |0.588356% |
| MTS primary | -5.70999472e-8 | -5.69634829e-8 | -5.76719435e-8 |0.239565% |1.22843% |
| MTS alternative | -5.66964859e-8 | -5.70483644e-8 | -5.76787097e-8 |0.616807% |1.09286% |

Relative spatial changes use the FINER diagnostic magnitude as denominator. The last MTS changes exceed their first changes. The primary diagnostic is nonmonotone. Adjacent phase differences are5.88859e-6 ->5.59131e-6 for the reference and approximately9.26051e-6 ->1.00693e-5 for either MTS extension. Therefore decreasing extension sensitivity does NOT establish convergence of the actual endpoint or give a continuum force-error bound. No convergence order or Richardson continuum value is fitted from these three levels.

The reference also changes under refinement; the issue is not assessed against an assumed perfect baseline. Its different background and the frozen-path restriction still prevent reading proximity to the reference as a physical MTS/GR test. The Gram contribution here is a resolution-dependent numerical term: a shrinking difference between its consistent extensions is not evidence that every physical motion-sector effect vanishes.

### Source inertia and arithmetic checks

The initial field Schur inertia Q in either MTS extension is approximately9.54965e-9 ->4.77388e-9 ->2.38694e-9. This nearly halves at each refinement and is consistent with the preceding weighted-projection residual interpretation. It is observed on this initial field, not a universal rate theorem or proof that the entire source force converges. Every measured Q is nonnegative without clipping, and every total source inertia is positive.

All unchanged arithmetic gates pass. Across the refined runs:

- Largest relative frozen-energy drift:3.55e-28 at32digits,2.00e-44 at48digits.
- Largest32/48-digit phase-energy difference:5.12e-28.
- Largest relative arithmetic change of the source diagnostic:5.87e-23.
- Largest backwards phase recovery error:1.78e-43.

Thus the measured spatial differences are not explained by arithmetic precision or the tested propagator order. This does not eliminate every possible implementation or modelling error. The independent whole-action source-force controls from the preceding stage remain inherited; this stage additionally checks all exact embeddings and bulk pullbacks.

The six refined case calculations, each with two arithmetic settings and backwards recovery, take8,881.22seconds (about2hours28minutes) on one actual single-core worker. Together with assembly, active calculation time is about2hours30minutes. No work was discarded to meet the four-hour check-in boundary.

## 5. Decision

**The particular extension-sensitivity question has a positive measured answer:** both absolute and relative gaps shrink across both joint refinements. This is useful evidence for the numerical construction, not a parent-uniqueness or continuum theorem. We can stop treating the initial0.71% gap as an unexplained irreducible difference.

**The full spatial force-convergence gate remains open:** the final primary and alternative mesh changes are still approximately1.23% and1.09%, and the phase changes have not begun a clean decreasing sequence. No original physical discrepancy or GR-recovery gate is closed by this run.

**Next substantive derivation: build the candidate's own gravitational constraint response from its action.** Use the already derived bulk metric covector and the nodal Gram covector, together with the original spherical gravity/source and boundary terms. Derive the radial constraint and its Jacobian rather than copying the old metric into the new candidate. Check that the reference reduces exactly when the Gram term is removed and verify metric variations independently before solving the candidate's initial metric.

That finite-dimensional derivation can proceed without pretending that today's spatial sequence is converged. Keep both numerical extensions and the spatial diagnostic uncertainty visible in the initial-metric comparison. Do NOT start a long coupled evolution, spend another night blindly doubling to8,752 variables, or select the alternative because its result is nearer the reference. After the metric-action consistency checks, decide on a short coupled pilot with an explicit spatial/error budget. A coupled physical or GR claim still requires actual source/metric evolution and controlled spatial behaviour, including the initial-time layer if it is responsible for the unresolved response.

The original12.5718% impulse,13.5770% fine/continuum endpoint and32.5535% coarse64/fine endpoint discrepancies remain unchanged, with their different denominators. The0.0117321% extension gap is not a replacement for any of those measurements.

## Evidence

- Construction: `scripts/build_annular_joint_refinement_20260920.py`.
- Assembly status: `source-intake/navier-stokes/20260914/annular-joint-candidate-refinement-build-attempt01/status.json`.
- Runner: `scripts/run_annular_joint_refinement_20260920.py`.
- Response status: `source-intake/navier-stokes/20260914/annular-joint-candidate-refinement-response-attempt01/status.json`.
- Base pilot: `source-intake/navier-stokes/20260914/annular-common-candidate-response-attempt01/status.json`.
- Preceding seal: `source-intake/navier-stokes/20260914/annular-complete-frozen-candidate-final-integrity.json`.

All work remains private inside post-checkpoint-work. No GitHub action, subagents, original live dynamics changes or edits to the sibling formalization-workbench. Executed scripts and their outputs are immutable. The protected-workbench check is a modification-time scan since2026-09-20T18:05:58Z, not a pre-turn whole-tree hash baseline.

Completed assembly and response runs have164 and94 scoped source/implementation checks respectively,258 total, all passed. No new failed execution;52 historical failed executions remain preserved. These counts are not independent physical confirmations.
