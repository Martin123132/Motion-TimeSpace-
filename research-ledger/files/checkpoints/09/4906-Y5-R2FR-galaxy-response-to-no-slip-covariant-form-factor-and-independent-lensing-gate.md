# 4906 - Galaxy response to no-slip form factor and independent lensing gate

Marker: `MTS_GALAXY_KERNEL_NO_SLIP_LENSING_ARBITRATION_4906`

## Decision

This checkpoint performs the import attempted by checkpoint 4905 and reaches
a decisive result.

1. The current MTS galaxy response is **not one fixed, source-independent
   linear convolution kernel**. The canonical law fails exact source
   homogeneity and additivity, while the active v18.21 browser result is a set
   of 175 exact pointwise support arrays rather than a native source operator.
2. Therefore the pointwise galaxy ratio
   `1 + Delta V^2/V_bar^2` cannot be inserted into the checkpoint-4905
   inverse formula as `mu_dyn(k)`. The direct no-slip form-factor import is
   rejected for the current artifacts.
3. This does **not** reject the galaxy phenomenology or prove that no universal
   action can generate it. It proves that such an action must be nonlinear or
   environmental, so that its background depends on the source, rather than
   the fixed quadratic `F(-Box)` response assumed in the first import.
4. The v19 conformal matter completion is a concrete environmental-action
   attempt. At leading weak-field order its conformal shift cancels from
   `Phi+Psi`, giving `mu_lens=1`, not no-slip. Its nontrivial intersection with
   the no-slip branch is empty.
5. The v19 disk pilot is rejected in its current form: its sink-target mean
   gain is `-1.173 km/s`, it generates zero negative-response target profiles,
   its protected maximum regression is `88.621 km/s`, and its boundary
   direction test fails.
6. An independent lensing score is deliberately not run against an undefined
   kernel. The next construction must derive a parent-owned environmental
   response for both dynamical and lensing potentials, or the galaxy residual
   must remain a phenomenological pillar outside the unified action.

The active baseline remains `Gamma_MTS,res=0`; no public modified-gravity or
lensing claim is made.

## 1. Galaxy corpus actually imported

The audit reads the independent galaxy project without modifying it.

| artifact | concrete content | action-kernel result |
|---|---:|---|
| canonical MTS | one radial shape with source-state `L_eff` | nonlinear source functional, not fixed convolution |
| v18.09 | 175 curves, 40 numerical amplitudes, 30 exponents | 64,601-character state-threshold expression, not one `mu(k)` |
| v18.21 | 175 exact support arrays | current browser-priority cache; no native formula |
| v18.38 | 175 exact support arrays | later shelf candidate; no native formula |
| v19 source/sink | state, boundary and memory gates | explicit phenomenological nonlinear operator |
| v19 matter completion | conformal scalar action candidate | conditional, not parent-owned |
| v19 disk pilot | nonlinear radial field solve | current source proxy rejected |

The current browser assignment in `app.js` chooses v18.21 before v18.09. Its
own release metadata says that the exact support cache remains the source of
truth and that a native formula cannot replace it. This is excellent for
reproducing the galaxy score, but insufficient for an action map.

## 2. Exact fixed-kernel no-go for the canonical backbone

Write the extra circular support as

\[
S[\rho](r)\equiv \Delta V^2(r)
=a\,\Gamma_0L[\rho]
\left[1-e^{-(r/L[\rho])^q}\right].
\]

For a fixed linear weak-field form factor around one background,

\[
\Delta\Phi[\lambda\rho]=\lambda\Delta\Phi[\rho],
\qquad
S[\rho_1+\rho_2]=S[\rho_1]+S[\rho_2].
\]

Now scale every baryonic surface density and component velocity squared by a
common positive `lambda`, while holding the measured radial support fixed.
The disk-scale fit uses the slope of `ln Sigma_disk`; a normalization change
adds a constant and leaves `h` unchanged. The outer gas fraction is a ratio of
component velocity squares and is also unchanged. Consequently `r_out`, `h`,
`f_gas,out` and

\[
L_{eff}=1.8h\left[1+S_{mem}
\left(1-e^{-m_{load}/S_{mem}}\right)\right]
\]

are unchanged. The canonical support therefore obeys

\[
S[\lambda\rho]=S[\rho],
\]

and hence

