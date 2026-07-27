# 5179 - Lowest reflection-even CTP boundary kernel, FLRW preparation and perturbative extra-stress no-go

Marker: `MTS_5179_LOWEST_EVEN_CTP_BOUNDARY_KERNEL_PERTURBATIVE_STATE_PREPARATION_GATE`.

Date: `2026-07-23`.

## Decision

This checkpoint performs the derivation selected at 5178. It does not invent
another occupation function and it does not stop at saying that the initial
state is missing. The lowest reflection-even non-Gaussian CTP kernel is
identified, derived from a covariant preparation contour, inserted into the
2PI/Kadanoff--Baym hierarchy, contracted into the Hilbert stress, and tested
against the already-locked amplitude and formation scales.

The result is restrictive. A weak parent-induced `alpha_4` exists, but it is
an initial-surface vertex rather than a stationary volume source. Adiabatic
vacuum preparation gives vacuum dressing already classified at checkpoint 5178
as local matching or calculable finite vacuum response, not galaxy occupation.
A controlled nonvacuum preparation contributes beyond the Vlasov response at
`O(c_ess^2)` and is far too small under the existing 4954--4959 bounds. A
standalone positive diagonal quartic state cannot even move the covariance in
the needed direction. A strong state can evade these weak statements only by
supplying a complete positive even hierarchy or a gapless occupied continuum;
that remains an explicit parent task, not a result hidden inside `alpha_4`.

## 1. Exact state-kernel hierarchy

For a general initial density matrix,

```text
<phi_+|rho|phi_->=exp(i F[phi]),

F[phi]=sum_(n>=0) (1/n!) integral_C alpha_n phi^n.
```

Every `alpha_n` is supported where all of its time arguments lie on the
initial CTP surface. Hermiticity gives

```text
i alpha_n^(a_1...a_n)
 =[i alpha_n^(-a_1...-a_n)]*.
```

The selected parent and state are invariant under `psi -> -psi`; therefore
all odd kernels vanish. `alpha_2` is the independent Gaussian covariance
already proved nonunique at checkpoint 5156. The first new kernel is exactly

```text
F_4=(1/4!) integral_(Sigma_0^4) alpha_4 psi^4.
```

This identifies the missing object without assigning it an arbitrary value.

## 2. Derivation from the bulk `X2-X3` parent

On spatially flat FLRW,

```text
sqrt(-g) [c_ess/4 (g^mn partial_m psi partial_n psi)^2]
 =c_ess/4 [-(psi')^2+(grad psi)^2]^2.
```

The `a^4` measure cancels the two inverse metrics. The symmetric four-leg
vertex is

```text
V_X2=2 c_ess sum_pairings (p_i.p_j)(p_k.p_l),
```

which reproduces the checkpoint-4953 shell amplitude

```text
M_22=(c_ess/2)(s^2+t^2+u^2).
```

For a Gaussian state prepared from `eta_i` to `eta_0`, the first connected
four-point is the exact first-order in-in expression

```text
C4_c(eta_0)
 =i integral_(eta_i)^eta_0 d_eta
   <[H_X2,I(eta),psi_1 psi_2 psi_3 psi_4(eta_0)]>_G
  +O(c_ess^2).
```

Equivalently, integrating the preparation contour `P` into an effective
initial surface gives

```text
alpha_4,X2(z_i)
 =-i integral_P d4v
   V_X2[nabla Delta_P(v,z_1),...,nabla Delta_P(v,z_4)]
  +O(c_ess^2).
```

This is the derivative-interaction version of the source-signed
Garny--Muller thermal initial-correlation construction. It is a real
derivation of the functional form. Its numeric value still depends on a
state-preparation contour, initial Gaussian state and endpoint that the
current parent has not selected.

One canonical contour can be completed exactly. Preparing the massless
adiabatic vacuum by a Euclidean half-space gives the free solution
`psi_k(tau)=psi_k(0)exp(k tau)` and therefore

```text
A_4,E(k_i)
 =[2 c_ess/k_t]
  sum_pairings
   [k_i k_j-k_i_vec.k_j_vec]
   [k_k k_l-k_k_vec.k_l_vec],

k_t=sum_i k_i.
```

For four equal magnitudes whose vectors form a regular momentum tetrahedron,
`k_i_vec.k_j_vec=-k^2/3`, so

```text
A_4,E=(8/3)c_ess k^3.
```

This is an explicit derived `alpha_4` benchmark, not an unspecified symbol.
It is also precisely interacting-vacuum wavefunctional dressing. It cannot be
relabelled as a populated galaxy state; the local part belongs to vacuum
matching and the finite part is a calculable vacuum response.

The dynamic-`N=8` GR-connected trajectory has
`c_ess=-7.2878119824619069e-111 eV^-4`. Under this canonical
Euclidean continuation its standalone quartic is therefore destabilizing,
not damping. This does not reject the functional `P(X)` trajectory: it proves
that the trajectory's higher even terms or a UV completion are mandatory to
define a global positive preparation. The locally converged Taylor germ
cannot be truncated to `X2` and used as a density matrix.

