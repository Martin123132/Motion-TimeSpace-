# 4079 - Third P0 Bound Or Torsion/Nonmetricity Zero Theorem

- Timestamp: `2026-07-02T03:00:54+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `TORSION_NONMETRICITY_ZERO_THEOREM_CONDITIONAL_THIRD_P0_TORSION_BOUND_SOURCED_NORMALIZATION_PENDING`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Zero Theorem

4079 gets a real conditional theorem-zero route.

For nonmetricity:

```text
omega_AB = -omega_BA
Q_AB := -D_omega eta_AB = 0
```

So nonmetricity vanishes identically if the parent signs an internal Lorentz connection.

For torsion in the spinless EC/Palatini branch:

```text
S_EC[e, omega] = (4 kappa)^-1 int epsilon_ABCD e^A wedge e^B wedge R^CD[omega]
```

and the `omega` variation gives the torsion/spin equation. In a spinless local exterior with no independent torsion kinetic/source term:

```text
T^A = D_omega e^A = 0
```

This is exact, but branch-conditional.

## Why It Is Not A Public Pass

The current corpus has not yet parent-signed all required clauses:

```text
Lorentz connection as parent-owned local geometry
spinless/local exterior domain
no independent torsion kinetic term
no axial torsion source leakage
same e_obs matter/EM/clock frame before PPN readout
```

So the theorem is usable as a promotion route, not as a finished local-GR claim.

## Third Finite Bound

If spin-coupled torsion is not theorem-zeroed, it gets a sourced external scale.

Kostelecky, Russell, and Tasson constrain 19 of 24 torsion components down to order:

```text
|T| ~ 1.0e-31 GeV
```

This is a finite experimental leash on spin-coupled torsion residuals.

Important caveat:

```text
the bound is dimensionful
dimensionless PPN aggregation requires an MTS coupling/normalization map
```

## Runner Update

The local runner now has:

```text
epsilon_reciprocal_lock      numeric Cassini gamma scale
epsilon_frame_gauge_quotient numeric alpha_1 scale
epsilon_torsion_spin         finite GeV torsion scale, normalization pending
```

The aggregate still cannot be claimed because:

```text
epsilon_spatial_metric_owner
epsilon_theta_parent
epsilon_B_derivation core
epsilon_kappa_normalization
torsion dimensionless normalization
```

remain open.

## Decision

```text
torsion/nonmetricity zero theorem = exact conditional
current MTS local-GR pass = false
third P0-adjacent bound = sourced torsion scale
```

## Sources

- Kostelecky, Russell, and Tasson, `Constraints on Torsion from Lorentz Violation`, DOI `10.1103/PhysRevLett.100.111102`, arXiv `0712.4393`.

## Next

`4080` should attack:

```text
kappa_eff / Newton G normalization
```

Either prove the topological constant-G branch, or source finite `Gdot/G` and local-G calibration bounds.
