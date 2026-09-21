# Weak product compatibility and an action-based repair direction

10 September 2026. Private canonical annular continuation.
**247/247 checks, 18 unchanged exact free-root neighborhoods**, with matched
GR-plus-scalar and metric-Gram branches. No new evolution or physical fit.

Predecessor: `DERIVATION-20260910-variational-shift-source-decomposition.md`.
We now derive its interior obstruction directly from the weak scalar,
mass and shift equations. The result identifies the required products of
test functions, rather than merely relabeling the previous Schur blocks.
It also constructs and rejects an ideal scalar-only enrichment at these
fixed states, and supplies a shift-derivative-free action form for the next
joint compatibility attempt. A working full repair is NOT yet established.

## 1. Canonical quantities and the question being tested

Use the original quadrature Q, including its weights, and original realized
maps. At zero shift the bulk Lagrangian density is

    L_B = N mu_R/(kappa sqrt(F)) + m q^2/2 - p w^2/2,
    F = 1-2mu/R,     q = chi_t,     w = chi_R,
    m = R^2/(N sqrt(F)),           p = R^2 N sqrt(F),
    s = kappa R^2 F q w,           kappa = 1/10.

The canonical Gram contribution is a potential, not an additional kinetic
term at this slice. Let u be the independently solved full-shift mass rate,
including the original Gram current. Let N_t be the source-owned trial
lapse rate from the predecessor, which solves the mass tangency equations
when all mass rates equal u. Define

    theta = N_t/N - u/(R F),       m_t = -theta m.

W[eta] is the resulting derivative of the lapse equation against a nodal
lapse test eta. A nonzero W prevents this all-shift trial from being the
actual constraint tangent. Neither observed mass tangents nor observed
shift errors are used to construct the new source.

## 2. Three required products, three finite-space remainders

Let V_0 be the existing free scalar velocity space: released Hermite slopes
are included, but the two nodal endpoint velocities are prescribed. Let U_h
be the continuous piecewise-linear face space used for mass and shift.
For each eta introduce

    phi  = eta q/N,
    h    = eta u/N,
    zeta = F (N eta_R - eta N_R).

Project phi onto V_0 in the positive Q[m . .] pairing. Denote the result
phi_h and remainder e_phi=phi-phi_h; differentiate both represented
functions to obtain e_phi,R. This is NOT projection of their derivatives.

Interpolate h at the mass faces, obtaining h_h with coefficients H and
remainders e_h=h-h_h and e_h,R=h_R-h_h,R. Project zeta onto U_h with
weight rho=1/(kappa N F^(3/2)), obtaining zeta_h and e_zeta=zeta-zeta_h.

The projections are explicitly solved with verified inverse enclosures.
The mass interpolation is a specified choice of partition, not an optimal
or unique causal attribution. Every remainder is calculated from fields
and test maps, never from the final obstruction it is intended to explain.

## 3. Derive the scalar cancellation

Write Pi=m q. For every free scalar test v_h the original action gives

    Q[v_h Pi_t] = -Q[p w v_h,R] - G_chi[v_h],

where G_chi is the Gram potential's scalar variation. Let a_B be the
reconstruction of the prescribed two endpoint accelerations. All remaining
scalar accelerations lie in V_0, so projection orthogonality yields

    Q[e_phi Pi_t] = Q[m e_phi (a_B-theta q)].

Directly differentiating the bulk lapse equation gives

    W_B[eta] = Q[eta A] - Q[phi Pi_t] - Q[eta (p/N) w q_R],
    A = u_R/(kappa sqrt(F)) + mu_R u/(kappa R F^(3/2))
        + R u (q^2/(N^2 F)+w^2)/(2 sqrt(F)).

Using the weak scalar equation with phi_h therefore gives

    W_B[eta] = Q[eta A + p w q (eta/N)_R]
              - Q[p w e_phi,R]
              - Q[m e_phi (a_B-theta q)] + G_chi[phi_h].

All scalar slope equations remain present. For the full lapse derivative,
also add the direct time derivative of the Gram lapse covector.
No integration by parts, continuum quadrature replacement, or omitted
endpoint term has been used in this identity.

