# 4075 - Flow-Coframe Repair Or Effective GR Residual Scorer

- Timestamp: `2026-07-02T02:39:19+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `RADIAL_THETA_REPAIR_CONDITIONAL_FULL_4D_THETA_NOT_PARENT_SIGNED_EFFECTIVE_GR_RESIDUAL_SCORER_BUILT`
- Public GR/Newton/PPN claim: `false`
- GitHub action: `false`

## Result

4075 takes the `Theta^A` repair seriously rather than just saying "coframe missing".

The good news:

```text
Theta^0 = T c dt
Theta^1 = sqrt(S) dr
ds^2_(t,r) = -(Theta^0)^2 + (Theta^1)^2
```

is a clean conditional radial observer-cell coframe. Together with:

```text
T^2 S = 1
```

it gives the familiar weak-field PPN result:

```text
gamma = 1
```

because `S = (1-L)^(-p)` gives `gamma = p`, and reciprocal routing fixes `p = 1`.

## Where The Repair Fails

The full local GR branch needs four one-forms:

```text
Theta^A = (Theta^0, Theta^1, Theta^2, Theta^3)
```

A clock one-form plus radial routing only builds the `t-r` cell. To build full `Theta^A`, we need:

```text
n_mu
h_mu_nu on ker(n)
orientation
local SO(3)/Lorentz frame gauge
E^i_mu with h_mu_nu = delta_ij E^i_mu E^j_nu
omega^AB
B^A = Theta^A - D_omega X^A
```

The reconstruction theorem exists mathematically. But unless MTS owns those objects before borrowing GR, it is a tetrad import.

## The Exact Theorem

Given a nonzero clock one-form `n_mu` and a positive spatial metric `h_mu_nu` on `ker(n)`, one can locally choose a spatial triad `E^i_mu` such that:

```text
h_mu_nu = delta_ij E^i_mu E^j_nu
Theta^0 = c n
Theta^i = E^i
g_mu_nu = -Theta^0_mu Theta^0_nu + delta_ij Theta^i_mu Theta^j_nu
```

That proves a conditional coframe reconstruction theorem.

It does not prove MTS derives the coframe.

## Safe Testing Bridge

Until the parent spatial triad/frame gauge is signed, local tests should use:

```text
effective GR baseline + MTS residual scorer
```

with:

```text
R_eff_GR = sqrt(sum_i w_i residual_i^2)
```

and P0 residuals:

```text
epsilon_theta_parent
epsilon_B_derivation
epsilon_reciprocal_lock
epsilon_torsion
epsilon_nonmetricity
epsilon_kappa_normalization
```

plus downstream EM/clock/source/frame residuals:

```text
Delta_Hodge_EM
epsilon_clock_strain
source_label_leak
Qcoh_Noether_deformation
Delta_ref_frame_profile_over_MH
```

## Decision

4075 moves the work forward in a precise way:

```text
radial Theta repair = conditional pass
full 4D Theta derivation = blocked without parent triad/frame gauge
testing route = effective GR residual scorer, not public derivation claim
```

## Next

`4076` should attack the exact remaining object:

```text
parent-owned spatial triad / SO(3)-Lorentz frame gauge
```

If that cannot be derived, instantiate the residual scorer with the best available local, EM, clock, R10, and orbital bound rows.
