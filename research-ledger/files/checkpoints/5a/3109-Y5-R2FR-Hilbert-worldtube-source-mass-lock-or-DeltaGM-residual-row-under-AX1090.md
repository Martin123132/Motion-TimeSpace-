# 3109 - Y5 R2FR Hilbert/worldtube source-mass lock or DeltaGM residual row under AX1090

**Purpose:** attack the exact throat left by `3108`: can the public Hilbert source mass and the dressed Hamiltonian/worldtube mass be made the same object, or is this only a closure assumption?

**Verdict:** the correct target is not bare rest mass. In an EH/public-metric local branch, the source that talks to Newtonian `GM` is a dressed active Hamiltonian mass. With that correction, `3103 + 3104 + 3108` give a real conditional theorem: the public branch forces a unique same-frame source charge. Full MTS inherits it only if non-EH charge, symplectic/reference leakage, extra-sector charge, projector leakage, and time/frame conversion residuals are zero or bounded. So this is progress, not just another missing-ledger pass.

## Source Register

| source_id | path | role |
|---|---|---|
| SRC3109_0 | `3103-Y5-R2FR-Xhat-matter-domain-conflict-resolution-under-AX1090.md` | removes source-only species weights and makes the active source the Hilbert/coframe variation of one quotient matter action |
| SRC3109_1 | `3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md` | supplies the public EH action route and names `E_res_munu` |
| SRC3109_2 | `3108-Y5-R2FR-source-charge-Gauss-bridge-or-GM-calibration-residual-under-AX1090.md` | derives the non-circular `GM_orbit = G_* M_H[W] + Delta_GM_total` bridge |
| SRC3109_3 | `2938-Y5-R2FR-Htau-worldtube-source-measure-ellJ-reference-lock-or-Qbar-tau-first-value-under-AX1090.md` | prior exact conditional `H_tau`/worldtube source-measure identity |
| SRC3109_4 | `2922-Y5-R2FR-Hamiltonian-sector-owner-or-source-mass-first-row-under-AX1090.md` | Hamiltonian owner audit and first-row schema |
| SRC3109_5 | `541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md` | compact Hamiltonian/PiM source-measure contract |
| SRC3109_6 | `510-worldtube-source-measure-glue-or-Meff-residual-runner.md` | older worldtube glue theorem and dressed-source warning |
| SRC3109_7 | `source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv` | states that dressed source charge, not bare rest mass, is the correct measured source |
| SRC3109_8 | `source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv` | Hamiltonian boundary-charge contract |
| SRC3109_9 | `source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv` | Poisson/Gauss calibration contract |
| SRC3109_10 | `00-martin-fork-heuristics-private.md` | guard against rejecting a branch merely because time/readout language differs from GR wording |

## Correction: The Bare-Mass Target Was Too Naive

`3108` used the helpful shorthand

```text
M_H[W] := int_{Sigma cap W} rho_H dV_pub,
rho_H := c^-2 T_total_munu u^mu u^nu.
```

That is fine at lowest Newtonian order, but it is not the exact source mass GR uses. The exact local-GR compatible object is a dressed active mass:

```text
M_dress[W;tau_pub] := c^-2 (H_tau_pub[S_outer] - H_ref).
```

For stationary EH plus minimally coupled matter this can also be written, schematically, as a Tolman/Komar-style active source integral:

```text
M_dress
= c^-2 int_Sigma (2 T_munu - T g_munu) n^mu tau_pub^nu dSigma
+ M_binding
+ M_boundary
+ M_field
```

with the exact split depending on the Hamiltonian/reference convention. In the weak, slow, low-pressure branch,

```text
M_dress = int rho_H dV_pub
+ O(v^2/c^2)
+ O(p/(rho c^2))
+ O(|Phi|/c^2)
+ boundary/reference corrections.
```

So the target is not:

```text
bare rest mass = measured gravitational source mass.
```

The target is:

```text
one parent-owned dressed public Hamiltonian source mass controls the 1/r metric coefficient.
```

This matters because it removes a false failure mode. MTS does not need raw matter mass to equal orbital mass. It needs the parent action to own the dressing, and it must not tune the dressing after reading the orbit.

## Public Branch Source-Mass Lock

Assume the public local branch adopts the `3103/3104` structure:

```text
S_pub =
(1 / (2 kappa_*)) int sqrt(-g_pub) (R[g_pub] - 2 Lambda_*)
+ S_matter[g_pub, psi, theta]
+ S_silent
+ S_res.
```

with ordinary matter restricted to the quotient/public metric and no source-only species slots. Varying `S_matter` gives one Hilbert stress:

```text
T_total_munu := -(2 / sqrt(-g_pub)) delta S_matter / delta g_pub^munu.
```

Diffeomorphism invariance gives the Ward identity:

```text
nabla_mu T_total^mu_nu = 0
```

when matter equations hold and no retained source-exchange channel is active. The public field equation is:

```text
G_munu[g_pub] + Lambda_* g_munu + E_res_munu = kappa_* T_total_munu.
```

Now choose a compact source worldtube `W`, a hypersurface `Sigma`, an outer linking surface `S_outer`, and one public time generator `tau_pub` normalized by the same clock convention used for local orbits.

The covariant Hamiltonian chain is:

```text
delta L = E_A delta Phi^A + dTheta(Phi,delta Phi),
J_tau = Theta(Phi,L_tau Phi) - i_tau L,
J_tau = dQ_tau + C_tau.
```

On shell in the compact source-free exterior, with fixed boundary/reference convention:

```text
C_tau = 0,
delta H_tau[S] = oint_S (delta Q_tau - i_tau Theta),
H_tau[S_outer] - H_ref = constant over linking surfaces.
```