`X3` does not provide another independent leading four-point shape. Contracting
two of its six legs gives

```text
delta V_4,X3=(1/2) Tr_G V_6,X3,
```

because `C(6,2)4!/6!=1/2`. This is a local tadpole renormalization of the
four-leg vertex. Genuine higher state information begins with `alpha_6`.
Two `X2` preparation vertices generate `alpha_6=O(c_ess^2)`, so a strong
prepared state necessarily carries a full even hierarchy.

## 3. Exact quartic positivity test

The projected diagonal family

```text
p_lambda(q)
 proportional exp[-q^2/(2C)-lambda q^4/(24 C^2)]
```

is the most favorable way to test whether the lowest kernel alone can raise a
mode covariance while preserving a manifest positive density. Exact Wick
combinatorics gives

```text
<q^2>/C       =1-lambda/2+O(lambda^2),
kappa_4/C^2  =-lambda+O(lambda^2).
```

The script enumerates all Wick pairings: `15` for six fields, `105` for eight
fields, `12` normalization-connected covariance pairings, and `24` fully
connected four-point pairings. The coefficients are therefore not fitted.

The sign result is global rather than merely perturbative:

```text
d<q^2>/d lambda
 =-Cov(q^2,q^4)/(24 C^2)<0,  lambda>=0,

2 Cov(Y,Y^2)=E[(Y-Y')^2(Y+Y')]>=0,  Y=q^2.
```

Every normalizable positive quartic damping suppresses the variance. The
minimum locked transition deficit `1.0219388173325461`
would require

```text
lambda_required=-2.0438776346650922.
```

That sign makes a quartic-only diagonal weight nonnormalizable at large
`|q|`, and its magnitude is outside weak non-Gaussian control. A positive
`alpha_6` or a complete constructive quantum density matrix can stabilize a
negative effective quartic region, but then `alpha_4` is not the complete
state and the full hierarchy must be derived.

This is scoped correctly: it is an exact no-go for a standalone positive
diagonal quartic family, not for every off-diagonal quantum density matrix.
A unitary preparation can preserve positivity, but then its amplitude is
fixed by the bulk coupling and preparation history and must pass the next
gate.

## 4. 2PI and stress contraction

The post-4951 parent is interacting, so the earlier displayed
`Gamma_2^scalar=0` must not be reused beyond its quadratic scope. For `X2`,
the weak 2PI hierarchy begins with

```text
Gamma_2,double-bubble proportional (1/8) integral_C V4 G G,
Gamma_2,basketball   proportional (1/48) integral_C V4 G^4 V4.
```

The first term is a local Hartree correction of order `c_ess`; the first
nonlocal self-energy is order `c_ess^2`. An initial `alpha_4` enters the
statistical Kadanoff--Baym equation through the source-signed surface term

```text
S_alpha,k
 =Pi_(lambda alpha),F F(eta_0,eta')
  +(1/4)Pi_(lambda alpha),rho rho(eta_0,eta').
```

At late times,

```text
delta T_mn^(2)=D_mn^(2) delta F,
delta T_mn^X2=c_ess D_mn^(4)[G G+C4_c].
```

If the same bulk `X2` vertex induces `alpha_4`, its genuinely connected
late-time stress contribution is `O(c_ess^2)`. An arbitrary order-one
`alpha_4` can instead change the state, but that is precisely the independent
boundary postulate being tested, not a derived bulk source.

The weak vacuum setting-sun cut is also analytic far below its
three-particle threshold. For locked `UGC09133`,

```text
hbar c/R_n=1.7549606539036143e-28 eV,
(hbar c/R_n)/m_gap=1.7549606539036146e-08,
[(hbar c/R_n)/m_gap]^2=3.0798868967498023e-16.
```

It cannot produce the `|k|` criticality required at checkpoint 5149. A
populated medium can carry a low-frequency cut, but its leading Wigner term is
the Vlasov response already evolved and subtracted. The remaining collision
piece starts at the same weak interacting order tested at 4954.

## 5. Quantitative amplitude gate

Define the operational tensor-contracted fourth-moment enhancement by

```text
|Delta T_X2|=|c_ess| rho^2 K_T.
```

Then an additional fractional stress `f` requires the identity

```text
K_T=f/(|c_ess|rho).
```

Using the deliberately generous comparator
`|c_ess|=Mbar_Pl^-4=2.8444882085516576e-110 eV^-4`,
even the densest of the `173` positive-target
checkpoint-4953 rows requires

```text
K_T>=1.0233690404038258e+114.
```

For `UGC09133`, the generous and trajectory-normalized requirements are

```text
K_T,generous  =1.7961810156526596e+117,
K_T,trajectory=7.0106305318299089e+117.
```

These are operational stress enhancements, so no order-one tensor convention
is hidden in the comparison. They are incompatible with a weakly
non-Gaussian state.

The independent dynamical calculation agrees:

```text
4954 maximum finite-preparation probability
 =3.1256442447836532e-58;

4954 maximum generous controlled log gain
 =0.038692310770790016;

4954 minimum required log multiplicity
 =14.911693718845843;

4959 minimum completed six-point kernel
 =1.2818941575824521e-61.
```

