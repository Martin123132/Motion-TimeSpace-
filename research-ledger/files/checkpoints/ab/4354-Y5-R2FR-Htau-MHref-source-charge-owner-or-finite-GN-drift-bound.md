# 4354 Y5-R2FR Htau MHref source charge owner or finite GN drift bound

Marker: `PPC4161_HTAU_MHREF_SOURCE_CHARGE_OWNER_OR_FINITE_GN_DRIFT_BOUND_4354`

Decision: `CONDITIONAL_HTAU_MHREF_NEWTON_BRIDGE_DERIVED_PRIVATE_SELECTOR_GN_DRIFT_BOUND_RETAINED_NONCLAIM`

## Result

4354 derives the exact local source-coupling fork. Clean branch:

```text
D_A ln G_cal = 0,
M_H^dress = H_tau[S_link] - H_ref,
int_W rho_H dV_H = M_H^dress,
nabla^2 Phi_N = 4*pi G_cal rho_H,
a_r = -G_cal M_H^dress/r^2.
```

The branch is private and conditional. Current MTS has the fair calibrated-`G` route and private `Pi_M/H_tau` glue, but no public local-GR claim until full `H_tau` integrability, fixed `H_ref`, same `tau/e_obs`, no boundary leakage, positive `M_H_ref`, and transition-shell source hair close.

If any clause opens, use `epsilon_Gsrc` as the finite no-cancellation source/coupling residual.

## Next

| next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- |
| 4355-Y5-R2FR-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md | Can the transition shell be shown to stay in the same Hilbert worldtube with no non-Hilbert residue, or must finite source-hair rows be carried into local tests? | derive transition same-worldtube membership, epsilon_mu_tr=0, Q_l>=1_tr=0 and time/range/frame/species/beta hair = 0 from the private Hamiltonian selector | create source-backed finite rows for transition non-Hilbert residue and feed them into epsilon_Gsrc |
