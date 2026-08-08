# 3116 - Public Hodge Maxwell Stress Lock or Constitutive Residual Vector under AX1090

Private checkpoint. This is the EM/Poynting source-coupling derivation promised by 3115.

## Verdict

The clean local-GR route is:

```text
public metric/coframe owns the Hodge star
visible U(1) field strength is F = dA_Q
EM kinetic normalization Z_EM is quotient-owned or fixed representation data
matter current normalization is owned by the same charge generator
```

Then:

```text
S_EM[g_pub,A_Q] -> Maxwell equations -> T_EM^munu -> Poynting vector -> Hilbert source
```

and EM energy flow is not an extra hidden force. It is part of the ordinary local source:

```text
T_total^munu = T_matter^munu + T_EM^munu + ...
```

If any Hodge, kinetic, current, clock/spectral, or constitutive piece is private rather than public-quotient-owned, the branch does **not** fail silently. It becomes an explicit EM residual vector:

```text
Delta_EM = {delta_star, b_alpha, delta_J, C_constitutive, delta_thetaFF, delta_clock_alpha, Delta_T_EM, Delta_S_Poynting}.
```

This is the useful interpretation of the Poynting/background intuition: if the background field is the parent origin of the local Hodge/flow rule, it must either descend into `g_pub/e_pub` or produce measurable constitutive/alpha/source residuals.

## Source Register

| source_id | path | role |
|---|---|---|
| 00-heuristics | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\00-martin-fork-heuristics-private.md` | Poynting/background/Hodge fork heuristic |
| 1046 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md` | alpha/constant/marker countermodels |
| 1098 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md` | ordinary constant owner signature and forbidden vertices |
| 1099 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md` | unique EM kinetic owner/no-extra-`F^2` theorem attempt |
| 1100 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md` | parent `T_Q`, charge lattice and gauge norm signature |
| 3115 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3115-Y5-R2FR-local-vertical-Noether-generator-certificate-under-AX1090.md` | Poynting is public Maxwell stress or explicit constitutive residual |

## Public Maxwell Lock

Work in the compact local branch with public metric/coframe:

```text
g_pub = g[q_parent(Phi)],
e_pub = e[q_parent(Phi)],
*_pub = *[g_pub,e_pub].
```

Let `A_Q` be the visible `U(1)` connection and:

```text
F = dA_Q.
```

The public Maxwell action is:

```text
S_EM = -1/2 integral Z_EM F wedge *_pub F + integral A_Q wedge J_Q
```

or in components:

```text
S_EM = -1/4 integral d^4x sqrt(-g_pub) Z_EM F_munu F^munu
       + S_int[A_Q,J_Q].
```

The lock conditions are:

```text
Lie_v(*_pub) = 0,
Lie_v Z_EM = 0,
Lie_v J_Q normalization = 0,
Lie_v charge labels = 0,
no independent lambda_A F^2 or f_X(X)F^2 operator,
no hidden constitutive tensor chi_X,
no readout/radiative re-entry of alpha_EM.
```

These conditions are stronger than ordinary `U(1)` gauge invariance. The gauge transformation:

```text
A_Q -> A_Q + d lambda
```

protects `F`, but it does not fix `Z_EM`, `alpha_EM`, the Hodge star, the charge base unit, or source/test current normalization.

## Maxwell Equations

Varying `A_Q` gives:

```text
dF = 0,
d(Z_EM *_pub F) = J_Q.
```

If `Z_EM` is local-constant or quotient-owned and `J_Q` is the same parent charge current used by ordinary matter, this is the standard local Maxwell sector in the public frame.

If not, the equation becomes:

```text
d(Z_EM *_pub F + Delta H_X) = J_Q + Delta J_X,
```

where:

```text
Delta H_X := hidden-Hodge/constitutive response,
Delta J_X := hidden source/test current normalization or marker response.
```

Those are not harmless notation changes. They feed clocks, spectra, WEP, R10, material response and EM source stress.

## Hilbert Stress Derivation

For the public action with `Z_EM` independent of private representatives:

```text
T_EM^munu := -2/sqrt(-g_pub) delta S_EM / delta g_pub_munu
```

gives:

```text
T_EM^munu =
Z_EM (F^mu_alpha F^{nu alpha}
      - 1/4 g_pub^munu F_alpha_beta F^{alpha beta}).
```

Thus the local gravity/source equation is:

```text
G_munu[g_pub] + Lambda_eff g_pub_munu
= kappa_eff (T_matter_munu + T_EM_munu + T_other_public_munu)
  + O(epsilon^6)
```

provided the strict local quotient conditions from 3114/3115 are signed.

This is the source-coupling win: EM field energy, radiation pressure and Poynting flow gravitate through the same Hilbert stress mechanism as ordinary matter.

## Poynting Vector Readout

For a public observer field `u^mu`, define the spatial projector:

```text
h^mu_nu = delta^mu_nu + u^mu u_nu/c^2.
```

The public energy flux is:

```text
S_pub^mu[u] = -h^mu_alpha T_EM^{alpha beta} u_beta.
```

In a local inertial frame this reduces to the usual Poynting vector form:

```text
S_pub ~ E x H
```

with `H` determined by the public constitutive relation:

