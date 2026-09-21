# Geometric collar response, memory, and the driven acceleration law

Date: 2026-09-13. Private continuation; no GitHub action.

## Result and scope

An explicit exterior response has been constructed for the **frozen scalar block** of the prepared, finite-width action. Its mass, stiffness, and interior coupling are determined by the action and initial geometry, not fitted to a constraint residual. Eliminating its exterior oscillator as an initial-value problem produces a causal memory kernel, with indispensable initial-data and source terms.

This is not the response of the full evolving metric/transport system. A separate calculation using the actual prepared geometric first derivatives finds that the **free outer scalar acceleration fails the inherited prescribed acceleration in all six GR/MTS cases**. That failure is retained. A required reaction trace is derived, but no point force has been adopted and no full second-order constraint calculation has been claimed.

The useful distinction is between a freely evolving exterior and the externally driven problem we actually specified. Their difference is not, by itself, an MTS-specific failure. Arbitrary prescribed experimental boundary histories need not be derived as laws of nature; their coupling, conservation accounting, and compatibility with the field equations do need to be specified.

Predecessor: `DERIVATION-20260913-cross-cut-source-action-and-driven-initial-boundaries.md`.

## 1. A geometric weight simplifies the frozen scalar action

Use the existing initial slice with gravitational momentum P=0, U=sqrt(1-2 mu/R)>0, positive lapse N, and transport exponent g. Keep the scalar momentum p distinct from P. The already derived initial equations give

```text
A = mu/(R^2 U^2),                 B_density = kappa epsilon/R,
(ln U)_R = A - B_density,
g_R = -(ln N)_R + A + B_density.

H(R) = N(R) U(R) exp(g(R)),
(ln H)_R = 2 mu/(R^2 U^2).
```

The explicit density term cancels in this last derivative, but mu still depends on matter. This is not a matter-independent geometry or a new free coupling. The verifier checks the integrated identity across the whole prepared support independently of the pointwise cancellation.

For each translated stencil, initial horizontal links obey T_fi(0)=0 and J_fi=exp(g_i-g_anchor). Freeze the metric coefficients and replace the links by these linear initial maps. Introduce the auxiliary synchronization parameter

```text
tau = exp(-g_i) t_i = exp(-g_anchor) s_anchor.
```

This is a coordinate for the frozen linear surrogate, **not proper time**, not physical interface-clock gluing, and not an exact time coordinate for the nonlinear history action. It implies d chi_i/d tau=exp(g_i) q_i on the initial slice. With the inherited node weights omega_i, factor matrix B_factor, nonnegative factor sampling matrix S, and fixed spacing h, the scalar block is

```text
S_0 = (1/2) integral [chi_dot^T M chi_dot - chi^T K chi] d tau,
M_ii = omega_i r_i^2/H_i,
Dbar_f = sum_i S_fi r_i^2 H_i,
K = B_factor^T diag(Dbar_f/h) B_factor.

exp(g_i) Gchi_i = -(K chi)_i,
chi_dot_i(0) = exp(g_i) q_i(0) = H_i p_i(0)/r_i^2.
```

Dots in sections 1–3 mean auxiliary tau derivatives only. The force identity is checked against the existing scalar variation, rather than defining a new force and comparing it to itself. Positive M and Dbar give K positive semidefinite by factorization. The connected base-gradient factor leaves precisely the constant scalar zero mode in these fixtures; the numerical spectral check explicitly handles only that roundoff-sized eigenvalue, not arbitrary negative modes.

A constant change g -> g+log(a), a>0, sends H -> a H, M -> M/a, K -> a K. The physical initial force -exp(-g) K chi is unchanged. These coefficients do not introduce an independently adjustable clock coupling.

Freezing omits metric variations, changes of H, and nonlinear transport-history variations. Consequently S_0 is neither the full constrained Hessian nor a local Hamiltonian construction for the complete coupled history action. Positive frozen scalar energy is not a proof of coupled gravitational stability.

## 2. Retaining the exterior gives an explicit response operator

The original physical cuts remain L=5.875 and R=6.125. With the tested nonzero translations and widths at most h/2, each translated 17-node stencil has one node outside these cuts: the left node for negative translation, or the right node for positive translation. Write its scalar as e and the 16 interior scalars as x. Partition the already constructed matrix, with m=M_EE, k=K_EE, b=K_EI:

```text
S_0 = integral [ (1/2) x_dot^T M_I x_dot - (1/2) x^T K_II x
                 + (1/2) m e_dot^2 - (1/2) k e^2 - e b x ] d tau,

m e_ddot + k e = -b x + j,
M_I x_ddot + K_II x = -b^T e,
omega = sqrt(k/m).
```

There is no adjustable restoring coefficient here: m, k, and b come from the same whole-factor action, including its cross term. For initial exterior position e_0 and velocity v_0,

