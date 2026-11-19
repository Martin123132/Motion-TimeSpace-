# Cold relative-phase coefficients and numerical realization

## Retained mathematics

Sources: ../mts-relative-phase-perturbations-20261107/relative_math.py,
../mts-joint-relative-metric-20261107/{joint_math.py,native_joint.py},
../mts-correlated-relative-phase-mean-20261107/DERIVATION.md.
We retain the scalar action, other matter, GR and spatial-Poisson comparison, G192 tail and the same initial preparation. This stage evaluates coefficients; it does not assign a late microscopic phase or reset the perturbation mode.

N=ln(a); H is the conformal Hubble rate. x=am phi, v=phi', rho=(x²+v²)/2,
theta=atan2(-v,x), mu=am/H, alpha=k²/(am H), eta=H_N/H.
The saved mean state supplies N, the slow field and velocity, heavy mean density and conformal clock.
Cold window: a=0.36273334952836184 to 0.46575884027469494, inherited from the parent's kinematic selection.

For y=(delta,W), the exact scalar relative equations and metric readouts are those of the retained relative_math.py.
The full metric is u=Lw and w=S zeta; R=S^-1. Consequently
B=R G S+R_N S, not an average of individually averaged factors.
The scalar rows are computed from the exact scalar generator A and forcing F:
G_h=A selector_h+F L. Other matter and its hierarchy remain native.

## A native point, not a synthetic late history

build/MTSTwoField.f90 adds an opt-in single-point API accepting full fields, velocities, their N-rates and the physical clock. Full fields avoid subtracting/readding a large early anchor.
Only this explicit mode permits canonical heavy-scalar evaluation past the old early matching boundary; a fluid-matching marker remains forbidden.
The original path is unchanged when the mode is off, and the original library is not edited.

Thermal sound speed/opacity retain the existing table indexed at the supplied scale factor, while streaming uses the saved physical clock. This is not a new recombination calculation.
The source-owned external jet is W_ext=(2 R_ext-R_ext,N)/3 and W_ext,N=(2 R_ext,N-R_ext,NN)/3.
Both external moments come from the retained positive Fermi integration.

The native thermal background uses a slightly different numerical representation. At large mu, an extremely small H mismatch becomes amplified by the coordinate conversion. matched_cold_fibre.py therefore uses the native H and enthalpy consistently in a native comparison while keeping the saved scalar state and clock fixed. It records and gates the representation shift at 1e-10, and retains the much larger saved background uncertainty separately. This is not a new fitted parameter or a change of physical background.

## Two cancellations derived before evaluation

The first scan failed, rather than being accepted with a larger tolerance.
Its error had two different sources.

1. Coordinate differentiation formed and subtracted large carrier/gauge terms.
For the scalar physical-energy map, write its carrier logarithmic block as C and its gauge column as s.
With Omega=sqrt(k²+(am)²), omega=am, and mu=omega/H, after removing the harmless common gauge unit:
s=(Omega v, H(v_N-v)),
s_N-C s=(5 Omega v/2, (9H/2-3H_N)v+omega² phi/2).
This identity removes the canceling mu² terms.
The relative-coordinate logarithmic block is exactly
[[-3 cos(2theta)/2, -3 sin(2theta)/alpha],
 [3 alpha sin(2theta)/4, -1-eta-3 cos(2theta)/2]].
There is no residual carrier mu in it.

The high-precision independent checker constructs the entire heavy forward/inverse map and its derivative at 70 decimal digits, from consistently represented primitive coefficients. A rounded chart rate must not be subtracted from a separately recomputed high-precision mass/H ratio: mathematically they are the same chart. Windows longdouble is not used as fictitious extra precision.

2. Native stress differentiation originally multiplied out canceling oscillator terms.
For synchronous perturbations p=delta phi and w=delta phi',
D=v w+omega² phi p, P=v w-omega² phi p, Q=k v p,
v'=-2Hv-omega²phi, p'=w,
w'=-2Hw-(k²+omega²)p-k z v.
Direct differentiation gives
D'=-H(D+3P)-k Q-k z v²,
Q'=-2H Q+k P.
The canonical-stress isolated build evaluates these algebraically equivalent expressions in instantaneous mode. The original inactive path is unchanged.
derive_cold_identities.py checks both identities, both gauge components and carrier cancellation symbolically.

## Derivatives and means

The slow variables are sigma=(N,phi_s,v_s,rho_h,tau), with theta_N=mu-3 sin(2theta)/2.
Rather than take an N-step of size 1/mu on a late history,
L_N=D_sigma L f+(mu-3 sin(2theta)/2) partial_theta L.
The phase derivative is spectral on the existing 256-node phase grid; 64 and 128 nodes are its nested tests.
Slow directional derivatives use the retained 0.001/0.002 fourth-order stencils. No tolerance is changed.

The physical-clock mean is
Bbar=integral(B/theta_N)dtheta / integral(1/theta_N)dtheta.
The primitive satisfies Q_theta=(B-Bbar)/theta_N with zero angle mean.
A small Q alone does not bound accumulated evolution. The retained exact remainder is
E=(I+Q)^-1[BQ-Q Bbar-D_sigma Q f].
Cold transport still needs its drift/error and background-replacement control plus initial/final maps. These are next calculation targets, not assumptions silently dropped here.

## Interpretation

The leading W equation retains alpha²/4 pressure and attractive -rho_h/(2H²) self-gravity. A scalar relative perturbation is not declared pressureless by fiat.
All quoted matrix maxima are coordinate-dependent operator coefficients, not fractional spectrum changes.
Baseline and MTS use their own saved histories and identical numerical gates.
