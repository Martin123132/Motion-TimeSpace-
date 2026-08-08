# 4979 - Massless scalar common-scheme finite determinant and TT match

Formal marker: `PPC4161_MASSLESS_SCALAR_COMMON_SCHEME_FINITE_TT_4979`.

## Decision

Checkpoint 4979 makes the finite direct-determinant comparison real rather
than inferring it from the ultraviolet logarithm. It derives the exact
massless scalar triangle integrand, performs the Feynman-parameter integral
in a declared MS-bar convention, fixes the conversion to the acquired
Barvinsky--Vilkovisky source convention from an independent two-point
calculation, and obtains an unfitted finite match on four new
transverse-traceless metric geometries.

The result is deliberately split:

```text
exact direct massless triangle integrand                 = derived;
universal pole and finite radial moments                 = derived;
two-point source/MS-bar scheme map                       = derived;
four unseen transverse-traceless finite TTT controls     = matched;
generic traceful finite contact                          = open;
complete traceful finite determinant match               = false;
interacting motion/graviton/ghost result                 = false;
full MTS                                                  = false.
```

The remaining generic traceful discrepancy is not present in the TT sector.
It changes under the evanescent continuation of the four-dimensional metric
and is therefore assigned to the trace-Ward/Gauss--Bonnet contact completion,
not to the already matched nonlocal TT kernel.

## 1. Exact determinant response

For a massless real scalar written in terms of the densitized inverse metric

```text
H^{mu nu}=sqrt(g) g^{mu nu},
A[H]=-partial_mu H^{mu nu} partial_nu,
W=(1/2) Tr log A,
```

the linear metric vertex carrying momentum `q` is

```text
V_h(p+q,p)=(p+q)_mu h^{mu nu}p_nu.
```

Because the massless operator is linear in `H`, the four-dimensional mixed
third response contains the two cyclic triangle orientations only:

```text
W_123=(1/2) integral_p [
 G(p)G(p+q3)G(p-q1)
 V3(p+q3,p)V2(p-q1,p+q3)V1(p,p-q1)
 +(2 <-> 3)].
```

The exact integrand agrees with the independently implemented order-six
continuum Taylor engine from checkpoint 4912 at relative residual
`3.5713232140706105e-16` over 96 loop momenta and two external scales. The
propagator inverse residual is `1.1102230246251565e-16`.

## 2. Feynman parameters and finite subtraction

For denominator shifts `s_i`, introduce simplex coordinates `alpha_i`,

```text
Q=sum_i alpha_i s_i,
Delta=sum_i alpha_i s_i^2-Q^2 > 0,
p=l-Q.
```

After rotational averaging, the numerator is

```text
<N>=E0+E1 l^2/[d]+E2 l^4/[d(d+2)]+E3 l^6/[d(d+2)(d+4)],
```

where the `E_k` are the corresponding Gaussian moments of the shifted vertex
product. With `d=4-2 epsilon`, subtraction of
`1/epsilon+log(4 pi)-EulerGamma` gives, per orientation and before the common
factor `(4 pi)^-2`,

```text
k=0: E0/(2 Delta),
k=1: E1/4 log(mu^2/Delta),
k=2: E2 Delta/8 [log(Delta/mu^2)-1],
k=3: E3 Delta^2/32 [log(mu^2/Delta)+3/2].
```

The respective pole coefficients are

```text
0, E1/4, -E2 Delta/8, E3 Delta^2/32.
```

The sharp ultraviolet shell is exactly twice the dimensional pole because
`d=4-2 epsilon`. This reproduces the checkpoint-4978 direct `q^4` residue and
removes the previous ambiguity about which finite constants accompany it.

## 3. Independent two-point scheme map

The same loop prescription was projected onto 48 independent two-point
sources. Covariant continuation through a flat evanescent block restores the
linear Ward identity and gives the exact direct-`W` coefficients

```text
W_MSbar^(2)=(4 pi)^-2 integral [
 Ricci ( +(1/60)log(-Box/mu^2) -23/450 ) Ricci
 +R    ( +(1/120)log(-Box/mu^2) -1/1800 ) R ].
```