All `692` high-frequency rows fail. This
closes the controlled perturbative state-preparation repair; it does not
pretend to calculate a strong nonquasiparticle state.

## 6. CMB gate without a false constraint

Planck 2018 reports

```text
g_NL^local       =(-5.8 +/- 6.5) 10^4,
g_NL^dot-pi^4    =(-0.8 +/- 1.9) 10^6,
g_NL^(partial pi)^4=(-3.9 +/- 3.9) 10^5.
```

These are real observational constraints. They cannot be directly pasted
onto a hidden motion-field `alpha_4`. The required projection is

```text
T_zeta^MTS
 =product_i T_(zeta X)(k_i) C4_X,c
  +metric-constraint terms,
```

followed by an overlap with the Planck templates. The current parent has not
derived `T_(zeta X)` or the shape overlap. Therefore this checkpoint records
the Planck numbers and the exact projection contract but does not fabricate a
numeric MTS trispectrum pass. The checkpoint-5156 empirical adiabatic
covariance remains a nonclaim baseline.

## 7. Result and next calculation

```text
lowest reflection-even non-Gaussian kernel       = alpha_4, derived;
covariant X2 preparation functional form         = derived;
X3 independent lowest four-point source          = rejected;
standalone positive diagonal quartic repair      = rejected exactly;
adiabatic-vacuum alpha_4 as galaxy occupation    = rejected by subtraction;
controlled weak X2-X3 prepared stress            = rejected quantitatively;
direct Planck g_NL bound on hidden alpha_4        = forbidden without transfer;
strong full even hierarchy                       = open, not claimed;
gapless occupied continuum                       = open, not claimed;
local GR/Newton/Maxwell branch                    = unchanged.
```

Route decision:
`THE_LOWEST_REFLECTION_EVEN_NON_GAUSSIAN_STATE_VERTEX_IS_THE_SURFACE_SUPPORTED_ALPHA4_AND_A_COVARIANT_PREPARATION_CONTOUR_DERIVES_ITS_LEADING_X2_KERNEL_BUT_NOT_A_FREE_GALAXY_STRESS_THE_STANDALONE_POSITIVE_DIAGONAL_QUARTIC_STATE_CAN_ONLY_SUPPRESS_VARIANCE_THE_BULK_INDUCED_WEAK_KERNEL_IS_VACUUM_LOCAL_OR_ORDER_CESS_SQUARED_AFTER_VLASOV_SUBTRACTION_AND_THE_EXISTING_CONTROLLED_FORMATION_BOUNDS_ARE_FAR_TOO_SMALL_SO_AN_ORDER_ONE_REPAIR_REQUIRES_A_PARENT_DERIVED_STRONG_FULL_EVEN_BOUNDARY_HIERARCHY_OR_GAPLESS_OCCUPIED_CONTINUUM_AND_CANNOT_BE_CLAIMED_FROM_ALPHA4_ALONE`.

The next parent-owned calculation is not another `alpha_4` inventory. It is
to construct the leading trajectory-normalized `X2-X3` retarded 2PI spectral
kernel on the occupied branch, subtract its Vlasov limit explicitly, and test
whether the remaining spectral density can close the gap or generate the
required infrared nonanalyticity. If it stays gapped and perturbative, the
state/interaction repair closes and any strong boundary state remains a
declared cosmogenesis postulate.

## 8. Sources and artifacts

Primary sources:

- J. Berges, *Introduction to Nonequilibrium Quantum Field Theory*,
  `https://arxiv.org/abs/hep-ph/0409233`;
- M. Garny and M. M. Muller, *Kadanoff--Baym Equations with Non-Gaussian
  Initial Conditions: The Equilibrium Limit*,
  `https://arxiv.org/abs/0904.3600`;
- Planck Collaboration, *Planck 2018 results. IX. Constraints on primordial
  non-Gaussianity*, `https://arxiv.org/abs/1905.05697`.

Generated artifacts:

- `scripts/Y5_R2FR_5179_lowest_even_CTP_boundary_kernel_and_perturbative_state_preparation_no_go.py`;
- `source-intake/functional_rg/5179/lowest_even_CTP_boundary_kernel.csv`;
- `source-intake/functional_rg/5179/X2_X3_FLRW_induced_fourpoint_contract.csv`;
- `source-intake/functional_rg/5179/exact_quartic_state_Wick_and_positivity_gate.csv`;
- `source-intake/functional_rg/5179/stress_contraction_and_kurtosis_bound.csv`;
- `source-intake/functional_rg/5179/CMB_covariance_and_trispectrum_projection_gate.csv`;
- `source-intake/functional_rg/5179/state_preparation_route_decision.csv`;
- `source-intake/functional_rg/5179/source_provenance.csv`;
- `source-intake/functional_rg/5179/lowest_even_CTP_state_preparation_results.json`;
- `source-intake/mts_residuals/P8_Y5_BRR545_5179_VALIDATION.csv`.

This is a private nonclaim checkpoint. It makes no local-GR, galaxy,
cosmology or full-MTS empirical claim.
