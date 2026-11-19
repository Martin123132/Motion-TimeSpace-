# Actual early state, coupled restart and stress recovery

This extends the retained positive-quadratic real-scalar parent. No action,
mass, gravitational coupling, abundance, primordial amplitude, phase window or
data fit changes. The imported gauge/source identities are from
`../mts-early-canonical-state-bridge-20261110/DERIVATION.md` and its
`STATE-COVARIANCE-BRIDGE.md`; the interpolation repair is from
`../mts-native-source-conservation-20261110`. The new result is their tested
use with an actual full native early-state handoff, not an output-only replay.

## 1. What must cross a handoff

Write the native perturbation dynamics as

    Y' = F(tau,Y; B, E).

Y is the entire active perturbation vector, B is the retained homogeneous and
thermal background, and E contains the active hierarchy configuration and
memories. Reproducing only density, momentum and a metric column does not
determine Y or E. A numerical restart at tau0 instead requires

    Y_restart(tau0) = Y_reference(tau0),
    E_restart(tau0) = E_reference(tau0),
    B_restart = B_reference.

The one-mode control copies the entire allocated vector and EvolutionVars.
The latter includes hierarchy indices/multipoles, the discrete heavy selector,
approximation flags, geometric coefficients and active caches. Only the
integrator's adaptive work arrays and indicator are reset. Both copies then
use GaugeInterface_EvolveScal and source their own metric from their evolving
matter/radiation state. No saved metric history drives the restarted branch.

At each observation both branches evaluate the native derivative and the same
real64 metric/source observer. The uninterrupted output must reproduce the
previous repaired run bit for bit at all4253 times. This detects changes from
instrumentation or interference through shared native state. The exported
initial states, derivatives, observables and active caches must match exactly.

The background owner CAMBdata, its thermal data and native global coefficients
remain live throughout this session. The saved numerical arrays are useful
physical evidence, but do not serialize this owner. This is not a standalone
cross-process restart format. Output pointers are detached after evaluation;
the snapshot owner pointer and all allocated capture buffers are released
before the owner is destroyed. The earlier late interface is unchanged.

## 2. Stress is computed from the saved physical state

Use c=hbar=1, reduced-Planck field units, conformal H=a'/a, mu=a*m and k=1/Mpc
for these controls. Native-scaled stresses are 8*pi*G*a^2 times physical
stresses. With synchronous field perturbation us and velocity ws directly
from Y, background field b and conformal velocity v, define

    alpha = sigma/k,       Phi = eta-H*alpha,
    u = us+v*alpha,
    p0 = ws-mu^2*b*alpha-3*eta*v.

The existing on-shell canonical momentum is a^2*p0. The fixed-background
affine map (us,ws) -> (u,p0) has unit Jacobian and never divides by b or v.
That Jacobian alone is not a proof about the full metric-plus-matter reduced
symplectic form. Its immediate use here is regular recovery through field
and velocity zeros, without discarding the coherent phase.

The action's retained algebraic source expressions are

    D = v*p0+mu^2*b*u+3*v^2*Phi,
    P = v*p0-mu^2*b*u+3*v^2*Phi,
    Q = k*v*u,
    Dstar = v*p0+mu^2*b*u.

Substitution reproduces the independent synchronous stress/gauge route:

    Ds = v*ws+mu^2*b*us,   Ps = v*ws-mu^2*b*us,   Qs = k*v*us,
    D = Ds-3*H*v^2*alpha,
    P = Ps-(3*H*v^2+2*mu^2*b*v)*alpha,
    Q = Qs+k*v^2*alpha.

Five symbolic checks re-establish these retained identities, the unit
coordinate Jacobian and the absence of a turning-point denominator. Native
scalar diagnostics are independently recovered from the FULL vector rather
than used to manufacture it. Then the canonical-source readouts of the two
coupled trajectories are compared component by component.

The off-shell qualification from the previous source-conservation stage is
not erased: if Eb=v'+2Hv+mu^2*b and Ea=alpha'-Psi+H*alpha, then the exact
derivative-defined p=u'-(Psi+3Phi)*v differs from p0 by

    p-p0 = alpha*Eb+v*Ea.

The algebraic recovery checks do not prove those remaining interpolation and
metric-history defects vanish. Previous conservation diagnostics remain part
of the evidence. No compensating force is added here.

## 3. Metric constraints are checked on each evolved copy

For the retained flat native conventions at k=1,

    3H^2 = R,
    sigma = (Dsync/2+eta)/H + 3Qsync/2,
    eta' = Qsync/2,
    Phi = -(Dsync+3H*Qsync)/2,
    (Phi+Psi)/2 = Weyl.

The first two are recomputed from each copy's real64 observer. The momentum
constraint uses the saved full-vector derivative, and Poisson/Weyl readouts
are independently checked with the reconstructed potentials. These are
algebraic/instantaneous constraints along the coupled trajectory, not a new
proof of the continuum Bianchi identity or a bound on all cosmological error.

## 4. Scope of the two windows

The matching-adjacent window2591..2890 has300 states and299 intervals. It is
already outside tight coupling. Therefore a second control was frozen at
the earlier original indices512..520:9 states and8 intervals with ACTIVE,
nonzero photon quadrupole and derivative caches. Both controls retain the
full4253-time native evolution and the same source tables/tolerances.

The approximate massive-neutrino G11/G30 cache is inactive in these windows;
the actual active neutrino hierarchy is preserved. Copying those inactive
members does not constitute a test of a later nonzero-cache regime. A change
of signature is rejected in this bounded interface, not silently frozen.

The early control produces nonzero adaptive-restart differences, independently
showing that reference and restart arrays are not echoed. The very dense later
window is bitwise identical. Neither observation certifies exact physical
accuracy. No ensemble covariance, primordial seed or galactic occupation is
selected by a successful numerical restart.