## 4. Derive the mass and shift cancellations

Set ell_mu=partial L_B/partial mu and ell_muR=partial L_B/partial mu_R:

    ell_mu = N mu_R/(kappa R F^(3/2))
             + R q^2/(2N F^(3/2)) + R N w^2/(2 sqrt(F)),
    ell_muR = N/(kappa sqrt(F)).

A pointwise product identity, independently checked symbolically, is

    eta A + p w q (eta/N)_R
      = ell_mu h + ell_muR h_R + rho (s-u) zeta.

The total mass covector includes the outer action term -C mu_outer/kappa
and the Gram mass variation. Its free entries vanish at the inherited
exact root; its inner entry is a retained boundary reaction, not zero.
The full shift equation gives

    Q[rho (u-s) zeta_h] = j_Gram[zeta_h].

Combining the equations produces the finite weak-product identity

    W[eta] = C_mass + C_shift + C_scalar,R + C_scalar,t
             + B_inner + B_outer + G_combined,

with explicit terms

    C_mass     = Q[ell_mu e_h + ell_muR e_h,R],
    C_shift    = Q[rho (s-u) e_zeta],
    C_scalar,R = -Q[p w e_phi,R],
    C_scalar,t = -Q[m e_phi (a_B-theta q)],
    B_inner    = H_inner Fcal_mu,total,inner,
    B_outer    = C H_outer/kappa,
    G_combined = G_chi[phi_h] + (G_N)_t[eta]
                 - G_mu[h_h] - j_Gram[zeta_h].

Away from an exact root, add H_free^T Fcal_mu,total,free. This term is
explicitly retained in the independent algebra check; its enclosure has
maximum upper norm 2.565e-14 across the cases. It is zero at each exact
free root, not a free parameter that has been fitted away.

The ten separately archived channels consist of the four C terms, two B
terms and four signed Gram terms. GR's Gram columns are exactly absent.
For interior nodal eta, both explicit B terms vanish algebraically. Tiny
subnormal outward intervals in those stored zero entries are rounding
padding, not a claimed physical interior boundary force. Boundary influence
can still enter scalar projection and prescribed histories.

The C in B_outer is the clock VALUE. The original clock RATE still enters
the trial N_t and hence theta. Changing this partition has not discarded it.

## 5. A structural obstruction, not just a small numerical discrepancy

On the uniform nodal grid, eta is a piecewise-linear hat; N is continuous
piecewise linear and F is continuous. At an interior nodal junction,

    [zeta] = F (N [eta_R] - eta [N_R]).

For an interior hat eta_j choose an adjacent interior node where eta_j=0.
There [eta_j,R]=1/h, giving

    [zeta_j] = F N/h > 0.

Every interior hat has such a neighbor on these grids. The run encloses a
strictly positive jump for each one at every root box. Consequently these
required shift test FUNCTIONS are not members of the continuous face space.
Increasing polynomial degree while keeping that space continuous cannot
make it contain these discontinuous functions with the lapse hats unchanged.

This proves a failure of this sufficient product-closure mechanism. It does
NOT prove the residual must be nonzero for every field: its pairing can
vanish accidentally, and a convergent method can have nonzero finite-mesh
defects. It is not a no-go theorem for finite elements or continuum GR.
The actual nonzero pairings in this run are established separately.

## 6. Construct an ideal scalar-only action enrichment and test it

At one fixed background, enlarge the free scalar space to include all
interior functions phi_j=eta_j q/N. They vanish at both endpoints and
are admissible H1 scalar variations. Freeze these enrichment functions
for the local construction, substitute the expanded field into the SAME
bulk-plus-Gram action, and take the additional canonical momenta from its
Legendre derivative at zero new coefficients. Their forces come from
the original action, not from subtracting W. A basis of the resulting
span removes any redundant enrichment functions.

This is a background-specific necessary-condition test, not a globally
defined adaptive action or an evolved replacement solution. At that
background the interior scalar products are now exact tests. Thus both
scalar C terms disappear there, independently of N_t and a_B, while the
Gram scalar term becomes the variation against phi itself:

    W_enriched[eta_j] = C_mass + C_shift
                       + G_chi[phi_j] + (G_N)_t[eta_j]
                       - G_mu[h_h] - j_Gram[zeta_h].

