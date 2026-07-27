# 4145 - Trace-free boundary, curvature routing and live adoption gate

## Decision
- Decision: `BOUNDARY_CLOSED_CONSTRUCTED_BRANCH_CURVATURE_SPLIT_LIVE_ADOPTION_UNSIGNED_MATTER_ROUTING_REQUIRED`.
- Real progress: the boundary blocker is closed inside the constructed parent branch.
- Still not claimed: local GR, Newtonian reduction, PPN beta, R10, WEP, clocks, orbital systems, or public evidence.

## Boundary closure
The well-posed parent action is

`S_TF^Omega=c_I[int_Omega sqrt|g| phi R + 2 int_partialOmega sqrt|h| phi K + 2 sum_corners int sqrt|sigma| phi eta]`.

With fixed induced metric `h_ab`, fixed/silent `phi` on the local readout boundary, and no unaccounted corner terms,

`delta_g S_TF^Omega=c_I int_Omega sqrt|g|[phi G_mn+(g_mn Box-nabla_m nabla_n)phi]delta g^mn`.

So `D_boundary=0` is derived for the constructed parent branch; it is no longer a free plateau axiom. The live corpus still needs one adoption row saying this is the boundary convention used by MTS.

## Curvature split
The same variation always gives

`Pi_TF(phi G_mn)=phi G_TF_mn`.

Therefore:
- On a genuine vacuum readout annulus, `G_mn=0`, so `D_phiG=0`.
- On finite-source support, `2 phi G_TF_mn=16 pi G phi T_TF_mn` under GR-like source routing.
- That source term is not automatically small; it needs parent-owned matter coupling or an explicit bound.

## Updated residual law
Before the 4145 closure:

`D_TF=(1-sigma_resp*c_I)K_L + 2 sigma_resp*c_I phi G_TF + D_owner + D_boundary + D_adoption`.

Inside the constructed parent branch with `sigma_resp*c_I=1` and the scalar-tensor boundary term:

`D_TF=2 phi G_TF + D_owner + D_adoption`.

In a vacuum collar, with owned `phi` and live `Khat` adoption, this would become `D_TF=0`. For finite-source tests it does not.

## Current gate table
| Gate | Result | Meaning |
|---|---|---|
| boundary | CLOSED_CONSTRUCTED_BRANCH | scalar-tensor `phi K`/corner term closes boundary variation |
| curvature | SPLIT_NOT_GENERIC_ZERO | zero in vacuum; source-coupling term inside matter |
| live Khat adoption | UNSIGNED | `Khat_current^TF` is not yet live-defined by this parent response |
| phi owner | RETAINED_BLOCKER | owner action and stress ledger still need adoption |

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4145_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4145_BOUNDARY_CLOSURE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4145_CURVATURE_ROUTING.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4145_LIVE_ADOPTION_GATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4145_RESIDUAL_UPDATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4145_DECISION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4145_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4145_NEXT_TARGET.csv`

## Next Target
- `4146-Y5-R2FR-finite-source-support-theorem-or-matter-routing-coupling-gate.md`
- Try to prove the readout/projector support theorem first. If finite-source overlap cannot be removed, derive matter-routing coupling for `16 pi G phi T_TF`; if that fails, emit `A_phiG/T_TF` bound rows.
