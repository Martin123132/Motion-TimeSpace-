# 4884 - Strong-matter contact-coefficient ownership and bound projection

Marker: `MTS_CONTACT_COEFFICIENT_OWNERSHIP_AND_BOUNDS_4884`

**Status:** Checkpoint 4883 overstated the ownership gap. The complete
renormalized `a_R,a_C` are not predicted, but their universal matter-loop
pieces were already derived in 4876-4877. This checkpoint traces that chain,
derives a positive-Einstein nonminimal branch using the existing maximal
three-real-scalar plus `U(1)` reading, propagates its loop ray through the
multi-EOS TOV/Love Jacobian, and constructs source-backed neutron-star
coefficient projections. The loop ray is negligible by more than `65` orders
of observational width. Broad interval projections are not promoted as
coefficient bounds because many leave the validated contact-linearization
corridor.

No full parent-spectrum, measured-coefficient, neutron-star likelihood or
fundamental-unification claim is opened.

## 1. Ownership correction

For scalar nonminimal weights

\[
h_s=1-6\xi_s,\qquad
S_h=\sum_s h_s,\qquad
S_{h^2}=\sum_s h_s^2,
\]

and `N_D` Dirac plus `N_V` Maxwell fields, checkpoint 4877 derived

\[
W_1=S_h+2N_D-4N_V,
\qquad
W_C=N_s+6N_D+12N_V.
\]

The parent-owned universal matter terms are

\[
\boxed{a_{R,\rm loop}=\frac{L S_{h^2}}{1152\pi^2}},
\qquad
\boxed{a_{C,\rm loop}=\frac{L W_C}{1920\pi^2}},
\]

with `L=ln(Lambda_UV/mu)`. Newton matching is

\[
\boxed{W_1\Lambda_{\rm UV}^2
=96\pi^2\overline M_{\rm Pl}^2}.
\]

The total coefficients remain

\[
\begin{aligned}
a_R(\mu)&=a_{R,\rm fin}(\mu_0)
+a_{R,\rm loop}(\mu)+a_{R,H/{\rm gh}}(\mu)
+a_{R,\rm th}(\mu),\\
a_C(\mu)&=a_{C,\rm fin}(\mu_0)
+a_{C,\rm loop}(\mu)+a_{C,H/{\rm gh}}(\mu)
+a_{C,\rm th}(\mu).
\end{aligned}
\]

Thus the correct status is **partial parent ownership**, not “both
coefficients missing.” Finite matching, the gauge-consistent integrated-`H`
and ghost determinant, and threshold-complete bath content remain open.

## 2. Existing-spectrum nonminimal rescue

For `N_s` scalar modes with a common `h`,

\[
W_1=N_sh+2N_D-4N_V.
\]

The positive-Einstein condition is therefore

\[
\boxed{h>\frac{4N_V-2N_D}{N_s}}.
\]

Two previously hidden consequences follow.

1. A real `psi` plus one public `U(1)` needs `h>4`, or `xi<-1/2`.
2. The maximal explicit bosonic reading—complex `psi` (`2` real modes), one
   scalar `Gamma`, and one public `U(1)`—needs only

\[
\boxed{h>\frac43,\qquad \xi<-\frac1{18}}.
\]

For this three-scalar branch,

\[
W_1=3h-4,\qquad S_{h^2}=3h^2,\qquad W_C=15,
\]

\[
\boxed{\frac{a_R}{a_C}=\frac{h^2}{3}}.
\]

Writing `r_UV=Lambda_UV/Mbar_Pl`, Newton matching removes `h`:

\[
\boxed{h(r_{\rm UV})
=\frac{4+96\pi^2/r_{\rm UV}^2}{3}},
\qquad
\xi(r_{\rm UV})=\frac{1-h(r_{\rm UV})}{6}.
\]

At `W1=1`, the same induced-gravity weight and cutoff ratio
`r_UV=4*pi*sqrt(6)=30.7812` used by the five-minimal-scalar completion are
obtained with the already-listed three modes by

\[
\boxed{h=\frac53,\qquad \xi=-\frac19,
\qquad \frac{a_R}{a_C}=\frac{25}{27}}.
\]

This is a real algebraic advance: two additional scalar species are not
required. It is not yet a primitive derivation because `Gamma` must own a
propagating UV determinant and the closed bath must select `xi` or `r_UV`.

## 3. Curvature-stability condition

The same negative `xi` that rescues `W1` changes the scalar operator to

\[
D=-\Box+m_s^2+\xi R.
\]

For positive `R` and `h>1`, absence of a local tachyon requires

\[
\boxed{m_s^2\ge\frac{h-1}{6}R_{\max}}.
\]

The nine BSK24, SLY4 and DD2 stellar backgrounds give

\[
R_{\max}=9.92791\times10^{-9}\ {\rm m}^{-2},
\]

so

\[
\boxed{m_s\ge
8.02675\times10^{-12}\sqrt{h-1}\ {\rm eV}}.
\]

At the `W1=1` anchor this is only
`m_s>=6.55382e-12 eV`. A strictly massless negative-`xi` mode is therefore not
automatically safe, but any ordinary microscopic bath threshold clears the
sampled compact-star curvature condition by an enormous margin.

## 4. Parent loop ray in strong matter

The stellar matching coefficients are

