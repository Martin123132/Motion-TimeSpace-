# 4082 - EM Hodge Maxwell Source Theorem Or Light-Cone Bound

- Timestamp: `2026-07-02T03:25:12+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `EM_HODGE_MAXWELL_THEOREM_EXACT_CONDITIONAL_PARENT_UNSIGNED_LIGHT_CONE_BOUNDS_SOURCED`
- Public Maxwell/QED/charge claim: `false`
- GitHub action: `false`

## Result

This checkpoint does move the work forward: the EM/Poynting route is no longer just a vague missing-coupling complaint.

The exact conditional theorem is:

```text
S_EM = -1/2 int F wedge *obs F + int A wedge *obs J
F = dA
dJ = 0
*obs = Hodge[e_obs(q)]
```

then:

```text
dF = 0
d*obs F = *obs J
principal cone = null cone of e_obs
T_EM is the Hilbert stress from the same observed coframe
nabla_mu(T_matter + T_EM)^{mu nu} = 0
```

So the Poynting vector is not a separate hidden source if the parent action puts EM in the same Hilbert branch before calibration/readout. It is the Maxwell momentum/energy flux already inside `T_EM`.

## Why It Is Not Promoted

The current MTS corpus still lacks a parent-signed package:

```text
A_mu or F
F = dA or dF = 0
conserved J
same observed Hodge star *obs
unique w_EM normalization
charge-current normalization C_JQ
Coulomb/static source limit
alpha_EM owner
```

That blocks:

```text
MTS derives Maxwell EM = false
MTS derives charge/QED/alpha_EM = false
```

but preserves:

```text
same-Hodge Maxwell theorem = exact conditional
Poynting Hilbert accounting theorem = exact conditional
```

## Conformal Hodge Point

In four spacetime dimensions, the Hodge star on two-forms is conformally invariant:

```text
*_(Omega^2 g) F = *_g F
```

This is helpful but not enough. Source-free EM can share the light cone while still leaving scale, clocks, current normalization, and `alpha_EM` open.

## External Bounds Acquired

Nonclaim residual scales now exist for the EM/Hodge branch:

```text
Delta gamma photon energy dependence < 2.100e-15
E_QG,1 linear dispersion > 7.6 E_Pl
E_QG,2 quadratic dispersion > 1.300e+11 GeV
birefringent photon relativity violation < 1.0e-37
```

These bounds do not prove MTS. They stop the EM branch from floating without empirical teeth.

## Decision

```text
same-Hodge Maxwell/Poynting theorem = exact conditional
current Maxwell/charge claim = false
finite photon light-cone/dispersion/birefringence residual scales = sourced
```

## Sources

- Kostelecky and Russell, `Data Tables for Lorentz and CPT Violation`, arXiv `0801.0287`, 2026 edition.
- Bartlett et al., `Constraints on Equivalence Principle Violation from Gamma Ray Bursts`, Phys. Rev. D 104, 084025.
- Vasileiou et al., `Constraints on Lorentz Invariance Violation from Fermi-Large Area Telescope Observations of Gamma-Ray Bursts`, Phys. Rev. D 87, 122001.
- Kostelecky and Mewes, `Sensitive polarimetric search for relativity violations in gamma-ray bursts`, Phys. Rev. Lett. 97, 140401.

## Next

The next non-circular target is:

```text
4083-Y5-R2FR-charge-current-normalization-or-standard-EM-import-contract.md
```

This should decide whether the local branch imports standard visible Maxwell as a disciplined sector while MTS derives gravity/source coupling, or whether MTS can actually parent-derive:

```text
J, q_e, w_EM, Coulomb limit, alpha_EM
```
