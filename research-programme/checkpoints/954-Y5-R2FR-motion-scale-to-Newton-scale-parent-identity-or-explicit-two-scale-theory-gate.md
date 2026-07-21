# 4938 - Motion/Newton scale identity or explicit two-scale gate

Marker: `MTS_MOTION_NEWTON_SCALE_IDENTITY_OR_TWO_SCALE_GATE_4938`.

Date: `2026-07-12`.

Status: private analytic, source-executed and trajectory-executed checkpoint.
Every scale-lock owner currently present in the corpus has been tested. None
invariantly selects the motion gap. The unchanged MTS parent is therefore an
explicit two-essential-scale theory at this checkpoint. This is a parameter-
count result, not a rejection of the theory and not a closure: the second
coordinate is the single universal ratio `J_gap=m_gap^2 G_N`, which must be
fixed once rather than retuned by arena. No full-MTS or local-GR/Newton/
Maxwell claim is made.

## 1. Physical scale coordinates

The dimensionless quantities identified at 4937 are

```text
I_M=g_psi G_N^(4/3),

J_gap=m_gap^2 G_N
     =c_m^2 I_M^(3/4).
```

`I_M` is useful for comparing the old fractional coupling to Newton's scale.
The regular fixed-functional result makes `J_gap` the primary low-energy
coordinate: the fractional one-coupling family is not RG closed, whereas the
renormalized mass perturbation is a regular eigenoperator.

With

```text
w_psi=m_gap^2/k^2,

g=G_N k^2,
```

the exact scale-ratio beta identity is

```text
J_gap=w_psi g,

beta_J/J=beta_w/w+beta_g/g.
```

At the Gaussian/GR endpoint,

```text
beta_w/w=-2,

beta_g/g=+2,
```

so `beta_J=0`. The infrared theory carries one fixed dimensionless gap ratio.
This identity transports a value; it does not choose one.

## 2. Exact old-field coordinate theorem

Checkpoint 4927 established the allowed old-field orbit

```text
phi_old'=s phi_old,

M_N'=s^2 M_N,

lambda_old'=s^(2/3)lambda_old,

B_old'=s^(-2)B_old.
```

Direct substitution gives the invariants

```text
g_psi=lambda_old M_N^(-1/3),

B_psi=B_old M_N,

I_M=g_psi G_N^(4/3).
```

Any physical parent scale identity must be constant on this orbit.

## 3. Golden-ratio formula does not fix the physical gap

The core corpus defines

```text
Phi_G^2=Phi_G+1,

Phi_G=(1+sqrt(5))/2,

gamma=Phi_G M_Pl,

lambda_old=Phi_G^4 M_Pl^3
```

in natural units. The golden-ratio equation does fix a dimensionless number.
The old-coordinate coupling formula does not survive the field orbit:

```text
lambda_old'/[Phi_G^4 M_Pl^3]=s^(2/3)
```

if `Phi_G` is held fixed. It therefore selects an old field coordinate rather
than an invariant observable.

Writing the missing action normalization as

```text
M_N=Phi_G^p M_Pl
```

exposes the exact family

```text
I_M(p)=Phi_G^(4-p/3).
```

No equation in the current parent fixes `p`. Two tempting choices already
give different answers:

```text
p=0, M_N=M_Pl:       I_M=Phi_G^4=6.85410196625;

p=1, M_N=gamma:      I_M=Phi_G^(11/3)=5.83832160163.
```

Neither is a prediction.

## 4. Why the remaining candidate owners fail

The audit is exhaustive over the current corpus routes.

### 4.1 Damping coefficient

For constant `gamma`,

```text
gamma phi partial_t phi
 =(gamma/2)partial_t(phi^2).
```

It is a boundary term. Setting `M_N=gamma` cannot normalize a physical pole.

### 4.2 Historical covariance metric

The dimensionally repaired covariance coefficient is `B_psi=B_old M_N`.
It is invariant while `B_old` and `M_N` transform inversely. Moreover, the
scalar-only public-metric branch was rejected before the integrated-`H`
parent was selected. It cannot fix the scale.

### 4.3 Einstein stress residue

Every old-coordinate stress vertex contributes `M_N^-1`, and every scalar
propagator contributes `M_N`. In a closed stress correlator the factors cancel
pairwise. Measured `G_N` has exact zero sensitivity to the redundant old-field
normalization.

### 4.4 Minimal UV critical surface

The functional spectrum itself retains a regular relevant mass direction.
The UV surface therefore does not reduce to one datum.

## 5. Coupled critical-surface theorem

Let `B_g` be the completed five-coordinate gravity/photon/C3 stability matrix.
At the constant motion point the mass beta is proportional to its own
perturbation. A field-independent change of the gravity coordinates does not
add a `phi^2` operator at zero mass. Consequently the enlarged matrix is

```text
B_aug=[[B_g,c],
       [0,  -theta_mass]].
```

For any upper-right threshold column `c`,

```text
det(zI-B_aug)
 =det(zI-B_g)(z+theta_mass).
```

