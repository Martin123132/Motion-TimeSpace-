# A spatial clock-normalized energy, with the actual interfaces retained

Date: 2026-09-09. Canonical annular continuation; publication handled separately.

## 1. Advance and limitation

This step derives and checks a spatially commuted energy identity through
two radial derivatives, without differentiating the clock again in time.
It uses the already-owned variables v=chi_t/c, w=chi_R, c=N sqrt(F).
The normalization itself is not new; applying it to this higher spatial
energy is the new step. No field equation, saved state or Gram term is changed.

The bulk coefficient estimate has no inverse mesh power and needs no
theta_t, theta_tt or second metric jet. This avoids generating an endless
chain of higher time-derivative assumptions in this particular energy argument.

The price is explicit and important: the reconstructed fields are only
piecewise smooth. The exact energy identity retains outer-boundary work,
internal-interface work, the actual scalar residual and quadrature IBP error.
Their paired estimate is NOT closed. Nor is equivalence to the preceding
higher graph norm H proved. This is not yet a stability or regularity theorem.

360/360 implementation/algebra checks pass on 18 unchanged saved states and
six manufactured controls. The same checks apply to GR and metric Gram.
Finite rate values, even positive ones, are not physical growth-rate forecasts.

## 2. Source ownership

Previous target and conditional T2 estimate:
`DERIVATION-20260909-second-metric-source-and-clock-acceleration-bound.md`.
Clock-normalized equations and physical residual definitions:
`DERIVATION-20260909-metric-flux-cancellation-and-exact-constraint-jets.md`.
Existing first-source and spatial coefficient bounds:
`DERIVATION-20260909-clock-spatial-gradient-and-derived-coefficient-input.md`.
Actual reconstructed action:
`scripts/annular_adm_mixed_action_20260909.py`,
`scripts/annular_released_hermite_action_20260909.py`,
`scripts/annular_metric_link_quadratic_20260909.py`.

New immutable helper and runner:
`scripts/annular_spatial_clock_energy_20260909.py`,
`scripts/derive_annular_spatial_clock_energy_20260909.py` (derive/seal).
Result:
`source-intake/navier-stokes/20260909/annular-spatial-clock-energy-derived/status.json`.
Integrity:
`source-intake/navier-stokes/20260909/annular-spatial-clock-energy-final-integrity.json`.

The runner uses one single-core BelowNormal process, python -B, inherited
source hashes and actual constraint tangents. No second-jet array is used
in the new computation. Old source hashes still include the previous evidence.
The separately requested public-repository export does not modify this source.

## 3. Exact normalized system, not an assumed continuum replacement

On each open reconstruction segment, the unchanged canonical equations give

    v_t=c w_R+(c_R+2c/R)w+r_v,
    w_t=c v_R+c_R v+r_w,
    theta=c_t/c.

r_w vanishes for the actual reconstructed chi and q=chi_t, up to arithmetic.
r_v is the actual weak-to-strong scalar residual. In the candidate it includes
the Gram force; it is not automatically an error that may be discarded.
The runner verifies r_v against the OLD stored scalar_defect arrays.

Write U=(v,w), J=[[0,1],[1,0]],
B=[[0,c_R+2c/R],[c_R,0]], r=(r_v,r_w). Then

    U_t=c J U_R+B U+r.

This identity uses only first metric rates. The cancellation of theta in the
normalized bulk equations does not assert that clocks stop evolving or that
metric backreaction disappears. Theta remains in the energy weight derivative.

## 4. Spatial commutation and the exact energy balance

Let U_k=partial_R^k U on each open segment. For k=0,1,2,

    (U_k)_t=c J (U_k)_R+F_k,
    F_k=sum_(j=1..k) binomial(k,j)c_j J U_(k+1-j)
         +sum_(j=0..k) binomial(k,j)B_j U_(k-j)+partial_R^k r.

Subscripts on c and B denote spatial derivatives, not time derivatives.
Define the broken spatial energy

    E_sp=one_half sum_(k=0..2) integral |U_k|^2/c dR.

This is a broken norm: derivatives are taken separately on segments formed
by the union of lapse/scalar nodes and mass faces. The continuous functions
v,w do not in general have continuous first or second derivatives.

For exact segment integrals,

    E_sp' = Outer + Interface
             +sum_k integral U_k^T F_k/c dR
             -one_half sum_k integral theta |U_k|^2/c dR,
    Outer=sum_k [v_k w_k]_(a to b),
    Interface=sum_(interior knots,k)
                    [(v_k w_k)_left-(v_k w_k)_right].

For the ACTUAL positive Gauss4 quadrature, retain the additional term

    delta_Q=sum_k Q[v_k w_(k+1)+w_k v_(k+1)]-Outer-Interface.

It is computed, not silently zeroed because the integrands are rational.
The corresponding E_sp,Q identity is exact in arithmetic. The implementation
uses local Taylor algebra through spatial order three and checks the time
derivative independently by complex differentiation of the energy itself.
No finite-difference second time acceleration is introduced.

## 5. Mesh-independent interior bounds

Keep the old canonical box: a=47/8, b=49/8, ell=1/4,
.65<=F<=.68, .8<=N<=.84, |mu_R|<=.002, |q|<=.02, |w|<=.03.
The prior mass-row estimate supplies L_N>=||N_R||_infinity.
Within each segment N and mu are linear. Consequently

    F_RR=-2F_R/R, F_RRR=6F_R/R^2.

