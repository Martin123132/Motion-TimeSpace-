# 5155 - Parent SP/Vlasov limit, homogeneous no-collapse theorem, post-equality transfer and wave runner

Marker: `MTS_5155_PARENT_SP_VLASOV_TRANSFER_WAVE_RUNNER`.

Date: `2026-07-20`.

## Decision

Checkpoint 5155 attempts the requested formation route instead of declaring
that the checkpoint-5154 equilibrium formed itself. The same rank-one metric
source used for local GR/Newton/Maxwell gives the weak-field
Schrodinger--Poisson system and its Vlasov limit. A real FFT split-step runner
reproduces the independently integrated linear modes at all three locked
masses. The galaxy-patch modes survive the executed post-equality dynamics.

The calculation also proves a hard boundary: the homogeneous checkpoint-5152
state cannot collapse without a nonzero spatial two-point covariance. That is
not a coding inconvenience. It follows from translation invariance and
uniqueness. A nonlinear run started from only `psi_i` and `Omega_X` would have
to insert perturbations secretly. The next missing object is therefore one
global primordial covariance, not another per-galaxy halo parameter.

## 1. Same parent action to the initial-value equations

The checkpoint-4947 local action contains

```text
S_psi=integral sqrt(-g)[-(nabla psi)^2/2-m_gap^2 psi^2/2
                        +c_ess X^2+higher operators].
```

In the weak one-metric branch, separate the fast rest-mass phase and retain the
leading `H/m`, velocity and gradient orders. With comoving number amplitude
`Psi_c`, the result is

```text
i hbar partial_t Psi_c
 =-hbar^2 nabla_x^2 Psi_c/(2m a^2)+m Phi Psi_c,

nabla_x^2 Phi
 =4pi G_N a^2(delta rho_b+delta rho_EM+delta rho_X).
```

The Poisson equation is the same checkpoint-4947 Einstein residue. Poynting
momentum and electromagnetic energy remain components of the same Hilbert
tensor; no galaxy-only `G`, direct scalar charge or second metric was added.
The current numerical runner uses the controlled free limit. The actual
infrared `c_ess` is still unsigned and is not silently set to a claimed parent
number.

Madelung linearization gives

```text
ddot delta+2H dot delta
 +[hbar^2 k^4/(4m^2a^4)-4piG rho_m]delta=0.
```

The Wigner equation gives Vlasov--Poisson with leading smooth-scale correction
`O[epsilon_L^2]`, `epsilon_L=hbar/(m v L)`. For the checkpoint-5154 isotropic
state, `f=f(E)` implies `{f,H}=f'(E){H,H}=0` exactly. Thus the `p=2` profile is
a genuine Vlasov equilibrium candidate, although stationarity is not a
formation theorem.

## 2. Exact homogeneous no-collapse theorem

For either homogeneous representative of the reflection-even primordial
mixture,

```text
psi(t_i,x)=+/-psi_i,
partial_i psi=0,
delta rho=0,
nabla Phi=0.
```

The parent equations and cosmological boundary state are translation
invariant. Uniqueness therefore preserves homogeneity. Evolving the `+` and
`-` representatives separately and averaging them does not manufacture an
inhomogeneous two-point function. Consequently

```text
P_delta(k)>0 for some k>0
```

or an equivalent parent 2PI covariance is necessary for halo formation. The
homogeneous abundance fixes the mean density, not the perturbation spectrum.

## 3. Three-mass post-equality transfer

To calculate what is possible without inventing that spectrum, the amplitude
cancels in a same-initial-mode transfer ratio. In `N=ln a`, the executed system
is

```text
delta_NN+[2+dlnH/dN]delta_N
 +[hbar^2 k^4/(4m^2a^4H^2)-3 Omega_m(a)/2]delta=0.
```

Both MTS and the zero-quantum-pressure comparator start at equality with the
Meszaros growing slope `delta_N/delta=3/5`. Radiation, matter and Lambda are
retained in `H(a)`. This is a **post-equality dynamical transfer**, not a full
radiation-era Boltzmann transfer and not a primordial-power claim.

Across the three masses, the curves collapse when plotted against
`k/k_J,eq` to maximum disagreement
`1.6653345369377348e-15`. The first
post-equality half-power crossing is