```text
G_ret(tau,s) = theta(tau-s) sin[omega(tau-s)]/(m omega),
e_hom(tau) = e_0 cos(omega tau) + v_0 sin(omega tau)/omega,
e(tau) = e_hom(tau) + integral_0^tau G_ret(tau,s) [j(s)-b x(s)] ds.
```

Thus the interior traction is

```text
-b^T e(tau) = -b^T e_hom(tau)
              + integral_0^tau b^T b G_ret(tau,s) x(s) ds
              - integral_0^tau b^T G_ret(tau,s) j(s) ds.
```

The first term cannot be erased by calling the rest a memory law. For the entire finite-width layer family, retain the weighted direct integral over translated copies and their distinct fields. Do not replace it by one endpoint number or average different scalar profiles into a single field.

This finite oscillator is reactive and can return energy. Its sine kernel is oscillatory, not everywhere positive, and not an absorbing bath. It proves neither black-hole absorption nor a dissipative continuum limit. The auxiliary-clock frequencies 59.7748–63.9099 belong to these fixtures, not to an SI observational prediction.

### Causal elimination is not automatically a single-history action

An ordinary quadratic expression (1/2) x^T K_ret x varies to (K_ret+K_ret^T)x/2, not K_ret x. The verifier checks this with a two-time strictly retarded matrix. Solving the exterior initial-value problem legitimately produces the causal equation above; it does not justify silently using that retarded kernel as an ordinary standalone action. The safe continuation is to keep the exterior canonical fields and their initial data explicit while deriving the coupled variations.

## 3. A prescribed drive has a derived reaction and work law

For an externally specified frozen-clock history d(tau), a constrained driving action can retain a multiplier j:

```text
S_drive = integral j(tau) [e(tau)-d(tau)] d tau,
e = d,
j = m d_ddot + k d + b x.
```

The sign follows from varying e in the full scalar action. This reaction is an equation-derived generalized force, not an independently fitted correction. If j is instead supplied as a fixed force history, the same scalar equation applies without varying j.

The scalar mechanical energy, excluding the external apparatus, obeys

```text
E = (1/2) chi_dot^T M chi_dot + (1/2) chi^T K chi,
E_dot = j e_dot.
```

The cross potential x^T K_IE e is part of E. Interior and exterior subsystem powers do not cancel unless its derivative is included. A genuine apparatus with its own dynamical variables would also need its own energy and coupling; neither has been supplied here for the full geometry.

The numerical forced control prescribes d=e_0+v_0 tau+(1/2)(0.05)tau^2, solves the 16 interior equations, constructs j from that solution, and independently replays the full 17 forced equations. This demonstrates the forced-response construction and work identity. **This manufactured auxiliary-clock drive is not the old physical acceleration history and is not evidence that the actual coupled boundary problem has been solved.**

## 4. The actual outer acceleration is a separate necessary condition

Return to physical coordinate-time derivatives on the prepared initial slice. The outer scalar velocity and prescribed gravitational boundary clock are

```text
q = N U p/R^2,              C_clock = N/U,
mu_1 = -kappa U Kbar/N,
N_1/N = (C_clock)_1/C_clock - mu_1/(R U^2).
```

Differentiating q, using U_1/U=-mu_1/(R U^2), gives

```text
q_1,free = [(C_clock)_1/C_clock - 2 mu_1/(R U^2)] q
           + (N U/R^2) p_1,
p_1 = Gchi/omega_node.
```

The prepared P=0 kinetic coefficient has no term linear in P; the actual scalar force and mass rate used here already retain the prepared transport. The prescribed clock derivative determines N_1/N at the outer boundary: it is not an extra lapse knob available to repair the acceleration.

The source files retain C_clock(0)=1.0000262973362133, (C_clock)_1=0.00025872745044339796, and the prescribed outer acceleration 0.05577372038655635. Only that outer scalar acceleration is reused: re-preparation changed the inner scalar velocity, so importing the old inner acceleration as though its history were unchanged would be unjustified. No unsourced second derivative of the inner mass drive is set to zero.

If a generalized force trace rho were added to the scalar momentum equation, its necessary value to match the outer acceleration would be

```text
Delta_a = q_1,prescribed - q_1,free,
rho_required = omega_node R^2/(N U) Delta_a.
```

This equation supplies a **required trace**, not its allowed finite-width spatial realization or a completed matter/source action. No such point force is installed in the run. In particular the untranslated physical boundary test here is not identical to the exterior oscillator at a nonzero layer translation in sections 2–3.

| Branch / profile | Free outer acceleration | Prescribed minus free | Required trace, not adopted |
|---|---:|---:|---:|
| GR / beta22, h/2 | -1.2603292913 | 1.3161030117 | 0.5728442575 |
| GR / beta22, h/4 | -1.2603362814 | 1.3161100018 | 0.5728456960 |
| GR / beta23, h/2 | -1.2603934363 | 1.3161671567 | 0.5728573810 |
| MTS / beta22, h/2 | -1.2539901527 | 1.3097638730 | 0.5700854800 |
| MTS / beta22, h/4 | -1.2539971280 | 1.3097708484 | 0.5700869151 |
| MTS / beta23, h/2 | -1.2540547087 | 1.3098284290 | 0.5700986871 |