That is the source lock. The exterior Hamiltonian charge cannot be chosen independently of the Hilbert source once the parent action, public time, and reference are fixed.

## The Conditional Theorem

Define:

```text
M_pub[W;tau_pub] := c^-2 (H_tau_pub[S_outer] - H_ref).
```

If:

```text
1. ordinary matter is quotient/public-metric Hilbert matter;
2. the local exterior action is EH at both equation and Hamiltonian-charge level;
3. tau_pub is the same observed time used by source, clocks, and orbital readout;
4. W is fixed by the support of the Hilbert source before fitting;
5. H_ref is fixed once and does not absorb source/radius/frame/readout changes;
6. S_res, non-EH, projector, boundary, memory, domain, and hidden charge channels are silent or bounded;
```

then:

```text
M_pub[W;tau_pub] = M_dress[W;tau_pub]
```

and the `3108` bridge becomes:

```text
GM_orbit = G_* M_pub[W;tau_pub] + Delta_GM_total.
```

If the residual vector vanishes in the local branch:

```text
GM_orbit = G_* M_pub[W;tau_pub].
```

This is exactly what is needed for calibrated `G1`: the measured Newtonian coupling is a calibration of `G_*`, not a definition of `M_pub`.

## Why 3103 + 3104 Help More Than The Older Route

The older R10 route tried to prove a broad topological/PiM equality:

```text
Pi_M J_H = J_M_top + dB_zero.
```

That is strong, but it keeps the "wrong conserved object" countermodel alive: a closed topological label can be conserved without being measured mass.

The `3103/3104` route is narrower and cleaner:

```text
same public matter action
+ same public metric/coframe
+ same public Hamiltonian time
+ EH local exterior
=> same dressed source mass.
```

This route is less vulnerable because it does not need an abstract topological mass selector to become the right object. The public EH Hamiltonian charge is already the object that controls the local metric monopole, provided the residual charge channels are silent.

## What Still Fails For Full MTS

The theorem above is not automatically the full MTS theorem. The residual is:

```text
R_Hsrc :=
M_pub[W;tau_pub]
- c^-2 (H_tau_MTS[S_outer] - H_ref_MTS).
```

Decompose it as:

```text
R_Hsrc =
R_nonEH_charge
+ R_symp_reference
+ R_extra_source
+ R_projector
+ R_boundary
+ R_time_frame
+ R_worldtube_support.
```

Then the `3108` correction becomes:

```text
Delta_GM_total =
Delta_GM_R
+ G_* R_Hsrc
+ Delta_GM_PPN
+ Delta_GM_multipole.
```

This is the useful narrowing. The coupling problem is no longer "what is the source?" in the public branch. The source is the dressed public Hamiltonian mass. The remaining MTS question is whether the full parent action reduces to that public Hamiltonian charge without extra mass hair.

## Time/Frame Fork Rule

If MTS keeps a separate traversal/flow/source-memory time, it is not automatically wrong. But the local-GR branch must identify which time controls the measured source charge:

```text
tau_source = tau_charge = tau_clock = tau_orbit = tau_pub
```

or else the mismatch must enter:

```text
R_time_frame != 0.
```

This lets the theory explore nonstandard time language without smuggling it into local GR. The tested branch uses public ephemeris time for `GM_orbit`. Any deeper MTS time variable has to reduce to that readout or pay a residual.

## Residual Row Written

The machine-readable first row is staged at:

```text
source-intake/mts_residuals/P8_Y5_R2FR_3109_SOURCE_MASS_LOCK_DELTA_GM_ROWS.csv
```

It keeps every full-MTS promotion nonclaim until the residual vector is either theorem-zeroed or source-backed.

## Gate Table

| gate_id | target | result | reason |
|---|---|---|---|
| GATE3109_0 | replace bare mass with dressed active mass | pass | exact local-GR source is Hamiltonian/active mass, not raw rest mass |
| GATE3109_1 | public EH source-mass lock | pass conditional | follows from diffeomorphism/Hamiltonian constraint chain if `3103/3104` public branch is adopted |
| GATE3109_2 | no orbital-GM circularity | pass | `M_pub` is fixed by action/time/reference before orbit readout |
| GATE3109_3 | full MTS source lock | not yet claimable | extra charge, symplectic/reference, projector, time/frame, and support residuals remain |
| GATE3109_4 | calibrated `G1` | improved but not claimable | the bridge target is now exact, but `R_Hsrc` and `Delta_GM_total` must close |
| GATE3109_5 | derived `G2` | not attempted | deriving the numerical size of `G` remains a separate parent-scale project |

## Claim Status

No local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, measured-`GM` pass, or derived-`G` claim is made here.

But the project did move:

```text
wrong target: bare matter mass equals gravity mass
right target: dressed public Hamiltonian mass is the gravity source
public branch: source lock is theorem-shaped
full MTS branch: residual is now R_Hsrc plus Delta_GM_total, not an undefined coupling hole
```

## Next Best Step

Write:

```text
3110-Y5-R2FR-local-PPN-residual-vector-from-Eres-and-RHsrc-under-AX1090.md
```

Direct target:

```text
Starting from
G_munu + E_res_munu = kappa_* T_munu
and
GM_orbit = G_* M_pub + Delta_GM_total,
derive the local PPN residual vector
{gamma-1, beta-1, alpha_i, zeta_i, xi}
as explicit functions/classes of E_res_munu, R_Hsrc, R_time_frame, and extra charge channels.
```

That is the next leap because source mass alone is not enough. To really reduce to GR, the same source must survive second-order PPN structure.