```text
k_half/k_J,eq=0.898452754021538.
```

For every one of the 1050 finite halo patches, the conservative
`k=2pi/R_L` mode remains below `k_J,eq`; its minimum present power ratio is
`0.9449157819262484`. The `pi/R_L` minimum is
`0.9964795190032412`. Thus the executed late dynamics
does not erase the mass supply found at 5153--5154. It does not prove the
patches occur with the required primordial probability.

## 4. Actual split-step wave propagation

A periodic three-dimensional Strang runner was executed, not merely written.
It evolves

```text
exp[-i m Phi dt/(2hbar)]
exp[-i hbar k^2 dt/(2m a^2)]
exp[-i m Phi dt/(2hbar)]
```

with Poisson recomputed between the kinetic and final potential stages. Two
linear modes, `k/k_J,eq=0.7` and `1.3`, were run at each locked mass from
equality to `a=4a_eq`. Across the six physical runs,

```text
maximum FFT-versus-ODE amplitude error
 =1.5731919207340184e-06,
maximum wave-norm drift
 =7.771561172376096e-15.
```

The strict-mass `k/k_J,eq=1.3` case was repeated at grids 24, 32 and 40; its
relative amplitude spread is
`1.7905711407661464e-06`. This validates the
equation plumbing and time integrator in the linear regime. It is not the
nonlinear attractor run.

## 5. Why a brute-force full wave box is the wrong next computation

For each finite halo define

```text
epsilon_n=hbar/(m v_infinity R_n)=m_WKB,row/m_gap.
```

The smooth Wigner/Vlasov correction at radius `r=xR_n` scales as
`(epsilon_n/x)^2`. Across all observed radii the largest proxy is
`0.25578164001889697`. At the strict mass,
`316/350` rows are below
one percent at every measured point; the counts are
`344/350` at
`1e-20 eV` and
`350/350` at
`1e-18 eV`. The core cannot universally be discarded, but most measured
radii are already collisionless.

Conversely, resolving the full diameter `2R_t` with eight cells per reduced
de Broglie length would require between
`15445` and
`481842299` cells per side. Even the minimum
working-memory estimate is far beyond the current machine for a full-edge
three-dimensional wave volume. This is a physical multiscale hierarchy, not
a reason to lower resolution until a run appears to pass.

The isolated coherent Schrodinger--Poisson scaling also fixes
`M R proportional m^-2`. The target invariant
`G M_edge m^2 R_n/hbar^2` spans a factor
`9018476241.723457` over the locked states. The
galaxy family therefore cannot be one rescaled coherent soliton. Its correct
candidate interpretation is the already-constructed multistream Vlasov halo
with a wave-resolved core.

## 6. Exact status and next calculation

```text
parent KG -> Schrodinger--Poisson limit             = derived;
same Einstein residue -> Poisson source              = derived;
SP -> smooth-scale Vlasov limit                      = derived;
homogeneous primordial state forms halos             = rejected exactly;
three-mass post-equality transfer                     = executed;
FFT wave runner versus independent mode ODE           = validated;
all finite halo-patch modes survive this late gate    = verified;
full 3D wave box as current route                     = rejected by resolution;

parent/empirical primordial covariance                = missing;
radiation-era Boltzmann transfer                       = missing;
actual infrared c_ess                                  = missing;
hybrid nonlinear collapse to q/core/p=2 edge          = not run;
projective profile as a cosmological attractor         = not derived.
```

The next calculation should derive the motion two-point covariance from the
4948 2PI state if possible. In parallel, construct one explicitly conditional
adiabatic comparator from a sourced CMB covariance and run a Vlasov volume
with wave-resolved zoom cores. The covariance, random seed, box and resolution
must be fixed before looking at the resulting halo profiles. The result must
be compared to `q_parent`, the core cut and `p=2` without refitting them.

Primary references:

- fuzzy transfer and Jeans scale: https://arxiv.org/abs/astro-ph/0003365
- cosmological SP numerics and resolution: https://arxiv.org/abs/1810.01915
- scalar adiabatic/isocurvature initial data: https://arxiv.org/abs/astro-ph/9811156
- nonequilibrium 2PI covariance: https://arxiv.org/abs/hep-ph/0409233

All `24` validations pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. All parent and galaxy
sources were read-only. No GitHub action occurred.