\[
\lambda_R=8\pi\bar\ell_P^2a_R,
\qquad
\lambda_C=8\pi\bar\ell_P^2a_C.
\]

Using a `12 km` matching momentum and the three-scalar branch gives:

| `r_UV` | `h` | `xi` | `L_NS` | `a_R,loop` | `a_C,loop` | maximum `|delta R|` | maximum `|delta Lambda_T|` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `1` | `317.161` | `-52.6934` | `87.8908` | `2.33277e3` | `6.95719e-2` | `3.89e-72 km` | `1.21e-70` |
| `4pi` | `10/3` | `-7/18` | `90.4218` | `2.65094e-1` | `7.15754e-2` | `1.07e-75 km` | `1.13e-73` |
| `4pi sqrt(6)` | `5/3` | `-1/9` | `91.3177` | `6.69301e-2` | `7.22845e-2` | `7.84e-76 km` | `1.20e-73` |

The imported-Standard-Model correspondence benchmark is also propagated and
remains more than `73` orders below the adopted observational widths. Across
all five candidate/reference rows, every loop value is over `50` orders below
the inherited strict-EFT coefficient-control caps.

This closes a useful conditional statement:

> The universal parent matter-loop ray cannot spoil the selected branch's
> strong-matter GR correspondence. Only the finite and omitted determinant
> pieces can do so.

## 5. Source-backed observational projection

The response matrix is projected against:

- LVK GW170817 common-EOS
  `Lambda_1.4=190^{+390}_{-120}` at `90%`, giving `[70,580]`;
- the same analysis's broad component-radius estimate
  `R=11.9+/-1.4 km`, used only as a near-canonical proxy;
- the NICER J0030 result
  `M=1.44^{+0.15}_{-0.14} M_sun`,
  `R=13.02^{+1.24}_{-1.06} km` at `68%`.

The primary PDFs are stored and hash locked under
`post-checkpoint-work/source-intake/strong_matter/4884`.

For each EOS and observable,

\[
O=O_{\rm GR}^{\rm EOS}
+D_R^{\rm EOS}\lambda_R+D_C^{\rm EOS}\lambda_C.
\]

Eighteen one-at-a-time intervals and twenty-four joint radius/tidal box
vertices are calculated. The normalized two-observable determinants are
nonzero, so radius and tidal data can in principle distinguish both contact
directions.

The narrowest linear coefficient half-span is still

\[
1.20953\times10^{74},
\]

over `17` orders weaker than the checkpoint-4878 local derivative-control
scale. More importantly, the largest joint vertex gives a central pressure
contact fraction `1.25458`; it lies outside a controlled linear response.
These boxes are therefore sensitivity projections, not posterior bounds.

## 6. Nonlinear robustness

For each EOS, each coefficient direction and both signs, the code constructs
the largest one-at-a-time coefficient with no more than a `1%` central
energy/pressure contact and then solves the full nonlinear fixed-mass TOV/Love
system. All `12` rows return `1.4 M_sun` solutions.

- maximum radius tangent/nonlinear delta discrepancy: `3.304e-3`;
- maximum tidal tangent/nonlinear delta discrepancy: `5.358e-2`.

This validates the local Jacobian across a materially wider coefficient range
than the original finite-difference step. It also supplies the correct scope
guard: a source-backed coefficient likelihood must solve the nonlinear stellar
system once it leaves this one-percent corridor.

## 7. Arbitration

1. Universal matter-loop `a_R,a_C`: **derived**.
2. Total renormalized `a_R,a_C`: **not derived**.
3. Existing three-scalar plus `U(1)` positive-Einstein route: **algebraically
   viable for `h>4/3`**.
4. `W1=1` anchor: **`h=5/3`, `xi=-1/9`, `a_R/a_C=25/27`**.
5. Sampled compact-star curvature stability: **closed by the stated mass
   floor**.
6. Parent loop strong-matter effect: **negligible by over 65 orders**.
7. Observational total-coefficient bound: **not claimed**; interval boxes are
   not likelihoods and their broad vertices exceed linear control.
8. Full parent promotion: **withheld** until `Gamma`, `xi`, finite matching and
   omitted determinants are owned.

The optional condition

\[
a_{R,\rm fin}(\Lambda_{\rm UV})
=a_{C,\rm fin}(\Lambda_{\rm UV})=0
\]

defines a falsifiable minimal Wilsonian branch. It is not silently relabelled
as a theorem.

## 8. Next target

`4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md`

The next calculation must attack the actual ownership fork: derive a
second-order UV operator and measure for `Gamma`, then derive its nonminimal
weight from the closed-bath/Hadamard parent. If that fails, demote the
three-boson route and retain the loop formulas only as conditional matching
relations. It must also state whether the minimal Wilsonian finite-coefficient
boundary is part of the theory definition or whether independent finite
coefficients remain.

## Sources

- [LVK, GW170817 neutron-star radii and EOS](https://dcc.ligo.org/ligo-p1800115/public)
- [Miller et al., NICER J0030 mass and radius](https://arxiv.org/abs/1912.05705)
- [Vassilevich, heat-kernel expansion](https://arxiv.org/abs/hep-th/0306138)
- `post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md`
- `post-checkpoint-work/4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md`
- `post-checkpoint-work/4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-multi-EOS-mass-radius-tidal-contact-response-gate.md`

