# 4934 - Source-complete minimal `C3-CFF-F4` flow

Marker: `MTS_SOURCE_COMPLETE_C3_CFF_F4_FLOW_4934`.

Date: `2026-07-12`.

Status: private source-executed derivation checkpoint; source-complete for the
declared minimal `C3-CFF-F4` natural-essential truncation, but not the full MTS
fixed point, an infrared trajectory, or a local-GR/Newton/Maxwell proof.

## 1. Decisive result

Checkpoint 4933 left two exact cross-source blocks open. Both are now derived
without closure coefficients:

1. the portal-dependent Weyl-cubic photon contribution through quadratic
   order in `g_CFF`;
2. the direct `h_C3` contribution to the photon-background flow.

The completed selected-row system has the common zero

```text
(g,g_plus,g_minus,g_CFF,h_C3)
  =(0.1305603732179711,
    0.3470041701608080,
    3.244460421436017,
    0.0037300003823489045,
    3.947320506281829e-6),

||beta||_infinity=1.43268557658e-14.
```

Its beta-matrix spectrum is

```text
lambda={
  -1.890832345405438,
   0.290512960464078,
   0.242082333593261 +/- 0.022779238325848 i,
   1.093933285951222
}.
```

Thus the completed minimal source truncation has exactly one relevant
direction and four irrelevant directions. Its signed distance from the
imaginary axis is

```text
delta_minimal=0.242082333593261.
```

## 2. Direct-row selection theorem

For

```text
I_C3=h_C3 integral sqrt(g) Tr(C^3),
```

the second variation begins as

```text
delta^2 I_C3
 =h_C3 integral sqrt(g)
  [6 Tr(Cbar deltaC deltaC)+3 Tr(Cbar^2 delta^2C)+...].
```

At first order in background curvature, the direct Hessian is therefore
Weyl-linear. In the irreducible photon-background basis this proves exact
zeros in

```text
{F2,FDeltaF,RFF,SFF,F2sq,F4}.
```

Only the Weyl-matched `CFF` row can survive. This removes six of the seven
previously open direct rows by representation content rather than by a small-
coupling estimate.

## 3. Exact linear portal zero

The nonminimal photon principal operator on the Ricci-flat projection is

```text
P_portal^nu_sigma
  =-8 g_CFF C^{mu nu rho}_sigma D_mu D_rho.
```

The four independent contributions to the Weyl-cubic heat-kernel projection
linear in `g_CFF` vanish separately:

```text
bundle connection squared =0,
RNC metric connection     =0,
scalar Van Vleck          =0,
derivative commutator     =0.
```

The generic four-dimensional Weyl-tensor contraction also reproduces

```text
C^{mu nu rho}_sigma [D_mu D_rho a_0]^sigma_nu / C^2=-1/4.
```

Therefore, in the declared source scheme,

```text
Delta RHS_C3 | linear in g_CFF =0.
```

The zero is tensorial and consequently does not depend on the scalar
threshold functional chosen within scalar functions of the source natural
photon Laplacian.

## 4. Exact quadratic portal row

For two insertions of

```text
U^nu_sigma=-8 C^{mu nu rho}_sigma D_mu D_rho,
```

the exact ordered-derivative contractions are

```text
flat ratio to C^2       =6,
bundle-curvature ratio  =3/2.
```

Odd first-derivative terms vanish under symmetric momentum integration. The
remaining second-derivative-on-Weyl term is proportional to
`delta_ab C^{a s b n}=0`. Matching the source Litim kernel gives

```text
Delta RHS_C3 | g_CFF^2
 =g_CFF^2(5 gamma_a-3 gamma_DF+20)/(80 pi^2).
```

At the completed point this row contributes

```text
Delta RHS_C3 | g_CFF^2=3.563163151510779e-7.
```

This is larger than the one-percent response threshold inferred in 4933 and
is the main reason `h_C3` moves by about `-7.62 percent` when the source block
is completed.

## 5. Direct `C3 -> CFF` coefficient

The unique surviving direct row has the form

```text
Delta RHS_CFF | direct C3
  =h_C3 K_C3toCFF(g,g_CFF;beta_g,
                  gamma_g,gamma_S,gamma_a,gamma_DF,gamma_FTL).
```

The complete exact rational expression for `K_C3toCFF` is stored in
`source-intake/functional_rg/4934/direct_c3_cff_principal_results.json`.
Its finite-index angular reductions are

```text
Maxwell diagonal       = 7/32,
Maxwell mixed          = 7/32,
CFF diagonal           =-7/8,
CFF mixed cross        =-7/8,
CFF mixed square       = 7/8,
pure C3 cubic          =-27/64,
trace RG-kernel block  =0.
```

