# 3317 - Minimal symbolic Hessian no-pole or finite-residue branch under AX1090

Run UTC: `2026-06-27T19:44:33.142254+00:00`

## Verdict

3317 turns the local-GR question into a small algebra problem.

For the minimal public metric channel `h` plus one extra local channel `x`, take

`H(p) = [[a p, b0+b1 p], [b0+b1 p, M2+z p]]`, `R=(1,u)`, `p=k^2`.

Then

`G_pub(p)=N(p)/D(p)`

`D(p)=a p (M2+z p)-(b0+b1 p)^2`

`N(p)=M2+z p-2u(b0+b1 p)+u^2 a p`.

A GR-like massless Newton pole first requires `b0=0`. After that, the finite pole is generic:

`p_f=-a M2/(a z-b1^2)`.

So the cleanest local-GR route is now exact: prove the local curvature-exchange/extra sector is algebraic and non-derivative-mixed in the public metric branch, `z=0` and `b1=0`, with `b0=0`. Then `D(p)=a M2 p` and there is no observable finite pole to fight in R10/WEP/PPN.

The action language is compatible with this because the macroscopic curvature-exchange term is potential-like, but it is not yet a proof because microscopic `psi` dynamics could induce a reduced finite pole after coarse graining.

## Source Register

- `SRC3317_0_3316_doc`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3316-Y5-R2FR-parent-quadratic-hessian-readout-extraction-for-ZiUi-under-AX1090.md` - exists=true; parse_ok=true; role=3316 invariant residue/readout formula and next target
- `SRC3317_1_3316_factor`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3316_A_FACTOR_UPDATE.csv` - exists=true; parse_ok=true; role=A_i updated to B_i residue law
- `SRC3317_2_3316_contract`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3316_RESIDUE_EXTRACTION_CONTRACT.csv` - exists=true; parse_ok=true; role=required H_AB and R map contract
- `SRC3317_3_fundamental_action`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-fundamental-action-of-motion-timespace-field-theory.md` - exists=true; parse_ok=true; role=macroscopic action and microscopic psi action source
- `SRC3317_4_motion_action`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-motion-timespace-action-principle.md` - exists=true; parse_ok=true; role=MTS action principle with curvature-exchange potential
- `SRC3317_5_1042_nohair`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md` - exists=true; parse_ok=true; role=conditional positive no-hair route if finite pole remains as physical X

## Minimal Hessian Formula

- `MH3317_0_ansatz` `minimal two-channel local Hessian`: `Phi=(h,x), H(p)=[[a p, b0+b1 p],[b0+b1 p, M2+z p]], R=(1,u), p=k^2` Meaning: h is the massless GR metric channel; x is the least extra finite/local MTS channel; u is public readout overlap.
- `MH3317_1_propagator` `public exchange propagator`: `G_pub(p)=N(p)/D(p)` Meaning: N and D decide whether local tests see a finite pole.
- `MH3317_2_denominator` `D(p)=det H`: `D(p)=a p (M2+z p)-(b0+b1 p)^2` Meaning: the zeros of D are the massless and finite pole candidates.
- `MH3317_3_numerator` `N(p)=R adj(H) R^T`: `N(p)=M2+z p-2u(b0+b1 p)+u^2 a p` Meaning: a pole is observable only if N is nonzero at that pole.
- `MH3317_4_GR_massless_condition` `massless Newton pole`: `D(0)=-b0^2, so a GR-like massless pole at p=0 requires b0=0` Meaning: constant h-x mixing gives the graviton a mass/deformation unless removed by symmetry/constraint.
- `MH3317_5_finite_pole` `finite pole location after b0=0`: `D(p)=p[a M2+(a z-b1^2)p], so p_f=-a M2/(a z-b1^2)` Meaning: generic derivative kinetic/mixing creates a finite pole unless the second factor is absent or unobserved.

## No-Pole Conditions