\[
\boxed{
S[\lambda\rho]-\lambda S[\rho]
=(1-\lambda)S[\rho]\ne0
}
\]

for nonzero support and `lambda != 1`. For two identical sources,

\[
S[\rho+\rho]-S[\rho]-S[\rho]=-S[\rho].
\]

This is an exact obstruction to representing the canonical galaxy support by
one source-independent quadratic metric kernel. It is not an obstruction to
a nonlinear parent action whose background or effective mass changes with
the source.

## 3. What physical profile the radial law does define

Under a deliberately stated spherical-equivalent diagnostic, the extra
enclosed mass is

\[
M_X(r)=\frac{rS(r)}{G}.
\]

With `x=r/L`, direct differentiation gives

\[
\boxed{
\rho_X(r)=\frac{a\Gamma_0}{4\pi GL}
\frac{1-e^{-x^q}+q x^q e^{-x^q}}{x^2}.
}
\]

The executable symbolic residual is exactly zero. The profile is positive for
`a>0`, has inner slope `q-2`, and tends to an isothermal `r^-2` tail. For the
canonical `q=0.77`, the inner spherical-equivalent slope is `-1.23`.

This is a useful physical translation of the rotation law, not a claim that a
thin disk literally has this three-dimensional density. Crucially, both its
normalization and radial scale remain source-state dependent.

## 4. The 175-galaxy response is not a common pointwise multiplier

The v18.21 support arrays were joined to all 175 bundled SPARC curves using
only the baryonic components and the recorded support; observed velocity is
not used to construct the ratios. All array lengths match.

Of the 175 curves, 87 are exact canonical-support matches and 88 contain a
noncanonical radial redistribution. The real-space diagnostic

\[
\mu_{point}(r)=1+\frac{S(r)}{V_{bar}^2(r)}
\]

has the following population spread:

| `r/r_out` | count | p16 | median | p84 | fraction above `4/3` |
|---:|---:|---:|---:|---:|---:|
| 0.25 | 172 | 1.389 | 2.853 | 6.491 | 0.884 |
| 0.50 | 175 | 1.684 | 3.098 | 5.013 | 0.931 |
| 0.75 | 175 | 2.022 | 3.578 | 5.376 | 0.954 |
| 1.00 | 175 | 2.236 | 3.966 | 6.369 | 0.971 |

These broad ratios are useful summaries of the empirical support but are not
Fourier transfer functions. Treating them as `mu(k)` would erase disk
geometry, finite boundaries and the source-dependent state law.

The `4/3` column is only a warning against a naive scalar-only pointwise map.
For the checkpoint-4905 metric response with `mu_lens=1`, positivity would
require `A0=1/(4-3mu_dyn)>0`, hence `mu_dyn<4/3`. Because `mu_point` is not
`mu(k)`, these counts are not a ghost proof; they show why the category error
cannot be repaired by simply relabelling the radial ratio.

## 5. Why the v19 conformal completion is not no-slip

The conditional v19 matter metric is

\[
g^J_{\mu\nu}=A^2(\phi)g^E_{\mu\nu},
\qquad
A(\phi)=e^{\beta\phi^2/2}.
\]

At linear weak-field order, writing `delta a=delta ln A`, the two Jordan-frame
potentials are

\[
\Phi_J=\Phi_E+\delta a,
\qquad
\Psi_J=\Psi_E-\delta a.
\]

Therefore

\[
\boxed{\Phi_J+\Psi_J=\Phi_E+\Psi_E}.
\]

If the scalar stress is higher order in the weak-field expansion so that
`Phi_E=Psi_E=Phi_N`, and `delta a=epsilon Phi_N`, then

\[
\boxed{
\mu_{dyn}=1+\epsilon,
\qquad
\mu_{lens}=1,
\qquad
\eta=\frac{1-\epsilon}{1+\epsilon}
=\frac{2}{\mu_{dyn}}-1.
}
\]

Imposing both no-slip relations gives `epsilon=0`. Thus a nonzero pure
conformal fifth-force response is not the no-slip branch. Scalar stress at
higher order or a disformal/spin-two interaction could change this result,
but those terms must be derived explicitly; they are absent from the tested
completion.

## 6. Exact two-observable inverse map

Checkpoint 4905 supplies

\[
\mu_d=\frac4{3A_2}-\frac1{3A_0},
\qquad
\mu_L=\frac1{A_2}.
\]

