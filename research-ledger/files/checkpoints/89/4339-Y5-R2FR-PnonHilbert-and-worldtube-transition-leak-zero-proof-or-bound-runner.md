# 4339 Y5-R2FR PnonHilbert and worldtube transition leak zero proof or bound runner

Marker: `PPC4161_PNONHILBERT_AND_WORLDTUBE_TRANSITION_LEAK_ZERO_PROOF_OR_BOUND_RUNNER_4339`

Decision: `FIRST_TWO_PLEAK_ZERO_PROOFS_FAIL_BUT_REDUCED_TO_DVQTR_AND_WORLDTUBE_TRACE_DEFECT_BOUND_MACHINERY_NONCLAIM`

## Result

The first two raw transition-shell leak channels are not zero-derived yet, but they are no longer vague:

```text
P_nonHilbert -> D_v q_tr = nabla(D_v Gamma_eff) - div(D_v K_hat) + connection/boundary
P_off_worldtube -> N_inner <= ||mu_tr|| + ||B_src^A||, reduced by lambda_* and S_U_not_inner
```

## Component Update

| component | zero_status_after | main_formula | next_input |
| --- | --- | --- | --- |
| P_nonHilbert_action_domain | NOT_ZERO_DERIVED_REDUCED_TO_DVQTR_BOUND | D_v q_tr^nu = nabla^nu(D_v Gamma_eff)-nabla_mu(D_v K_hat^(mu nu))+C_conn^nu+B_boundary^nu | Delta_K zero/bound plus D_v Gamma quadratic values |
| P_off_worldtube_readout_order | NOT_ZERO_DERIVED_REDUCED_TO_TRACE_DEFECT_BOUND | N_inner <= \|\|mu_tr\|\|+\|\|B_src^A\|\| <= C_N[K_U C_col S_U_not_inner/lambda_*+R_U]+\|\|B_src^A\|\| | lambda_*, S_U_not_inner, mu_tr/B_srcA, same-worldtube readout-order contract |

## Next

| next_target | target_question | preferred_route |
| --- | --- | --- |
| 4340-Y5-R2FR-DvKhat-DeltaK-and-worldtube-trace-defect-input-fill.md | Can Delta_K and the worldtube trace-defect inputs be zeroed or sourced enough to score the first local bound? | derive Delta_K=0 from Khat metric ownership while proving lambda_*>0 and S_U_not_inner/B_srcA/mu_tr silence |
