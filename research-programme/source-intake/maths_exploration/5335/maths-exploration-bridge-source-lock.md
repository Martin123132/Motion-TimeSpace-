# Maths-exploration bridge source lock

This private source note freezes only the formulas being tested at checkpoint
5335. It does not promote the source repository's toy constructions to an MTS
parent derivation.

## Provenance

- Repository: `https://github.com/Martin123132/maths-exploration-`
- Commit: `f253617090be3917b9949bde3c90ff0aea263c80`
- `Maths` blob: `aec6a84e4e945e30ea051f0e00a6e99dea3aa326`
- `Spectrum` blob: `cb0ffb13091055d28cfbc65c5f7c33095eca9646`
- Acquisition method: authenticated read-only GitHub API inspection on
  `2026-08-06`; no repository mutation.

## Locked source formulas

In the source's flat-frame wave construction,

```text
S_j=c u_j n_j,
v_E=(sum_j S_j)/(sum_j u_j).
```

Two equal counter-propagating components have zero net flux but positive total
energy and a timelike composite four-momentum. The source explicitly does not
infer binding from this observation.

For a scalar wave with speed `u` and point-history source,

```text
(partial_t^2-u^2 Laplacian) phi=J,
J(x,t)=q(t) delta^3(x-z(t)),
t-tau_r=|x-z(tau_r)|/u,
phi(x,t)=sum_r q(tau_r)/[
  4 pi u^2 R_r |1-rhat_r dot v_r/u|
].
```

The denominator is the retarded history-map Jacobian. The source reports
independent toy validations of the regular-root formula, fold/cusp/critical
exponents, multi-root interference, and finite-band history recovery.

## Claim boundary

These formulas are source-owned flat-background kinematics and toy-model
validation. Checkpoint 5335 must independently determine whether their
covariant form can be a state observable or spectral ingredient of the MTS
motion sector. They do not by themselves derive the Einstein-Hilbert action,
Newton's constant, an MTS coupling, a local-GR attractor, or a galaxy law.
