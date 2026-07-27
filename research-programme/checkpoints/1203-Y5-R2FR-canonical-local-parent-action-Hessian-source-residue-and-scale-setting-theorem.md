# 5187 - Canonical local parent action, Hessian, source residue and scale-setting theorem

Marker: `MTS_5187_CANONICAL_LOCAL_PARENT_ACTION_SCALE_SETTING_THEOREM`

Date: `2026-07-23`.

Status: private analytic and source-executed checkpoint. No GitHub action.

## 1. Verdict

This checkpoint does **not** hunt for another source coefficient. Checkpoint
4960 already proved that the declared integrated-`H`, exact-Diff/BRST parent
has one universal leading spin-two source residue. The new result is to put
the surviving local theory into one canonical action and prove, in one place,
what follows from it.

The leading local result is now:

```text
INSIDE_THE_EXPLICIT_INTEGRATED_H_EXACT_DIFF_BRST_PARENT_WITH_ONE_POSITIVE_MASSLESS_SPIN_TWO_POLE_CANONICAL_U1_AND_REFLECTION_EVEN_MOTION_MATTER_THE_LOCAL_ZERO_FIELD_HESSIAN_IS_BLOCK_DIAGONAL_THE_HILBERT_SOURCE_MAP_IS_INVERTIBLE_SOFT_AND_BIANCHI_CONSISTENCY_LEAVE_ONE_COMMON_SPIN_TWO_RESIDUE_AND_FIELD_NORMALIZATIONS_CANCEL_FROM_EXCHANGE_THE_SAME_CANONICAL_ACTION_THEREFORE_GIVES_EINSTEIN_POISSON_NEWTON_GEODESIC_LENSING_AND_MAXWELL_COULOMB_LORENTZ_STRESS_POYNTING_CHAINS_WITH_NO_ARENA_RETUNING_THE_RELATION_GN_EQUALS_ONE_OVER_EIGHT_PI_MR_SQUARED_IS_DERIVED_BUT_AN_AUTONOMOUS_DIMENSIONLESS_RG_FLOW_RETAINS_ONE_TRANSLATIONAL_SCALE_MODULUS_SO_THE_NUMERICAL_VALUE_OF_GN_REQUIRES_ONE_ABSOLUTE_GRAVITATIONAL_SCALE_CALIBRATION_UNLESS_A_FUTURE_PARENT_SUPPLIES_AN_INDEPENDENT_DIMENSIONFUL_ANCHOR
```

In ordinary language:

1. the local vacuum Hessian has separate metric, photon and motion blocks;
2. ordinary matter has a metric stress source and an electric current but no
   one-motion-scalar source on the reflection-even branch;
3. one metric residue produces Einstein, Poisson, Newton, geodesic, lensing
   and leading radiation laws;
4. one photon normalization produces Maxwell, Coulomb, Lorentz force,
   electromagnetic stress and Poynting flux;
5. neither field-coordinate normalization can manufacture an extra coupling;
6. the *relation* `G_N=1/(8 pi M_R^2)` and cross-arena universality are
   derived, while the numerical value of `G_N` still requires one absolute
   scale datum in the current autonomous dimensionless RG parent.

This is a genuine consolidation and promotion of the **leading local branch**.
It is not a derivation of the metric/Diff parent from one scalar and it is not
an all-operator or full-MTS theorem.

## 2. Exact premises

The theorem is conditional on these explicit parent data:

- `H^mn=sqrt(-g)g^mn` is an integrated rank-ten tensor-density field;
- `g^mn=H^mn/sqrt(-det H)` and exact Diff/BRST identities hold;
- the infrared spectrum contains one positive massless helicity-two pole and
  no additional massless pole;
- the visible fields and their `U(1)` representations are parent content;
- the motion sector is reflection even and ordinary matter contains no term
  odd in `psi`;
- the expansion is made about an on-shell zero-field background
  `bar A=bar psi=0`; local flat formulas additionally take
  `q^2 >> |Lambda_cal|`.

