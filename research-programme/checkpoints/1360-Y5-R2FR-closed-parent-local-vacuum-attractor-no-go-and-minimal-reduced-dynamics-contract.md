# 5344 - Closed-Parent Local-Vacuum Attractor No-Go and Minimal Reduced-Dynamics Contract

Date: `2026-08-10`

Formal marker: `MTS_5344_CLOSED_PARENT_LOCAL_STATE_ATTRACTOR_NO_GO`.

Private derivation checkpoint. No GitHub action, no edit to
`formalization-workbench`, and no local-GR or full-MTS promotion.

## Executive result

This checkpoint settles one repeatedly open item rather than naming it again.
The current parent cannot make

```text
rho_local -> rho_0
```

an asymptotic attractor by closed Hamiltonian evolution. The obstruction is
exact: unitary similarity preserves the spectrum, purity, entropy and
unitarily invariant distances of the density matrix. Equivalently, the
closed Liouville generator `-i[H,.]` is skew-adjoint and has no
negative-real-part relaxation gap.

For the binary state already used by the parent,

```text
rho(n)=(1-n)rho_0+n rho_1,
```

with orthogonal pure projectors,

```text
D_trace(rho(n),rho_0)=n,
Tr[(rho(n)-rho_0)^2]=2 n^2.
```

Closed unitary dynamics cannot turn a finite `n` into zero. Therefore a
Hamiltonian Lyapunov hunt for density-matrix purification is the wrong
mathematical problem and is now closed for the present parent.

This does **not** undo checkpoint 5211. The exact selected
two-derivative GR/Newton/Maxwell branch survives because
`rho_local=rho_0` is admissible initial/boundary state data, while `chi=0`
is independently an exact stable bulk-field solution. What cannot be said is
that the current parent dynamically prepares that state from arbitrary local
initial data.

## 1. Closed-unitary no-go

For

```text
rho(t)=U(t)rho(0)U(t)^dagger,
```

unitary similarity leaves every eigenvalue of `rho` unchanged. If `rho_0`
is stationary under the same local Hamiltonian, then

```text
D(U rho U^dagger,rho_0)=D(rho,rho_0)
```

for every unitarily invariant distance. A state at nonzero distance cannot
converge to `rho_0`.

The same result appears at generator level. For a two-level witness,

```text
L=-i[H,.],
spec(L)={0,0,+i Delta_E,-i Delta_E},
L^dagger=-L.
```

The real relaxation gap is zero. Oscillation and dephasing after an
unrecorded coarse graining are possible, but exact attraction is not present
in the closed parent equation.

Checkpoint 5178 identifies `Gamma_rho0` as initial density-matrix vertices.
Checkpoint 5200 shows that the known Gaussian bulk Hessian does not select
the projectors or their occupation. Checkpoint 5201 proves exact silence at
`n=0` on an open domain. These statements are mutually consistent: a
boundary functional can specify a state without dynamically attracting all
states to it.

## 2. Field stability is not state selection

The selected motion equation is

```text
E_chi=nabla_mu(K_eff nabla^mu chi)-m_gap^2 chi,
K_eff=1-2P_X+2u_O4 C^2.
```

In the retained local EFT corridor, `K_eff>0` and `m_gap^2>0`. On a
stationary local background its quadratic energy is

```text
E_chi = integral_Omega [
 K_eff(dot chi^2+|grad chi|^2)/2
 +m_gap^2 chi^2/2
].
```

Hence `chi=0` is a positive-energy, Lyapunov-stable equilibrium. With zero
boundary flux, however,

```text
dE_chi/dt=0.
```

The Hamiltonian field oscillates rather than asymptotically forgetting its
initial data. More importantly, this energy estimate acts on the one-point
field `chi`; it cannot change the eigenvalues of the CTP density matrix.
Checkpoint 5211 was correct to separate stationarity from preparation.

## 3. Candidate routes and their actual gate

### 3.1 Local escape with global unitarity

For a bounded local domain `Omega`, let `N_Omega` be the occupied-state
content. A continuity equation gives

```text
dN_Omega/dt=-Phi_boundary+S_Omega.
```

If the parent proves

```text
S_Omega=0,
Phi_boundary >= kappa N_Omega,
kappa>0,
```

then Gronwall's inequality gives

```text
N_Omega(t)<=N_Omega(0) exp(-kappa t).
```

This route preserves global unitarity: the excitation leaves the local
subsystem instead of being destroyed. It nevertheless fails as a universal
attractor for the current spectrum. The exact homogeneous solution

```text
chi=A cos(m_gap t),
partial_i chi=0
```