```text
H = Z_EM *_pub F.
```

So:

```text
Poynting flux is not an extra gravitational source.
Poynting flux is the spatial energy-flow component of T_EM.
```

If MTS wants to say the Poynting vector is "working on the background field", the rigorous translation is:

```text
the background determines *_pub and/or Z_EM and/or J_Q.
```

Then the branch choice is sharp:

```text
background -> public quotient Hodge/normalization
=> clean Maxwell-Hilbert source lock.

background -> private hidden constitutive/alpha/current response
=> explicit Delta_EM residual vector.
```

## Conservation and Source Coupling

With the public Maxwell equations:

```text
nabla_mu T_EM^{mu nu} = -F^{nu lambda} J_lambda
```

up to sign convention for the interaction term. Charged matter has the opposite Lorentz-force exchange:

```text
nabla_mu T_charged_matter^{mu nu} = +F^{nu lambda} J_lambda.
```

Therefore:

```text
nabla_mu (T_EM^{mu nu} + T_charged_matter^{mu nu}) = 0.
```

This is exactly what the Bianchi identity needs in the public local-GR branch.

If hidden constitutive pieces exist:

```text
nabla_mu T_EM^{mu nu} + F^{nu lambda}J_lambda = R_EM^nu,
```

then `R_EM^nu` is a real residual source/current term. It must be projected into PPN, clock, WEP, orbital, R10 or EM propagation tests.

## Constitutive Residual Vector

The most general local hidden EM leak can be written schematically as:

```text
S_EM^hidden =
-1/4 integral sqrt(-g_pub)
  [ Z_EM(q,X) F^2
    + C_X^{munu rho sigma} F_munu F_rhosigma
    + theta_X F_munu *F^munu ]
  + integral A_Q wedge Delta J_X
  + S_readout_alpha[X].
```

The residual vector is:

| residual_id | symbol | meaning | arena links |
|---|---|---|---|
| EMR3116_0 | `delta_star` | hidden/private Hodge-star or coframe dependence | light propagation, clocks, PPN, EM stress |
| EMR3116_1 | `b_alpha` | vertical derivative of `ln alpha_EM` or `ln Z_EM^-1` | clocks, spectra, WEP, R10 |
| EMR3116_2 | `delta_J` | hidden source/test current normalization | WEP, R10, charge-source calibration |
| EMR3116_3 | `C_constitutive` | anisotropic or material/background constitutive tensor | birefringence, EM wave propagation, stress |
| EMR3116_4 | `delta_thetaFF` | axion/pseudoscalar `theta_X F wedge F` response | polarization, propagation, parity-odd EM |
| EMR3116_5 | `delta_clock_alpha` | spectral/clock readout re-entry | clock comparisons, alpha drift |
| EMR3116_6 | `Delta_T_EM` | extra Hilbert stress from hidden EM operator | local GR, PPN, orbital/source mass |
| EMR3116_7 | `Delta_S_Poynting` | hidden correction to EM energy flux readout | radiation pressure, source coupling, EM tests |

These rows do not claim a failure. They define the honest residual slots if public Hodge/Maxwell lock is not derived.

## What Is Signed Here

3116 signs the conditional theorem:

```text
If *_pub, Z_EM, J_Q, charge lattice, no-extra-F2, and clock/spectral readout
all descend through the public quotient or fixed representation data,
then EM stress and Poynting flux source gravity through T_EM with no extra local residual.
```

3116 does **not** sign the parent inputs:

```text
T_Q owner,
fixed generator norm,
no independent F_Q^2,
same current owner,
radiative/readout closure.
```

Those remain the live EM coupling gap identified by 1099/1100.

## No-Smuggling Rules

1. Do not add Poynting as a second gravitational source outside `T_EM`.
2. Do not claim compact `U(1)` alone derives `alpha_EM`; it fixes relative charge labels, not the continuous kinetic coefficient.
3. Do not hide `b_alpha` with unit choice; `alpha_EM` is dimensionless.
4. Do not call a private Hodge/constitutive shift vertical unless it passes the 3115 Noether/readout/boundary certificate.
5. Do not use Maxwell closure as a local-GR claim until source current, charge normalization and EM stress are in the same public frame as gravity.

## Claim Status

No public Maxwell, EM-stress, Poynting, alpha, WEP, R10, clock, local-GR, derived-`G`, or unification claim follows from 3116.

The internal advance is:

```text
Poynting/background intuition has a formal route:
public Hodge/Maxwell lock -> clean Hilbert source,
private Hodge/constitutive leak -> explicit residual vector.
```

## Next Target

Write:

```text
3117-Y5-R2FR-EM-coupling-owner-no-extra-F2-or-alpha-residual-bound-priority-under-AX1090.md
```

Direct target:

1. try the derivation route first: parent `T_Q`, fixed charge lattice/base unit, fixed gauge-fibre norm, no independent `F_Q^2`, same current owner, radiative/readout closure;
2. if the owner theorem fails, prioritize which residual coefficient must be bounded first: `b_alpha`, `delta_J`, `delta_star`, or `C_constitutive`;
3. connect that choice to the existing clock/WEP/R10 alpha rows without claiming an MTS pass.
