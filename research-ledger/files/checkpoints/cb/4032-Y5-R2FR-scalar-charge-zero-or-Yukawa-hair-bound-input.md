# 4032 - Scalar Charge Zero Or Yukawa Hair Bound Input

- Timestamp: `2026-07-01T22:53:42+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## What Actually Moved

4032 turns the remaining scalar-hair clause into a concrete charge identity. With

`u := phi - phi_*`

and

`(Delta - mu_phi^2)u = (2/3)F`,

the exterior scalar charge is

`Q_phi[S]=int_S n.grad u dS`.

Integrating over the compact source worldtube gives

`Q_phi = mu_phi^2 int_W u dV + (2/3)int_W F dV`.

So `Q_phi=0` is not magic. It follows if the source branch has neutral `F` charge and fixed-branch/no-flux `u`.

## If The Zero Fails

For `lambda_phi=1/mu_phi`,

`u(r)=Q_phi exp[-r/lambda_phi]/(4*pi*r)+multipoles+outer_boundary`.

That maps to a finite-range row:

`alpha_phi(lambda_phi)=C_alpha_phi*(Q_phi/M_H)*(q_test/m_test)`.

Universal test response may remove composition dependence, but it does not remove the common fifth force. So surviving `Q_phi` must go to R10 `alpha(lambda)`, source-WEP, and `C_beta_TF` scoring.

## Current Verdict

- Current evaluator result: `QPHI_ZERO_NOT_LIVE_YUKAWA_BOUND_READY_SYMBOLIC`.
- Claim result: `NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4032`.
- Source needles found: `8/8`.

## Next Target

- `4033-Y5-R2FR-source-neutral-F-proof-or-alpha-lambda-curve-row.md`
- `scripts/Y5_R2FR_4033_source_neutral_F_proof_or_alpha_lambda_curve_row.py`
