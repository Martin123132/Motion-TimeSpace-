# The frozen weak remainder: native closure, finer tests, geometry and Gram stencil

Private continuation of `DERIVATION-20260920-mixed-weak-frozen-force-integrals.md`.

Status: COMPLETE, including independent forward/adjoint force channels, separated refinement and an exact source-trace audit. Original action, source-force covector, physical parameters and full mode content unchanged. No new live evolution or physical pass claimed.

## 1. Target and why this is not another initial-field probe

The previous exact frozen calculation found a mixed weak remainder of +1.35133591391e-9 for the reference branch and -3.02762656364e-8 for MTS. Transfer/assembly accounting did not remove it. This stage evaluates the further identity derived there against the same actual frozen coarse trajectory and fine adjoint. It does not substitute arbitrary static fields for the force integral.

The comparison is still a frozen homogeneous operator contribution, not the complete moving-source evolution or the total nonlinear source-force error. The finer-test split is a fixed comparison convention, not a unique allocation of physical causes.

## 2. Five exact channels

Retain native M_c,K_c,M_f,K_f and A_c=M_c^-1 K_c. E_c,E_f are the exact common-space embeddings and R_c,R_f their native evaluation left inverses. Define

    C = R_c E_f,     J = R_f E_c.

B_f,G_f pair fine tests and coarse trials with the fine physical mass and gradient weights. B_c,G_c do the same with the coarse physical weights. M_c^*,G_c^* are common-integrated coarse/coarse mass and gradient matrices. The original native coarse gradient and Gram matrices are K_grad,c and K_Gram,c, with K_c=K_grad,c+K_Gram,c.

For the specified Gram extensions,

    H_fine = H_f^T W_f H_f J,
    H_counter = H_f^T W_f|coarse H_f J,
    H_coarse = C^T K_Gram,c.

W_f|coarse is the previously sourced fine stencil weight evaluated on coarse geometry, not a fitted counterterm. S_f=G_f+H_fine.

Each defect is D_j=P_j A_c-Q_j:

| Channel | P_j | Q_j |
|---|---|---|
| Coarse native closure | C^T(M_c^*-M_c) | C^T(G_c^*-K_grad,c) |
| Unresolved finer test | B_c-C^T M_c^* | G_c-C^T G_c^* |
| Mass/gradient geometry | B_f-B_c | G_f-G_c |
| Gram geometry weight | 0 | H_fine-H_counter |
| Same-geometry Gram stencil | 0 | H_counter-H_coarse |

The sum is exactly B_f A_c-S_f: expansion leaves that term plus C^T(K_c-M_c A_c), which vanishes by the original native equation. The mass convention remains the exact symmetric matrix defined by the original lower-triangle solve; unused upper-band rounding entries are not substituted.

For a fine test t=E_f z, its unresolved part is t_perp=t-E_c C z. Exact R_c E_c=Id gives R_c t_perp=0. The specified coarse Gram extension therefore contributes zero to this test defect. Mass and gradient pairings need not vanish between coarse nodes. This is nodal interpolation of a test, not an orthogonal projection or a proof that the continuum field has a physical defect.

All five channels are constructed directly from original arrays and common-cell moments. No singular projected mass inverse, representative deletion, smoothing or coefficient refit is introduced.

The same-geometry Gram channel includes the effect of the canonical restrictions J and C. It is not just a change of scalar stencil weights, and is not automatically an independent physical cause alongside the finer-test term.

## 3. Force integrals and independent controls

For each channel, propagate

    u_c'' = -A_c u_c,
    r_j'' + A_f r_j = M_f^-1 (P_j A_c-Q_j)u_c,
    r_j(0)=r_j'(0)=0.

