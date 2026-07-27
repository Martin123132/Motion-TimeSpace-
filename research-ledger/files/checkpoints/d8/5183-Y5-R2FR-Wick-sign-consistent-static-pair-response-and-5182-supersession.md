# 5183 - Wick-sign-consistent static pair response and 5182 supersession

Marker: `MTS_5183_WICK_SIGN_CONSISTENT_STATIC_PAIR_RESPONSE_GATE`.

Date: `2026-07-23`.

## Correction

Checkpoint 5182 correctly derived the static Hilbert pair vertex and its
rank-one projector, but it combined the Euclidean matter-determinant sign
with the Lorentzian static Einstein constraint kernel. Its conclusion that
every curvature-improved passive pair must screen the Newtonian potential is
therefore retracted.

This correction does not reopen the current parent pair route. The
parent-owned value remains `eta=0`, where the pair is pure gravitational
slip and exactly invisible to dust. In addition, the local two-derivative
Hilbert pair correction has the wrong momentum scaling for checkpoint 5148.

## 1. Action-level sign map

Let

```text
x=(Phi,Psi),
S_L,EH^(2)=+1/2 x^T K_L x,
S_L,src=-J^T x.
```

For a static Wick rotation,

```text
S_E,EH^(2)=-1/2 x^T K_L x,
S_E,src=+J^T x.
```

The bosonic Euclidean determinant is

```text
Gamma_E,pair=+1/2 Tr log(A_0+V[x]),

Gamma_E,pair^(2)=-1/2 x^T C x,
C>=0.
```

Euclidean stationarity therefore gives

```text
(-K_L-C)x+J=0,

(K_L+C)x=J.
```

Checkpoint 5182 instead inverted `K_L-C`. That was the precise mixed-sign
step.

## 2. Exact two-sign response

Write

```text
K_sigma=K_L+sigma d w w^T,
K_L=a[[0,-1],[-1,1]],
a=2M_R^2 k^2,
d>=0,
w=(u,v).
```

For a dust source,

```text
Delta_sigma=a-sigma d u(u+2v),

Phi/Phi_GR
 =1+sigma d(u+v)^2/Delta_sigma,

Psi/Psi_GR
 =(a-sigma d u v)/Delta_sigma,

(Phi-Psi)/Phi_GR
 =sigma d v(u+v)/Delta_sigma.
```

The old checkpoint used `sigma=-1`. The consistent static free-energy
response has `sigma=+1`. On its GR-connected side `Delta_+>0`,

```text
Phi/Phi_GR>=1.
```

Thus a nonminimal positive pair projector can enhance rather than screen.
This is not a parent prediction because the exact shift-symmetric parent has
no `R chi^2` vertex.

For the operational vector

```text
w(eta)=(4eta-1,1-8eta),
F(eta)=48eta^2-16eta+1,
Delta_+=a+dF(eta),
```

the parent value `eta=0` still obeys

```text
w=(-1,1),
Phi=Psi=Phi_GR.
```

At the nontrivial no-slip value `eta=1/8`,

```text
Phi/Phi_GR=Psi/Psi_GR=4a/(4a-d)>1
```

before the pole. At the pure-common value `eta=1/6`,

```text
Phi/Phi_GR=(9a+d)/(9a-3d),
Psi/Psi_GR=(9a-d)/(9a-3d),
lensing/GR=3a/(3a-d).
```

These replace the corresponding screening formulas in checkpoint 5182.

## 3. Correct route rejection: momentum scaling

Let `x=k/mu` and use the already derived external pair form factor

```text
n_q(x)=1/(1+x^q).
```

Checkpoint 5148 requires

```text
C_q(x)=n_q(x)/x,
```

with slopes `-1` at small `x` and `-(1+q)` at large `x`.

Two local two-derivative Hilbert vertices multiplying the massless
`B_0~1/k` pair bubble give a metric correction `d~k^3 n_q`. Relative to
the Einstein kernel `a~k^2`,

```text
d/a proportional x n_q(x).
```

Its slopes are `+1` and `1-q`. The exact shape ratio is