Checkpoint 4961 proved that a lone scalar does not supply the rank or gauge
structure needed to derive these premises. This checkpoint keeps that
boundary visible rather than concealing it.

## 3. Canonical local action

Through the displayed EFT order the action is

```text
Gamma_loc=int sqrt(-g){M_R^2(R-2Lambda_cal)/2-Z_A F_mn F^mn/4-Z_psi(nabla psi)^2/2-m_gap^2 psi^2/2+c_IR C_mnrs F^mn F^rs+G_C3 I_C3-u_O4 C_abcd C^abcd (nabla psi)^2+P_ge_2(X)}+S_matter[g,A,Phi_SM]+Gamma_contact+Gamma_nonlocal+Gamma_p8plus
```

Here `I_C3` is the selected parity-even cubic-curvature invariant with
`G_C3=M_R^2 a_plus/2=A_C3^S l_P^2`, `P_ge_2(X)` begins at `X^2`, and the
p4 neutral-vacuum `R^2,C^2` coordinates have been quotiented at first
strict-EFT order. Their surviving matter-supported content belongs to
`Gamma_contact`, not to a second long-range vacuum gravitational residue.

## 4. Quadratic Hessian theorem

At `bar A=bar psi=0`, gauge invariance makes every photon term at least
quadratic in `A`, while reflection symmetry makes every motion term at least
quadratic in `psi`. Therefore

```text
delta^2 Gamma/(delta h delta A)   =0,
delta^2 Gamma/(delta h delta psi) =0,
delta^2 Gamma/(delta A delta psi) =0.
```

The three diagonal blocks on a curved zero-field background are

```text
K_hh       =M_R^2 K_Einstein+K_C3+K_nonlocal+K_p8plus,
K_AA       =Z_A q^2 P_T+c_IR K_CFF[bar C],
K_psipsi   =(Z_psi+2u_O4 bar C^2)q^2+m_gap^2+lower-gradient terms.
```

The exact field-degree audit gives mixed-derivative sum
`0`. The four-dimensional
trace-reversal source map has rank
`10`, nullity
`0`, determinant
`-1`, and squares exactly to the
identity. It therefore loses neither trace nor species information.

Five independent source classes give a soft/Bianchi constraint matrix of
rank `4` and nullity
`1`, with sole null direction
`(1,1,1,1,1)`. This is the one common leading gravitational coupling.

For `g=eta+a h`,

```text
Gamma_2=M_R^2 a^2 q^2 K/4,
D_a=4K^-1/(M_R^2 a^2 q^2),
V_a=a/2,
V_a^2 D_a=K^-1/(M_R^2 q^2).
```

The executed maximum normalization residual is
`0.000e+00`. Likewise
`A_c=sqrt(Z_A)A` and `e_c=e/sqrt(Z_A)` leave only `e^2/Z_A`, with maximum
executed residual `2.220e-16`.

## 5. Einstein to Newton

One variation and one sequence of limits give

```text
M_R^2(G_mn+Lambda_cal g_mn)=T_total,mn,
G_N=1/(8 pi M_R^2),

Box hbar_mn=-16 pi G_N T_mn,
nabla^2 Phi=4 pi G_N rho-Lambda_cal c^2,

Phi=-G_N M/r-Lambda_cal c^2 r^2/6,
a_r=-G_N M/r^2+Lambda_cal c^2 r/3.
```

The same metric follows from `-m int ds` for neutral bodies and controls null
rays. Hence there is no independent inertial, passive, active, orbital,
lensing or leading-wave value of `G`. The local constant PPN values are
`gamma=beta=1`, while the C3 and determinant tails remain explicit
higher-gradient corrections.

The Green-function normalization residual is
`0.000e+00` and all
`19` limit-chain rows pass.

## 6. Maxwell to Poynting

The same photon action yields

```text
nabla_m F^mn-4c_IR nabla_m(C^mnrs F_rs)=J^n,
nabla_m J^m=0,

u.nabla u^m=(q/m)F^m_n u^n,

T_EM,mn=F_ma F_n^a-g_mn F^2/4+c_IR H_CFF,mn,
T_EM^0i=(E cross B)^i.
```

