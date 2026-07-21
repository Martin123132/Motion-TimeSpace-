# 4886 - Canonical-memory local scalarization and same-parent cosmology gate

Marker: `MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886`

Status: private derivation and falsification checkpoint; not a public claim.

## 1. Decision

Checkpoint 4886 directly solves the local memory-scalar problem left by 4885.
It reaches a mixed but much sharper result.

1. The pointwise negative `M=0` Hessian found in 4885 does **not** imply a
   neutron star scalarizes at the anchor `b Mbar_Pl^2=-1/18`. Gradient energy
   and the full stellar trace profile matter. All nine BSK24, SLY4 and DD2
   backgrounds lie below their first global zero mode by factors `19.57` to
   `25.76`.
2. The same anchor does **not** screen a weak Solar-System source. The Sun's
   scalar-charge ratio is `1.000000566`, a tiny enhancement rather than a
   suppression, and the ambient scalar range is about `2.46e4 Mpc`.
3. Giving the printed `b T M^2` term its minimal covariant universal matter
   owner fixes an exact relation between the corpus cosmological suppression
   amplitude `B0` and the PPN scalar coupling.
4. A deliberately conservative two-sigma Cassini envelope then requires
   `B0<7.54e-5`. The corpus large-scale growth modification is approximately
   `-B0`, so a one-percent effect misses this ceiling by a factor `132`.
5. The significant trace-driven active-`M` cosmology branch is therefore
   rejected under this minimal covariant owner. The canonical `M`
   determinant, its overdamped `Gamma` readout and the renormalized-Einstein
   local branch remain intact.

This is not a rejection of every possible memory source. It is a rejection of
using the direct universal `bTM^2` branch for a significant cosmological
effect while also retaining local GR.

## 2. Covariant owner of the trace interaction

Define the canonically normalized dimensionless scalar

\[
\phi=\frac{M}{\overline M_{\rm Pl}},
\qquad
\beta=b\overline M_{\rm Pl}^2.
\]

The least-assumptive diffeomorphism-invariant universal matter completion is

\[
S_m=S_m[A^2(\phi)g_{\mu\nu},\Psi_m],
\qquad
A(\phi)=\exp(\beta\phi^2).
\]

Its leading expansion is exactly the printed interaction:

\[
S_m[A^2g]=S_m[g]
+\int d^4x\sqrt{-g}\,\beta\phi^2T
+O[(\beta\phi^2)^2],
\]

because `beta phi^2 T=b M^2 T`.

The scalar coupling in the present normalization is

\[
\alpha_\phi=\frac{d\ln A}{d\phi}=2\beta\phi.
\]

Damour--Esposito-Farese conventions use

\[
\varphi=\frac{\phi}{\sqrt2},
\qquad
\alpha_{\rm DEF}=\frac{d\ln A}{d\varphi}
=\sqrt2\alpha_\phi=2\sqrt2\beta\phi.
\]

The same completion also fixes the matter exchange equation:

\[
\nabla_\mu T_m^{\mu\nu}
=\alpha_\phi T_m\nabla^\nu\phi.
\]

For Einstein-frame dust,

\[
\dot\rho_m+3H\rho_m
=\alpha_\phi\rho_m\dot\phi.
\]

Consequently the corpus assumption `rho_b proportional a^-3` is exact only
when the coupling exchange vanishes. Treating `T` as an externally conserved
source while retaining `bTM^2` would not be a closed field theory.

## 3. Static spherical boundary problem

On the fixed GR background

\[
ds^2=-e^\nu dt^2+e^\lambda dr^2+r^2d\Omega^2,
\qquad
e^{-\lambda}=1-\frac{2m(r)}{r},
\]

the exact radial scalar equation is

\[
\phi''+\left[\frac2r+\frac{\nu'-\lambda'}2\right]\phi'
=\frac{1}{1-2m/r}
\left[\kappa\phi^3
+16\pi\beta(\rho-3p)\phi\right],
\]

where `kappa=a Mbar_Pl^2` in inverse-length units.

The zero-mode and weak-response problem linearizes about `phi=0`:

\[
\phi''+\left[\frac2r+\frac{\nu'-\lambda'}2\right]\phi'
=\frac{16\pi\beta(\rho-3p)}{1-2m/r}\phi.
\]

Boundary conditions are

\[
\phi'(0)=0,
\qquad
\phi\ \text{regular at }r=0.
\]

In the Schwarzschild exterior the exact massless solution is

\[
\phi(r)=\phi_\infty
+\frac{C}{2M}\ln\left(1-\frac{2M}{r}\right),
\]

so

\[
\phi(r)=\phi_\infty-\frac{C}{r}+O(r^{-2}).
\]

