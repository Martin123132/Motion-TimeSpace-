# 4164 - PPC4161 Local PPN Readout Gate

Timestamp UTC: `2026-07-02T12:18:56+00:00`  
Branch: `MTS_R2FR_Y5_PPC4161_LOCAL_PPN_READOUT_GATE_4164`  
Decision: `PPC4161_LOCAL_PPN_RESIDUAL_VECTOR_DERIVED_PUBLIC_LOCAL_GR_CLAIM_STILL_BLOCKED`

## Purpose
4163 synced the private PPC4161 local packet into the formal spine without making a public claim. 4164 now does the next real mathematical job: translate the packet into a local PPN residual vector.

This is not another target list. The derivation gate is:

```text
S_loc^{<=2PN} =
S_EH[g_obs;kappa_*]
+ S_matter[psi,g_obs,theta]
+ S_EM[A,g_obs]
+ S_binding
+ S_GK
+ B_proper
+ S_top
+ S_vertical
+ S_reset
```

Varying with respect to `g_obs` gives the effective local equation:

```text
G_mu_nu(g_obs)
= kappa_* T_total_mu_nu
+ R_GK_mu_nu
+ R_top_mu_nu
+ R_vertical_mu_nu
+ R_reset_mu_nu
+ R_boundary_mu_nu.
```

Normalize against the measured local Newton source:

```text
E_mu_nu := G_mu_nu - 8*pi*G_N*T_total_mu_nu/c^4.
```

Then the PPN deviations are projections of the residual tensor:

```text
Delta p_A = <W_A, E_mu_nu> + O(E^2),
A in {gamma,beta,alpha1,alpha2,alpha3,xi,zeta1,zeta2,zeta3,zeta4,Gdot/G}.
```

## Private PPN Theorem
If PPC4161 is adopted and its `<=2PN` readout clauses hold, then:

```text
R_PPN =
(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta1,zeta2,zeta3,zeta4,Gdot/G)
= 0.
```

That is the actual leap: the local packet is now mapped onto the full standard local-GR PPN vector, not only the first-order Newton kernel.

## Fallback Bound
If any clause fails, the result demotes immediately to:

```text
epsilon_PPN
<= C_kappa epsilon_kappa
+ C_EH epsilon_EH
+ C_m epsilon_matter
+ C_EM epsilon_EM
+ C_extra epsilon_extra
+ C_B epsilon_boundary
+ C_tau epsilon_tau
+ C_cosmo epsilon_cosmo_leak.
```

So the branch no longer falls into vague failure. It either gives the GR PPN vector privately, or it gives a named residual vector to bound.

## Claim Firewall
- This is not a public local-GR theorem.
- This is not a prediction of the numerical value of `G`.
- This is not an empirical PPN pass.
- It is a private symbolic readout gate from PPC4161 to the standard PPN vector.

## Next Target
`4165-Y5-R2FR-kappa-G-normalization-superselection-or-coupling-derivation.md`

Reason: the next exposed coupling issue is `kappa_*`. Either MTS derives/superselects it from the parent action, or we explicitly treat `G_N` as a measured calibration constant in the same practical sense GR does.

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4164_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4164_CLAUSE_AUDIT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4164_DERIVATION_GATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4164_PPN_RESIDUAL_VECTOR.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4164_THEOREM_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4164_CLAIM_FIREWALL.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4164_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4164_NEXT_TARGET.csv`