When `C_mnrs=0`, ordinary Maxwell theory is exact for any `c_IR`. The
Poynting vector is therefore not an extra postulated coupling to a hidden
background: it is the `0i` Hilbert-stress component of the same canonical
gauge action. A future microscopic interpretation may explain the field, but
it cannot alter this normalization chain without changing the action.

## 7. Absolute scale theorem

For any autonomous dimensionless flow,

```text
dg/dln(k)=beta(g),
g(k)=g_hat(k/Lambda_g).
```

The executed counterfamily

```text
g_hat(x)=g_star x^2/(1+x^2),
beta(g)=2g(1-g/g_star)
```

has the same Gaussian endpoint and the same ultraviolet fixed point for every
`Lambda_g`. Its maximum beta-function residual is
`3.320e-17`, but

```text
G_N=lim(k->0) g(k)/k^2=C_g/Lambda_g^2.
```

Changing `Lambda_g -> s Lambda_g` leaves every dimensionless beta function
and fixed point unchanged while sending `G_N -> G_N/s^2`.

The motion ratio does not remove this freedom:

```text
J_gap=w_psi g=m_gap^2 G_N,
beta_J/J=(-2)+(+2)=0.
```

At fixed `J_gap`, the same scale translation sends
`m_gap -> s m_gap`; it does not select `s`. Therefore the current autonomous
GR-motion trajectory requires exactly
`1` absolute
gravitational scale calibration. `Lambda_cal`, `c_IR`, contact coefficients
and state data retain their separately listed roles below. A future parent
can improve the gravity-scale result only by supplying a genuine
dimensionful anchor or a derived relation to one—not by renaming a
dimensionless fixed-point coordinate.

## 8. Parameter and state count

The corrected count is:

| class | current count/status |
|---|---|
| leading local force normalizations | `2`: `G_N`, `alpha_EM` |
| background curvature calibration | `1`: `Lambda_cal` |
| unselected universal motion coordinate | `1`: `J_gap` |
| physical curvature-photon LEC | `1`: total `c_IR` open |
| neutral-vacuum p4 long-range inputs | `0` |
| p6 empirical inputs | `0`; `A_C3^S` is trajectory selected |
| matter-contact pre-reduction directions | `2` open |
| p8 aggregate completion coordinates | `2` open |
| occupied-state data classes | `2` open, not action couplings |

The state abundance and covariance found at 5186 are not smuggled into this
action count. They remain conditional initial-state data.

## 9. Higher-derivative corridor

The current numerical corridor is:

```text
classical one-scalar fifth force              = exactly zero;
standard constant Delta gamma and Delta beta = exactly zero;
neutral-vacuum p4 long-range input count      = zero;

max selected local C3 exterior |Delta a/a_N|
  = 3.6208461805802824e-124;

max massless-endpoint determinant |Delta a/a_N|
  = 1.3684320168245822e-61;

max compact finite C3 |Delta a/a_N|
  = 7.4150865005221568e-158;

max known nonQCD c_IR / one-ppm arena budget
  = 1.3813540140137983e-32.
```

These small numbers do not close the full theory. The C3 number is a selected
local source-scheme coordinate, the determinant number is a massless-endpoint
two-point subset, the physical `m_gap` threshold form factor is open, the
finite QCD part of `c_IR` is open, and the p8-plus response basis has not been
projected. Therefore

```text
leading two-derivative local GR/Newton branch = established inside premises;
flat Maxwell/Lorentz/stress/Poynting chain    = established inside premises;
all-operator compact equality to GR           = not established;
full MTS unification                          = not claimed.
```

## 10. What this changes

The project no longer needs another search for a separate Newton, lensing,
orbital, photon-stress or Poynting coupling. Such a coefficient would
duplicate a residue already fixed by the canonical action and Ward
identities.

The unresolved foundational task is now sharply different:

```text
derive the integrated H/Diff/visible-field parent from a genuinely
non-scalar relational or coframe construction,
or retain it honestly as fundamental parent data.
```