Let f1=(1-F_min+2U0)/a, f2=2f1/a, f3=6f1/a^2, and

    s1=f1/(2sqrt(F_min)),
    s2=f2/(2sqrt(F_min))+f1^2/(4F_min^(3/2)),
    s3=f3/(2sqrt(F_min))+3f1 f2/(4F_min^(3/2))
                                      +3f1^3/(8F_min^(5/2)).

These bound the broken derivatives of sqrt(F). With c_+=N_max sqrt(F_max),
c_-=N_min sqrt(F_min), set

    a1=L_N sqrt(F_max)+N_max s1,
    a2=2L_N s1+N_max s2,
    a3=3L_N s2+N_max s3.

They bound |c_R|,|c_RR|,|c_RRR| INSIDE segments. They do NOT bound delta
distributions at knots; those belong to Interface, which remains in the
energy law. Claiming a global C3 metric from these bounds would be wrong.

Define

    B0=a1+2c_+/a,
    B1=a2+2a1/a+2c_+/a^2,
    B2=sqrt(ell)(a3+2a2/a+4a1/a^2+4c_+/a^3),
    U0sup=sqrt((.02/c_-)^2+.03^2),
    G_sp=Theta+2B0+4a1+a2+3B1,
    S_sp=U0sup B2/sqrt(c_-).

Weighted Cauchy-Schwarz and 2xy<=x^2+y^2 give the conditional inequality

    E_sp,Q' <= Outer+Interface+delta_Q
                 +G_sp E_sp,Q
                 +sqrt(2E_sp,Q)(S_sp+R_sp),
    R_sp^2=sum_(k=0..2) Q[|partial_R^k r|^2/c].

For example, the highest commuted terms are 2c_R J U2+c_RR J U1,
B U2+2B_R U1+B_RR U0. Only the last is put into the explicit coefficient
source S_sp, using the existing amplitude box. This explains the derivative
count and constants, rather than inserting numerically fitted growth rates.

Every interior coefficient here is derived from the current box and the
previous first-rate bounds. R_sp and signed surface terms are explicitly
unclosed; measuring them does not make them uniformly bounded inputs.

## 6. What the saved states actually show

At the unchanged final relative time .01:

| Grid/branch | E_sp,Q | actual rate | interface work | scalar residual work | interface+residual+delta_Q |
|---|---:|---:|---:|---:|---:|
| N16 GR | 6.24726 | -2.97718 | 11.0523 | -16.1248 | -5.07249 |
| N16 Gram | 7.80679 | 91.7051 | 137.012 | -145.993 | -8.98083 |
| N32 GR | 6.42307 | 19.0256 | 27.2692 | -16.0855 | 11.1837 |
| N32 Gram | 7.45258 | 48.1689 | -43.4335 | 195.333 | 151.899 |
| N64 GR | 6.41141 | 35.4059 | 49.0051 | -19.9680 | 29.0371 |
| N64 Gram | 6.83537 | 213.656 | 76.3106 | 19.0377 | 95.3483 |

At N64 the remaining OUTER flux is 2.93544 for GR and 114.96883 for Gram.
The interior reaction work is about 3.43332 and 3.33874, respectively.
The algebraic decomposition accounts for the complete rate, not just its
most favorable pieces. The full rate is visibly not established as converged
by these grids, despite comparatively moderate energy values.

The interior bounds give G_sp~3.18721 (GR) and 6.97138 (Gram).
The full conditional upper rates, including actual surface terms and the
absolute residual norm, are ~607.427 and 1156.929. These are NOT directly
comparable to the previous graph-energy upper bounds: the energy is different
and equivalence has not been established. Do not advertise a numerical gain
in stability merely by comparing different norms.

Gauss4 IBP residuals at N64 are about 1e-14, with Gauss12 cross-checks of the
same order. This is a numerical control, not a theorem that delta_Q vanishes.
The first-order fields are continuous; higher derivative jumps are not zero.
The six manufactured controls include zero scalar fields and smooth polynomial
fields on N16/32/64. The latter retain nonzero outer flux and negligible
artificial interface flux, checking that the decomposition distinguishes them.

## 7. Interpretation and next derivation

There is a concrete route away from the repeated higher-time-derivative
hierarchy: evolve normalized first-order fields with spatial derivatives.
The bulk coefficient part is now explicit. What is left is NOT permission
to enforce C2 continuity, zero flux, remove the Gram force or reset residuals.

Next derive a paired estimate for

    Outer + Interface + scalar residual work + delta_Q

from the ACTUAL finite variational equations and original endpoint histories.
Some saved terms cancel strongly, others reinforce; neither universal
cancellation nor a favorable sign has been proved. Separate absolute bounds
may destroy precisely the cancellations needed for a useful estimate.
Use the released slope equations and trace compatibility explicitly.

In the same derivation establish the transfer to the previous H norm, or
construct a boundary/interface-corrected equivalent energy. Do not call the
present broken norm equivalent by inspection. An energy diagnostic on the
old states is not a new time evolution, a continuum limit or a physical test.

Full shift/DAE compatibility, nonlinear P(X), parent calibration and horizon
or global regularity remain open. The canonical F>=.65 fixture is not a
black-hole interior. The public summary must retain these limitations.

Protected-workbench scan: mtimes since 2026-09-09T22:14:00Z, not a full
pre-turn hash baseline. Research source files are not changed by the exporter.
