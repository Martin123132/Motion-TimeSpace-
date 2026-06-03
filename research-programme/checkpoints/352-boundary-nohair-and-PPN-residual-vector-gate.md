# 352 - Boundary No-Hair And PPN Residual Vector Gate

Private derivation checkpoint. This is not a public local-GR, PPN, WEP, clock, Cassini, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 351 rejected the tempting but invalid shortcut:

```text
two GR spin-2 polarizations != rank(P_active)=2 for B_mem.
```

So this checkpoint turns back to the thing that actually matters for a fundamental theory:

```text
does the local exterior reduce to GR, with explicit PPN residuals?
```

The target is to decompose whatever survives after quotient `P_D` silence into:

```text
trace,
trace-free shear,
vector/preferred-frame,
clock/ruler/WEP coupling,
bulk residual,
conservation flux.
```

Then write the symbolic PPN residual vector.

## 2. Run Ledger

Script:

```text
scripts/boundary_nohair_and_PPN_residual_vector_gate.py
```

Run directory:

```text
runs/20260601-231500-boundary-nohair-and-PPN-residual-vector-gate
```

Command:

```text
python scripts/boundary_nohair_and_PPN_residual_vector_gate.py --timestamp 20260601-231500
```

Status:

```text
boundary_residual_decomposition_and_symbolic_PPN_vector_written_no_nohair_or_local_GR_promotion
```

Claim ceiling:

```text
symbolic_PPN_contract_only_no_boundary_nohair_local_GR_or_observational_pass_claim
```

Outputs:

```text
results/source_register.csv
results/boundary_residual_decomposition.csv
results/symbolic_PPN_residual_vector.csv
results/nohair_conditions.csv
results/conditional_theorem_ledger.csv
results/gate_results.csv
results/decision.csv
```

## 3. Local Exterior After Quotient P_D

The current best local route is:

```text
parent relative-chain data
  -> quotient P_D
  -> metric-independent/topological local projector
  -> no projector bulk stress
```

That conditionally improves N5.

But after that, the local field equation may still contain:

```text
E_bulk^MTS,
B_munu,
C_clock,
C_WEP,
boundary flux.
```

So the real local branch is:

```text
G_munu = 8 pi G T_matter_munu + R_munu^local
```

where:

```text
R_munu^local = E_bulk^MTS + B_munu + C_munu^coupling.
```

GR follows only if this residual is zero, pure gauge, or absorbable into measured mass without changing local observables.

## 4. Boundary Residual Decomposition

The boundary residual must be split as:

```text
B_munu =
  B_tr^mono
  + B_tr^rad(r)
  + B_TF,munu
  + B_0i
  + B_flux
```

with coupling residuals:

```text
C_clock,
C_WEP,
C_nonmetric.
```

Interpretation:

| Sector | Allowed for GR | Risk |
|---|---|---|
| `E_bulk^MTS` | zero | modified Poisson / fifth force |
| `B_tr^mono` | measured mass renormalization | safe only if constant monopole |
| `B_tr^rad(r)` | zero or bounded | `gamma`, `beta`, radial-potential residual |
| `B_TF,ij` | zero / no-hair | anisotropic potentials, lensing slip |
| `B_0i` | zero or pure gauge | preferred-frame PPN residuals |
| `C_clock`, `C_WEP` | zero | redshift, WEP, nonmetric coupling |
| `n_mu B^{mu nu}` | zero or owned exchange | Bianchi/conservation failure |

This decomposition is the local "police tape".
Nothing gets to hide inside the phrase "boundary effect".

## 5. Symbolic PPN Residual Vector

The residual vector is now:

```text
V_PPN =
(
  gamma - 1,
  beta - 1,
  alpha_1,
  alpha_2,
  xi,
  alpha_clock,
  eta_WEP,
  delta_G
).
```

with symbolic sources:

```text
gamma - 1
  ~ c_gamma_TF ||B_TF||
  + c_gamma_rad ||B_tr^rad||
  + c_gamma_bulk ||E_bulk^MTS||

beta - 1
  ~ c_beta_rad ||B_tr^rad||
  + c_beta_nl ||nonlinear boundary self-coupling||

alpha_1, alpha_2
  ~ c_alpha_vec ||B_0i||
  + c_alpha_u ||u_MTS^i||

xi
  ~ c_xi_TF ||B_TF,l>=2||
  + c_xi_ext ||external-domain anisotropy||

alpha_clock
  ~ c_clock ||C_clock||
  + c_nonmetric ||delta g_matter - delta g_photon||

eta_WEP
  ~ c_WEP ||C_WEP||
  + c_comp ||composition-dependent MTS charge||

delta_G
  ~ c_G_bulk ||E_bulk^MTS||
  + c_G_rad ||B_tr^rad||.
```

Zero residual conditions:

```text
E_bulk^MTS = 0,
B_tr^rad = 0,
B_TF = 0,
B_0i = 0,
C_clock = 0,
C_WEP = 0,
n_mu B^{mu nu} = 0 or exactly owned.
```

This is not yet a numerical PPN pass.
It is the symbolic vector we needed before a serious bound run.

## 6. Conditional Boundary No-Hair Theorem

The conditional theorem is:

```text
If:
  H1 quotient P_D removes projector bulk stress,
  H2 no non-projector MTS bulk stress survives,
  H3 boundary trace is only conserved monopole mass renormalization,
  H4 trace-free/shear boundary terms vanish or are below PPN reach,
  H5 vector/preferred-frame terms vanish,
  H6 all matter/clocks/rulers/photons couple to one metric,
  H7 boundary flux obeys an owned Ward/Bianchi identity,

then:
  local exterior = metric-only Einstein-Hilbert exterior,
  V_PPN = 0 up to measured-mass renormalization,
  Newton/PPN follows in the usual GR way.
```

This is strong but conditional.

Currently only:

```text
H1
```

has a conditional route from the quotient/topological `P_D` branch.

The others remain open.

## 7. What Improved

Before this checkpoint, the local obstruction was too vague:

```text
boundary effects / local residuals / PPN issue.
```

Now the obstruction is decomposed:

```text
bulk,
trace,
trace-free shear,
vector,
clock/WEP,
conservation.
```

and each one has an explicit PPN consequence.

That is progress because it turns "does MTS reduce to GR?" into a finite checklist rather than a fog bank.

## 8. What Did Not Improve

No no-hair theorem was derived here.

No official bound was run.

No PPN residual was numerically proven small.

No local GR promotion is allowed.

The status is:

```text
symbolic PPN residual vector: written
boundary no-hair: open
local GR: conditional only
PPN pass: not claimed
```

## 9. Gate Results

| Gate | Result | Meaning |
|---|---:|---|
| source paths exist | pass | cited local-GR/PPN checkpoints and script exist |
| boundary decomposition written | pass | residuals split into trace/shear/vector/clock/bulk/conservation |
| symbolic PPN residual vector written | pass | `gamma`, `beta`, preferred-frame, clock, WEP, fifth-force rows emitted |
| quotient `P_D` projector bulk silence | conditional pass | depends on 348/350 |
| boundary no-hair derived | fail | H2-H7 remain open |
| PPN residuals numerically bounded | fail | symbolic only, no official local-bound run |
| local GR or PPN promoted | fail | conditional theorem only |
| next bound/theorem target selected | pass | 353 |
| claim ceiling enforced | pass | no local-GR/PPN pass claim |

## 10. Next Target

Next checkpoint:

```text
353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md
```

Two possible routes:

```text
Route A:
  attempt a boundary no-hair theorem:
  show B_TF=0, B_0i=0, B_tr^rad=0 from quotient symmetry / compact exterior regularity.

Route B:
  if theorem fails, build a symbolic/numeric bound runner:
  assign residual amplitudes epsilon_TF, epsilon_rad, epsilon_vec, epsilon_clock, epsilon_bulk,
  propagate into the PPN vector,
  compare against local-bound scales.
```

Default should be Route A first.
If it fails cleanly, Route B makes the failure quantitative instead of emotional.

## 11. Decision

```text
boundary_residual_decomposition_and_symbolic_PPN_vector_written_no_nohair_or_local_GR_promotion
```

This is the right kind of progress:

```text
closer to GR,
more explicit,
less handwavy.
```

But the belt is not won yet:

```text
boundary no-hair remains open,
PPN vector is symbolic only,
local GR is not derived.
```