The one-scalar bootstrap route is already rejected by rank. Repeating it
would be circling. The next derivation should therefore test a minimal
relational coframe/tensor parent, while local residual work can proceed
independently through the physical `c_IR` match and p8 projection.

## 11. Claim guard

```text
THIS_IS_A_LEADING_LOCAL_THEOREM_INSIDE_EXPLICIT_PARENT_FIELD_AND_SYMMETRY_DATA_NOT_A_DERIVATION_OF_H_OR_DIFF_FROM_ONE_MOTION_SCALAR_NOT_A_NUMERICAL_PREDICTION_OF_GN_NOT_AN_ALL_OPERATOR_COMPACT_GR_THEOREM_AND_NOT_A_FULL_MTS_UNIFICATION_CLAIM
```

## 12. Generated evidence

- `source-intake/functional_rg/5187/canonical_local_parent_action.csv`
- `source-intake/functional_rg/5187/vacuum_quadratic_Hessian_and_source_vertices.csv`
- `source-intake/functional_rg/5187/universal_residue_and_limit_chain.csv`
- `source-intake/functional_rg/5187/RG_scale_setting_no_go.csv`
- `source-intake/functional_rg/5187/canonical_parameter_and_state_count.csv`
- `source-intake/functional_rg/5187/higher_derivative_local_corridor.csv`
- `source-intake/functional_rg/5187/cross_arena_no_retuning.csv`
- `source-intake/functional_rg/5187/source_provenance.csv`
- `source-intake/functional_rg/5187/canonical_local_parent_action_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5187_VALIDATION.csv`

Locked source inputs:

- `4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md`
  SHA-256 `b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4`
- `source-intake/functional_rg/4938/critical_surface_scale_lock_results.json`
  SHA-256 `544375b68725e8722507eea59414e91a3a76f2bad84c57ac3bdca1ae75a8a175`
- `4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md`
  SHA-256 `64b96ca4e19a058ced85c0c4b800ae7a237408606799dd8c4a5b58935f635c5f`
- `source-intake/functional_rg/4942/local_homogeneous_branch_identities.csv`
  SHA-256 `e9e4532679843c78ab2c86ddc39589bb6c694ca9cb17aae6a7bae47af66d4d0a`
- `4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md`
  SHA-256 `a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5`
- `source-intake/functional_rg/4943/junction_scalar_charge_and_fifth_force.csv`
  SHA-256 `5fbca2c1672d7fbb6f1741e56a3c72a2adbaee544a4fd5fd5525a616cb836df6`
- `4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md`
  SHA-256 `4985b31aa5d5253ec64fd1575bbd0f844c1b5c0924a11482fb77374ddee477b6`
- `source-intake/functional_rg/4946/local_Maxwell_action_stress_and_calibration_certificate.csv`
  SHA-256 `8b80ddf7b5cb469fa7c580b24f6b0d759322871bfb7064111839565ba290799a`
- `source-intake/functional_rg/4946/universal_CFF_calibration_transfer_functions.csv`
  SHA-256 `8707daa86fac5daf0bd6859bf8d8c29f18777349c9dbac24e259f729facd15a8`
- `4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md`
  SHA-256 `0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f`
- `source-intake/functional_rg/4947/source_residue_chain.csv`
  SHA-256 `b08468f29f938dfe72f13b9eec93f73c2b4f9c58ff89e7b67008c6de2cfc1e1d`
- `4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md`
  SHA-256 `6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d`
- `source-intake/functional_rg/4960/parent_definition_vs_derived_source_contract.csv`
  SHA-256 `93937d1ed9b13eab2c9e13fdf45a98c2236d037759abbdbec77e8da96ec9ddaf`
- `source-intake/functional_rg/4960/soft_Bianchi_species_coupling_nullspace.csv`
  SHA-256 `ad714332cf51eccb8b271394715b8de27affe3baee21889223da74aeeee1ac51`
