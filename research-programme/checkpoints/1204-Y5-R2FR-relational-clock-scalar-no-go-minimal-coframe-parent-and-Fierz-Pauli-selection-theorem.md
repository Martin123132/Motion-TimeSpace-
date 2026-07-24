# 5188 - Relational-clock scalar no-go, minimal coframe parent and Fierz-Pauli selection theorem

Marker: `MTS_5188_RELATIONAL_COFRAME_AND_FIERZ_PAULI_SELECTION_THEOREM`

Checked: `2026-07-23`

Status: private analytic and source-executed checkpoint. No GitHub action.

## 1. Verdict

This checkpoint takes the foundational route selected by 5187 and gets a
definite answer rather than creating another missing-input queue.

Four scalar clocks/rods are enough to span ten metric variations at one
point, but that fact is **not** enough to generate gravity. With a constant
internal Lorentz metric,

```text
J^A_m = partial_m X^A,
g_mn  = eta_AB J^A_m J^B_n,
det(g)=-(det J)^2.
```

There are only two branches:

```text
det(J) != 0  -> X^A are local coordinates and g=X^*eta is exactly flat;
det(J)  = 0  -> det(g)=0 and the candidate metric is degenerate.
```

The executed nonlinear witness `X=(t,exp(x),y,z)` gives
`g=diag(-1,exp(2x),1,1)` and `R=0`.
Therefore a scalar-clock-only parent cannot own generic curved GR.

The minimal repair is a genuinely non-scalar relational coframe distortion:

```text
e^a_m = E^a_A(x) partial_m X^A,
g_mn  = eta_ab e^a_m e^b_n,
H^mn  = sqrt(-g) g^mn.
```

For every nondegenerate coframe and every invertible `J`,
`E=e J^-1`; the map is exactly surjective. This is not a derivation of `E`
from the old one-scalar corpus. It is the smallest honest parent extension
that can carry curvature.

## 2. What earlier routes become

The construction keeps, but sharpens, the useful earlier work:

- checkpoint 787's four-field rank result is correct but only pointwise;
- checkpoint 788's flat-pullback warning is now an exact dichotomy;
- checkpoint 1963's owned-coframe action becomes a concrete relational
  factorization rather than a free symbol;
- the additive `e=dX+A` work is replaced by the multiplicative,
  exactly-surjective `e=E dX` map;
- checkpoint 2048's `T,S` coframe is a static spherical reduction;
- checkpoint 3846's `g=h-c_*^2 tau tau` bridge is the invariant
  time/space decomposition of the same coframe;
- checkpoint 4961's one-scalar rank obstruction remains valid;
- checkpoint 5187's independent integrated `H` can be replaced, inside this
  candidate, by the full-rank coframe composite `H[e]`.

No corpus search found an already parent-owned full-rank MTS field that could
be identified with `E`. That absence is not hidden: `E`, or equivalently the
time one-form plus spatial triad, is new non-scalar parent data.

## 3. Exact factorization and gauge ranks

At `E=J=I`,

```text
(delta E,delta J) -> delta e = delta E+delta J:
rank=16, nullity=16;

delta e -> delta g:
rank=10, nullity=6;

(delta E,delta J) -> delta g:
rank=10, nullity=22;

delta e -> delta H:
rank=10, nullity=6.
```

The six `e->g` null directions are precisely local Lorentz frame rotations.
The sixteen first-jet split null directions express the redundancy between
`E` and `dX`; locally they come from four relational relabelling functions
and their derivatives.

The runner verifies with exact rational matrices that

```text
J -> S J, E -> E S^-1       leaves e exactly invariant;
E -> Lambda E, Lambda^T eta Lambda=eta
                              leaves g and H exactly invariant;
det(g)=-(det E det J)^2.
```

Thus the candidate loses no metric or Hilbert-source direction and does not
introduce a second observable frame.

## 4. Motion, time and space become an exact dictionary

The coframe gives the non-metaphorical MTS variables

```text
time:   tau = e^0/c_*;
space:  h_mn = sum_i e^i_m e^i_n,  rank(h)=3,  h_mn u^n=0;
motion: u and K_ij=(1/2) L_u h_ij;
metric: g_mn=h_mn-c_*^2 tau_m tau_n.
```

On a foliation `tau=N dt`, Einstein-Hilbert is exactly, up to the standard
boundary term,

```text
S_EH=(M_R^2/2) int dt d3x N sqrt(h)
     [R3+K_ij K^ij-K^2-2 Lambda_cal].
```

