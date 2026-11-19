# A state-preserving route into the quadrature formulation

The recovered real history need not be replaced by an isotropic phase
population to use the parent's quadrature machinery. This is an extension
of the state/source representation of the SAME quadratic action, not a
new force, a second populated field, or a newly derived halo abundance.

## 1. Retain the state information in the source contraction

Let b, v=b', u and p be two-component real quadrature vectors. For a real
coefficient vector xi, the physical realization is phi=xi^T b,
delta_phi=xi^T u, canonical momentum/a^2=xi^T p. Define the second-moment
matrix Sigma=<xi xi^T>, positive semidefinite. This is a second moment,
not necessarily a centered statistical covariance. A deterministic coherent
realization xi=(1,0) has Sigma=diag(1,0); uniform unit-circle phase averaging
instead has Sigma=I/2. These are different states.

The phase-averaged parent action and its metric variation give, without
discarding a quadrature or assuming an isotropic Sigma,

    rho_g = (v^T Sigma v + mu^2 b^T Sigma b)/2,
    pressure_g = (v^T Sigma v - mu^2 b^T Sigma b)/2,
    S = v^T Sigma v,
    Dstar = v^T Sigma p + mu^2 b^T Sigma u,
    Pstar = v^T Sigma p - mu^2 b^T Sigma u,
    D = Dstar + 3 S Phi,   P = Pstar + 3 S Phi,
    Q = k v^T Sigma u.                                      (5)

For Sigma=I/2, contractions are one half of the corresponding real complex
inner products. Dividing by rho_g reproduces the retained normalized
four-real-coordinate ensemble source rows. For Sigma=diag(1,0), (5)
reproduces the recovered coherent real sources exactly and is independent
of the unoccupied auxiliary quadrature. Its initial values therefore need
not be manufactured as physical occupation. Use the same Sigma in the
homogeneous background AND perturbation sources.

## 2. Conservation and basis independence

For constant Sigma and the componentwise retained equations

    b'=v,  v'=-2H v-mu^2 b,  (mu^2)'=2H mu^2,
    u'=p+(Psi+3Phi)v,
    p'=-2H p-(k^2+mu^2)u+mu^2(3Phi-Psi)b,

direct differentiation yields

    rho_g'=-H(rho_g+3pressure_g),
    D'=-H(D+3P)-k Q+3 S Phi',
    Q'=-2H Q+k(P+S Psi).                                   (6)

These are matter-sector identities for the stated on-shell background and
linear perturbations, not a numerical validation of the full coupled IVP.
If Sigma varies with time there are extra terms, including
k*v^T Sigma' u in Q', and
v^T Sigma' p+mu^2 b^T Sigma' u+3Phi*v^T Sigma' v in D'.
Silently changing the averaging state would remove those contributions.

For a constant invertible quadrature basis change b_new=A b, and the same
change on v,u,p, use Sigma_new=A^(-T) Sigma A^(-1). Every contraction in
(5) is invariant. Rank(Sigma) is invariant as well: no invertible change
of coordinates turns the coherent rank-one state into a rank-two uniform
phase population. Time-dependent basis changes additionally require their
connection terms; the previous carrier action already tracks that issue.

## 3. Coherent reconstruction versus instantaneous source inversion

For one real field the map (u,p) -> (Dstar,Q) has matrix

    [[mu^2 phi, v], [k v, 0]],  determinant=-k*v^2.

It is invertible away from background velocity turning points. The raw
field/velocity reconstruction in DERIVATION.md remains regular even there.
This two-real-state fact and the rank-two/four-column ensemble map are
different statements. They must not be conflated to claim either that
the real state is lost or that an ensemble is uniquely prepared.

The original harmonic-window matching procedure extracts a secular
coefficient using signed regression weights. It is not in general a
positive averaging measure: a negative weight can give a negative result
on a nonnegative history localized at that node. This does NOT invalidate
the historical secular fit. It means its two coefficients cannot, without
an additional coarse-graining argument, be interpreted as a uniquely
specified positive Sigma. No regression coefficients or tolerances change.

## 4. Concrete continuation

Use the recovered real (u,p) and original oscillatory background at a saved
matching-window epoch. The rank-one form of (5) supplies its exact source
ports into the retained metric constraints without D0 or an invented phase
population. Carry this coherent reference through a short forward window;
then test the existing phase projection against it, including the projected
products in the gauge conversion. Preserve the cold control.

A nonsingular complex carrier, if desired, needs an explicitly constructed
auxiliary homogeneous solution and its Wronskian; the auxiliary basis is
not extra matter when Sigma has rank one. Do not reuse a phase-averaged dust
background as that coherent reference, nor replace the saved phase state
with I/2 merely to fit the previous ensemble interface. A later emergence
of an effectively phase-invariant population needs a justified formation
or averaging argument. It is separate from the coordinate bridge proved
here and from Galaxy Lab's independently measured baryonic geometry.