The eigenvalues are the union of the old gravity spectrum and the motion mass
eigenvalue. Off-diagonal threshold backreaction can rotate the eigenvector;
it cannot remove the additional relevant direction.

The known scalar threshold supplies

```text
Delta beta_g=g^2/[6pi(1+w_psi)],

partial Delta beta_g/partial w_psi|_0
 =-g_*^2/(6pi)
 =-0.000904318973124.
```

Using this known Newton component, the unit mass eigenvector develops a
sizeable gravity-sector admixture because

```text
theta_g=1.89083234541,

theta_mass=1.84666--1.85882
```

are close. The response solve residuals are below `1.9e-16`. Nevertheless,
all three source/sign variants have exactly two relevant eigenvalues. This is
the decisive answer to the 4937 coupling question: coupling rotates the
direction but does not lock the scale in the unchanged minimal block.

## 6. Independent UV trajectory label

Near the fixed point,

```text
delta x_g=C_g exp(-theta_g t),

delta w=C_w exp(-theta_mass t).
```

Hence

```text
p=theta_mass/theta_g=0.97664--0.98307,

R_UV=delta w_seed/epsilon^p
```

is constant in the linear UV regime, where `epsilon` is the 4935 relative
gravity-eigenvector amplitude. `R_UV` is an independent critical-surface
coordinate. Its numerical normalization changes if the eigenvectors are
renormalized, but its existence and the second relevant dimension do not.

One-scale predictivity would require a parent boundary condition selecting
one `R_UV`. The owner audit proves that no current parent equation does so.

## 7. Propagation down the GR separatrix

The scale response was integrated together with the exact completed 4935
five-coordinate beta system for all five negative GR seeds,

```text
epsilon={1e-4,3e-5,1e-5,3e-6,1e-6}.
```

An infinitesimal probe `R_UV=1e-12` keeps

```text
w_psi(endpoint)<0.00263,
```

so the calculation remains a controlled linear derivative. Every run reaches
`g=1e-10`. The transfer law is

```text
J_gap,IR=K R_UV+O(R_UV^2),
```

in the declared 4935 eigenvector convention, with

```text
v=+2lambda: K=0.262094420818,

v=-2lambda: K=0.261707706805.
```

Across the five gravity seeds the maximum relative drift is below
`4.94e-5`. Thus the map to the GR endpoint is stable and sign robust.

This is a transfer Jacobian, not a scale prediction. A continuum of `R_UV`
values maps to a continuum of physical `J_gap` values.

## 8. Existing local bound translated to the new coordinate

Checkpoint 4926's one-real-pole compact-safety envelope becomes

```text
I_M>1.960375552989088e-211.
```

Using the unpromoted conservative `c_m` union gives

```text
4.93497e-159 <= J_gap,floor <= 1.31810e-158,

7.02493e-80 <= m_gap/M_Pl floor <= 1.14808e-79.
```

In the current UV eigenvector convention this corresponds to

```text
R_UV floor about 1.88e-158 to 5.04e-158.
```

These are conditional lower safety floors, not measurements. No upper bound
or preferred value is derived. Their practical meaning is that almost the
entire positive two-scale parameter space is already safe from this specific
local Weyl-cubic threshold.

## 9. Parameter-count decision

The low-energy unchanged parent should now be written with

```text
essential scale 1: G_N,

essential scale 2: J_gap=m_gap^2 G_N.
```

`g_psi` and `c_m` are not added as two extra low-energy fit parameters. They
are a microscopic factorization of the same physical gap ratio and remain
relevant only when the nonanalytic microscopic reconstruction is revisited.
Every empirical sector must share one `J_gap`; per-arena values are forbidden.

Multiple essential scales are normal in field theory. The gain here is that
the theory's actual parameter count is now known instead of being hidden
behind `M_N`, `Phi_G`, `c_m` or a closure.

## 10. Claim boundary

```text
old-field invariant theorem                     = derived;
golden-ratio physical scale selection            = false;
gamma scale selection                            = false;
Einstein-residue scale selection                 = false;
minimal UV one-scale locking                      = false;
physical J_gap beta identity                      = derived;
block-triangular two-relevant-direction theorem   = derived;
known threshold eigenvector rotation              = calculated;
linear GR transfer Jacobian                       = calculated;
motion scale value selected                       = false;
explicit second essential scale                   = required;
fully backreacted motion/O4 trajectory             = false;
full MTS fixed point                              = false;
local GR/Newton/Maxwell promotion                  = false.
```

## 11. Next target

`4939-Y5-R2FR-two-scale-motion-O4-curved-flow-and-backreacted-GR-family-gate.md`

Use `J_gap` as the sole universal motion-scale coordinate. Derive the curved
`C^2p^2` flow of `O4`, include the complete mass-threshold backreaction rather
than the spectator derivative, integrate the resulting family to the GR
endpoint, and calculate local Newton/Maxwell residuals as functions of the
same fixed `J_gap`. No arena-specific mass, source or closure is permitted.

