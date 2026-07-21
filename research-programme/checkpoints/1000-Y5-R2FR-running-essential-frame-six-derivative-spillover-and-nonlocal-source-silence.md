# 4984 - Running essential-frame six-derivative spillover and nonlocal source silence

Date: `2026-07-14`.

Formal marker: `PPC4161_RUNNING_FRAME_P6_NONLOCAL_SILENCE_4984`.

Status: private analytic and numerically executed checkpoint. No GitHub
action.

## 1. Question closed here

Checkpoint 4983 derived the scale-dependent scalar coordinate

```text
psi_old=chi+s Box chi,
partial_t psi=gamma_Box Box psi,
gamma_Box=beta_bBox/(2Z),
```

but left two possible obstructions:

1. the unknown `beta_bBox` might feed the physical six-derivative `O2`
   coefficient; and
2. a nonanalytic two-point form factor might source the local scalar branch
   even though the local `(Box psi)^2` germ does not.

Both questions can be answered without inventing `beta_bBox`.

## 2. Derivative grading

The frame generator `Box psi` raises the derivative order of every local
scalar operator by two and preserves its scalar field degree. Therefore a
six-derivative operator contributes only at eight derivatives under this
scalar frame connection.

At first order in an RG step:

```text
(Z/2)X          -> -Zs(Box chi)^2                         [order 4],
(b_Box/2)Y^2   -> b_Box s Y Box Y                       [order 6],
cX^2            -> running-frame EOM packet              [order 6],
O2              -> order 8,
O3=C^3          -> no classical scalar variation,
O4=C^2X         -> order 8.
```

On the maintained `b_Box=0` surface, the `b_Box s` row is second order in
the infinitesimal RG step and supplies no first-order six-derivative beta
term.

## 3. Exact spillover from `cX^2`

Let

```text
v_mu=nabla_mu psi,
H_mn=nabla_mn psi,
X=v_mu v^mu,
Y=Box psi.
```

The direct variation is

```text
delta_s int sqrt(g)cX^2
 =4cs int sqrt(g) X v^mu nabla_mu Y.
```

The exact divergence identity

```text
nabla_mu(XYv^mu)
 =X v.nabla Y + X Y^2 + 2Y v^mu v^nu H_mn
```

gives

```text
delta_s S_X2
 =-4cs int sqrt(g) A6
  -8cs int sqrt(g) B6
  +4cs surface integral n_mu X Y v^mu,

A6=X(Box psi)^2,
B6=(Box psi)v^mu v^nu H_mn.
```

Thus the running connection contributes

```text
beta_A6|frame=-4c gamma_Box,
beta_B6|frame=-8c gamma_Box.
```

Both coordinates contain the leading scalar EOM explicitly. Twenty-four
independent Euclidean and Lorentzian local-jet controls reproduce the
direct variation from the reduced bulk plus divergence at maximum relative
residual `3.73e-15`.

The four-derivative curvature coordinates give only the analogous EOM
packets

```text
delta_s[ctilde R_mn v^m v^n]
 =-2ctilde s Y nabla^n(R_mn v^m)+boundary,

delta_s[dRX]
 =-2ds Y nabla_m(Rv^m)+boundary.
```

They vanish on the already maintained `ctilde=d=0` minimal-essential
surface. The separate derivative spillover of the metric field
redefinition remains a distinct calculation and is not hidden here.

## 4. No physical `O2` contamination

For four all-incoming flat scalar momenta, the two redundant projectors have
the schematic permutation sums

```text
P_A=sum_perm (k_a.k_b) k_c^2 k_d^2,
P_B=sum_perm k_a^2 (k_b.k_d)(k_c.k_d).
```

Every term vanishes for `k_i^2=0`. In contrast, checkpoint 4959 derived
the gauge-complete essential projector

```text
P_O2=-3stu.
```

Fourteen independent massless events give a maximum induced-frame to
`O2` projector ratio `3.25e-16`, while `P_O2` is nonzero on every event.
Therefore

```text
delta_beta_wO2|gamma_Box=0.
```

This is independent of the numeric value of `beta_bBox`. It does not
calculate the genuine parent `O2` loop source, and it does not calculate
the derivative spillover of the running metric frame.

The classical scalar-frame shift of the essential six-derivative vector is

```text
delta_beta_(O1,O2,O3,O4,O5)|scalar frame=(0,0,0,0,0),
```

where the `O3` entry refers only to classical action substitution. The
field-redefinition Jacobian is metric dependent and remains explicit.

## 5. Source and boundary map

For a hypothetical scalar source,

```text
S_J=-int sqrt(g)J psi_old
   =-int sqrt(g)[J+s Box J]chi
    +Green boundary term.
```

Hence

```text
J_new=J+s Box J.
```

Zero is an exact fixed source. In the selected parent, ordinary matter is
independent of `psi`, so `J_psi=0` before and after the frame change.
The selected global profile is `psi=0`; consequently `Box psi` and every
normal derivative also vanish, so the field-coordinate and Green boundary
terms vanish exactly. This does not assert preservation of arbitrary
nonzero Dirichlet or Neumann data.

