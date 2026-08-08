# 4968 - CFF-squared p8 helicity source and completed trajectory

Marker: `MTS_4968_CFF_P8_HELICITY_TRAJECTORY_BOUND`.

Formal marker: `PPC4161_CFF_P8_HELICITY_TRAJECTORY_BOUND_4968`.

Date: `2026-07-13`.

**Canonical correction:** checkpoint 4969 proves that `B=v/g^3` requires
`beta_B=[6-3beta_g/g]B+source`, not `[4-2beta_g/g]B+source`. The complete
CFF amplitude, Ward tests and helicity source derived here remain retained;
the `diag(4,4)` propagation, fixed boundary and endpoint values are
superseded by the canonical-repaired 4969 trajectory.

Status: private analytic and executable checkpoint. This calculation closes
the lowest-loop omitted photon/`CFF` source identified by checkpoint 4967.
It derives the complete linear-`CFF` two-graviton/two-photon tree amplitude
from the covariant action, validates it by eight Ward identities, projects
the two-insertion photon cut onto both Ricci-flat parity-even `p8` helicity
coordinates, and reintegrates the four `N=6,N=8` GR-connected trajectories.
The three-loop pure-Einstein source and unselected parent thresholds remain
open, so this is not a full finite-parent or full-MTS claim.

## 1. Action and amplitude normalization

The calculation starts from one action convention rather than an inferred
vertex:

```text
S=int sqrt(-g)[2R/kappa^2-F_mn F^mn/4+c C_mnrs F^mn F^rs],
kappa=2/M_P,
c=G_CFF.
```

An exact commutative-nilpotent field expansion constructs the `hAA`, `hhAA`
and `hhh` vertices, including the Maxwell, Einstein-Hilbert and `CFF`
exchange diagrams. The complete physical amplitudes are

```text
M(h+ h+ -> gamma- gamma-)=kappa^2 c s^2/2,
M(h- h- -> gamma+ gamma+)=kappa^2 c s^2/2,

M(h+ h- -> gamma+ gamma+)=kappa^2 c t u/2,
M(h+ h- -> gamma- gamma-)=kappa^2 c t u/2,
```

plus parity and particle exchanges. The other sampled helicity branches
vanish. For `kappa=c=E=1`, the first nonzero branch is exactly `8` and the
opposite-graviton branch is exactly `2 sin(theta)^2`.

The independently sourced all-plus amplitude is

```text
A(gamma+ gamma+ h+ h+)
 =[12]^2[34]^4/[M_P^2 Lambda^2 s].
```

The generated covariant-action amplitude is

```text
A(gamma+ gamma+ h+ h+)
 =kappa^2 c [12]^2[34]^4/(2s).
```

Using `kappa=2/M_P` gives the exact coupling map

```text
Lambda^-2=2c.
```

This comparison locks the normalization without identifying a schematic
`RF^2` coefficient by dimensional analogy.

## 2. Gauge-completion check

The amplitude generator replaces each external photon polarization by its
momentum and each external graviton polarization by
`p_(mu xi_nu)`. It performs these checks on both independent nonzero tree
branches. The maximum residual over the eight replacements is

```text
1.42492443457e-15.
```

The nonzero amplitude also scales as `E^4` to numerical precision. The Ward
test is essential: before the Einstein-exchange sign was corrected, the
photon identities passed but the graviton identity failed by order unity.
The accepted result is therefore the gauge-complete sum, not a single
contact diagram.

## 3. Partial-wave projection

Define

```text
q=M_P^2 c=2W_C,
W_C=c/(16pi G_N)=g_CFF/(16pi g).
```

The one-loop formula includes `-1/(8pi^2)` and a factor `1/2` for the two
identical internal photons.

### Direct s channel

For the mixed-helicity `R4prime` target, the physical pair is
`h-- -> h--`. The tree amplitude `h-- -> gamma++` is pure `J=0`:

```text
a_tree^0=2q,
a_R4prime^0/C_R4prime=1.
```

Only one internal photon-helicity row contributes, hence

```text
gamma_s(C_R4prime)=-q^2/(4pi^2).
```

### Crossed t and u channels

For an opposite-helicity graviton pair,

```text
A_tree/(s/M_P^2)^2=(q/2)(1-z^2),
d^4_40(z)=sqrt(70)(1-z^2)^2/16.
```

The exact projection gives

```text
a_tree^4
 =(1/2) int_-1^1 dz d^4_40(z)(q/2)(1-z^2)
 =q sqrt(70)/70.
```

The crossed `R4prime` target is pure `J=4` with

```text
a_R4prime^4/C_R4prime=1/9.
```

Both `gamma++` and `gamma--` internal rows contribute. Their factor two is
combined with the identical-state factor one half, giving

```text
gamma_t(C_R4prime)=gamma_u(C_R4prime)
 =-9q^2/(560pi^2).
```

### Complete helicity result

