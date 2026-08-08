# 4093 - Adopt Parent Normal Form, Test Gamma/Beta/Zeta Or Reject To Residuals

## Purpose

4092 wrote a candidate parent normal form. 4093 tests what that normal form actually buys for the remaining local-GR rows.

- Decision: `PARENT_NORMAL_FORM_FIXES_SOURCE_AND_PROJECTOR_BLOCK_BUT_GAMMA_BETA_ZETA_STILL_NEED_EH_R11_SOURCE_CLOSURE`
- Candidate fixed-source denominator: `yes, if PNF4092 is adopted`
- Candidate projector/domain preferred-frame block: `zero, if PNF4092 is adopted`
- Public `gamma=beta=1`, `zeta_i=0`, or local-GR claim: `false`

## Result

The parent normal form is useful but not sufficient by itself.

It gives the clean route

```text
U = G_ref M_H / r
GM_orb is output-only
P_D = q_src^* Pbar_top
epsilon_domain_vector = epsilon_domain_flux = epsilon_domain_anisotropy = 0
```

so it supports the 4090/4091 projector-domain result and prevents source-denominator laundering.

But `gamma`, `beta`, and `zeta_i` still require more:

```text
gamma-1 = 0  needs EH-only tracefree spatial response plus no live R11/q_loc stress
beta-1  = 0  needs EH 2PN nonlinear completion plus no source-normalization/boundary beta term
zeta_i  = 0  needs same Hilbert stress conserved and no hidden source-current leak
```

## Nonprojector R11 Status

The q-basic/projector-domain sector is the good news. The bad news, honestly stated, is that these families remain live unless separately zeroed or bounded:

- `R2_fR_scalar_mode`
- `Ricci_Weyl_squared`
- `scalar_tensor_class_metric`
- `torsion_nonmetricity`
- `bulk_X_force_law`
- `nonlocal_memory_kernel`
- nonprojector pieces of `source_normalization_operator`
- boundary/reference source terms unless source-blind no-flux is parent-signed

That means 4093 does not circle the same missingness. It narrows the next fight: nonprojector R11 must be absent, double-zero, topological, massive/screened with a sourced bound, or kept as an explicit residual.

## Decision

Keep the parent normal form as the leading derivation route, but do not claim local GR from it yet. Next target is nonprojector R11 double-zero/absence or gamma/beta bounds.

## Outputs

- `P8_Y5_R2FR_4093_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4093_NORMAL_FORM_ADOPTION_TEST.csv`
- `P8_Y5_R2FR_4093_GAMMA_BETA_ZETA_THEOREM.csv`
- `P8_Y5_R2FR_4093_R11_RESIDUAL_FAMILY_AUDIT.csv`
- `P8_Y5_R2FR_4093_FALLBACK_RESIDUAL_CONTRACT.csv`
- `P8_Y5_R2FR_4093_PUBLIC_PROMOTION_GATE.csv`
- `P8_Y5_R2FR_4093_DECISION_GATE.csv`
- `P8_Y5_R2FR_4093_NEXT_TARGET.csv`
- `P8_Y5_BRR545_4093_VALIDATION.csv`