```text
[x n_q]/[n_q/x]=x^2.
```

For the locked `q=0.77`, the numerical slopes are

```text
pair low/high     = 0.99999840025142,
                    0.230001599748579,
target low/high   = -1.00000159974858,
                    -1.76999840025142,
ratio slope       = 2.
```

No constant normalization can turn the pair response into the required
response over the scale corridor. A finite-`k` zero of `Delta_+` is a
constraint pole, not the required asymptotic `1/k` enhancement.

## 4. Claim disposition

Retained from checkpoint 5182:

- the exact static metric expansion and pair covariance;
- `eta=0` pure-slip projection;
- exact dust invisibility of the current parent;
- gap collapse alone does not rescue the current parent route.

Retracted from checkpoint 5182:

- the all-`eta` screening theorem;
- the `eta=1/8` screening formula;
- the `eta=1/6` screening and lensing formulas.

The current zero-background pair route remains rejected, now for two
sign-consistent reasons: the parent owns `eta=0`, and the local pair
correction has `x n_q` rather than `n_q/x` scaling.

## 5. Next calculation

Checkpoint 5184 must now derive or reject the parent stationary nonzero
motion background and its actual linear `h-delta chi` Hessian. It must test
the shift-current equation, regular boundary conditions, background Hilbert
stress, static versus finite-frequency mixing, and the local-GR limit.

Checkpoint 5151's direct conserved state stress remains a distinct
conditional route.

No local-GR, galaxy, cosmology or full-MTS claim is made. The protected
formalization digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758` and checkpoint 5176
remains `254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`.

## Evidence

- `source-intake/functional_rg/5183/Lorentzian_Euclidean_static_sign_chain.csv`
- `source-intake/functional_rg/5183/two_sign_constrained_response.csv`
- `source-intake/functional_rg/5183/critical_pair_vs_required_response_scaling.csv`
- `source-intake/functional_rg/5183/checkpoint_5182_claim_disposition.csv`
- `source-intake/functional_rg/5183/sign_consistent_parent_route_decision.csv`
- `source-intake/functional_rg/5183/source_provenance.csv`
- `source-intake/functional_rg/5183/Wick_sign_consistent_pair_response_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5183_VALIDATION.csv`

## Machine decision

`CHECKPOINT_5182_MIXED_THE_EUCLIDEAN_PAIR_DETERMINANT_SIGN_WITH_THE_LORENTZIAN_STATIC_EINSTEIN_CONSTRAINT_SIGN_THE_CONSISTENT_WICK_AND_SOURCE_MAP_GIVES_THE_PHYSICAL_STATIC_EQUATION_KL_PLUS_C_TIMES_X_EQUALS_J_SO_THE_5182_ALL_ETA_SCREENING_THEOREM_IS_RETRACTED_THE_PARENT_OWNED_ETA_ZERO_RESULT_SURVIVES_EXACTLY_BECAUSE_THE_MINIMAL_PAIR_IS_PURE_SLIP_AND_DUST_INVISIBLE_A_NONZERO_CURVATURE_IMPROVEMENT_CAN_ENHANCE_PHI_BEFORE_ITS_CONSTRAINT_POLE_BUT_IT_IS_NOT_PARENT_OWNED_AND_THE_LOCAL_HILBERT_PAIR_CORRECTION_SCALES_AS_K_TIMES_NQ_RELATIVE_TO_EINSTEIN_WHEREAS_THE_REQUIRED_RESPONSE_SCALES_AS_NQ_OVER_K_THEIR_RATIO_IS_K_SQUARED_AND_NO_CONSTANT_NORMALIZATION_CAN_REPAIR_THE_FULL_CORRIDOR_THEREFORE_THE_CURRENT_ZERO_BACKGROUND_PAIR_ROUTE_REMAINS_REJECTED_FOR_THE_CORRECT_REASONS_AND_THE_NEXT_CALCULATION_IS_THE_PARENT_STATIONARY_BACKGROUND_LINEAR_METRIC_MOTION_HESSIAN`