Nodal evaluation gives G_chi[phi_j]=(q_j/N_j)(G_chi)_j.
All quantities on the right are known at the original background. There
is no need to invent new accelerations or assume an enlarged full-system
inverse exists to test this necessary condition.

**All 18 cases retain a sign-certified nonzero interior W_enriched.**
Therefore this scalar-only enrichment, at these unchanged fields and with
the existing mass/shift rules, cannot be the complete repair. Other scalar
discretizations at changed backgrounds are not ruled out. In particular,
the result calls for joint compatibility, not removal of the Gram term.

At saved time 0.01, outward-rounded infinity-norm enclosures are:

| Intervals | Branch | Original interior W | Ideal scalar-enriched necessary W |
| --- | --- | --- | --- |
| 16 | GR | [5.98180e-6,5.98184e-6] | [5.59338e-6,5.59341e-6] |
| 16 | metric-Gram | [8.34506e-6,8.34512e-6] | [1.18120e-5,1.18122e-5] |
| 32 | GR | [7.50193e-7,7.50230e-7] | [7.57912e-7,7.57934e-7] |
| 32 | metric-Gram | [1.76952e-6,1.76959e-6] | [2.71042e-6,2.71048e-6] |
| 64 | GR | [1.75910e-7,1.75953e-7] | [1.62924e-7,1.62944e-7] |
| 64 | metric-Gram | [4.49023e-7,4.49089e-7] | [1.14856e-6,1.14862e-6] |

These are lapse-source covectors, NOT the shift covector norms in the
predecessor. They use code normalization, not SI observational units.
Mesh-dependent coordinates and six samples do not establish convergence.

At final N64 GR, C_mass is bounded above by 2.292e-11, C_shift has norm
about 1.629e-7, and the scalar gradient/time terms individually have norms
about 1.456e-6 and 1.464e-6. Their cancellation matters. At final N64 Gram,
the Gram scalar/shift terms are about 5.285e-6 and 4.788e-6, while their
combined contribution including the other Gram terms is about 4.980e-7.
Adding these norms as signed scalars would be incorrect.

## 7. Derive an action form suitable for the joint attempt

Merely appending discontinuous zeta tests to the existing smooth action
would leave shift-derivative/interface terms undefined. Instead start
from the actual spherical action in
`scripts/annular_adm_mixed_action_20260909.py`.
Let a=F^(-1/2) and beta be the shift. Its shift-dependent gravity density is

    L_beta = (R beta a_t/N - R beta^2 a_R/N
              - R a beta beta_R/N - a beta^2/(2N))/kappa.

For smooth fields the exact product identity is

    L_beta = L_beta,weak - partial_R J_beta,
    L_beta,weak = (R beta a_t/N
                   - R (a N)_R beta^2/(2 N^2))/kappa,
    J_beta = R a beta^2/(2 kappa N).

Thus the integrated smooth action can be written with no beta_R by
retaining -[J_beta] at the physical boundaries. Its canonical matter term
is R^2 a (q-beta w)^2/(2N) - R^2 N w^2/(2a).
At beta=0 its shift variation is still rho (mu_t-s); no correction was
chosen from the measured mismatch. The boundary flux is quadratic in beta
and has zero first variation at beta=0.

This offers a concrete starting weak action for a joint scalar/shift
enrichment or interface formulation. It does NOT yet justify a nonsmooth
spacetime metric, prove a consistent Gram-link extension, or give a full
regularity/evolution result. A broken-field extension must specify traces
and interface variation rather than silently discarding them.

Nor are the two FINITE quadrature actions automatically identical:

    Q[L_beta] - (Q[L_beta,weak]-[J_beta])
       = [J_beta] - Q[partial_R J_beta].

This exact quadrature defect must be retained or bounded when comparing
discretizations. At beta=0 its first shift variation vanishes, but its
quadratic/second-variation contribution need not vanish. No current data
identifies quadrature alone as responsible for W.

Reproducible symbolic control of the smooth identity and first variation:

