# 4016 - G_ref Superselection Universal Calibration Or Gdot/Range Row

- Timestamp: `2026-07-01T21:15:36+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

This checkpoint attacks the coupling directly.

The clean route is:

`Q_parent ~= Q_dyn x K_G`, with `kappa_* in K_G` and `T_local K_G=0`.

Then compact-support local variations obey `delta_local kappa_*=0`, so `kappa_*` is not a scalar field with local hair.

The second required clause is the no-Hom gate:

`Hom(source_label,K_G)=Hom(material_label,K_G)=Hom(range,K_G)=Hom(domain,K_G)=Hom(memory,K_G)=0`.

If those clauses are parent-signed, then

`D_X ln G_ref=0` for `X in {t,r,A,lambda,frame,domain,memory,projector}`.

The same-branch calibration is simply

`G_ref := c^4 kappa_*/(8*pi)`.

That can make one universal coupling channel. It still does **not** predict the numerical value of `G`; it prevents source/range/time/frame drift once the parent sector is signed.

## Bianchi Guard

`nabla_mu(kappa T^{mu nu})=0` gives `T^{mu nu} nabla_mu kappa + kappa nabla_mu T^{mu nu}=0`.

So Bianchi only forces `nabla kappa=0` in an arbitrary-source, same-frame, separately conserved matter branch. If exchange terms remain, the exchange row stays live. No magic constant-G proof.

## Finite Residual Vector

`epsilon_Gref_superselection_4016 <= |C_sector|+|C_local_scalar|+|C_noHom|+|C_Gref_kappa|+|D_t lnG|/B_Gdot+L_r|partial_r lnG|+|partial_A lnG|+|partial_lambda lnG|+|partial_frame lnG|+|delta_kappa_exchange|+|C_product_tuning|+|C_absolute_G_claim|`.

## Evaluator Results

- `CASE4016_0_full_superselection_signed`: owner=`CONDITIONAL_GREF_SUPERSELECTION_LOCK`, residual=`D_t_D_r_D_A_D_lambda_D_frame_lnG_ZERO_IF_PARENT_SIGNED`, claim=`CONSTANT_UNIVERSAL_GREF_CONDITIONAL_ONLY`, next=`move to kappa-sector insertion or then PPN source stability`
- `CASE4016_1_sector_open`: owner=`GREF_SUPERSELECTION_BLOCKED`, residual=`C_sector`, claim=`NO_GLOBAL_COUPLING_CLAIM`, next=`insert or derive parent K_G coupling sector`
- `CASE4016_2_local_scalar_kappa`: owner=`LOCAL_KAPPA_SCALAR_BRANCH_ACTIVE`, residual=`C_local_scalar+D_t_lnG+partial_r_lnG`, claim=`NO_GDOT_RANGE_SILENCE_CLAIM`, next=`either prove kappa is not local or run scalar-coupling residual bounds`
- `CASE4016_3_noHom_open`: owner=`SOURCE_RANGE_HOM_BLOCKED`, residual=`C_noHom+partial_A_lnG+partial_lambda_lnG`, claim=`NO_SOURCE_BLIND_OR_R10_CLAIM`, next=`prove no-Hom gate or build source/range residual rows`
- `CASE4016_4_Bianchi_only_attempt`: owner=`BIANCHI_ONLY_CONSTANT_G_PROOF_REJECTED`, residual=`delta_kappa_exchange`, claim=`NO_CONSTANT_G_CLAIM`, next=`prove arbitrary same-frame conserved sources or keep exchange residual`
- `CASE4016_5_product_cancellation_attempt`: owner=`MEASURED_GM_CANCELLATION_REJECTED`, residual=`C_product_tuning`, claim=`NO_MEASURED_GM_SILENCE_CLAIM`, next=`require separate zeros or explicit parent identity`
- `CASE4016_6_constant_offset_branch`: owner=`GLOBAL_CONSTANT_CALIBRATION_ONLY`, residual=`DERIVATIVE_ZERO_BUT_ABSOLUTE_VALUE_NOT_PREDICTED`, claim=`UNIVERSALITY_CONDITIONAL_NO_NUMERICAL_G_CLAIM`, next=`look for parent normalization theorem only after local universality is closed`
- `CASE4016_7_numeric_residual_pack`: owner=`GREF_SUPERSELECTION_BLOCKED`, residual=`C_sector`, claim=`NO_GLOBAL_COUPLING_CLAIM`, next=`insert or derive parent K_G coupling sector`

## Verdict

This is progress on the actual coupling problem. The theory now has a precise way to make `G_ref` universal without pretending to derive the measured number: parent-owned global coupling sector plus no-Hom into it. Current corpus does not yet parent-sign that sector, so claims stay blocked and residual rows remain live.

## Next Target

- `4017-Y5-R2FR-kappa-sector-parent-insertion-or-Gref-residual-runner.md`
- `scripts/Y5_R2FR_4017_kappa_sector_parent_insertion_or_Gref_residual_runner.py`

## Source Count

- source needles found: `38/38`
