# 3108 - Y5 R2FR source-charge/Gauss bridge or GM calibration residual under AX1090

**Purpose:** push the `G1` bridge instead of circling it. `3107` separated calibrated Newton coupling from a deeper parent derivation of `G`. This checkpoint derives the non-circular weak-field chain

```text
T_total_munu
-> parent Hilbert source charge M_H[W]
-> Gauss/Poisson surface charge
-> exterior 1/r potential
-> orbital GM readout
```

and states exactly where current MTS still lacks parent signatures.

**Verdict:** the Gauss/orbital part is derivable once a same-frame Hilbert source mass `M_H[W]` and residual silence are supplied. Current MTS is closer than before because the bridge theorem is explicit and does not require deriving the numerical value of `G`, but a local-GR/Newton pass is still not claimable until the Hilbert-worldtube/source-mass lock and residual vector close.

## Source Register

| source_id | path | role |
|---|---|---|
| SRC3108_0 | `3103-Y5-R2FR-Xhat-matter-domain-conflict-resolution-under-AX1090.md` | gives the quotient ordinary-matter domain and forbids source-only species weights |
| SRC3108_1 | `3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md` | supplies the EH/Poisson principal operator plus `E_res_munu` |
| SRC3108_2 | `3107-Y5-R2FR-Newton-constant-calibration-vs-parent-scale-derivation-under-AX1090.md` | defines the `G0/G1/G2` split and forbids early orbital-GM import |
| SRC3108_3 | `1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md` | keeps `M_H_ref` and orbital denominator use nonclaim until source bridge is derived |
| SRC3108_4 | `1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md` | records the conditional same-object lemma and retained equality residuals |
| SRC3108_5 | `1149-Y5-R10-source-normalization-owner-minimal-lemma-or-channel-bound-fallback.md` | separates Hilbert charge, PiM flux, Gauss/orbital calibration, and extra channels |
| SRC3108_6 | `1150-Y5-R10-Hilbert-worldtube-glue-or-PiM-equality-commutator-first-row.md` | warns that a closed charge is not enough if it is the wrong charge |
| SRC3108_7 | `00-martin-fork-heuristics-private.md` | private fork guard: do not reject alternate time language before checking which clock/readout notion is being used |

## The Object We Need

Let `W` be a compact source worldtube fixed before any orbital fit. In the quotient matter branch, the source density candidate is the Hilbert energy density measured by the public metric/coframe:

```text
rho_H := c^-2 T_total_munu u^mu u^nu
```

where `u^mu` is the public-frame rest observer field for the source in the weak static branch. The corresponding compact source mass is

```text
M_H[W] := int_{Sigma cap W} rho_H dV_pub
```

or, in the dressed Hamiltonian language inherited from the older R10 work,

```text
M_H[W] := c^-2 (H_tau[S_outer] - H_ref)
```

provided the Hamiltonian charge, Hilbert source measure, reference, and observed time generator are all the same object. This is the crucial same-frame condition. It is not an optional detail: without it, one can always choose a mass denominator after seeing the orbit.

## Weak-Field Equation

Start from the `3104/3107` public field equation:

```text
G_munu[g_pub] + Lambda_* g_munu + E_res_munu = kappa_* T_total_munu.
```

In the weak, static, slow-motion, compact-source limit, write

```text
g_00 = -1 - 2 Phi/c^2 + O(c^-4),
g_ij = delta_ij (1 - 2 Psi/c^2) + O(c^-4),
T_total_00 = rho_H c^2 + O(v^2 rho_H).
```

The Einstein-Hilbert principal operator then gives the Poisson form

```text
nabla^2 Phi = 4 pi G_* rho_H + R_N,
G_* := kappa_* c^4 / (8 pi),
```

where `R_N` is not a fudge factor. It is the named Newtonian residual inherited from:

```text
R_N = R_Eres + R_Lambda + R_pressure + R_time_dep + R_gauge + R_extra_source.
```

If all of those are zero or bounded below the relevant local tests, the Poisson source is the Hilbert source. If any survive, they shift the inferred orbital `GM`.

## Gauss/Poisson Bridge

Let `V` be a spatial volume enclosing `W`, with boundary `S = partial V`. Integrating the Poisson equation gives

```text
oint_S grad Phi . n dA
= 4 pi G_* int_V rho_H dV_pub + int_V R_N dV
= 4 pi G_* M_H[W] + int_V R_N dV.
```

Define the residual surface charge

```text
Delta_GM_R[S] := (1 / 4 pi) int_V R_N dV.
```

Then the Gauss readout is

```text
GM_Gauss[S] := (1 / 4 pi) oint_S grad Phi . n dA
= G_* M_H[W] + Delta_GM_R[S].
```

This is the first useful result: once `M_H[W]` is fixed by the parent source and not by the orbit, the surface integral predicts the inverse-square coefficient.

## Exterior 1/r Potential

Outside a compact source, suppose the exterior branch is static, asymptotically flat over the local domain, and has no long-range residual source:

```text
rho_H = 0 outside W,
R_N = 0 outside W,
Phi -> 0 at local infinity.
```

Then

```text
nabla^2 Phi = 0
```

outside `W`, and the monopole solution is

```text
Phi(r) = - GM_Gauss/r + Phi_multipole + Phi_res_boundary.
```

For an approximately spherical or monopole-dominated source,

```text
Phi(r) = - (G_* M_H[W] + Delta_GM_R)/r + O(r^-2 multipoles) + Phi_res_boundary.
```

Therefore the radial acceleration readout is

```text
r^2 |a_r| = G_* M_H[W] + Delta_GM_R + Delta_GM_multipole + Delta_GM_boundary + Delta_GM_PPN.
```