This is a precise version of "space evolving through time": `K_ij` is the
motion of spatial geometry. Its momentum is

```text
pi^ij=M_R^2 sqrt(h)(K^ij-K h^ij).
```

The executed DeWitt kinetic form has rank `6` and inertia
`(5+, 1-, 00)`.
Lapse and shift impose one Hamiltonian and three momentum constraints.
The exact configuration-space degree count is

```text
(12-2*4)/2=2,
```

the two massless spin-two polarizations. The constrained conformal direction
is visible rather than mistaken for a propagating ghost.

If the action depends on `E` and `X` only through `e`, with
`E_e,a^m=delta S/delta e^a_m`,

```text
delta S/delta E^a_A = E_e,a^m J^A_m,
delta S/delta X^A   = -partial_m(E_e,a^m E^a_A).
```

Invertible `J` makes the `X` equation a differential consequence of the
coframe equation. The relational split adds no physical pole. Separate
`X`- or `E`-kinetic terms not reducible to `e` would break this theorem and
must be independently constrained; they are excluded from the minimal parent.

## 5. The spin-two kinetic term is selected, not inserted

Write the most general local Lorentz-invariant quadratic two-derivative
action for a symmetric field as

```text
L=a (partial h_mn)^2
 +b (partial_m h^mn)(partial^r h_rn)
 +c (partial_m h^mn) partial_n h
 +d (partial h)^2.
```

Requiring invariance under
`delta h_mn=partial_m xi_n+partial_n xi_m` gives an exact rational
`120 x 4` constraint matrix. The runner finds

```text
rank=3,
nullity=1,
kernel=(1,-2,2,-1).
```

The positive-residue convention is

```text
L_FP=-1/2 L1+L2-L3+1/2 L4.
```

So the massless spin-two Hessian is unique up to the one overall
normalization `M_R^2`; it is not chosen coefficient by coefficient.
Checkpoint 4960's local consistency/self-coupling theorem then gives the
Einstein interaction at two derivatives, up to field redefinitions,
boundary/topological terms and `Lambda_cal`. Controlled higher-derivative
and nonlocal operators remain in the 5187 EFT corridor.

## 6. Curved and weak-field witnesses

The construction is not merely formal:

```text
FLRW e=diag(1,a,a,a):
R=6*(a(t)*Derivative(a(t), (t, 2)) + Derivative(a(t), t)**2)/a(t)**2;

a=exp(Ht):
R=12*H**2;

weak static e^0_0=1+Phi, e^i_j=(1-Phi)delta^i_j:
g00=-(1+2Phi)+O(Phi^2),
gij=(1-2Phi)deltaij+O(Phi^2),
gamma=1.
```

The independently executed linearized Einstein tensor is

```text
G00=2*Derivative(Phi(x, y, z), (x, 2)) + 2*Derivative(Phi(x, y, z), (y, 2)) + 2*Derivative(Phi(x, y, z), (z, 2)).
```

Therefore

```text
M_R^2 G00=rho
-> nabla^2 Phi=rho/(2M_R^2)=4 pi G_N rho,
G_N=1/(8 pi M_R^2).
```

The same metric gives `d2x/dt2=-grad(Phi)` for slow bodies and the
`gamma=1` null/lensing branch. No separate Newton or light coefficient is
introduced.

## 7. One parent action carries GR and electromagnetism

The minimal local candidate is

```text
S_parent=(M_R^2/2) int d4x e (R[e]-2 Lambda_cal) -(Z_A/4) int d4x e F_mn F^mn +S_matter[e,omega_LC[e],A,Phi_visible] +S_motion[e,psi]+Gamma_controlled_EFT.
```

Its consequences retain the source-executed 5187 chains:

```text
Einstein/Newton chain retained = True;
Maxwell/Poynting chain retained = True;
universal spin-two residue      = True.
```

`F=dA` and the Maxwell Hodge star use the same coframe. Variation gives

```text
nabla_m(Z_A F^mn)=J^n,
m u.nabla u^m=q F^m_n u^n,
T_EM,mn=Z_A(F_ma F_n^a-g_mn F^2/4),
T_EM^0i=Z_A(E cross B)^i=(E_c cross B_c)^i.
```

The local orthonormal-frame stress calculation is also executed directly:
`F^2=2*B_x**2 + 2*B_y**2 + 2*B_z**2 - 2*E_x**2 - 2*E_y**2 - 2*E_z**2`,
`T^00=B_x**2/2 + B_y**2/2 + B_z**2/2 + E_x**2/2 + E_y**2/2 + E_z**2/2`,
`T^0i=['-B_y*E_z + B_z*E_y', 'B_x*E_z - B_z*E_x', '-B_x*E_y + B_y*E_x']`, and
`trace(T)=0`.

