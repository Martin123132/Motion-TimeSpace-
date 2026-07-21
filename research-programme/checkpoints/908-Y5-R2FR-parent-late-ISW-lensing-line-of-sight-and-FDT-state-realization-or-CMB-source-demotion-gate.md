# 4892 — Parent late-ISW/lensing line of sight and FDT-state realization gate

Marker: `MTS_PARENT_LOS_KMS_STATE_GATE_4892`

## Decision

Checkpoint 4892 advances the 4891 result in two places rather than writing
another missing-input ledger.

1. It inserts the derived parent Weyl response into CAMB's actual non-Limber
   temperature and lens-potential line-of-sight transfers and calculates
   `TT`, `phi-phi`, and `T-phi` spectra.
2. It constructs an explicit positive Gaussian KMS bath state, evaluates its
   filtered FDT covariance, and tests it against the 4891 noise bound.

The fixed-background line-of-sight calculation runs and the bath-state
existence question closes constructively. A CMB likelihood claim remains
blocked because the parent response grid does not yet cover the infrared and
high-`k` tails, the line-of-sight insertion is not yet a self-consistent
compiled parent Einstein–Boltzmann solve, and the parent action does not select
the bath cutoff, temperature, or spectral-cell measure.

## Source and normalization contract

The input parent response is the already validated 4891 table

```text
P8_Y5_R2FR_4891_PARENT_RESPONSE.csv
```

with

\[
R_W(k,z)=\frac{\Phi_{\rm parent}(k,z)}
                 {\Phi_{\rm matched\ GR}(k,z)}.
\]

CAMB's scalar transfer normalization was independently reconstructed as

\[
C_\ell^{XY}=4\pi\int d\ln k\,
\mathcal P_{\cal R}(k)\Delta_\ell^X(k)\Delta_\ell^Y(k).
\]

For temperature and lens potential the reconstructed raw spectra agree with
CAMB to a worst sampled fractional residual of `1.199e-3`. This fixes the
normalization before modifying any transfer.

## Exact late-source insertion

CAMB's symbolic source derivation proves

\[
S_T^{\rm ISW}=2e^{-\tau}\partial_\eta\Phi_W.
\]

The built-in evolution variable obeys

\[
W_{\rm CAMB}=k^2\Phi_W.
\]

Therefore the parent-minus-control temperature source is

\[
\delta S_T^{\rm ISW}(k,\eta)
=\frac{2e^{-\tau}}{k^2}\partial_\eta
 \left[(R_W-1)W_{\rm CAMB}\right].
\]

The lens-potential source is linear in the same Weyl potential, so

\[
\delta S_\phi(k,\eta)=(R_W-1)S_\phi^{\rm CAMB}(k,\eta).
\]

The non-Limber transfer corrections are then

\[
\delta\Delta_\ell^X(k)=
\int_{\eta_*}^{\eta_0}d\eta\,
\delta S_X(k,\eta)j_\ell[k(\eta_0-\eta)].
\]

Directly integrating the unmodified CAMB lens source reconstructs the sampled
CAMB lens transfer with worst fractional residual `5.934e-4`. The calculation
uses 2,401 conformal-time samples and 526 exact CAMB `k` nodes in the validated
parent interval `0.0010367–0.0998484 h/Mpc`.

## Non-Limber result

The central `target=1e-3` fixed-background response gives:

| `ell` | `Delta TT/TT` | `Delta C_phi-phi/C_phi-phi` | `Delta C_T-phi/C_T-phi` | TT grid coverage | lens grid coverage |
|---:|---:|---:|---:|---:|---:|
| 2 | `+1.0243%` | `-1.2887%` | `+1.6959%` | `28.25%` | `80.28%` |
| 4 | `+1.2390%` | `-1.3495%` | `+2.9524%` | `31.85%` | `93.44%` |
| 10 | `+0.8291%` | `-1.2472%` | `+4.9414%` | `93.05%` | `99.61%` |
| 40 | `+0.07126%` | `-0.75357%` | `+5.6779%` | `99.88%` | `98.85%` |
| 80 | `+0.00820%` | `-0.49462%` | `+4.5748%` | `99.72%` | `97.23%` |
| 150 | `+0.000615%` | `-0.29495%` | `+2.9333%` | `99.52%` | `92.24%` |
| 200 | `+0.000174%` | `-0.20621%` | `+2.2476%` | `99.33%` | `86.93%` |
| 400 | `+0.000043%` | `-0.02116%` | `+1.2639%` | `90.75%` | `55.69%` |