- `4961-Y5-R2FR-integrated-H-origin-and-induced-EH-residue-from-motion-Hessian-or-explicit-fundamental-field-boundary.md`
  SHA-256 `ec6c5ff4056ed13ad92cad5e70ce125d81183abd0d79c59345dd6393987e2de2`
- `4962-Y5-R2FR-compact-body-sensitivity-binary-flux-and-junction-matching-or-strong-GR-residual-boundary.md`
  SHA-256 `93c88dd74a719106c998399a4f51bf78f44ed679ff19d3d570c8f3408d2c9134`
- `source-intake/functional_rg/4962/compact_body_sensitivity_and_no_dipole.csv`
  SHA-256 `e7c3fbefdc369b0493420d7bdc7318b060866981a85e7c1b845dfba4e1ba9717`
- `4963-Y5-R2FR-strong-field-C3-Wilson-selection-and-global-scalar-branch-exclusion-or-compact-GR-finite-residual.md`
  SHA-256 `ea2df6892c729fc3c49eb00074eb2d999c426c18046db60aa1f963b8cc9fcc48`
- `source-intake/functional_rg/4963/compact_C3_residual_domain.csv`
  SHA-256 `75285482928f6b1f897e365968e6d38514ca5d22fe70c6b8538610531e3b2383`
- `4964-Y5-R2FR-four-derivative-redundant-quotient-CFF-one-LEC-contract-and-p8-tail-norm-or-all-operator-compact-GR-boundary.md`
  SHA-256 `8bcfe51f2960789c575c0b4f9c85e65a6ca83be6a8a49c689e58c3180d4c8f57`
- `source-intake/functional_rg/4964/finite_matching_parameter_count.csv`
  SHA-256 `82d4178a1f7f983e47726451502f131075ecbd5b5905c31d068402f83828bd02`
- `source-intake/functional_rg/4964/CFF_one_LEC_calibration_contract.csv`
  SHA-256 `bd96a132e80647ac4f106a8c026afba3a8f4060d095fda3451cbbaac21d8236c`
- `source-intake/functional_rg/4964/p8plus_tail_norm_gate.csv`
  SHA-256 `a17f8fc7c652fec0b9a33985fe7c23045073114784bc2304a084ad4ca057510f`
- `4986-Y5-R2FR-common-scheme-log-invariant-and-local-metric-exterior-bounds.md`
  SHA-256 `6a2bea097597f0a1b39e035e0d8241abe7939371e980efd7c1eeaf5c0a5511a8`
- `source-intake/functional_rg/4986/C3_exterior_compactness_bounds.csv`
  SHA-256 `e6f8feab5e170b90420438385ba031295f7203fae857b1d5784d6ccff4b9e757`
- `source-intake/functional_rg/4986/determinant_exterior_tail_bounds.csv`
  SHA-256 `5fab5cb73fcb1328b24291d3a4f7cf3a71f32f7ce7ed44610b8f40a09242f83d`
- `5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-cog-theorem.md`
  SHA-256 `b2d5bddd8ce3cee2299b2cdadd66a0688bbd07c945bc329ac2ade4c20c113352`
- `5184-Y5-R2FR-stationary-PX-background-no-lump-and-mixed-Hessian-gate.md`
  SHA-256 `e4a3427963b4de0b5b40baab67b905e9e7054e8033c72dee768fb8973a258e33`
- `5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-collision-gate.md`
  SHA-256 `d47db7fefdb8b9f799a48a1e4d5a7c4266880d41d97b40ae2cefe33cd62d07a5`
- `5186-Y5-R2FR-FLRW-Bogoliubov-neutral-vacuum-production-and-abundance-no-go.md`
  SHA-256 `b3846c2e4bc1270b4c2f50d431fc5d812944f648ebec36f3250a95916101c05a`
- `source-intake/functional_rg/5186/FLRW_Bogoliubov_neutral_production_results.json`
  SHA-256 `08928a8d61f6a9defdb1b283e8d2faaa4ee2c8a3f11998071f829567c83ba28b`

All validation rows pass. The formalization workbench and checkpoint-5176
ensemble remain locked. No GitHub action occurred.
