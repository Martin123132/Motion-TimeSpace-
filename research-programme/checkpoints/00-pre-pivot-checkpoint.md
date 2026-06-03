# Pre-Pivot Checkpoint

Date:

```text
2026-05-30
```

Purpose:

```text
freeze the current state before testing the motion-load simplification route.
```

## 1. Frozen Source Workbench

Main workbench:

```text
[local-MTS-workspace]/formalization-workbench
```

Do not mutate the main workbench from this post-checkpoint folder until the new
route earns promotion.

Most recent pre-pivot files:

```text
176-C0-radflat-demotion-decision.md
177-parent-amplitude-repair-contract.md
178-parent-amplitude-theorem-attempt.md
attachments-intake/20260530-new-material-intake.md
```

## 2. Cosmology State

The C0 radflat cosmology branch is:

```text
closure-only benchmark
```

Reason:

```text
full-joint C0 is near-competitive but b_mem is not stable or parent-predicted.
```

Key numbers:

```text
C0_frozen_delta_AIC_vs_best_baseline = 0.36437287900487547
C0_frozen_delta_BIC_vs_best_baseline = 1.2547446369010444
C0_full_joint_b_mem = 0.1124525903286696
C0_CMB_only_reference_b_mem = 0.015730508794745142
```

The parent-amplitude theorem attempt found:

```text
amplitude corridor derived = true
amplitude prediction derived = false
eta=1 requires a_F DeltaR = 0.3373577709860088
if a_F DeltaR <= 1 then eta <= 1.7216887463098034
```

So:

```text
C0 is not evidence;
C0 is not dead;
C0 is a useful closure benchmark.
```

## 3. Local-GR / PPN State

The prior local branch established strict demands:

```text
F1 = F'(m_L) = 0 is required for local safety;
quadratic residuals need strong amplitude suppression;
local q_loc and PPN gates remain the hard survival route.
```

The new attachment adds a possible route-clean toy closure:

```text
A_B =
  [A_curv/(A_curv+5)]^1.5
  [I_mat/(I_mat+0.3)]^0.5
  [0.02/(E_theta+0.02)]
  P_mem

N = E sqrt(A_B)
raw = M_base(1-A_B) exp[-E sqrt(A_B)] + M0 A_B(1-A_B)^3
M_tr,loc = A_B raw
```

with reported toy-range pass:

```text
E = 8.7
M0 = 1e-4
M_base = 1e-2
local_solar and local_vacuum_shell pass the stiff proxy
inner/outer galaxy and FLRW avoid over-screening
```

This is promising but still a toy closure, not a theorem.

## 4. Motion-Load Simplification Hypothesis

New route:

```text
motion capacity/load -> clock residue + spatial routing -> effective GR/MTS variables
```

Instead of starting with:

```text
fundamental motion field -> corrections
```

test whether the previous field variables emerge from:

```text
c^2 = v_space^2 + v_clock^2 + v_load^2
d tau/dt = sqrt(1 - v^2/c^2 - v_load^2/c^2)
v_load^2 = 2GM/r
S_p(r) = 1/(1 - 2GM/(rc^2))^p
```

Reported weak-field scaffold:

```text
GPS net = +38.60879935757566 microseconds/day
solar light bending at p=1 = 1.7512432813682448 arcsec
Mercury at p=1 = 42.98142433117389 arcsec/century
Shapiro at p=1 = 119.475 microseconds
```

The live question:

```text
can p=1 and the GR weak-field metric coefficients be derived rather than dialed?
```

## 5. Protection Rule

If the motion-load route fails:

```text
return to formalization-workbench/178-parent-amplitude-theorem-attempt.md
and continue with 179-strict-MTS-cosmology-branch-contract.md.
```

If the motion-load route succeeds:

```text
promote it into the main workbench only after a written promotion gate.
```