The scalar-charge transfer is

\[
\frac{\alpha_A}{\alpha_\infty}
=\frac{C/\phi_\infty}{4\beta M}.
\]

This exact exterior match avoids imposing an arbitrary finite-radius
Dirichlet condition.

## 4. Nine-EOS solution

The equation was solved on the hash-locked checkpoint-4883 TOV backgrounds.
Each EOS contributes `1.4 M_sun`, `2 M_sun` and `0.99 Mmax` models.

| EOS/model | `M/M_sun` | `R` km | `phi_c/phi_inf` | `alpha_A/alpha_inf` | first `beta_crit` | `beta_DEF,crit` |
|---|---:|---:|---:|---:|---:|---:|
| BSK24 1.4 | 1.400 | 12.577 | 1.0600 | 0.7330 | -1.2299 | -4.9195 |
| BSK24 2.0 | 2.000 | 12.307 | 1.0665 | 0.5311 | -1.0950 | -4.3801 |
| BSK24 0.99 Mmax | 2.257 | 11.521 | 1.0435 | 0.3326 | -1.4002 | -5.6010 |
| SLY4 1.4 | 1.400 | 11.725 | 1.0636 | 0.6976 | -1.1669 | -4.6674 |
| SLY4 2.0 | 2.000 | 10.636 | 1.0501 | 0.3692 | -1.3023 | -5.2090 |
| SLY4 0.99 Mmax | 2.029 | 10.422 | 1.0415 | 0.3233 | -1.4311 | -5.7245 |
| DD2 1.4 | 1.400 | 13.197 | 1.0580 | 0.7493 | -1.2672 | -5.0689 |
| DD2 2.0 | 2.000 | 13.131 | 1.0674 | 0.5808 | -1.0870 | -4.3481 |
| DD2 0.99 Mmax | 2.394 | 12.301 | 1.0462 | 0.3465 | -1.3586 | -5.4343 |

Important checks:

- The anchor is `beta=-0.055556`, whereas the first zero modes occur from
  `-1.0870` to `-1.4311`.
- The minimum threshold margin is `19.566`.
- The maximum coarse/fine scalar-charge discrepancy is `1.217e-6`.
- Pressure makes `rho-3p` negative in several high-mass cores; the solver uses
  the complete sign-changing trace rather than a dust substitution.
- The ambient quartic term is below `1e-40` of the central stellar trace term
  on every row. It fixes the cosmological boundary but does not alter these
  stellar response profiles.

The correct refinement of 4885 is therefore:

```text
pointwise m_eff^2<0 at M=0: true;
global neutron-star zero mode at beta=-1/18: false.
```

The 4885 pointwise floor was a sufficient local condition, not a necessary
global stability theorem.

## 5. Weak-source screening and scalar range

For a constant-density weak source,

\[
x^2=12|\beta|\mathcal C,
\qquad
\frac{\alpha_A}{\alpha_\infty}
=\frac{3}{x^2}\left(\frac{\tan x}{x}-1\right).
\]

At the solar compactness `C_sun=2.12250e-6`,

\[
x^2=1.41500\times10^{-6},
\qquad
\frac{\alpha_\odot}{\alpha_\infty}=1.000000566.
\]

The Sun is therefore unscreened at this anchor.

At the cosmological density-supported minimum,

\[
m_\infty^2=12|\beta|\Omega_bH_0^2.
\]

Using the reference `Omega_b=0.049` gives

\[
\frac{m_\infty}{H_0}=0.18074,
\qquad
\lambda_\infty=2.461\times10^4\ {\rm Mpc}.
\]

The attenuation exponent across one AU is only `1.97e-16`. A bare mass with
a one-AU Compton range is `1.319e-18 eV`, about `5.08e15` times the
cosmological fluctuation mass. Yukawa suppression cannot hide the local field
without simultaneously deleting its cosmological-range role.

## 6. Exact PPN--cosmology amplitude link

The corpus defines the minimum-branch growth amplitude

\[
B_0=\frac{2|b|^2\rho_{b0}}{a}.
\]

At that minimum,

\[
\phi_\infty^2=\frac{B_0}{|\beta|}.
\]

Therefore the standard long-range scalar coupling is not independent:

\[
\alpha_{\rm DEF,0}^2
=8|\beta|B_0.
\]

For a weak unscreened source,

\[
\gamma-1
=-\frac{2\alpha_{\rm DEF,0}^2}
{1+\alpha_{\rm DEF,0}^2}.
\]

Cassini measured `gamma-1=(2.1 +/- 2.3)e-5`. To avoid exploiting the positive
central value against a branch predicting a negative residual, this
checkpoint uses the deliberately loose absolute two-sigma envelope

