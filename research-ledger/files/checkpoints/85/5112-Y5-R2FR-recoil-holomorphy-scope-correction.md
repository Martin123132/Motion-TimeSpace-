# 5112 - recoil holomorphy scope correction

## Question

Checkpoint 5111 stopped on the first control job because the pair

`direct:g2:plus_u` / `subtraction:decay:minus_u`

had a stable nonzero outer relative residue even though the structural 5084 certificate declared it zero. The issue was not resolved by suppressing the row. The direct additive component was isolated and recomputed at 60 decimal digits on two relative-contour radii and two global-contour radii.

## Conditional theorem and failed premise

Let

`R_D(q) = Res_w[D(w,q) dw/w]`

for the causally owned direct pole. If `R_D` is holomorphic at a nonzero collision point `q_0`, then

`Res_q[R_D(q) dq/q] = 0`.

That conditional Cauchy statement is valid. What fails is 5084's claim that separation from the catalogued direct roots plus regular recoil energies proves the holomorphy premise. The finite-`x` pole catalogue does not exhaust the singularities of the direct KLT/spinor coefficient.

## Decisive source-separated result

For `E020__S507611_N0000__A00__primary24`, the two roots of the same labelled collision behave differently.

| root | `|q_0|` | direct-only arbitrary-precision residue | classification |
|---|---:|---:|---|
| `-0.0605289692653992 + 0.0000060673740820 i` | `0.06052897` | maximum magnitude `1.73e-35` | event-local zero |
| `-13.21682562520198 + 0.00528353577870 i` | `13.21682668` | `31.01294678732344 - 0.254009009904149 i` | stable nonzero |

The outer value is unchanged across all four radius combinations to the printed precision. Because only the direct component is integrated, this cannot be leakage from the nearby subtraction pole. Double-precision Laurent moments also remain stable on radii differing by a factor of two, confirming that the outer point carries an omitted direct singularity.

## Historical impact

All eight v12 rows previously zeroed by the generalized 5084 theorem were recomputed individually with the same source-separated arbitrary-precision evaluator. Their largest measured magnitude is `4.25e-28`, below the locked `1e-20` numerical-zero tolerance. They therefore survive as exact-event numerical certificates, not as consequences of a family theorem.

The replacement registry contains nine rows: the eight historical v12 rows plus the 5111 inner root. It is scoped by exact job, event, argument, pair, ownership and root. No new row may inherit a zero from shared symbolic labels alone.

## Runner correction and replay

The 5077 kernel policy now:

1. preserves every stable numerical row, including a stable nonzero;
2. rejects the broad 5084 holomorphy theorem;
3. promotes an unstable row to numerical zero only when it exactly matches the 5112 arbitrary-precision registry;
4. otherwise falls through to the remaining certified repairs or fails closed.

The previously blocked 5111 job was replayed under this policy. It completed and converged in `31.54 s`, retained the outer residue, used no zero-registry promotion, and left `179` jobs missing. This resolves the failure without deleting the physical/topological contribution.

## Status

- broad 5084 family theorem: **rejected**;
- 5084 conditional Cauchy identity: **retained with an unproved holomorphy premise**;
- eight historical zero uses: **rescued by event-local arbitrary precision**;
- 5111 outer residue: **retained as stable nonzero**;
- first 5111 job: **converged**;
- full control matrix: **not yet complete**;
- independent efficiency or full MTS claim: **not allowed**.

## Outputs

- `scripts/Y5_R2FR_5112_recoil_holomorphy_scope_correction.py`
- `source-intake/functional_rg/5112/recoil_holomorphy_scope_correction.json`
- `source-intake/functional_rg/5112/event_local_direct_zero_registry.json`
- `source-intake/functional_rg/5112/direct_component_arbitrary_precision_audit.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_5112_VALIDATION.csv`