has positive energy density but

```text
T_0i=-dot(chi) partial_i chi=0.
```

Thus `Phi_boundary=0` while `N_Omega>0`, which rules out every universal
`kappa>0`. The same obstruction follows from

```text
omega(k)=sqrt(k^2+m_gap^2),
v_g/c=k/sqrt(k^2+m_gap^2),
lim_(k->0+) v_g=0.
```

Standing or reflecting modes provide a second exact zero-flux
counterexample. Therefore the current parent does **not** own a universal
local escape gap.

A restricted outgoing finite-wavelength sector remains useful. If
`k>=hbar/R`, with no reflection or incoming collective flux, then

```text
v_g/c >= [1+(m_gap R/hbar c)^2]^-1/2,
tau_cross <= R sqrt(1+(m_gap R/hbar c)^2)/c.
```

Across the checkpoint-5208 Sun-through-Saturn/Moon arenas,

```text
max (m_gap R/hbar c)^2 =6.35161828520e-29;
max tau_cross          =4781.74137389 s
                       (Saturn solar orbit).
```

Those finite-wavelength packets therefore move essentially at `c`. This is
a crossing-time statement, not exponential state selection. The homogeneous
component remains separate and its largest already-calculated solar-system
tidal ratio is `1.054152e-19`.

### 3.2 Reduced CTP dissipation

A minimal two-level witness uses

```text
dot rho=-i[H,rho]
 +gamma[L rho L^dagger-{L^dagger L,rho}/2],
L=|0><1|.
```

It gives exactly

```text
dot n=-gamma n,
n(t)=n(0) exp(-gamma t).
```

This demonstrates the missing mathematical ingredient: a positive real
gap. It is not being added to MTS. A legitimate parent completion would
have to derive the reduced retarded/noise kernel, positivity, `gamma`, its
environment, and the compensating Hilbert stress. Otherwise damping would
silently violate the same Ward conservation chain that produced Newton and
Maxwell.

## 4. Reclassification of the local-GR result

The exact status is now:

```text
chi=0 stationary bulk branch                         = derived;
chi=0 local positive-energy stability                = derived conditionally;
rho_local=rho_0 exact open-domain silence             = derived;
rho_local=rho_0 admissible boundary preparation       = yes;
closed-parent attraction to rho_0                     = rejected exactly;
universal positive local escape rate kappa            = rejected exactly;
finite-wavelength outgoing crossing kinematics         = derived conditionally;
reduced CTP dissipation gap gamma                     = not derived;
exact selected two-derivative GR/Newton/Maxwell       = retained;
unconditional parent preparation theorem              = not claimed;
full MTS                                               = not claimed.
```

This removes an impossible target from the local-GR ladder. Local GR no
longer waits for a closed-system attractor theorem that cannot exist. It is
an exact prepared branch of the parent action, just as a field theory still
requires physical initial and boundary data. The broader unification
programme must nevertheless derive a common history explaining why local
domains are on the vacuum branch while collective galactic domains can be
occupied.

## 5. Next calculation

Do not insert a Lindblad rate and do not keep searching for a universal
Hamiltonian escape gap; both routes are now settled for the present parent.
The remaining state derivation would have to produce a covariant history or
projector that excludes zero, trapped and incoming occupied modes:

```text
DERIVE_OR_REJECT_PARENT_PREPARATION_HISTORY
WITH_LOCAL_VACUUM_PROJECTOR,
ZERO_INCOMING_COLLECTIVE_FLUX,
AND_COVARIANT_HILBERT_STRESS_EXCHANGE.
```

Until such a history is derived, keep `rho_local=rho_0` explicitly as
preparation data. That is a transparent conditional branch, not a hidden
closure. The active D4 `E00125` matched-excess calculation remains the main
all-operator local-GR route and is unaffected by either no-go.

## Reproducibility

Run:

```text
post-checkpoint-work/.venv-score/Scripts/python.exe -B
post-checkpoint-work/scripts/
Y5_R2FR_5344_closed_parent_local_state_attractor_gate.py --dry-run

post-checkpoint-work/.venv-score/Scripts/python.exe -B
post-checkpoint-work/scripts/
Y5_R2FR_5344_closed_parent_local_state_attractor_gate.py

post-checkpoint-work/.venv-score/Scripts/python.exe -B
post-checkpoint-work/scripts/
Y5_R2FR_5344_closed_parent_local_state_attractor_gate.py --validate-saved
```

All generated rows retain
`valid_for_full_MTS_claim=false` and
`valid_for_parent_state_selection_claim=false`.