\[
|\gamma-1|<|2.1|\times10^{-5}
+2(2.3\times10^{-5})=6.7\times10^{-5}.
\]

Then

\[
\alpha_{\rm DEF,0}^2<3.35011\times10^{-5},
\]

and at `|beta|=1/18`,

\[
\boxed{B_0<7.53775\times10^{-5}}.
\]

The corpus large-scale result is `beta_*(k->0) approximately -B0`. Hence the
largest same-branch growth suppression is below `7.54e-5`.

| Intended large-scale effect | Predicted `abs(gamma-1)` | Cassini-envelope ratio |
|---:|---:|---:|
| `7.54e-5` | `6.70e-5` | 1.00 |
| `1e-3` | `8.88e-4` | 13.26 |
| `1e-2` | `8.85e-3` | 132.08 |
| `5e-2` | `4.35e-2` | 648.93 |

Thus the branch can be locally safe or cosmologically significant, but not
both, under this matter owner.

## 7. FLRW dynamics and the early-time fork

Linearizing near the small-field branch during matter domination gives

\[
\phi_{,NN}+\frac32\phi_{,N}
+6\beta f_c\phi=0,
\]

where `f_c` is the fraction of nonrelativistic matter coupled to `M`.

At `beta=-1/18`:

| Coupled sector | growing exponent `s+` | growth from recombination |
|---|---:|---:|
| baryons only, `f_c=0.049/0.315` | 0.03381 | 1.267 |
| all nonrelativistic matter | 0.19648 | 3.960 |

The small-field mode evolves slowly. It does not reproduce the claimed
instantaneous-minimum scaling `phi_min proportional a^-3/2`.

Conversely, exact minimum tracking gives

\[
B(a)=B_0a^{-3},
\qquad
\ln A=-B(a).
\]

Even at the conservative Cassini maximum,

\[
B(z=1100)=1.006\times10^5,
\]

so the exact conformal completion is nonperturbative and the original
`bTM^2` truncation is unusable. Requiring merely `abs(ln A)<0.01` at
recombination gives

\[
B_0<7.49\times10^{-12}.
\]

The same-parent branch therefore has a clean dichotomy:

```text
track the minimum -> early trace coupling becomes nonperturbative;
remain on the small-field branch -> minimum-branch growth formula does not apply.
```

The direct Cassini link already excludes a significant late growth effect;
the FLRW analysis shows why minimum tracking is not a hidden escape.

## 8. Arbitration

| Question | Result |
|---|---|
| Does the anchor scalarize the tested neutron stars? | No |
| Was the 4885 pointwise tachyon warning sufficient? | No; globally refined |
| Is the Sun screened? | No |
| Is the scalar short ranged locally? | No |
| Can `B0` produce percent-level growth and pass Cassini? | No |
| Is significant `bTM^2` active cosmology retained? | Rejected under the minimal covariant owner |
| Is canonical `M` retained as a UV determinant? | Yes |
| Is the overdamped `Gamma` map retained? | Yes |
| Is the renormalized-EH local branch retained? | Yes |

The branch status is

```text
bTM2 cosmology = perturbatively negligible or phenomenological closure only;
canonical M + Gamma readout = retained;
local renormalized EH correspondence = retained.
```

## 9. Next target

`4887-Y5-R2FR-conserved-derivative-memory-source-with-local-PPN-silence-and-FLRW-activation-or-active-M-cosmology-demotion-gate.md`

The next constructive attempt should replace direct trace activation with a
source satisfying all of the following in one action:

1. diffeomorphism-invariant and variationally closed;
2. vanishes, becomes a boundary term, or is derivative-suppressed in a
   stationary weak local system;
3. remains nonzero on an evolving FLRW background;
4. preserves common-metric matter conservation and the 4879 local-GR
   certificate;
5. does not reintroduce a preferred frame or an arbitrary arena switch.

If no such source is derived, active-`M` cosmology should be demoted while
`M` remains the canonical UV memory determinant and `Gamma` remains its
overdamped response coordinate.

## Sources

- MTS action: `cosmology/activation-cosmology/frw-background-and-linear-perturbations-for-the-curvature-memory-field-with-interaction-b-t-m-2.md`.
- MTS minimum branch: `cosmology/activation-cosmology/cosmology-branch-of-the-curvature-memory-theory-derived-from-the-action-with-interaction-term-b-t-m-2.md`.
- EOS backgrounds: `post-checkpoint-work/4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-multi-EOS-mass-radius-tidal-contact-response-gate.md`.
- [Bertotti, Iess and Tortora, Cassini test](https://doi.org/10.1038/nature01997).
- [Damour and Esposito-Farese, tensor-scalar gravity](https://arxiv.org/abs/gr-qc/9602056).