The low-`ell` TT correction is below one twentieth of the single-multipole
cosmic-variance scale. This is a scale statement, not a likelihood.

The independently calculated non-Limber lens shifts agree with the 4891
lowest-order Limber calculation to at worst `8.84e-5` in absolute fractional
shift over their common sampled multipoles. The old Limber result was therefore
not a numerical mirage.

The result is incomplete at `ell<10` for temperature because most of the
baseline low-multipole power lies below the current `k=0.001 h/Mpc` parent
response floor. It becomes incomplete for high-multipole lensing because the
response grid ends at `0.1 h/Mpc`. Neither tail is extrapolated.

## Constructive KMS state

Use the normalized e-fold frequency convention and the positive super-Drude
spectral density

\[
J(\omega)=\frac{\bar\gamma\,\omega}
 {[1+(\omega/\bar\Lambda)^2]^2},
\qquad \bar\gamma=1.
\]

It is Ohmic at low frequency, positive for `omega>0`, and falls as
`omega^-3`. A retarded kernel exists with

\[
-\operatorname{Im}\Sigma_R(\omega)=J(\omega),
\]

and real part fixed by a once-subtracted Kramers–Kronig transform. The Gaussian
KMS state is

\[
\rho_B=Z^{-1}\exp\left[-\int_0^\infty d\omega\,
\frac{\omega b_\omega^\dagger b_\omega}{\Theta_B}\right],
\]

with symmetric noise

\[
N(\omega)=J(|\omega|)
\coth\!\left(\frac{|\omega|}{2\Theta_B}\right).
\]

For a top-hat impulse window of width `DeltaN`, its exact filtered variance is

\[
\operatorname{Var}I_{\Delta N}
=\frac4\pi\int_0^\infty d\omega\,
J(\omega)\coth\!\left(\frac{\omega}{2\Theta_B}\right)
\frac{\sin^2(\omega\Delta N/2)}{\omega^2}.
\]

The explicit normalized state

```text
Lambda_bar = 0.3 per e-fold
Theta_B    = 0.1 per e-fold
DeltaN     = 1
```

has

```text
Var I = 0.0210361 < 0.0282438.
```

Thus a positive KMS/FDT state satisfying the 4891 normalized bound exists.
The zero-temperature bound also gives

```text
Lambda_bar DeltaN <= 0.434222.
```

This matters: a broad local-Markov bath with
`Lambda_bar DeltaN >= 3` already exceeds the bound from vacuum fluctuations.
The constructive state therefore lives in a non-Markov regime and requires the
retarded memory kernel retained in the parent. It cannot justify replacing that
kernel by a local damping constant over the same window.

This is an existence proof in the declared normalized spectral cell. It is not
a derivation of the physical bath temperature. The parent still has to select
`Lambda_bar`, `Theta_B`, and the comoving cell measure.

## Arbitration

Closed in 4892:

- CAMB transfer-to-`C_ell` normalization;
- exact parent late-ISW source insertion;
- exact parent lens-source insertion;
- non-Limber fixed-background `TT`, `phi-phi`, and `T-phi` projection;
- existence of a positive normalized KMS/FDT state under the 4891 bound.

Still open:

- parent Weyl response below `0.001 h/Mpc`;
- parent Weyl response above `0.1 h/Mpc` where required;
- parent selection of bath cutoff, temperature, and spectral-cell measure;
- one self-consistent compiled parent Einstein–Boltzmann evolution;
- an official CMB likelihood.

No CMB, local-GR, Newton, Maxwell, or stochastic-noise claim is promoted by
this checkpoint. The stationary local correspondence remains unchanged.

## Next target

`4893-Y5-R2FR-infrared-Weyl-response-full-CMB-transfer-and-parent-bath-cutoff-selection-or-CMB-likelihood-demotion-gate.md`