Then, with the original terminal force covector c,

    F_j = c^T(r_j(T),r_j'(T))
        = integral_0^T z_f(s)^T D_j u_c(s) ds,
    z_f=M_f^-1 lambda_v,  lambda(s)=exp((T-s)L_f^T)c.

The independent reverse evolution uses D_j^T z=A_c^T P_j^T z-Q_j^T z. It checks each channel, not just their cancelling sum. A dense small-system exponential checks the generalized channel integrator with noncommuting mass/stiffness, pure-stiffness channels and an identically zero channel. Only identically zero response channels may be skipped; no physical mode is dropped.

Original source geometry and coefficients remain binary64 inputs. Accumulation is evaluated at 32/48 digits and time-Taylor order48/64. Spatial moment order32/64 is tested separately at fixed 48-digit/order64 propagation. Literal predecessor force tolerances are retained, not relaxed.

Before propagation, independent common-field contractions reproduce every assembled channel on a full-support fixture, including the weighted Gram terms. Both the zero-coarse-node condition and zero coarse Gram action of t_perp are verified. The full operator reconstruction is checked, including the original native mass semantics. These are implementation controls, not independent physical experiments.

## 4. Results

Signed contributions to the same spatial64 frozen weak remainder, in its original code-unit normalization:

| Channel | Reference | MTS |
|---|---:|---:|
| Coarse native closure | +5.05091e-19 | -3.62963e-17 |
| Unresolved finer test | +1.35133591309e-9 | -1.50908397993e-8 |
| Mass/gradient geometry | +3.08793e-19 | -2.10862e-17 |
| Gram geometry weight | 0 | +5.50760e-18 |
| Same-geometry Gram stencil | 0 | -1.51854257853e-8 |
| Sum / preceding weak remainder | +1.35133591391e-9 | -3.02762656364e-8 |

All channels retain their signs. The two large MTS terms have the same sign; they do not hide a large cancellation against one another. Their nearly equal sizes apply to this prescribed comparison, not to unique percentages of physical error. The Gram channel can include unresolved source-trace information, as the exact audit below demonstrates structurally.

Every five-term sum reconstructs the preceding weak remainder. Both branches pass the unchanged literal thresholds (3.002e-16 for reference; approximately3.064e-16 for MTS), without fitting or relaxing tolerances. Every individual channel is checked against its independently formulated adjoint integral; the largest difference is2.381e-46 for fixed saved inputs. The original fine-adjoint endpoint arrays are unchanged at recorded48-digit precision.

Separated refinements give maximum channel changes of2.853e-30 for arithmetic/time-order refinement and3.960e-19 for spatial moment-order refinement. The latter is an integration check, not a new spatial mesh refinement or continuum convergence test. No claim of physical accuracy at these tiny levels is made.

Four completed runs contain202 scoped implementation/source checks:104 matrix/field controls,12 dense integrator controls,70 actual force/refinement controls and16 exact source-trace checks. They are not202 independent physical tests. The main force calculation took about33.8 minutes on one actual single-core worker. One short trace audit also ran, staying within the two-worker limit. No new failed execution; the50 previously recorded failures remain preserved.

## 5. Interpretation and next substantive calculation

The remaining frozen discrepancy is not predominantly the change in geometry weights or ordinary native quadrature/basis closure in this test. Reference is overwhelmingly a finer-test residual. MTS has two similarly sized terms: the mass/gradient finer-test residual and the same-geometry Gram comparison.

This does not by itself establish two independent physical defects, or prove that either disappears in the continuum. In particular, the coarse nodal Gram extension used in the decomposition can miss a real source derivative trace of a fine test. The exact construction below is a concrete way to test that possibility without changing the native actions.

Prioritize the new rank-one trace comparison for the MTS Gram term, retaining the common finer-test residual alongside it. Do not refit the Gram coefficient, drop the term, declare the reference broken, or repeat the already-rejected explanation that ordinary coarse-to-fine transfer accounts for the full force discrepancy. The force integrals for the trace-aware comparison are the next missing calculation, not another search for unspecified parent parameters.

### An additional exact result: the coarse test projection loses a source derivative trace

An exact rational audit on the saved meshes gives, for BOTH branches,

    j_f^* J = j_c^*,       j_c^* C != j_f^*.

Here j_L^* is the exact one-sided REFERENCE-COORDINATE derivative jump at the anchored source, evaluated from the native P2 polynomial; the star distinguishes this canonical trace from binary64 assembly arithmetic. It is not being silently identified with a physical-radius derivative after the moving pullback. The true common jump ell satisfies ell E_c=j_c^* and ell E_f=j_f^* exactly.

Thus coarse trials transferred canonically to the fine space preserve this source jump, but fine tests projected onto the coarse space do not. Fine basis columns555 and556 are entirely invisible to C while carrying nonzero source jumps. For unit basis555 the exact jump is 4503599627370496/8246337209. The original MTS fine Gram quadratic form of this UNIT BASIS is 1.02580527266e9, whereas the coarse projected form is zero. Reference Gram is zero as expected. This is a structural witness, not the amplitude, energy or force of the physical solution and not a quantitative attribution of the integrated Gram channel.

The original action builds its lifted Gram factor as H_c=O_c-g_c j_c, where g_c is the lifted hinge vector. That structure is explicit in `scripts/annular_P2_graded_source_20260919.py`; the prior static expansion is in `scripts/annular_P2_bulk_refinement_20260919.py`. The new question is its actual time-integrated force effect, not another static expansion.

### Derived trace-aware comparison that preserves the original native action

Use the original stored H_c and g_c, but define its off-native common-space extension by

    Hhat_c = H_c R_c - g_c (ell - j_c^* R_c).

This does NOT replace the native physical action: Hhat_c E_c=H_c exactly because R_c E_c=Id and ell E_c=j_c^*. The analogous fine extension also preserves H_f. The exact trial commutation already proved makes Hhat_f E_c=H_f J.

Set delta = j_f^* - j_c^* C (the NEGATIVE of the saved test-defect row). On fine tests,

    Hhat_c E_f = H_c C - g_c delta.

Writing p_c=g_c^T W_c H_c, the trace-aware same-geometry mixed Gram difference is

    Q_trace = H_counter - C^T K_Gram,c + delta^T p_c.

Consequently the ORIGINAL same-geometry Gram defect has the exact split

    D_Gram,old = -Q_trace + delta^T p_c.

This isolates a rank-one lost-test-trace contribution from the remaining Gram comparison without changing any native mass, stiffness, coefficient or time evolution. The native binary64 H_c is retained; the canonical jump correction vanishes on every native coarse field, so it does not silently replace its assembled derivative rows.

The next targeted calculation is to source and reproduce g_c and H_c from the original action, verify this two-term identity numerically, then evaluate BOTH terms against the same frozen force paths. These two integrals have NOT been computed here. A large witness is not sufficient to predict their sizes, and changing the comparison extension alone cannot repair the original force discrepancy. Its purpose is to decide whether the apparent Gram-stencil contribution is mainly another unresolved-test trace or a residual requiring a genuinely action-consistent discretization change.

The original 12.5718% impulse, 13.5770% fine/continuum endpoint and 32.5535% coarse64/fine endpoint discrepancies remain unchanged. They are different comparisons and must not be collapsed into one error percentage. No local-GR, full-GR, continuum certificate or observational pass follows from these frozen calculations.

## Evidence

- Previous result: `DERIVATION-20260920-mixed-weak-frozen-force-integrals.md`.
- Matrix algebra: `scripts/annular_weak_residual_split_20260920.py`.
- Independent matrix and field checks: `scripts/derive_annular_weak_residual_matrices_20260920.py`.
- Channel evolution: `scripts/annular_weak_channel_evolution_20260920.py`.
- Dense controls: `scripts/validate_annular_weak_channel_evolution_20260920.py`.
- Actual frozen integrals: `scripts/derive_annular_weak_residual_force_20260920.py`.
- Matrix evidence: `source-intake/navier-stokes/20260914/annular-weak-residual-matrices-attempt01/status.json`.
- Integrator controls: `source-intake/navier-stokes/20260914/annular-weak-channel-controls-attempt01/status.json`.
- Force results: `source-intake/navier-stokes/20260914/annular-weak-residual-force-attempt01/status.json`.
- Exact trace audit: `scripts/derive_annular_exact_source_trace_comparison_20260920.py`.
- Trace evidence: `source-intake/navier-stokes/20260914/annular-exact-source-trace-comparison-attempt01/status.json`.

One actual single-core BelowNormal worker, no subagents, no GitHub action, no sibling edits. Executed evidence remains immutable.