Solving for both response denominators gives

\[
\boxed{
A_2=\frac1{\mu_L},
\qquad
A_0=\frac1{4\mu_L-3\mu_d}.
}
\]

The corresponding form factors are

\[
\boxed{
F_R=\frac{-4\mu_L+3\mu_d+1}
{12\bar\ell_P^2k^2(4\mu_L-3\mu_d)},
\qquad
F_C=\frac{\mu_L-1}{4\bar\ell_P^2k^2\mu_L}.
}
\]

Both reconstruction residuals vanish symbolically. Static positivity requires

\[
\mu_L>0,
\qquad
4\mu_L-3\mu_d>0.
\]

This exposes the information boundary cleanly: kinematics alone supplies only
one equation for `A0,A2`. No-slip is one parent relation; pure conformal
coupling is another. Lensing cannot be used both to choose that relation and
then advertised as an independent prediction.

## 7. Direct verdict on the v19 disk construction

The v19 route did more than fit another threshold. It proposed a conformal
action, derived

\[
V_\phi^2=Rc^2\beta\phi\,\partial_R\phi,
\]

solved a nonlinear radial boundary-value problem, and used one global
velocity-squared scale. That is the right type of attempt. Its current source
proxy nevertheless fails the empirical gate:

| diagnostic | result |
|---|---:|
| target mean gain | `+2.475 km/s` |
| additive-target mean gain | `+6.123 km/s` |
| sink-target mean gain | `-1.173 km/s` |
| negative-field target count | `0` |
| protected maximum regression | `88.621 km/s` |
| boundary-direction agreement | `false` |

The result rejects the trace/force-equivalent source proxy and boundary
closure used in that pilot. It does not reject every conformal or
environmental parent, but the tested candidate is not promoted.

## 8. Independent-lensing gate

The no-refit rule from checkpoint 4905 is retained. The lensing test is not
executed here because neither candidate defines a claim-safe target:

- v18.21 supplies pointwise source-specific arrays, not a universal covariant
  response;
- the v19 conformal completion predicts the scalar-only relation rather than
  no-slip and fails its disk pilot;
- fitting a two-function `A0,A2` response to both rotation and lensing data
  would remove the independent prediction.

Running a likelihood now would produce a precise score for an undefined
theory object. Refusing that score is a completed safety gate, not a missing
calculation.

## 9. What survives

```text
GALAXY EMPIRICAL PILLAR
    -> substantial and reproducible;
    -> 175 curves join exactly;
    -> current response is nonlinear/state dependent;
    -> not yet a covariant action kernel.

DIRECT 4905 FIXED NO-SLIP IMPORT
    -> rejected for current galaxy artifacts.

UNIVERSAL NONLINEAR PARENT POSSIBILITY
    -> remains open;
    -> must generate the environmental background and both metric potentials.

V19 CONFORMAL COMPLETION
    -> calculable candidate;
    -> not parent-owned;
    -> not no-slip except at zero response;
    -> current disk source/boundary implementation rejected.

ACTIVE RESIDUAL
    -> Gamma_MTS,res = 0;
    -> active novel MTS numerical predictions = 0.
```

## Next target

`4907-Y5-R2FR-parent-derived-environmental-bi-response-action-or-galaxy-residual-freeze.md`

The next checkpoint must construct, from the parent rather than from residual
labels, one environmental action whose background produces the galaxy scale
and whose linearized perturbations determine both `mu_dyn` and `mu_lens`. If
that cannot be done without restoring a retired field or inserting empirical
state gates, the galaxy law remains a valuable phenomenological pillar but is
frozen outside `Gamma_MTS,res`.

## Sources

- `post-checkpoint-work/4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md`.
- `post-checkpoint-work/source-intake/galaxy_kernel/4906/PROVENANCE.md`.
- `D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo\README.md`.
- `D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo\app.js`.
- `D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo\data\v18-21-radial-phase-candidate.js`.
- `D:\Users\ollet\Desktop\Galaxy Work\mts-output-packs\mts-v19-parent-matter-completion-v1\mts_v19_parent_matter_completion_formula.json`.
- `D:\Users\ollet\Desktop\Galaxy Work\mts-output-packs\mts-v19-parent-disk-pilot-v1\mts_v19_parent_disk_pilot_capsule.json`.