The numerical projection has residual `9.485687728000913e-12`; its four
coefficients differ from the exact rationals by at most
`1.3564169318996955e-10` relatively.

The acquired source tabulates `-W`, not `W`. Its convention is fixed without
using any three-point geometry:

```text
(-W)_source = UV_shell - W_MSbar.
```

At quadratic order the shell local coefficients are `-1/30` for `Ricci^2`
and `-1/60` for `R^2`. The identity therefore reconstructs exactly

```text
Ricci: -(1/60)log(-Box/mu^2) +4/225,
R:     -(1/120)log(-Box/mu^2) -29/1800,
```

which are the source coefficients used in checkpoints 4977 and 4978. No
G03/G04 coefficient is fitted in this conversion.

## 4. Unseen transverse-traceless comparison

Four new metric triples were generated after the source and direct engines
were fixed. Every polarization satisfies

```text
q_mu h^{mu nu}=0,
tr(h)=0,
```

to at most `1.163e-16`. The comparison target is fixed by the two-point map:

```text
W_MSbar,target = UV_shell - (-W)_source.
```

| geometry | direct `W_MSbar` | fixed target | absolute residual |
|---|---:|---:|---:|
| TT00 | `-2.246546451552404e-05` | `-2.2465464515380346e-05` | `1.4369405730400853e-16` |
| TT01 | `+6.714484556092753e-05` | `+6.714484556116605e-05` | `2.38524477946811e-16` |
| TT02 | `+1.1116750733103686e-04` | `+1.1116750733244353e-04` | `1.4066710036370056e-15` |
| TT03 | `-2.2834827462411813e-06` | `-2.2834827463653424e-06` | `1.2416105402385073e-16` |

The maximum relative residual is `5.4373545944886145e-11`; the maximum
absolute residual is `1.4066710036370056e-15`. This is an independent finite
determinant match of the complete massless scalar TT three-point kernel, not
only its ultraviolet logarithm.

The low/high simplex-order difference is at most `8.365408445541949e-10`.
The `mu -> 2 mu` Ward identity holds to `7.369754340563324e-15`, common
momentum-and-`mu` scaling to `2.3094588435705593e-15`, and the independently
computed TT ultraviolet shell to `2.3944337905989737e-15`.

## 5. Generic traceful audit

The same calculation was applied to the original traceful controls. The
four-dimensional and product-metric continuations differ, proving that a
finite continuation choice is active:

| geometry | fixed direct target | product-continuation direct result | relative mismatch |
|---|---:|---:|---:|
| G03 | `+4.018630738550688e-05` | `+3.478824754266967e-05` | `0.1343258486293271` |
| G04 | `-1.21874608583716e-04` | `-1.1743215563280749e-04` | `0.03645101307428589` |

For G03 the product continuation contains triangle and pair-contact
evanescent pieces `-1.2923955988977403e-05` and
`+1.1086497703595222e-05`; for G04 they are
`+2.096079454345868e-05` and `+2.111197259300408e-05`. They are individually
large enough that dropping them is not a valid prescription.

Because all four TT rows match while the traceful rows depend on continuation,
the remaining target is narrow: derive the trace Ward completion and the
finite remnant of the dimensionally continued Gauss--Bonnet constraint. A
geometry-specific finite fit is prohibited.

## 6. Scope and next target

The runner passes `16/16` internal gates and the independent validator passes
`63/63`. This checkpoint promotes

```text
valid_for_exact_massless_triangle_integrand=true,
valid_for_two_point_common_scheme_map=true,
valid_for_TT_common_scheme_finite_determinant_match=true.
```

It retains

```text
valid_for_complete_traceful_common_scheme_finite_determinant_match=false,
valid_for_full_MTS_claim=false.
```

Next target:
`4980-Y5-R2FR-trace-Ward-and-evanescent-Gauss-Bonnet-contact-completion-or-trace-sector-demotion.md`.

Construct the trace/longitudinal Ward completion from the already derived
two-point kernel and the scalar type-A anomaly. It must predict G03 and G04
with one source-owned prescription and then pass new traceful geometries. If
that cannot be done, retain the exact TT kernel and demote only the generic
trace-contact comparison; do not disturb the matched TT or local-GR branches.

No GitHub action.
