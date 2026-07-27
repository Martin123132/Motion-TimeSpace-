# 3124 - No-`c_A` Slot Parent Grammar or `delta_J` Finite Branch Selection under AX1090

Private checkpoint. This follows 3123 by asking the exact grammar question: does the parent matter object-language forbid a hidden species/current coefficient

```text
c_A(y) A_Q_mu J_A^mu
```

or must `delta_J` remain a finite before-variation source-coupling branch?

## Verdict

The no-`c_A` theorem has a clean form:

```text
Parent matter grammar = q-basic matter functor
                      + fixed representation labels n_A
                      + no hidden-visible coefficient hom
                      + no species/source prefactor slot
                      + variation-before-readout
                      + radiative/effective-action closure

=> no well-typed c_A(y) A_Q J_A term
=> Lie_v J_Q = 0
=> delta_J = 0.
```

But the current corpus does not sign the needed grammar. Existing rows explicitly retain:

```text
hidden-visible coefficient hom obstruction,
species/source action weights,
matter-normalization owner gap,
post-variation/readout leakage,
radiative/effective-action re-entry.
```

Therefore 3124 selects the default finite branch:

```text
FINITE_BEFORE_VARIATION_PROJECTS_BOTH
```

meaning:

```text
if delta_J survives, treat it first as a before-Maxwell/Hilbert-variation current insertion
that can project into material Coulomb response, EM Hilbert stress, source GM, WEP and R10.
```

This is not a claim that this branch is physical. It is the strict live branch to use for bounding until the no-`c_A` grammar is proved.

## Source Register

| source_id | path | role |
|---|---|---|
| 1088 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md` | minimal ordinary matter signature and legal countermodels |
| 1091 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md` | no hidden-visible coefficient hom theorem failure |
| 3123 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3123-Y5-R2FR-current-owner-action-variation-or-deltaJ-projection-exclusion-under-AX1090.md` | action-variation current owner and projection classifier |
| direct-matter-grammar | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_AMATTER_COEFFICIENT_PACK.csv` | direct matter/source coefficient gaps |
| matter-normalization | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_MATTER_NORMALIZATION_OWNER_2646_DELTAW_SPECIES_COEFFICIENT_ROWS_NONCLAIM.csv` | species/action normalization coefficient gaps |
| 3123-output | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3123_DELTAJ_PROJECTION_CLASSIFIER_OUTPUT.csv` | branch classifier source |
| 3124-clauses | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3124_NO_CA_SLOT_GRAMMAR_CLAUSES.csv` | no-`c_A` proof clauses |
| 3124-runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3124_deltaJ_branch_selector.py` | branch selector |

## Grammar Derivation Attempt

Let the parent matter grammar be:

```text
S_matter = sum_A S_A[Psi_A, e_pub(q), A_Q(q), n_A, theta_A].
```

Here `A` is a representation/species label, not a free coefficient slot, and `n_A` is fixed representation data. A hidden current coefficient would require a map:

```text
c_A : C_hid x Species -> R
```

and a mixed operator:

```text
Delta S = sum_A integral sqrt(-g_pub) n_A c_A(y) A_Q_mu J_A^mu.
```

This term is not well typed if all of the following are true:

```text
1. ordinary matter is a q-basic functor;
2. Species labels are fixed representation data, not coefficient targets;
3. Hom(C_hid, Coeff_A(A_Q J_A)) = Const or absent;
4. the parent action has no species/source prefactor slot w_A(y)S_A;
5. current and Hilbert stress are varied before material/readout fitting;
6. S_eff/readout cannot regenerate the slot.
```

Under these clauses:

```text
c_A(y) = constant common mode or absent.
```

The constant common mode is calibration, not a differential current residual. The nonconstant/differential part is killed:

```text
delta_J_A = Lie_v ln c_A = 0.
```

## Why It Fails To Promote

The proof is blocked by the current corpus:

| blocker | current evidence |
|---|---|
| no hidden-visible coefficient hom | 1091 and 3118 keep hidden scalar coefficient maps live |
| no species/source prefactor | 1088, 2612, and 2646 retain `w_A`, `delta_w_species`, and source/action weights |
| matter-normalization owner | 2646 says the owner theorem is not derived |
| variation/readout closure | 1088 and 3123 keep post-variation selectors live |
| radiative/effective closure | 988/989/1091 keep effective/readout re-entry unsigned |

So the no-`c_A` theorem is exact conditional, not a present MTS claim.

## Branch Selection

3124 makes the branch policy explicit:

```text
default live branch = before-variation finite current insertion
```

because it is the strictest unexcluded countermodel:

```text
c_A(y) A_Q J_A inserted before Maxwell solve and Hilbert variation.
```

It projects to:

```text
F_Q[J_Q],
T_EM[J_Q],
material Coulomb response,
source GM,
WEP if differential,
R10 source/test current strength.
```

The other branches remain as guards:

```text
calibration-only:
  retained only for universal common-mode current-unit shifts;

readout-only:
  retained if the current factor enters after action variation;

effective-action ambiguous:
  must be split into before-variation or readout-only before scoring.
```

This prevents hiding the dangerous branch inside "maybe calibration" while also preventing us from falsely treating every current-unit choice as observable.

## Runner Result

3124 adds:

| artifact | path |
|---|---|
| grammar clauses | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3124_NO_CA_SLOT_GRAMMAR_CLAUSES.csv` |
| branch output | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3124_DELTAJ_BRANCH_SELECTION_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3124_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3124_NO_CA_SLOT_BRANCH_GATE.csv` |

The runner selects exactly one default branch. In the current state it selects:

```text
FINITE_BEFORE_VARIATION_PROJECTS_BOTH
```

with all rows nonclaim.

## Claim Status

No current-owner, Maxwell, WEP, source-`GM`, PPN, orbital, R10, local-GR, derived-`G`, or unification claim follows from 3124.

The internal advance is:

```text
the exact no-cA grammar proof clauses are written;
the proof is not smuggled in;
the finite delta_J branch is selected by insertion stage;
future coefficient work now has a strict default projection target.
```

## Next Target

Write:

```text
3125-Y5-R2FR-before-variation-deltaJ-source-bound-interface-under-AX1090.md
```

Direct target:

1. use the selected before-variation branch;
2. connect the 3122 `C_J` material coefficient to the 3121 source-`GM` bridge without mixing the two;
3. build the first strict no-cancellation bound interface for `delta_J` across WEP, source-GM, R10, and readout guards.