```python
import sympy as symbolic

radius = symbolic.symbols('radius', positive=True)
kappa = symbolic.symbols('kappa', positive=True)
scale = symbolic.Function('scale')(radius)
lapse = symbolic.Function('lapse')(radius)
shift = symbolic.Function('shift')(radius)
scale_time = symbolic.Function('scale_time')(radius)
original = (radius * shift * scale_time / lapse
            - radius * shift**2 * symbolic.diff(scale, radius) / lapse
            - radius * scale * shift * symbolic.diff(shift, radius) / lapse
            - scale * shift**2 / (2 * lapse)) / kappa
weak = (radius * shift * scale_time / lapse
        - radius * symbolic.diff(scale * lapse, radius) * shift**2
        / (2 * lapse**2)) / kappa
flux = radius * scale * shift**2 / (2 * kappa * lapse)
assert symbolic.simplify(original - weak + symbolic.diff(flux, radius)) == 0
amplitude, spatial_f, speed, velocity, gradient = symbolic.symbols(
    'amplitude spatial_f speed velocity gradient', real=True)
matter = radius**2 * scale * (velocity - shift * gradient)**2 / (2 * lapse)
linear = symbolic.diff((weak + matter).subs(shift, amplitude), amplitude).subs(amplitude, 0)
linear = linear.subs({scale: spatial_f**(-symbolic.Rational(1, 2)),
                      scale_time: speed / (radius * spatial_f**symbolic.Rational(3, 2))})
expected = (speed - kappa * radius**2 * spatial_f * velocity * gradient)
expected /= kappa * lapse * spatial_f**symbolic.Rational(3, 2)
assert symbolic.simplify(linear - expected) == 0
print('weak_shift_action_identity: exact_zero; shift_first_variation: exact_zero')
```

## 8. Evidence, limitations and the next concrete construction

The 247 checks cover the local symbolic product identity, map preservation,
three verified inverse applications per case, weak identity versus a direct
lapse derivative and the prior independent Schur result, positive hat
jumps, GR controls and exact array roundtrips. Maximum midpoint discrepancy
against the prior source is 7.830e-18. Inverse proofs use the inherited
outward comparison-radius method, not floating inverse norms alone.

The identity is exact for the defined quadrature algebra. The verification
uses the exact real interpretation of realized binary maps and rational
kappa=1/10 under the inherited IEEE interval assumptions. Product
derivatives use the stored companion derivative maps; identifying them with
ideal analytic basis derivatives requires the usual map-rounding accounting.
The jump proof concerns the underlying continuous piecewise-linear spaces.
No integration-by-parts remainder or internal trace was silently set to zero
to obtain the numerical weak identity. This is not a continuum error bound.

Authoritative sources and outputs:
- `scripts/annular_weak_product_compatibility_20260910.py`
- `scripts/derive_annular_weak_product_compatibility_20260910.py`
- `source-intake/navier-stokes/20260910/annular-weak-product-compatibility-attempt01/status.json`
- `source-intake/navier-stokes/20260910/annular-weak-product-compatibility-attempt01/canonical_N64_metric_Gram_sample64.npz`
- `source-intake/navier-stokes/20260910/annular-weak-product-compatibility-final-integrity.json`

Probes are preserved, but only attempt01 owns the complete 18-case result.
The seal binds inherited evidence and the resume snapshot and checks cited
paths. The frozen-workbench check is an mtime scan, not a full pre-turn hash
baseline. No protected work, shared process, repository or public claim is changed.

**Next:** construct the joint weak-action compatibility prototype, using
the derivative-free shift form with explicit boundary/quadrature terms.
Derive its scalar, mass, lapse and shift variations together; include the
Gram link and potential variations together. Test zero-shift embedding and
constraint preservation on the same GR/candidate backgrounds before any
new evolution. If continuous shifts are retained instead, the lapse test
space must change to remove the proven hat-jump obstruction; that alone
does not guarantee the remaining nonlinear products close.

Do not retry endpoint acceleration or scalar-only enrichment as complete
repairs at these fixed states. Do not reinterpret W=0 as a fitted extra
force. Local-GR recovery, continuum convergence and horizon results remain
unproved; this step advances the numerical/action compatibility problem.
