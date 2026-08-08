# 4069 - Psi To Observed Metric/EH Induction Or Demotion

- Timestamp: `2026-07-02T02:02:51+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `SINGLE_SCALAR_COVARIANCE_REJECTED_PSI_PACKET_COFRAME_EH_ROUTE_CONSTRUCTED_CONDITIONALLY`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## The Important Result

4069 rejects the weak version:

```text
one real scalar psi -> <d psi d psi> -> full spacetime metric
```

That route fails as a derivation because a single scalar gradient outer product is rank `<=1`, and a Euclidean covariance cannot by itself produce Lorentzian signature.

But 4069 does **not** kill the GR bridge. It upgrades the viable route:

```text
rank-four psi packet / motion coframe
e^A_mu = L_A <D_mu Psi^A>_loc
g_obs_mu_nu = eta_AB e^A_mu e^B_nu
```

If `det(e) != 0` and `eta_AB` is an internal Lorentzian metric, then `g_obs` is a genuine nondegenerate Lorentzian metric. That part is a clean conditional proof, not handwaving.

## EH Normal Form

The EH step is still conditional but now sharply stated:

```text
psi packet -> induced coframe/metric
local diffeomorphism + internal Lorentz symmetry
only massless spin-2 survives at leading two-derivative order
extra torsion/scalar/vector/higher-curvature modes silent or residualized
=> EH + Lambda + boundary/topological terms
```

So the win is: the metric-signature problem has a plausible derived route. The remaining work is parent-action ownership of the packet, normalization, internal Lorentz form, and extra-mode silence.

## What Must Be Demoted

The old phrase "a scalar field psi defines the metric by gradient covariance" should not be used literally anymore. The safe version is:

```text
an MTS motion packet, whose rank-four local coframe/covariance descends through q_parent,
induces the observed metric.
```

## Next

`4070` should build the psi-packet/coframe parent action gate: field content, normalization, internal Lorentz symmetry, torsion/extra-mode silence, and the route to EH normal form.
