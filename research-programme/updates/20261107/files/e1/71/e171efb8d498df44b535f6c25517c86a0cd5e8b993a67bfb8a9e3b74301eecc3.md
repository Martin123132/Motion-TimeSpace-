# 5192 - Parent motion FLRW branch, memory separation, and mass-gap cosmology gate

Marker: `MTS_5192_PARENT_MOTION_FLRW_BRANCH_MEMORY_SEPARATION`

**Verdict:** the actual MTS motion sector does not turn the fitted direct-memory
closure into a derived homogeneous `P(X)` solution. The source-free analytic
massless branch obeys an exact shift-current theorem which rejects that
identification. The parent nevertheless already contains a distinct and
constructive cosmological route: its universal renormalized motion gap
`J_gap=m_gap^2 G_N` gives a massive homogeneous scalar that can freeze and
thaw. This route has now been integrated directly.

The direct parent scalar is not the old fixed `p=3,u=1/4` closure. Across the
nonnegative-`Lambda` fixed-step scan the closest admissible branch remains a
substantial shape mismatch. The zero-`Lambda` physical boundary has

```text
m_gap/H0 = 0.69524102062141,
Omega_psi,0 = 0.699910000000001,
Omega_psi,early = 0.773984074074074,
Delta Omega_psi = 0.0740740740740734,
RMS versus fixed p=3,u=1/4 = 0.161633102799274,
maximum absolute shape residual = 0.399259850058825.
```

Its shape is accurately summarized only as a diagnostic by

```text
p_eff = 1.10597003979209,
u_eff = 0.436156123659685,
RMS of diagnostic summary = 0.00319571763170777.
```

The next empirical model must therefore integrate the parent scalar ODE
itself rather than fit or rename the old memory ansatz.

No GitHub action and no edit to `formalization-workbench` occurred.

## 1. Full parent background equations

Write the local kinetic function in the 4957 convention as

```text
P_k(X_c)=k^4 p_k(x),
x=X_c/k^4,
p_k(x)=x/2+sum_(n>=2) a_n(k)x^n.
```

With physical Lorentzian density convention `L=-P-V`, a homogeneous field
has

```text
rho_psi=P+V-2X P_X,
p_psi=-(P+V),
rho_psi+p_psi=-2X P_X.
```

The exact scalar equation is

```text
(P_X+2X P_XX)ddot(psi)
 +3H P_X dot(psi)+V_psi/2=0.
```

For `V_psi=0`,

```text
a^3 P_X dot(psi)=Q,
c_s^2=P_X/(P_X+2X P_XX),
dln|X|/dlna=-6c_s^2.
```

The symbolic continuity residual is exactly

```text
0.
```

For the canonical germ, `X proportional a^-6`, so the nonzero massless state
is stiff. `Q` is a cosmological state constant; the action does not select it.

The complete current parent is not exactly shift symmetric. Checkpoint 4935
owns a microscopic fractional potential, but 4937 proves that it is not a
closed regular fixed-function eigenoperator. The low-energy 1PI coordinate is
instead the regular mass gap

```text
V_1PI=m_gap^2 psi_c^2/2,
J_gap=m_gap^2 G_N.
```

Checkpoint 4938 proves that `J_gap` is one universal essential action
parameter but does not predict its value.

## 2. Local functional-germ check

The order-eight `g=10^-10` endpoints were evaluated at
`-0.1<=x<=0` with 80-digit arithmetic. This is a local timelike analytic
continuation diagnostic, not a global Lorentzian fixed-function theorem.

```text
dynamic eta_N:
  min P_X                 = 0.50000000000000000000000404082694330721699603542751914075237893696814215592238282
  min(P_X+2xP_XX)         = 0.50000000000000000000001212248082992165138017713759570832665255877700388330144540
  max|w-1|                = 8.0816538866667097042766055285524027378872365662653498681159677E-19
  max|c_s^2-1|            = 1.61633077733856955031013185219913153471455931746272407044473218E-18

reference eta_N=0:
  min P_X                 = 0.50000000000000000000000400373624017485719603542535707390237893546977639592237967
  min(P_X+2xP_XX)         = 0.50000000000000000000001201120872052457198017712678537407665254828844356330141706
  max|w-1|                = 8.0074724804019901038790814714293451203438406633099782914170500E-19
  max|c_s^2-1|            = 1.60149449608562563020877734535012177318183890078211974682380541E-18
```

The infrared functional branch is therefore numerically canonical throughout
this local chart. It does not generate a late vacuum-like memory plateau.

## 3. Exact no-go for identifying M6 with the massless clock

The tested closure is

```text
F(n)=1-exp[-(n/u)^3],
rho_mem=B_mem F(n),
n=ln(1+z).
```

It has

```text
F(0)=0,
F'(0)=0,
F(infinity)=1.
```

Conservation gives

```text
rho+p=(1/3)d rho/dn.
```

At the present endpoint the enthalpy is zero. On the healthy analytic
`P_X>0` branch,

```text
rho+p=-2X P_X=0  =>  X=0.
```

The current is then

```text
Q=a^3P_X sqrt(-X)=0.
```

Since `Q` is conserved, a connected healthy branch has `X=0` at every time
and cannot produce nonzero `B_mem F(n)`.

There is an independent endpoint check. For any finite nonzero `Q`, a
barotropic reconstruction gives

```text
X Q^2=-a^6(rho+p)^2/4,
P=-p=rho-(1/3)d rho/dn.
```