## 6. Nonanalytic two-point source-silence theorem

Consider the most general covariant quadratic motion kernel needed here,

```text
Gamma_2[H,psi]=(1/2)<psi,F_H(-Box)psi>,
```

where `F_H` can be analytic or nonanalytic, is self-adjoint on the declared
domain, and has no field-independent scalar tadpole. Then

```text
delta Gamma_2/delta psi=F_H(-Box)psi,
delta_H Gamma_2=(1/2)<psi,delta_H F_H psi>+measure terms.
```

At `psi=0`, both the scalar EOM and the explicit classical metric stress
vanish. Every retained reflection-even motion interaction has scalar degree
at least two, so its first scalar variation and stress also vanish at the
origin. Diffeomorphism covariance gives

```text
nabla_mu T^mu_nu=E_psi nabla_nu psi=0.
```

Therefore the selected `J_psi=0`, zero-boundary branch remains classically
source-, stress-, charge-, and one-scalar-force-silent for an arbitrary
covariant analytic or nonanalytic two-point kernel.

This proves existence of the zero branch, not uniqueness. A zero mode,
nonzero homogeneous solution, instability, or different boundary sector
requires a spectral and domain analysis.

## 7. Quantum measure boundary

The field-coordinate Jacobian is

```text
log J_frame=Tr log(1+s Box).
```

It contains no scalar field and therefore cannot generate an `O2`, `O4`,
or one-scalar source. It can generate regulator- and measure-dependent
pure-metric terms. Those terms can affect the `O3` coordinate or lower
metric counterterms and must be evaluated in the common parent scheme.
They are not set to zero.

Likewise, integrating the quadratic motion fluctuations gives
`(1/2)Tr log F_H`. That determinant can produce a pure-metric quantum
response even on the classical `psi=0` profile. Checkpoints 4977--4981
already distinguish that response from classical scalar hair.

## 8. Local GR and Newton consequence

On the selected branch:

```text
O1=X^3                         =0,
O2=X H_mn H^mn                =0 for arbitrary w_O2,
O4=C^2X                       =0,
O5                            =absent by reflection and zero at psi=0.
```

`O3=C^3` remains a pure-metric higher-curvature operator. Around flat
space it begins at cubic order in the metric perturbation, so its second
metric variation vanishes and it does not alter the leading classical
`p^2` Newton propagator. It can affect nonlinear/curved observables, and
quantum curvature-squared form factors can affect higher-momentum metric
response. Thus leading Newton silence is proved, not exact PPN or
all-operator local GR.

## 9. Decision

Established:

```text
scalar running-frame derivative grading                 = derived;
raw p6 connection vector (A6,B6)                       =(-4c,-8c)gamma_Box;
covariant IBP reduction                                = jet checked;
essential O2 shift from beta_bBox connection           = exactly zero;
numeric beta_bBox needed for that zero                 = false;
selected nonanalytic two-point scalar source silence   = proved;
selected classical stress and one-scalar force         = zero;
leading flat Newton p2 Hessian from p6 packet           = zero.
```

Not established:

```text
numeric beta_bBox                                      = false;
genuine parent beta_wO2                                = open;
metric-frame derivative spillover into O2              = open;
quantum field-coordinate Jacobian coefficients         = open;
uniqueness and stability of the nonlocal zero solution = open;
finite interacting parent metric TTT                   = false;
exact all-operator local GR                            = false;
full MTS                                               = false.
```

The live runner passes `32/32` gates; the independent validator passes
`98/98`.

## 10. Next target

Checkpoint 4985 should calculate the genuine parent `O2` momentum-flow
source and the metric-frame derivative spillover in one common measure
scheme. In parallel, the pure-metric `C^3` and determinant corrections must
be bounded before any exact local-GR promotion. The scalar `beta_bBox`
connection is no longer an `O2` obstruction.

## Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4984_running_frame_six_derivative_spillover_and_nonlocal_silence.py`
- `post-checkpoint-work/source-intake/functional_rg/4984/running_frame_derivative_grading.csv`
- `post-checkpoint-work/source-intake/functional_rg/4984/running_frame_six_derivative_spillover.csv`
- `post-checkpoint-work/source-intake/functional_rg/4984/running_frame_IBP_jet_crosscheck.csv`
- `post-checkpoint-work/source-intake/functional_rg/4984/running_frame_flat_onshell_projector.csv`
- `post-checkpoint-work/source-intake/functional_rg/4984/nonlocal_two_point_source_silence_theorem.csv`
- `post-checkpoint-work/source-intake/functional_rg/4984/selected_branch_six_derivative_silence_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4984/running_frame_nonlocal_silence_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4984/running_frame_nonlocal_silence_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4984/PROVENANCE.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4984_running_frame_six_derivative_spillover_and_nonlocal_silence_validation.py`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4984_VALIDATION.csv`
- `post-checkpoint-work/source-intake/functional_rg/4984/VALIDATION_PROVENANCE.md`
- `formalization-workbench/1000-PPC4161-running-frame-p6-and-nonlocal-source-silence.md`