The Poynting vector is therefore not a separate background field. It is the
energy flux of the Maxwell field measured by the same time/space coframe.
This directly addresses the earlier question about whether electromagnetic
flow acts on the background geometry: it sources the coframe through its
Hilbert stress tensor.

The `U(1)` representation and charge spectrum remain visible parent content;
the coframe construction does not derive them.

## 8. Honest boundary

Derived now:

- scalar-clock-only curved geometry is rejected exactly;
- the minimal relational coframe map is exact and surjective;
- integrated `H` is a rank-ten coframe composite in this candidate;
- relational split and Lorentz redundancies are exact;
- the e-only split adds no extra physical mode;
- the ADM motion/time/space dictionary and two-mode count close;
- massless spin-two gauge symmetry uniquely fixes the Fierz-Pauli ratios;
- the 5187 Einstein/Newton and Maxwell/Poynting chains survive unchanged.

Still parent data or open:

- the non-scalar distortion `E`, or equivalently `tau,h,u/K`, is not derived
  from the old scalar MTS corpus;
- spacetime Diff is realized exactly by the parent construction but is not
  manufactured by one scalar;
- visible `U(1)` representations and charge assignments remain parent data;
- the absolute gravitational scale still needs one calibration;
- physical total `c_IR`, nonlocal and complete `p8+` amplitudes remain open;
- the factorization is local to patches with `det(E)det(J)!=0`; global
  relational-chart caustics, topology and nonproper edge charges are not
  solved here;
- the no-extra-split-mode theorem requires every leading `E,X` dependence to
  factor through `e`; any direct split-breaking operator reopens the mode
  count;
- this is not a full unification or all-operator compact-GR claim.

The correct ontology decision is now sharp. A serious MTS parent must either
take the coframe/time-space-motion package as fundamental or derive it from a
genuinely non-scalar microscopic sector. Returning to a one-scalar metric
bootstrap is mathematically closed.

## 9. Next target

Checkpoint 5189 should not repeat the rank audit. It should project the
surviving MTS motion variables into the exact coframe/ADM invariants
`tau`, `h_ij`, `u`, `K`, and the traceless shear `sigma_ij`, then test whether
one parent motion Hessian:

1. preserves the four ADM constraints and the two local spin-two modes;
2. is reflection-even and source-silent on the compact local branch;
3. supplies the cosmology/galaxy response without changing `G_N` or
   `gamma=1` by arena.

If no such map exists, the coframe remains fundamental and the old motion
sector is retained honestly as controlled stress/exchange matter.

## 10. Artifacts and integrity

Generated evidence:

- `source-intake/functional_rg/5188/prior_relational_parent_supersession.csv`
- `source-intake/functional_rg/5188/scalar_clock_pullback_no_go.csv`
- `source-intake/functional_rg/5188/minimal_relational_coframe_factorization.csv`
- `source-intake/functional_rg/5188/coframe_H_rank_and_invariance.csv`
- `source-intake/functional_rg/5188/Fierz_Pauli_gauge_nullspace.csv`
- `source-intake/functional_rg/5188/MTS_ADM_dictionary_and_mode_count.csv`
- `source-intake/functional_rg/5188/curved_and_weak_field_witnesses.csv`
- `source-intake/functional_rg/5188/same_coframe_GR_Newton_Maxwell_chain.csv`
- `source-intake/functional_rg/5188/parent_upgrade_claim_boundary.csv`
- `source-intake/functional_rg/5188/source_provenance.csv`
- `source-intake/functional_rg/5188/relational_coframe_parent_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5188_VALIDATION.csv`

Claim guard:

`THIS_DERIVES_THE_SCALAR_CLOCK_NO_GO_THE_COFRAME_FACTORIZATION_GAUGE_RANK_MODE_COUNT_AND_FIERZ_PAULI_SELECTION_IT_DOES_NOT_DERIVE_THE_NONSCALAR_DISTORTION_FIELD_FROM_THE_OLD_ONE_SCALAR_MTS_CORPUS_DOES_NOT_DERIVE_VISIBLE_U1_REPRESENTATIONS_OR_THE_ABSOLUTE_NEWTON_SCALE_AND_IS_NOT_A_FULL_MTS_UNIFICATION_CLAIM`

The formalization workbench and checkpoint-5176 ensemble remain locked.
No GitHub action occurred.
