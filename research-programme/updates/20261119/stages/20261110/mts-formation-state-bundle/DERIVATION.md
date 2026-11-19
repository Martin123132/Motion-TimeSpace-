# Physical canonical preparation and the averaged formation interface

## 1. Canonical data include the metric volume

Use the retained Newtonian convention

    ds^2=a^2[-(1+2Psi)d tau^2+(1-2Phi)dx^2],

with Planck-normalized canonical real field phi, conformal background velocity
v=phi', H=a'/a and inverse-Mpc mass m. The covariant scalar action gives

    pi_phi = a^2(1-Psi-3Phi) phi_total'.

At linear order let d=delta phi_N and u=delta phi_N'-Psi v, the perturbation
of normal-frame time velocity multiplied by the background scale factor.
Then

    delta pi_phi=a^2(u-3Phi v).

The term-3Phi v is the spatial-volume correction, distinct from the lapse
correction already present in u. The exact parent gauge map supplies

    alpha=-H V_c/k^2,
    Phi=etak/k-H alpha,  Psi=2 Weyl/k^2-Phi,
    d=delta phi_S+v alpha,
    u=delta phi_S'+(phi''-Hv)alpha,
    phi''=-2Hv-(am)^2 phi.

These are the already retained gauge conventions. They do not turn the old
unresolved finite-difference alpha-prime diagnostic into a resolved one.

Apply the background time-dependent canonical transformation

    q=a^(3/2)phi,
    p=pi_phi/a^(3/2)+(3/2)(H/a)q.

The added term follows from adding the background boundary term
d[(3/4)H_cosmic q^2]/dt. At fixed prescribed metric the transformation has
unit symplectic determinant. Its linear perturbation is

    delta q=a^(3/2)d,
    delta p=a^(1/2)[u-3Phi v+(3/2)H d].

This transforms the scalar matter pair on a given metric slice; it does not
diagonalize the complete constrained matter-plus-gravity phase space.
The homogeneous pair matches Stage49. For any positive reference m,

    b=e^(imt)(m q+i p)/sqrt(2m),
    B=delta b/b0=(m delta q+i delta p)/(m q+i p).

This is an invertible phase-space chart, not an assumption that the envelope
is slow, cold or populated thermally. The common carrier phase cancels in B.
The earlier external-metric seed used a different momentum chart; do not
combine the two covariances without the explicit transformation.

The inverse is division-free in the background velocity:

    d=delta q/a^(3/2),
    u=delta p/a^(1/2)-(3/2)H d+3Phi v.

The physical native source is

    D=v u+(am)^2 phi d,
    P=v u-(am)^2 phi d,
    Q=k v d.

D and P have units Mpc^-2; Q uses the parent's same normalization. Omitting
the final+3Phi v when interpreting the canonical momentum causes

    Delta D=Delta P=-3Phi v^2,  Delta Q=0.

This is a concrete, testable missing-volume error, not an extra matter source.

## 2. Propagate the retained precision honestly

V_c and Weyl pass through the original float32 transfer buffer, as do the
standard density and velocity transfer outputs. The raw scalar field,
scalar velocity and etak diagnostics retain their recorded precision.
The saved source/precision owners are hashed before extraction.

The contribution from V_c rounding to alpha has radius
epsilon_alpha=|H/k^2| half_ulp(V_c). Because Phi=etak/k-H alpha, the two errors
are correlated. Thus the exact affine canonical variations are

    d(delta q)/d alpha=a^(3/2)v,
    d(delta p)/d alpha=a^(1/2)[(3/2)Hv-(am)^2 phi].

These coefficients propagate to the real/imaginary B errors without pretending
that rounding in alpha and Phi is independent. Weyl still affects Psi and
future dynamics; its cancellation in this instantaneous canonical pair is
not permission to discard its precision error in evolution.

The saved primordial curvature power is
Delta_R^2=2.1e-9(k/.05 Mpc^-1)^(-.0347).
At each k, covariance of Re B and Im B is
Delta_R^2 outer((Re B,Im B),(Re B,Im B)), with anomalous power Delta_R^2 B^2.
These are correlated classical perturbation statistics, not a newly thermalized
quantum mixed state. The mean field and its normalization remain separate.

