# 5171 - Action-angle retarded Vlasov polarization, static response and double-counting gate

Marker: `MTS_5171_ACTION_ANGLE_RETARDED_VLASOV_POLARIZATION_GATE`.

Date: `2026-07-21`.

## Decision

The compensated kernel requested by checkpoint 5170 is not an arbitrary
closure: its static scalar Vlasov projection follows directly from the
positive checkpoint-5154 Eddington state. For relative energy `Epsilon` and
an orbit labelled by `(Epsilon,L)`, the retarded action-angle solution gives

```text
delta f_n=[n.partial_J f_0/(n.Omega-omega-i0)] delta Phi_n,
delta f(omega->0)=f_Epsilon[delta Psi-<delta Psi>_(Epsilon,L)].
```

Consequently the discrete orbit kernel is

```text
B=sum_a C_a[diag(p_a)-p_a p_a^T],
B 1=0,
1^T B=0,
u^T B u=sum_a C_a Var_(p_a)(u)>=0.
```

The compensated zero mode, sign-changing density response and kinetic Ward
identity are therefore derived rather than imposed. However, this same
collisionless response is already evolved nonlinearly by checkpoints
5164-5169. It cannot be added to their scored profile as a new collective
stress without double counting.

## Executed parent-state response

The fixed state is `UGC09133`, `Wetterich_v_equals_minus_2lambda`,
`benchmark_1e_minus20_eV`, with no changed gravity or response coefficient.
The orbit integral uses `1536` `(Epsilon,L)` cells and
reconstructs the phase-space mass with relative error
`-1.872257101487307e-05`. The kernel symmetry residual is
`0.0` and its mass-mode residual is
`2.388465384022028e-15`.

Self-gravity is solved, not fitted:

```text
delta Psi=(I-kappa K B)^(-1) delta Psi_b.
```

The maximum static radial dielectric eigenvalue is
`0.5522232579424047` and the solve condition
number is `3.490339764695916`. Thus this benchmark has
no static radial pole. This does not prove the finite-frequency relativistic
spectrum.

The response has `30` positive and
`66` negative density shells and
conserves total occupied mass to relative residual
`3.2951935733112233e-16`. Its cumulative response
peaks at `77.94611143262613 kpc` with
`322373239229.3224 Msun`. The independently
reconstructed checkpoint-5170 shape requirement peaks at
`166.08144847903398 kpc` with
`587481756491.7664 Msun`.

## Does it close the 5170 residual?

No. The target is read only after the prediction. The profile cosine is
`0.9202693383295976`, so action conservation naturally
produces the right broad compensated orientation, but the predicted-to-required
ratio ranges from `0.23408343819975605`
to `2.6511207080165695` across
the frozen score window and is
`1.917559127085508` at the transition.
No constant multiplier can repair that radial mismatch, and no such
multiplier was used.

The linear hierarchy also fails globally: the largest self-consistent
perturbing-potential/background-potential ratio is
`4.2643327730030665`. A nonlinear
adiabatic calculation would therefore be required even if the response had
not already been included by the particle evolution.

## Convergence

- `COARSE_N64_E32_L20_T48`: phase-mass error=`-1.8667733666655195e-05`, lambda_max=`0.5577617398070236`, peak response=`328369613716.51245 Msun` at `69.62253582102169 kpc`
- `PRIMARY_N96_E48_L32_T80`: phase-mass error=`-1.872257101487307e-05`, lambda_max=`0.5522232579424047`, peak response=`322373239229.3224 Msun` at `77.94611143262613 kpc`
- `FINE_N128_E64_L40_T96`: phase-mass error=`-1.8640448632645246e-05`, lambda_max=`0.5500786384835554`, peak response=`319653742198.31274 Msun` at `82.23972299119485 kpc`

The fine-versus-primary changes in dielectric eigenvalue and peak cumulative
response are `0.003883609442384084` and
`0.008435864706112017`. The static result
is numerically controlled at this gate.

## Scientific correction and next route

Checkpoint 5170 correctly excluded a missing constant coupling, but its
remaining `Vlasov polarization` label was too broad. The classical density
part is now derived and identified as already counted. A genuinely new
mechanism must be one of the following, and must be parent-derived: a
nonclassical/interacting stress not present in Vlasov-Poisson, a different
parent-selected occupied state, or the source geometry omitted by the
spherical baryon projection. The next least-assumptive calculation is the
geometry gate: replay the same state and frozen source history with the
source-backed axisymmetric disk/gas force before inventing another stress.

```text
retarded action-angle scalar kernel                    = derived;
compensated mass zero mode                             = derived exactly;
radial sign-changing response                          = predicted;
static radial dielectric pole                          = absent in benchmark;
full covariant finite-frequency Pi_R                    = not derived;
linear hierarchy for the executed baryon source         = failed;
independent stress beyond checkpoints 5164-5169          = no;
adding this response to checkpoint 5169                  = forbidden double count;
local GR/Newton/Maxwell branch modified                  = no;
galaxy or full-MTS claim                                 = false.
```

All `27` validation rows pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
