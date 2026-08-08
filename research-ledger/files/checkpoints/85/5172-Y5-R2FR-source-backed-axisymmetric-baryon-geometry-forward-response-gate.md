# 5172 - Source-backed axisymmetric baryon geometry forward response gate

Marker: `MTS_5172_AXISYMMETRIC_SOURCE_GEOMETRY_FORWARD_RESPONSE_GATE`.

Date: `2026-07-21`.

## Question

Checkpoint 5169 evolved the measured visible source as a spherical-equivalent
mass. Checkpoint 5171 showed that adding a separate static Vlasov response
would double-count those same characteristics. This checkpoint therefore asks
the narrower forward question: does the measured non-spherical source geometry
close the remaining response gap with the parent state, source history and
calibrated `G_N` held fixed?

## Derived geometry operator

The frozen SPARC components define

```text
v_flat^2(R)=v_gas(R)|v_gas(R)|+0.5 v_disk^2(R).
```

For the unique razor-thin axisymmetric completion of that midplane force,

```text
H(k)=k integral dR v_flat^2(R) J1(kR),
zeta=sqrt(z^2+epsilon^2),
g_R(R,z)=-integral dk H(k)J1(kR)exp(-k zeta),
g_z(R,z)=-(z/zeta)integral dk H(k)J0(kR)exp(-k zeta).
```

The exponential is the exact Hankel form of the same Plummer-softened Green
function used by the particle calculation. The measured `0.7 v_bulge^2`
component remains spherical. No galaxy target, response amplitude or new
coupling appears in this construction.

The Hankel reconstruction has RMS relative error
`1.9446289569274164e-05` and maximum
error `0.00012738032875273282`. The
reconstructed surface-density negative-mass fraction over `0.05--500 kpc` is
`0.0`. The component
outer masses close to relative residual
`0.0`.

## Forward replay

The checkpoint-5169 isobaric `Z=0.3` transport, arrival clock and full
antithetic states are replayed without alteration about three orthogonal disk
axes. A doubled time resolution is also run for the primary axis.

- `AXIS_Z_PRIMARY`: q=`2.360216786674679`, RMSE=`0.2907262635454763` dex, compatible=`False`
- `AXIS_X_CONTROL`: q=`2.376265465075138`, RMSE=`0.2917243445466116` dex, compatible=`False`
- `AXIS_Y_CONTROL`: q=`2.3564847213863844`, RMSE=`0.2900817181037569` dex, compatible=`False`
- `AXIS_Z_TIME_REFINEMENT`: q=`2.365336461267273`, RMSE=`0.2906952329051777` dex, compatible=`False`

The checkpoint-5169 spherical result was q=`2.234007139940017` and
RMSE=`0.27740773926786666` dex. The primary geometry shifts these by
`Delta q=0.12620964673466206` and
`Delta RMSE=0.013318524277609656` dex. The maximum
orthogonal-axis displacement from the primary is
`0.016048678400458982`, and the doubled-time-step
displacement is `0.005119674592593881`.

## Decision

`SOURCE_BACKED_AXISYMMETRIC_GEOMETRY_DOES_NOT_IMPROVE_THE_PARENT_Q_GATE_SO_THE_CURRENT_OCCUPIED_STATE_SOURCE_BRIDGE_REQUIRES_NEW_PARENT_PHYSICS_NOT_A_GEOMETRY_OR_COUPLING_PATCH`.

This is a controlled source-geometry gate. It does not derive the thin-disk
completion from the parent matter action, validate a full local PPN branch, or
authorize a galaxy/full-MTS claim. It does remove spherical source projection
as an untested approximation while retaining the same state and one calibrated
`G_N`.

```text
measured source components used                = yes;
same parent state and source history           = yes;
same calibrated G_N                            = yes;
new response coefficient                       = no;
checkpoint-5171 response added                 = no;
orientation and time controls run              = yes;
galaxy or full-MTS claim                       = false.
```

All `15` validation rows pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
