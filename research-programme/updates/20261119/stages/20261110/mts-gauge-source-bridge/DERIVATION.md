# Mixed-gauge source substitution without a new closure

Use the previous canonical-metric-closure conventions. The live rest
hierarchy is in synchronous CDM-comoving coordinates; the new heavy
canonical state supplies Newtonian sources. This is a coordinate bridge,
not a change of gravitational coupling.

## 1. Solve the gauge clock together with the metric

Native flat constraints give, with eta its spatial synchronous potential,

    z=(D_sync/(2k)+k eta)/H,
    sigma=z+3 Q_sync/(2k^2), alpha=sigma/k,
    Phi=eta-H alpha, Psi=Phi-Pi/k^2.

Let Dr,Qr be the synchronous density/current of all OTHER species at their
current state, and Rh,Sh the heavy homogeneous energy and enthalpy.
The new state supplies compensated dstar=(D_h,N-3Sh Phi)/Rh and
qN=Q_h,N/Rh. Its physical gauge transformation is

    D_h,sync=Rh dstar+3Sh eta,
    Q_h,sync=Rh qN-Sh k alpha.

Consequently

    Phi=-(Dr+Rh dstar+3H(Qr+Rh qN)/k)/(2k^2+3Sh),
    alpha=(eta-Phi)/H.

ONLY heavy enthalpy appears in this denominator because the other states
remain synchronous. Using the previous total-enthalpy denominator while
leaving Dr,Qr synchronous would double-count the other species' gauge
response. Transforming them too reproduces the previous all-Newtonian
total-stress formula exactly.

Inject into the native heavy slots

    delta_slot=(Rh dstar+3Sh eta)/Rn,
    current_slot=(Rh qN-Sh k alpha)/Rn,

where Rn=matching_density/a is the actual native slot normalization. This
does not choose Rh or alter a coupling. Setting Rh=Sh=Rn and using the
native state recovers its original two slots exactly.

The retained native source first assembles other-species D/Q, then adds
the dark-energy/scalar stress. Its late photon/massless-neutrino RSA uses
the pre-dark-energy matter sources; that retained approximation is not
silently changed by this bridge. The new heavy stress enters the rest
RHS through total D/Q and hence z,sigma,eta'. Its native heavy derivatives
are discarded when substituting a new scalar law. Pressure affects the
new heavy law; it is not forced to equal the native fluid pressure.

## 2. A native-equivalent control in these coordinates

For the existing dust background Rh=Sh=Rn, let dstar=delta_sync-3eta and
qN=q_sync+k alpha. Native equations imply

    dstar'=-k qN-3H pi,
    qN'=-H qN+k(pi+Psi),
    pi=r(dstar+3Phi+3H qN/k),
    r=(k/mu)^2/[sqrt(1+(k/mu)^2)+1]^2.

Thus the bridge can be tested without changing a physical equation. This
native-equivalent control is not the new four-coordinate scalar.

## 3. Unrestricted scalar with a stable slow/fast separation

The prior stage gave independent complex (Z,U). Set

    V=U-lambda_k Z, a0=lambda0-H,
    Omega_k^2=k^2+mu^2-H'-H^2,
    Rk=lambda_k'+lambda_k^2+Omega_k^2.

Then exactly

    Z'=(lambda_k-lambda0)Z+V+C a0,
    V'=-(lambda0+lambda_k)V-Rk Z+C(H-lambda_k)a0+mu^2 Dm,
    C=Psi+3Phi, Dm=3Phi-Psi.

Evaluate lambda_k-lambda0 using the already-tested separate frequency
beat, not subtraction of large carrier frequencies. This avoids numerical
loss of the slow branch without deleting the fast homogeneous solution.
The prior affine plane is V=D-C a0, so the preparation remains explicit.

For Db=|a0|^2+mu^2,

    dstar=2 Re[a0*((lambda_k-H)Z+V)+mu^2 Z]/Db,
    qN=2k Re[a0*Z]/Db,
    pstar=dstar-4mu^2 ReZ/Db,
    pressure=pstar+3(Sh/Rh)Phi.

Conjugation on a0 is denoted by *. These couple via section1to the live
rest hierarchy. No future supplied Phi/Psi or species histories are needed.

The carried W2ensemble energy is proportional to Db/(a^2W0), enthalpy to
2|a0|^2/(a^2W0). Normalize it to the retained cosmological Rh on the initial
slice, not to a galaxy fit. Any mismatch from the native dust background
must be included in the earlier defect budget, not declared zero because
it is numerically small. A complete coupled comparison must retain this
qualification and the nonzero W2residual.
