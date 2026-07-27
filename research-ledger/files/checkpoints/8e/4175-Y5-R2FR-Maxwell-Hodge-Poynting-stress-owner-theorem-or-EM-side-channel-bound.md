# 4175 - Maxwell-Hodge/Poynting Stress Owner Theorem Or EM Side-Channel Bound

Timestamp UTC: `2026-07-03T02:14:29+00:00`  
Branch: `MTS_R2FR_Y5_MAXWELL_HODGE_POYNTING_STRESS_OWNER_4175`  
Decision: `MAXWELL_HODGE_POYNTING_STRESS_OWNER_THEOREM_CLOSES_EM_SIDE_CHANNEL_PRIVATE_SELECTOR`

## Move Made
4174 isolated the EM/Poynting owner gate as the most physical coupling leak. 4175 closes it inside the private selector branch.

## Derivation

```text
S_MH[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu
```

varies to:

```text
T_EM^mu_nu = F^mu_alpha F^nu_alpha - 1/4 g_obs^mu_nu F_alpha_beta F^alpha_beta.
```

The local Poynting vector is:

```text
S_i = -T_EM(n,e_i) = (E cross B)_i.
```

Therefore Poynting flux is already owned by the Hilbert source tensor. It cannot be added again as a hidden background force/source.

## Conservation

```text
nabla_mu T_EM^mu_nu = -F_nu_lambda J^lambda,
nabla_mu T_matter+binding^mu_nu = F_nu_lambda J^lambda,
nabla_mu T_total^mu_nu = 0.
```

So the Lorentz force is internal matter-EM exchange, while total source conservation remains intact.

## Guardrail
Radiative EM flux is not erased. Nonzero flux across the collar boundary must be boundary/Hamiltonian charge flux. The next target is the boundary/interface no-flux theorem.

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4175_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4175_MAXWELL_HODGE_ACTION_VARIATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4175_POYNTING_STRESS_IDENTIFICATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4175_TOTAL_CONSERVATION_AND_LORENTZ_EXCHANGE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4175_EM_SIDE_CHANNEL_CLOSE_OR_REACTIVATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4175_BRANCH_DECISION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4175_CLAIM_FIREWALL.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4175_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4175_NEXT_TARGET.csv`