All six necessary free-boundary acceleration checks fail. These are internal fixture quantities, not experimentally measured accelerations or source forces in SI units.

### Why the GR control cannot fix this by a small free-boundary adjustment

In the GR base-gradient stencil at the outer node, chi_16-chi_15>0 and the positive factor density makes p_1<0. The prepared cases also have mu_1>=0 and q>0. Therefore

```text
q_1,free < [(C_clock)_1/C_clock] q ~ 3.97e-6
          < q_1,prescribed = 0.05577372038655635.
```

This is a conditional sign obstruction to the stated **free** endpoint assumptions, not a no-go result for externally driven GR, nor for MTS. MTS is evaluated with its actual added factors rather than inheriting the GR-only sign argument. Both controls require source accounting. Their mismatch does not undo the previous initial C0/C1 checks, but those checks never established compatibility with the second-order prescribed histories.

## 5. Numerical evidence and limitations

The matrix covers six prepared cases times four translations z=-0.4,-0.1,0.1,0.4. All 24 free and manufactured-driven frozen responses finish. The main run records 137 successful implementation checks; successful bookkeeping checks do not turn a failed physical compatibility gate into a pass.

| Comparison, maximum absolute error | Observed |
|---|---:|
| Full free oscillator integration versus independent spectral solution | 6.73e-18 |
| Retarded exterior reconstruction | 1.09e-18 |
| Retarded interior traction | 2.23e-15 |
| Conserved free scalar energy drift | 6.08e-18 |
| Full forced replay versus prescribed exterior/interior solution | 1.31e-18 |
| External work versus scalar mechanical energy change | 3.75e-18 |

Numbers in this table are rounded upward from the recorded maxima. They are finite-fixture floating-point checks, not interval certificates or uniform convergence proofs. The retained negative controls are substantial: omitting exterior initial data gives errors 0.000485–0.001440, while dropping the cross potential from the power balance gives 0.0304–0.0803.

Independent verification also checks block-action decomposition, compact-time exterior action variations with the derived drive, the geometric-weight integral, direct complex-step differentiation of the physical kinetic and clock laws, and the GR sign obstruction. The final integrity record is the authority for its completion and exact check count; this note is sealed rather than rewritten after execution.

Unclosed items remain explicit: full varying-geometry/transport response, full variational boundary matching, complete source/clock histories, full second-order C2 propagation, full first jet, physical radial-port action, GR reduction, and a uniquely parent-selected regularizer. Prior profile sensitivity, including the roughly 38% shift in the unprescribed outer mass rate between layer shapes, is not removed by the present scalar response construction.

## 6. Concrete next construction

Retain the explicit exterior scalar fields. Extend the prescribed clock/source histories through a declared finite-width coupling, and vary the shared metric, horizontal transport, scalar fields, and driving variables together. Derive the reaction and its work terms before installing any new source. Then test the actual necessary second-order boundary rows and full C2 with the same GR/MTS controls.

Do not choose a force-spreading profile because it makes C1 pass, identify horizontal transport with proper time, or replace the full action by its frozen memory kernel. If a new coupling profile remains a modeling choice, identify it as such and compare admissible choices rather than calling it derived. This next stage is a coupled variational calculation, not another inventory of missing inputs.

## 7. Reproducible local evidence

- Prepared-action predecessor: `source-intake/navier-stokes/20260913/annular-finite-width-boundary-cut-final-integrity.json`.
- Prepared-case ledger: `source-intake/navier-stokes/20260913/annular-finite-width-boundary-cut-attempt01/status.json`.
- GR clock/acceleration source: `source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02/canonical_N16_GR_sample0.npz`.
- MTS clock/acceleration source: `source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02/canonical_N16_metric_Gram_sample0.npz`.
- Matrix construction and response equations: `scripts/annular_collar_response_20260913.py`.
- Immutable executed runner: `scripts/derive_annular_collar_response_20260913.py`.
- Completed main ledger with all matrix/trajectory file hashes: `source-intake/navier-stokes/20260913/annular-collar-response-attempt01/status.json`.
- Independent verifier: `scripts/verify_annular_collar_response_20260913.py`.
- Final verification and source/output hashes: `source-intake/navier-stokes/20260913/annular-collar-response-final-integrity.json`.

Executed sources and old evidence remain unchanged. Runs use one below-normal-priority, single-core Python worker at a time, with no bytecode cache. The protected original workbench check covers file modification times since 2026-09-13T03:03:48Z; it is not a pre-turn content-hash comparison. No full spacetime evolution or new publication is performed.