The all-same-helicity `R4` cut has no common internal photon helicity in any
channel and is exactly zero. Summing the three mixed channels gives

```text
dC_R4/dln(mu)=0,

dC_R4prime/dln(mu)
 =-[1/4+9/560+9/560]q^2/pi^2
 =-79q^2/(280pi^2)
 =-79W_C^2/(70pi^2).
```

With the checkpoint-4967 normalization

```text
C_R4=B_minus/(128pi^3),
C_R4prime=B_plus/(128pi^3),
```

the photon source is

```text
source(beta_Bminus)|CFF^2=0,
source(beta_Bplus)|CFF^2=-79g_CFF^2/(140pi g^2),

source(beta_BC)|CFF^2=-79g_CFF^2/(280pi g^2),
source(beta_Bt)|CFF^2=-79g_CFF^2/(280pi g^2).
```

This is a new `[0,1]` direction in the helicity basis. It was not set to
zero by a truncation choice.

## 4. Completed calculated p8 trajectory

The two running equations now read

```text
beta_BC=[4-2beta_g/g]B_C
        -6h_C3/g
        +u_O4^2(1-eta_psi/10)/(pi g^2)
        -79g_CFF^2/(280pi g^2),

beta_Bt=[4-2beta_g/g]B_t
        +6h_C3/g
        -79g_CFF^2/(280pi g^2).
```

The `p8` stability subblock remains `diag(4,4)`. The photon source is
triangular at this order, adds no relevant parameter, and shifts the
UV-regular boundary rather than introducing a fitted finite coefficient.

All four `N=6,N=8` integrations succeed. The completed calculated `N=8`
brackets are

```text
0.0138769287424 <= B_C <= 0.0138777960481,
-0.0122356429173 <= B_t <= -0.0122353157427,

0.0261122444851 <= B_minus <= 0.0261134389654,
0.00164161299966 <= B_plus <= 0.00164215313078.
```

Relative to checkpoint 4967, the direct CFF source leaves `B_minus`
unchanged within integration tolerance and shifts `B_plus` by about
`1.655e-3`. The largest `N=6` to `N=8` relative displacement is

```text
4.77600528411e-8.
```

## 5. Static compact response

Static spherical gravity reads only `B_C`:

```text
Delta A=128B_C chi^3(8-11M/r),
Delta B=128B_C chi^3(36-67M/r).
```

Applying the completed endpoint to all eleven inherited compact rows gives

```text
max(|Delta A|,|Delta B|)=9.82370208177e-234.
```

The CFF source raises this source-truncated number by about six percent but
does not remotely approach the declared one-percent compact gate. This is a
calculated EFT suppression statement, not evidence that the remaining
three-loop or parent-threshold coefficients vanish.

## 6. Decision

```text
complete linear-CFF hhAA tree amplitude       = derived;
photon Ward identities                        = pass;
graviton Ward identities                      = pass;
action-to-amplitude normalization              = locked;
CFF-squared same-helicity p8 source            = exact zero;
CFF-squared mixed-helicity p8 source           = derived;
four CFF-completed GR trajectories             = integrated;
new relevant p8 parameters                     = zero;
N6/N8 order convergence                        = pass;
source-truncated static compact correction      = bounded;
three-loop pure-Einstein p8 source              = open;
unselected parent mass/motion thresholds        = open;
full finite parent [B_C,B_t]                    = open;
exact all-operator compact GR                   = false;
full MTS                                       = false.
```

The next calculation should attack the three-loop pure-Einstein `p8`
source as an explicit residual boundary. It must not reopen the rank-two
`p8` basis, remove the now-derived photon source, or call the current local
Wilson coordinates complete scattering observables.

## 7. Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4968_CFF_p8_helicity_source.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4968_CFF_p8_trajectory_and_static_bound.py`
- `post-checkpoint-work/source-intake/functional_rg/4968/CFF_tree_helicity_amplitudes.csv`
- `post-checkpoint-work/source-intake/functional_rg/4968/CFF_squared_p8_partial_wave_projection.csv`
- `post-checkpoint-work/source-intake/functional_rg/4968/CFF_squared_p8_helicity_source_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4968/p8_CFF_completed_fixed_point.csv`
- `post-checkpoint-work/source-intake/functional_rg/4968/p8_CFF_completed_GR_connected_trajectory.csv`
- `post-checkpoint-work/source-intake/functional_rg/4968/p8_CFF_completed_IR_endpoint_convergence.csv`
- `post-checkpoint-work/source-intake/functional_rg/4968/p8_CFF_completed_static_compact_response.csv`
- `post-checkpoint-work/source-intake/functional_rg/4968/p8_CFF_completed_trajectory_and_static_bound_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4968/PROVENANCE.md`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4968_VALIDATION.csv`

Validation: `P8_Y5_BRR545_4968_VALIDATION.csv` passes `23/23`, SHA256
`80549949db0e5f8263c1e1a3741d04b3dd1a98a1d11fed593ebc53fe69362d44`.