Call the whole correction vector

```text
Delta_GM_total :=
Delta_GM_R
+ Delta_GM_multipole
+ Delta_GM_boundary
+ Delta_GM_PPN
+ Delta_GM_time_frame
+ Delta_GM_worldtube
+ Delta_GM_extra_channel.
```

The clean bridge is therefore

```text
GM_orbit = G_* M_H[W] + Delta_GM_total.
```

This is the second useful result. Orbital `GM` is a readout after the source bridge, not an input used to define the source mass.

## No-Orbital-GM Rule

Forbidden:

```text
M_H[W] := GM_orbit / G_ref
```

before proving the Gauss bridge and fixing the source worldtube.

Allowed after the bridge:

```text
G_* := GM_orbit / M_H[W]
```

as an empirical calibration of the universal coupling, provided:

```text
Delta_GM_total is zero or bounded,
M_H[W] is fixed independently of orbital readout,
the same G_* works across source composition, clocks, PPN, and orbital systems.
```

This is exactly the `G1` standard. It does not pretend to be `G2`, the deeper derivation of the numerical value of `G`.

## Time/Traversal Fork Guard

The private time heuristic does not alter the proof. It changes what we do at forks.

If a future MTS branch says that some field/process/traversal parameter behaves opposite to local proper time, do not reject it just because the words sound anti-GR. First separate:

```text
proper time / local clock time,
coordinate time / public orbital readout time,
field phase or propagation parameter,
source-memory time,
background traversal time.
```

For this bridge, the measured orbital `GM` is tied to the public metric readout and ephemeris clock. Any alternative MTS time variable must either reduce to that public readout in the local branch or appear explicitly inside `Delta_GM_time_frame`. It cannot silently redefine `M_H[W]` or hide in `G_*`.

## Residual Vector

| residual_id | term | definition | blocks claim if not zero/bounded |
|---|---|---|---|
| DGM3108_0 | `Delta_GM_R` | volume integral of Newtonian residual `R_N` | yes |
| DGM3108_1 | `Delta_GM_worldtube` | shift from changing `W` or source support after readout | yes |
| DGM3108_2 | `R_eq_integral` | Hilbert-to-topological/PiM equality residual from `1015` | yes if PiM route is used |
| DGM3108_3 | `I_commutator` | `[d,Pi_M]J_H` annulus/source leakage | yes if PiM route is used |
| DGM3108_4 | `B_zero_flux` | exact/reference boundary flux | yes |
| DGM3108_5 | `Delta_GM_extra_channel` | hidden memory/projector/non-EH/domain charge channel | yes |
| DGM3108_6 | `Delta_GM_time_frame` | mismatch between source time, public ephemeris time, and any MTS traversal parameter | yes |
| DGM3108_7 | `Delta_GM_PPN` | velocity, preferred-frame, scalar/tensor, or nonmetric orbital correction | yes |
| DGM3108_8 | `Delta_GM_multipole` | ordinary nonspherical multipole correction | no if modeled/removed in standard orbital reduction |

## What Is Derived Now

Conditional theorem:

```text
If:
1. ordinary matter is quotient/public-metric Hilbert matter;
2. the local principal operator is EH/Poisson;
3. W is a compact source worldtube fixed before readout;
4. M_H[W] is the same-frame Hilbert/Hamiltonian source charge;
5. R_N and Delta_GM_total are zero or bounded;

then:
GM_orbit = G_* M_H[W] + Delta_GM_total,
and if Delta_GM_total -> 0:
GM_orbit = G_* M_H[W].
```

This proves the shape of the non-circular calibration bridge. It is not merely a missing-items list.

## What Is Not Yet Parent-Derived

| gate_id | target | status | reason |
|---|---|---|---|
| GATE3108_0 | quotient Hilbert matter source | improved conditional | `3103` supplies the domain rule, but full corpus adoption remains proposed |
| GATE3108_1 | EH/Poisson principal operator | improved conditional | `3104` gives the route, but `E_res_munu` must still close or be bounded |
| GATE3108_2 | fixed compact `W` | not yet parent-signed | `1015/1150` keep worldtube/support lock unsigned |
| GATE3108_3 | same-frame `M_H[W]` | not yet parent-signed | Hamiltonian/Hilbert/source measure equality remains conditional |
| GATE3108_4 | Gauss bridge algebra | pass conditional | follows from Poisson integration once source and residuals are fixed |
| GATE3108_5 | orbital readout | pass conditional | follows from exterior 1/r solution plus PPN/multipole bounds |
| GATE3108_6 | calibrated `G1` | not yet claimable | needs `GATE3108_2`, `GATE3108_3`, and residual bounds |
| GATE3108_7 | derived `G2` | not attempted here | parent scale/cell-measure theorem is a stronger future target |

## Claim Status

No local-GR pass, Newton pass, measured-`GM` pass, PPN pass, WEP pass, R10 pass, or derived-`G` claim is made here.

What this checkpoint does achieve is sharper:

```text
The source-to-orbit bridge is now a theorem-shaped target.
The algebra from Poisson to GM is clean.
The remaining failure is not "Python" or vague coupling.
It is the parent-signed same-frame source mass plus residual silence.
```

## Next Best Step

Write:

```text
3109-Y5-R2FR-Hilbert-worldtube-source-mass-lock-or-DeltaGM-residual-row-under-AX1090.md
```

with the direct target:

```text
Can 3103's quotient matter rule and 3104's public metric action force
M_H[W] = c^-2(H_tau[S_outer] - H_ref)
for one fixed compact source worldtube and one public time/coframe,
or must Delta_GM_worldtube and Delta_GM_time_frame remain explicit closure rows?
```

That is the next place to attack the coupling properly.