- `NPC3317_0_GR_pole` `GR_massless_first_gate`: condition `b0=0`. Effect: keeps D(0)=0 and prevents constant h-x mixing from deforming the Newton pole Scrutiny: must be symmetry/constraint derived, not fitted.
- `NPC3317_1_algebraic_decoupled` `no_finite_pole_by_algebraic_decoupling`: condition `b0=0, z=0, b1=0, M2 nonzero`. Effect: D(p)=a M2 p, so G_pub has only the massless Newton pole plus contact/algebraic terms Scrutiny: best local-GR route if Gamma/extra sector is nonpropagating and does not derivative-mix with h.
- `NPC3317_2_degenerate_constraint` `no_finite_pole_by_constraint_degeneracy`: condition `b0=0 and a z-b1^2=0 with first-class/constraint degree-count proof`. Effect: the finite denominator factor vanishes rather than producing a physical extra pole Scrutiny: dangerous unless the degeneracy is a true gauge/constraint, not an under-specified Hessian.
- `NPC3317_3_readout_orthogonal` `finite_pole_unobserved`: condition `N(p_f)=M2+p_f(z-2u b1+u^2 a)=0`. Effect: a finite eigenmode may exist but has zero public-metric residue B_i Scrutiny: looks like tuning unless enforced by a parent projector/orthogonality theorem.
- `NPC3317_4_short_range` `finite_pole_retained_but_short_range`: condition `m_f^2=a M2/(a z-b1^2)>0 and m_f r_local >> 1`. Effect: finite pole exists but is exponentially suppressed in local tests Scrutiny: requires parent range or empirical bound; not as clean as no-pole.
- `NPC3317_5_generic_residue` `finite_residue_branch`: condition `b0=0, a z-b1^2 != 0, N(p_f) != 0`. Effect: local finite mode has nonzero B_i and must face R10/WEP/PPN/clock/orbital tests Scrutiny: no local-GR claim without bounds or screening.

## Action Compatibility Test

- `ACT3317_0_EH_anchor`: answer=true; Does the corpus contain a massless EH/GR anchor? Impact: supports h channel as the massless pole.
- `ACT3317_1_curvature_exchange_potential`: answer=true; Does the macroscopic action describe curvature exchange as potential-like rather than explicit local kinetic Gamma? Impact: compatible with the algebraic-decoupled no-finite-pole branch, but not a proof because microscopic psi dynamics may induce a reduced Hessian.
- `ACT3317_2_matter_coupling`: answer=true; Does the corpus include ordinary matter coupling language? Impact: compatible with Hilbert source theorem from 3315.
- `ACT3317_3_microscopic_psi_caveat`: answer=true; Can microscopic psi dynamics reintroduce finite local poles after coarse graining? Impact: prevents claiming no-pole from macroscopic potential language alone.

## Branch Decision Matrix

- `BR3317_0_best_route` `prove algebraic/nonpropagating curvature-exchange in local compact branch`: it gives D(p)=a M2 p and no finite public pole, matching local GR without fifth-force fine tuning Needed: Gamma/extra sector has z=0, b1=0, b0=0 after local reduction and no psi-induced finite readout pole. Status: BEST_NEXT_TARGET_NOT_CLAIMED.
- `BR3317_1_second_best` `prove readout orthogonality N(p_f)=0`: finite mode can exist internally but has B_i=0 in ordinary public metric tests Needed: parent projector orthogonality theorem for R against finite eigenvector. Status: VIABLE_BUT_TUNING_RISK.
- `BR3317_2_empirical` `retain finite B_i envelope`: scoreable if no-pole fails Needed: range, residue sign, residual source tails, R10/WEP/PPN/clock/orbital bounds. Status: FALLBACK.

## Promotion Gates

- `GATE3317_0_algebra`: passed=true; claim=minimal Hessian pole algebra is derived; reason=D(p), N(p), GR b0 gate, finite pole, and no-pole branches are explicit
- `GATE3317_1_no_finite_pole`: passed=false; claim=MTS local branch has no observable finite pole; reason=algebraic-decoupled/no-pole clauses are compatible but not parent-signed
- `GATE3317_2_local_GR`: passed=false; claim=local GR/Newton limit is derived; reason=requires parent proof of no finite pole, orthogonal readout, short range, or no-hair/screening

## Decision

- `DEC3317_0`: it derived the two-channel finite-pole algebra and the exact no-pole conditions - the local-GR problem reduces to b0=0 plus either z=b1=0, az-b1^2=0 with constraints, N(p_f)=0, or short-range/screened finite residue Next: attack the algebraic/nonpropagating Gamma/local-extra-sector proof first.
- `DEC3317_1`: yes, weakly: the macroscopic curvature-exchange term looks potential-like and therefore compatible with algebraic no-pole - the action scan does not expose an explicit Gamma kinetic term, but microscopic psi dynamics may still generate one after reduction Next: prove or reject z=0 and b1=0 for the local compact branch.
- `DEC3317_2`: no - compatibility is not derivation; the no-pole branch needs parent signature Next: 3318 should specifically test Gamma/extra-sector nonpropagation rather than broad source sweeps.

## Next Target

- `3318-Y5-R2FR-Gamma-extra-sector-nonpropagation-proof-or-Bi-envelope-under-AX1090.md`
- `scripts/Y5_R2FR_3318_Gamma_extra_sector_nonpropagation_proof_or_Bi_envelope.py`
- Objective: prove or reject the best 3317 no-pole route: local curvature-exchange/extra sector has b0=0, z=0, b1=0 in the public metric Hessian, so no finite observable pole exists
- Fallback: retain finite B_0/B_2 and score them through R10/WEP/PPN/clock/orbital bounds with residual epsilon tails