The closure sends `X->0` at both endpoints but requires `P->0` at one and
`P->B_mem` at the other. It is not a single-valued analytic `P(X)`.
Source/exchange dynamics or an extra field may evade this theorem; silently
calling the closure the massless clock may not.

## 4. Direct massive parent branch

Set

```text
chi=psi_c/(sqrt(6)M_R),
mu=m_gap/H0,
N=ln a.
```

At leading canonical order the exact flat-background system used here is

```text
E^2=[Omega_m e^(-3N)+Omega_r e^(-4N)+Omega_Lambda
     +mu^2 chi^2]/[1-(chi')^2],

chi''+[3+dlnH/dN]chi'+mu^2 chi/E^2=0,

dlnH/dN=[
 -3 Omega_m e^(-3N)/2
 -2 Omega_r e^(-4N)
 -3E^2(chi')^2]/E^2.
```

The finite-start frozen-mode condition is `chi'(N=-5)=0`. For each `mu`,
flatness and the nonclaim comparator `Delta Omega_psi=2/27` solve for the
early amplitude and nonnegative `Omega_Lambda`. No closure shape is inserted
into this ODE. Repeating the zero-`Lambda` solve from `N=-6` and `N=-7`
changes `mu` by at most
`7.25649e-07` and changes
the normalized branch shape by RMS at most
`1.79213e-06`. The finite
start is therefore numerically converged for this checkpoint.

The smallest admissible nonnegative-`Lambda` solution is the zero-`Lambda`
boundary quoted above. For `H0=70 km/s/Mpc`, it corresponds to

```text
m_gap = 1.0381226114215e-33 eV,
J_gap = 7.23009869080443e-123.
```

These are conditional translations of the comparator transition, not parent
predictions. They show that a late thaw requires the already-owned universal
gap to lie near the Hubble scale.

## 5. Why the old fixed shape is not derived

The direct ODE rises too broadly in `n=ln(1+z)`:

```text
direct scalar best diagnostic: p=1.10597004,
                               u=0.436156124;
old closure:                    p=3,
                               u=1/4.
```

The direct scalar is a viable model family, but it is not mathematically the
same model. This is useful progress: the previously fitted `B_mem,p,u3`
furniture can now be replaced by one universal action mass, one homogeneous
state amplitude, and the separately declared `Lambda_cal`, then penalized
fairly against `Lambda`CDM, `w`CDM and CPL.

## 6. O4 prediction on the massive branch

For `B=-c_O4 dot(psi_c)^2`, the 5191 order-reduced coefficients were
evaluated directly, including the potential-sourced time derivatives rather
than using the massless shift-current shape law. Differentiating the massive
Klein-Gordon equation gives

```text
psi'''=-3 dot(H) dot(psi)-3H ddot(psi)-m_gap^2 dot(psi),

[ddot(B)+Hdot(B)]/(-2c_O4)
 =ddot(psi)^2-3dot(H)dot(psi)^2
  -2Hdot(psi)ddot(psi)-m_gap^2dot(psi)^2.
```

The symbolic reduction residual is exactly
`0`. Over
`0<=z<=exp(2)-1`,

```text
max|delta_Q/(H0 t_P)^4|
  = 7.81984228041762,

max|delta_F/(H0 t_P)^4|
  = 21.9316804206443.
```

At the displayed `H0` calibration this is

```text
max|delta_Q| = 1.74962465879476e-243,
max|delta_F| = 4.90703104957204e-243.
```

Thus the massive thaw route does not endanger low-energy tensor propagation.
The all-scale UV completion boundary from 5191 remains unchanged.

## 7. Decision

```text
parent FLRW stress and scalar equation         = derived;
massless shift-current branch                  = derived;
massless nonzero branch state selection        = not supplied;
M6 equals source-free analytic P(X)             = rejected exactly;
universal massive parent-scalar route           = retained;
J_gap numerical value                           = not selected;
homogeneous amplitude                           = state datum;
fixed p=3,u=1/4 parent identity                 = rejected numerically;
direct parent-scalar likelihood                 = next calculation;
O4 massive-branch tensor safety                 = passed conditionally;
full cosmology or unified-theory claim          = false.
```

## 8. Next target

Checkpoint 5193 should add a direct ODE likelihood model, not another closure
ledger. It should score:

```text
LambdaCDM,
wCDM,
CPL,
old fixed M6 comparator,
parent scalar with Lambda_cal free,
parent scalar with Lambda_cal=0 ablation.
```

The parent scalar must use one universal `J_gap`, one homogeneous state
amplitude, the same Pantheon+/DESI DR2 covariance treatment, explicit
parameter penalties, prior-edge diagnostics, and order-reduced
`delta_Q,delta_F` outputs. A fit may estimate the universal mass and state; it
may not be relabelled as their derivation.

## 9. Machine artifacts

- `source-intake/functional_rg/5192/parent_motion_FLRW_contract.csv`
- `source-intake/functional_rg/5192/functional_PX_timelike_IR_germ.csv`
- `source-intake/functional_rg/5192/memory_PX_exact_no_go.csv`
- `source-intake/functional_rg/5192/massive_parent_scalar_scan.csv`
- `source-intake/functional_rg/5192/closure_vs_parent_scalar_shape.csv`
- `source-intake/functional_rg/5192/O4_massive_branch_tensor_prediction.csv`
- `source-intake/functional_rg/5192/branch_decision.csv`
- `source-intake/functional_rg/5192/source_provenance.csv`
- `source-intake/functional_rg/5192/parent_motion_FLRW_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5192_VALIDATION.csv`