## 3. The later saved chart is averaged, not a zero field

Stage56 stores complete late main-band histories for both models. In the
averaged heavy chart the diagnostic raw delta-phi slots are intentionally zero;
they must not be read as an empty wave. The populated state is stored as

    R=8piG a^2 rho_h=C/a,
    D_S=R delta_S, Q_S=R u_S,
    delta_N=delta_S-3H alpha,
    u_N=u_S+k alpha, theta_N=k u_N.

The pressure closure in this retained averaged model is

    Pi_ret = c_h^2(delta_N+3H u_N/k),
    c_h^2=x^2/(sqrt(1+x^2)+1)^2, x=k/(am).

The exact raw-field and averaged interfaces remain separately labelled. No
late anomalous covariance or absolute carrier phase is fabricated from the
averaged stress alone.

In a leading single-stream coherent NR description, with comoving envelope
A and peculiar velocity v_pec=grad S/(am), the perturbation/current relation is

    A/Abar=1+delta_N/2+i S + O(perturbation^2),
    S(k)=-am theta_N/k^2=-am u_N/k.

This is the spatial phase transfer. It predicts the supplied density and
current at first order using the same mass and metric coupling. Inverse
gradient reconstruction requires irrotational flow and fixes phase only up
to a spatial constant. That constant is irrelevant to the averaged NR
density/current but is not a recovered relativistic carrier-clock phase.

For a classical realization one can define positive initial density through
A=sqrt(nbar_com(1+delta))exp(iS) wherever1+delta>0. Choosing the nonlinear
completion from linear delta and S is an initial-data approximation, not a
derived second-order cosmological solution. No realization is generated by
this export, and no collapse or core occupation is inferred from it.

The direct leading NR Hilbert pressure is

    Pi_NR=x^2 delta_N/4.

Its difference from Pi_ret includes both the dispersion correction and the
relativistic velocity/slicing term. Report it explicitly; round-tripping
density/current alone is not proof of exact stress agreement.

## 4. Physical abundance and identical preparation discipline

Restoring SI only for the homogeneous normalization,

    rho_h = C c^2/[8piG a^3 (one Mpc in metres)^2],
    m_kg = hbar m_inverse_Mpc/[c (one Mpc in metres)],
    nbar_com = a^3 rho_h/m_kg.

C is the retained global benchmark input. It is not a local halo mass.
A finite comoving patch gets its total number from this density and its
declared realization/volume; bound and aperture populations then follow the
previous transport/readout laws. No Vobs normalization is used.

Pair MTS and cold at the same nominal scale factor and wavenumber, with their
own physical backgrounds and conformal times. Preserve the same primordial
curvature realization if later drawing one. Do not make the two cosmologies
share a false common clock or retune their primordial amplitude separately.

The remaining CDM, baryon and slow-field outputs are retained with the metric.
All other raw species observations remain present. Observer packets do not
supply every native radiation/polarization/neutrino multipole and hidden
regime state, so this is not advertised as a complete nonlinear all-species
restart.

## 5. Decide which approximation is available, rather than assuming it

The exact flat-background beat frequency is
omega=a m(sqrt(1+x^2)-1). The fractional error when using k^2/(2am) is
x^2/(sqrt(1+x^2)+1)^2 when normalized by the leading frequency.
This is an exact local dispersion diagnostic, not the total expansion or
metric error.

Together with the dimensional scale diagnostic (H/k)^2, demanding each below
epsilon leaves

    H/sqrt(epsilon) < k < 2am sqrt(epsilon)/(1-epsilon),
    H/(am) < 2epsilon/(1-epsilon)

as the overlap condition. This is only a screen on approximations: source
coefficients, radiation, averaging and accumulated dynamics need independent
control. Preserve long-wavelength GR modes outside the screen rather than
deleting them from the cosmology.

Evaluate all five saved epochs, not just the best-looking one. The nominated
next starting slice is a=.01; its status must come from the saved data and
these declared diagnostics. The high-k exploratory tail above5Mpc^-1 remains
outside the main-band contract, with the old failure labels unchanged.
