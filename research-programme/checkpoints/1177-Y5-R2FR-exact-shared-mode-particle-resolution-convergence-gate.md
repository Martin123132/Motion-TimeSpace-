# 5161 - Exact shared-mode particle-resolution convergence gate

Marker: `MTS_5161_EXACT_SHARED_MODE_PARTICLE_CONVERGENCE_GATE`.

Date: `2026-07-20`.

## Decision

Checkpoint 5161 removes the phase ambiguity left by checkpoint 5160. The
coarse constrained pair is treated as one periodic trigonometric field and
Fourier-resampled from `64^3` to `96^3`. Both samplings use the same `192^3`
force mesh, 120 KDK steps, box, target and antithetic signs. Particle sampling
is therefore the only changed numerical variable.

## 1. Exact field identity

The fine field contains no modes above the coarse Nyquist surface. Resampling
it back to `64^3` gives maximum pointwise error
`3.552713678800501e-14`. The largest constrained-peak error is
`1.1102230246251565e-15` and the largest fine high-mode power
fraction is `9.64402999770094e-32`. This is a stricter
comparison than reusing a random seed at a different grid size.

## 2. Executed convergence gate

The four nonlinear runs contain `275251200`
particle-step updates. Their common resolved radius is
`155.841824557513` kpc. Fine versus coarse gives:

```text
fixed-edge mass fractional difference = 0.015487167413585357;
velocity-squared log-RMSE              = 0.004321914431131502;
density log-RMSE                       = 0.01797143585763045;
outer-ratio absolute difference        = 0.02011875380712097;
particle convergence gate              = PASS.
```

The comparison remains nonclaim because one constrained pair is not an
ensemble and no above-Nyquist physical modes were added.

## 3. Outer profile and compact edge

The frozen target is scored without refitting. The compact-edge threshold
passes in `0` of `4`
scores; the smallest exterior/interior excess-density ratio is
`0.3349058700395164`. All target transition radii remain below
the common resolved radius, so `q_parent` is not numerically judged.

## 4. Required transition zoom

Resolving the `36.43917542575495` kpc transition with
three force cells requires cells no larger than
`12.146391808584983` kpc. A uniform global run requires
at least grid `822` and the next power of
two is `1024`. The present float64 PM layout has
an estimated lower-bound peak of `44.0390625` GiB,
so a 32-GiB uniform run is not safe. A four-edge-radius local box needs only
the next power-of-two grid `128`. The next
calculation must therefore be a shared-mode nested force/particle zoom, not an
uncontrolled uniform rerun.

## 5. Single-machine verdict

Nothing in the action, metric, `G_N`, visible source, Maxwell stress or
Poynting momentum was changed. The local GR/Newton/Mercury zero state and the
occupied galactic state remain two states of one parent law. This checkpoint
tests only whether the latter result survives particle sampling; it cannot be
used to compensate for a broken local cog.

All `35` validations pass. Every row remains
nonclaim. The protected `formalization-workbench` digest is
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. Galaxy inputs were read-only
and no GitHub action occurred.