The calculation includes the Maxwell and `CFF` metric/mixed Hessians, all
terms through `g_CFF^2`, the `gamma_FTL` metric-kernel block, the
`gamma_DF/gamma_FTL` mixed-kernel blocks and the source Litim radial moments.
The raw pure-C3 trace is calibrated to the source coefficient

```text
120 pi g^3/(1-2g rho)^4
```

by the exact graviton-polarization factor `1/2`.

At the completed point,

```text
K_C3toCFF=-0.004314603640978981,

Delta RHS_CFF | direct C3
  =-1.703112342851458e-8.
```

## 6. Canonical projection contract

The square projection remains

```text
13 general-background C3 rows
+7 photon-background rows F2 through CFF
=20 equations for 20 flow/redefinition variables.
```

The 13 general-background rows are authoritative for the lower vacuum-
curvature sector because they contain the `h_C3` vacuum Hessian. The five
lower-curvature rows also available from the four-derivative photon source do
not contain that Hessian and are retained only as a duplicate
scheme/truncation diagnostic.

At the completed point their residual vector is

```text
{ 1.59251491090e-6,
 -6.18819875975e-5,
  8.89352137109e-5,
 -2.33688715889e-4,
 -2.60857589064e-5 }.
```

Its infinity norm `2.33688715889e-4` is not an omitted canonical beta row and
is not hidden as zero. It measures the compatibility of two unequal source
truncations.

## 7. Movement from checkpoint 4933

Relative to the partial point, the coordinate shifts are

```text
Delta x={
 -7.93973934e-8,
 -8.04994130e-8,
  2.39977617e-5,
  5.78065354e-8,
 -3.25717831e-7}.
```

The relative shifts are approximately

```text
{-6.08e-7,-2.32e-7,7.40e-6,1.55e-5,-7.6226e-2}.
```

The completed terms do not destroy or materially displace the photon-gravity
coordinates, but they do produce a non-negligible renormalization of the tiny
Weyl-cubic coordinate. The one-relevant-direction index and the `0.242`
signed gap survive direct recomputation; they are not inferred from the 4933
perturbation bound.

## 8. Source-completeness statement

```text
minimal Maxwell C3 row                         = derived;
principal g_CFF^3 C3 row                       = derived;
linear g_CFF C3 row                            = exact zero;
quadratic g_CFF^2 C3 row                       = derived;
direct C3 rows F2,FDeltaF,RFF,SFF,F2sq,F4      = exact zero;
direct C3 row CFF                              = derived;
remaining exact blocks in declared system      = none;
minimal five-coordinate common zero            = solved;
minimal signed index                            = one relevant;
full MTS fixed point                            = false;
GR-connected MTS trajectory                     = not integrated;
local GR/Newton/Maxwell derivation               = not promoted.
```

“Source-complete” here means complete for this declared source basis and row
selection. It is not a regulator-, gauge-, basis- or truncation-independent
theorem about the full MTS theory.

## 9. Next physics step

The next target is

`4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md`.

The required order is:

1. integrate trajectories leaving the completed point along its single
   relevant direction and test for the Gaussian/GR infrared branch;
2. verify regularity of `g_CFF`, both four-photon directions and `h_C3` along
   that trajectory;
3. test basis enlargement before treating the minimal point as robust;
4. append the already defined MTS motion-sector Hessian and recalculate the
   common zero, index and trajectory.

This is the first point at which trajectory integration is preferable to
another source-completion ledger: there are no exact source blocks left in
the declared minimal system.

## 10. Reproducible artifacts

- `scripts/Y5_R2FR_4934_c3_photon_projection_selection.py`.
- `scripts/Y5_R2FR_4934_portal_linear_c3_zero.py`.
- `scripts/Y5_R2FR_4934_portal_quadratic_c3.py`.
- `scripts/Y5_R2FR_4934_direct_c3_cff_principal.py`.
- `scripts/Y5_R2FR_4934_completed_combined_flow.py`.
- `source-intake/functional_rg/4934/c3_photon_projection_selection_results.json`:
  SHA-256 `ab925e077ca13913127105bf3619604e022dd57305f9b5cb4cbe053760eabc01`.
- `source-intake/functional_rg/4934/portal_linear_c3_zero_results.json`:
  SHA-256 `f0f30c1233d36d47a92655dd0023918f978d5a76056ffd196a378cdb3156c002`.
- `source-intake/functional_rg/4934/portal_quadratic_c3_results.json`:
  SHA-256 `a939bf7f1464dc58cd61ea69f907d4d3bb29dd2b8aec36fa51c2ffbaa15ec574`.
- `source-intake/functional_rg/4934/direct_c3_cff_principal_results.json`:
  SHA-256 `00c2c4ed4a2ece0611a6b167e885a9811b8748cace0a456337ac03e426034a95`.
- `source-intake/functional_rg/4934/completed_combined_flow_results.json`:
  SHA-256 `c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978`.

