# 4950 - Reflection-even pair operators and the galaxy/local bifurcation window

Marker: `MTS_PAIR_OPERATOR_RG_BIFURCATION_WINDOW_4950`.

Date: `2026-07-13`.

Status: private analytic, source-acquired, source-executed and data-executed
checkpoint. The pair-source route proposed at 4949 has been attacked rather
than merely listed. Curved-space RG proves that an interacting even scalar
potential cannot in general be completed without a nonminimal `F_k(psi)R`
function. The existing parent simultaneously excludes an independent direct
`T_matter psi^2` vertex at fixed metric and contains a generated derivative
`X^2` channel whose parent-scheme coefficient is still unsolved. The exact
stabilized environmental zero-mode law is derived. Applied to all 175 public
LTG samples and four universal Compton ranges, the minimal spherical
`R psi^2/T psi^2` activation window is empty against the Sun, white dwarf and
neutron-star stability ceilings. The current minimal local pair route is
therefore rejected. The next legitimate route is the coupled parent
`V_k-F_k-Z_k-X^2` flow, not a fitted scalarization coefficient.

## 1. Correction and refinement of checkpoint 4949

Checkpoint 4949 correctly rejected the **displayed quadratic** scalar 2PI
route. Its `Gamma_2^scalar=0` statement must remain scoped to that displayed
truncation. Checkpoint 4941 had already established the lower essential
derivative interaction

```text
c_ess X^2,

c_ess=c+8pi g(ctilde+d),

beta_c,ess|0=16g^2
```

in its source comparator. Its Type-II parent-scheme fixed-point value was not
calculated or spliced into the completed six-coordinate point. Since `X^2`
is quartic in fluctuations, it gives nonzero 2PI scattering kernels in an
occupied state. But

```text
delta^2(X^2)/delta psi^2|psi=0=0,
```

so it supplies neither a static mass source nor a vacuum bifurcation. The
4949 static-vacuum rejection survives; its collisionless language does not
extend to a future occupied `X^2` completion.

## 2. Parent operator-generation audit

The selected reflection permits even operators. A curved-space scalar
functional has the form

```text
Gamma_k
 =int sqrt(g)[Z_k(psi)X/2+V_k(psi)+F_k(psi)R+...].
```

Primary curved-space functional-RG calculations show that `V_k` and `F_k`
flow together. In the four-dimensional one-loop limit at constant `Z`,

```text
partial_t V
 =(V'')^2/[2(4pi)^2 Z^2],

partial_t F
 =-V''[(1/6)-F''/Z]/[(4pi)^2 Z].
```

For

```text
V=lambda psi^4/24,

F=xi psi^2/2,
```

this gives exactly

```text
beta_lambda=3lambda^2/(4pi)^2,

beta_xi=lambda(xi-1/6)/(4pi)^2.
```

Therefore

```text
beta_xi|xi=0=-lambda/[6(4pi)^2]
```

and the minimal `xi=0` surface is not invariant when the regular even
potential has nonzero quartic coupling. The conformal value is the one-loop
fixed surface in this comparator. Quantum gravity can change the beta
function and fixed point, so the number `1/6` is not inserted as an MTS
prediction. What is imported is the structural conclusion: a source-complete
curved motion flow must solve `F_k`, not omit it.

This sharpens the parent status:

- `R psi^2` is symmetry allowed and required as an RG coordinate once the
  interacting regular potential is retained, but its MTS value is unknown;
- a direct `T_matter psi^2` term is excluded by the fixed-metric hidden/visible
  factorization of checkpoint 4919;
- metric field redefinitions or the leading Einstein trace can map a
  curvature term into a correlated trace interaction, but do not create a
  second independent coefficient;
- `X^2` is a generated derivative interaction, not a static mass source;
- `O4=C^2X` remains a positive kinetic portal, not an environmental negative
  mass;
- the regular quartic stabilizer is a Taylor coordinate of the unsolved full
  potential and cannot be copied from the rejected fractional one-coupling
  family.

The current pair sector is consequently not RG closed.

Primary structural sources:

- R. Martini and O. Zanusso, *Renormalization of multicritical scalar models
  in curved space*, `https://arxiv.org/abs/1810.06395`;
- B. S. Merzlikin, I. L. Shapiro, A. Wipf and O. Zanusso,
  *Renormalization group flows and fixed points for a scalar field in curved
  space with nonminimal F(phi)R coupling*,
  `https://arxiv.org/abs/1711.02224`.

## 3. One effective local pair coefficient

Test the most economical local extension without adopting it:

```text
S_pair
 =int sqrt(-g)[
  -X/2
  -(m_gap^2+xi_R R+xi_T T/M_R^2)psi^2/2
  -lambda psi^4/24].
```

The trace of the 4947 Einstein equation, at negligible `Lambda` and
higher-gradient order, is

```text
R=-T/M_R^2.
```

Hence the two written quadratic terms reduce to one physical coefficient:

```text
m_eff^2=m_gap^2+(xi_R-xi_T)R,

B:=-(xi_R-xi_T)>0
```

for an attractive environmental channel. Introducing separate fitted
`xi_R` and `xi_T` values would double-count one leading local operator.

The static spectral operator is

```text
L_B=-nabla^2+m_gap^2-BR(x).
```

Its exact lowest eigenvalue is the Rayleigh quotient

```text
lambda_0(B)
 =inf_f
  {int[|grad f|^2+m_gap^2f^2]-B int Rf^2}
  /int f^2.
```

The local GR branch requires `lambda_0>0`. A galaxy branch requires
`lambda_0<0`. The same `B`, `m_gap` and stabilizer must be used everywhere.

## 4. Exact stabilized top-hat law

For a constant-density sphere of radius `L` and compactness

```text
C=GM/(Lc^2),

R_0=6C/L^2,
```

the first zero mode has an interior `sin(kappa r)/r` profile and an exterior
`exp(-m_gap r)/r` profile. Continuity of the field and flux gives

```text
x cot x=-mu,

mu=m_gap L,

x in [pi/2,pi),

B_crit=(mu^2+x^2)/(6C).
```

The massless/longest-range case is the most favorable:

```text
B_crit(m=0)=pi^2/(24C).
```

For a normalized lowest eigenfunction `f_0`, let `psi=A_0 f_0`. Near a
negative crossing, the exact one-mode energy is

```text
Delta E
 =lambda_0 A_0^2/2
  +lambda A_0^4 int f_0^4/24.
```

If `lambda>0`, minimization gives

```text
A_0^2
 =-6lambda_0/[lambda int f_0^4],

Delta E_min
 =-3lambda_0^2/[2lambda int f_0^4].
```

Thus a stabilizer would predict an amplitude only after `lambda`, `B` and the
physical eigenfunction are parent-derived. The amplitude cannot be an
additional galaxy fit.

## 5. Local stability ceilings

The unchanged 4947 systems give the massless spherical thresholds

```text
Earth        B_crit=5.90741454e8,
Sun          B_crit=1.93743502e5,
white dwarf  B_crit=1.94940997e3,
neutron star B_crit=2.38703262.
```

The horizon row is not treated as a uniform material trace source. The
neutron-star number is only a top-hat comparator; checkpoint 4886 already
demonstrated with full EOS profiles that gradient energy and trace sign must
be solved rather than inferred pointwise. The Sun and white-dwarf rows are
enough for the present weak/local gate.

Any universal `B` above the relevant ceiling destroys the automatic
`psi=0` continuation used in the 4947 correspondence theorem.

## 6. Public 175-galaxy window

For each public ROTMOD record, the locked baryonic outer compactness proxy is

```text
C_bar
 =[V_gas|V_gas|+0.5V_disk^2+0.7V_bulge^2]/c^2.
```

The exact spherical threshold was evaluated for

```text
m_gap=0,
lambda_C=100 kpc,
lambda_C=10 kpc,
lambda_C=1 kpc.
```

In the most favorable massless case,

```text
minimum galaxy B_crit =9.10410878e5,
median galaxy B_crit  =1.784007996e7,
maximum galaxy B_crit =4.688973474e8.
```

The most easily activated public galaxy still requires

```text
B_gal,min/B_Sun=4.69905,

B_gal,min/B_WD=467.019.
```

Every one of the 700 galaxy/range rows has

```text
window versus Sun          = false,
window versus white dwarf  = false,
window versus neutron star = false.
```

Finite mass increases the separation because galaxy radii are vastly larger
than local-body radii. A local mass term cannot selectively stabilize the Sun
while leaving a galaxy-wide mode easier to excite.

## 7. Shape-aware potential diagnostic

The spherical result is not silently promoted to an exact thin-disk theorem.
As a separate shape-aware diagnostic, each complete baryonic rotation curve
was integrated into a midplane potential-depth proxy:

```text
|Phi_bar|_proxy
 =V_bar^2(r_min)/2
  +int_(r_min)^(r_out)V_bar^2(r)dlnr
  +V_bar^2(r_out).
```

The first and last terms are explicit solid-body-inner and Kepler-tail
continuations. For the massless Birman-Schwinger kernel, the corresponding
no-bound-state scale is

```text
U_proxy=2|Phi_bar|_proxy/c^2,

B_floor,proxy=1/U_proxy.
```

Across the public sample,

```text
min B_floor,proxy=1.43202586e5.
```

This remains `73.46` times above the white-dwarf spherical ceiling. It
supports the same ordering but is not a full three-dimensional disk
eigenvalue solve. A centrally localized mode would also not by itself supply
the galaxy-wide occupation stress required by rotation curves.

## 8. Decision

```text
curved scalar V-F RG closure                      = required;
one-loop beta_xi identity                         = derived;
xi=0 invariant with nonzero quartic               = false;
independent direct T_matter psi2                   = excluded;
X2 derivative interaction                         = generated channel;
X2 parent-scheme coefficient                      = open;
X2 static mass source                             = zero;
stabilized bifurcation amplitude law              = derived;
175-galaxy spherical window                       = executed;
universal spherical galaxy/local window           = empty;
potential-depth proxy                             = locally incompatible;
full three-dimensional disk spectrum              = not solved;
xi lambda X2 parent values                        = not predicted;
current minimal local pair route                  = rejected;
4947 automatically survives arbitrary pair term  = false;
full MTS galaxy unification                       = false.
```

This is a second constructive rejection. It prevents the theory from escaping
the 4949 no-source result by adding the first available even scalarization
term. The missing coupling is not merely a number: the entire curved motion
functional block has to close on the same critical trajectory.

## 9. Next target

`4951-Y5-R2FR-coupled-motion-VFZX2-functional-flow-fixed-point-index-and-GR-connected-trajectory-or-even-pair-sector-rejection.md`

Construct a common parent-scheme polynomial/functional projection for
`V_k(psi)`, `F_k(psi)R`, `Z_k(psi)` and `c_ess X^2`, append it to the existing
gravity-motion stability block and determine:

1. whether a finite reflection-even fixed point exists;
2. how many relevant directions it adds after `G_N` and `J_gap`;
3. whether the GR-connected trajectory fixes `xi`, `lambda` and `c_ess`;
4. whether its infrared spectrum remains positive in local systems.

Do not run another galaxy fit unless that parent flow produces a coefficient
and a viable local spectrum.

No GitHub action is authorized.
