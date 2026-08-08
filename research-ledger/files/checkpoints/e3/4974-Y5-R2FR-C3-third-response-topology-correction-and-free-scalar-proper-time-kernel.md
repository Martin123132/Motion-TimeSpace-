# 4974 - C3 third-response topology correction and free-scalar proper-time kernel

Marker: `MTS_4974_C3_THREE_RESPONSE_AND_SCALAR_PT_KERNEL`

Formal marker: `PPC4161_C3_THREE_RESPONSE_AND_SCALAR_PT_KERNEL_4974`

## Decision

Checkpoint 4973 correctly derived the `C3` form-factor characteristic, but
its proposed fluctuation-kernel topology was one derivative short. The
displayed `Gamma^(4)` tadpole plus `Gamma^(3)-Gamma^(3)` diagram in the
acquired source is explicitly the **second** metric derivative used for
curvature-squared form factors. A Weyl-cubic operator starts at third order
in the metric perturbation and therefore requires the **third** response.

The corrected `C3` kernel contains:

```text
one Gamma^(5) contact,
Gamma^(3)-Gamma^(4) mixed terms,
Gamma^(3)-Gamma^(3)-Gamma^(3) triangle terms.
```

This is not only a bookkeeping correction. The already validated 4912 scalar
determinant implements the complete one-loop `1+3+2` version of this
topology. Using its exact local coefficient and the source-locked
proper-time `m=3` regulator gives the first regulator-resolved parent kernel
row:

```text
d_t zeta_scalar(k)
  =-162 C0 k^6/(m^2+3k^2)^4,

C0=1/[30240(4 pi)^2].
```

It vanishes at both RG endpoints but integrates exactly from the ultraviolet
to the infrared to

```text
zeta_scalar(0)-zeta_scalar(infinity)=C0/m^2.
```

Thus the endpoint-silent direction proved in 4973 is real, but it is no
longer arbitrary in this free-scalar sector: the Hessian and regulator fix
its full local threshold profile and finite integral.

This does **not** close the full parent kernel. The graviton and ghost
`Gamma^(3/4/5)` contractions, interacting motion contacts, finite external
momentum dependence, and common-scheme four-graviton match remain open.

## 1. Why the previous topology was insufficient

Let

```text
A=Gamma^(2),
G=A^(-1),
A_i=delta_i A=Gamma^(3)_i,
A_ij=delta_i delta_j A=Gamma^(4)_ij,
A_123=delta_1 delta_2 delta_3 A=Gamma^(5)_123.
```

The source equation used in 4973 was quoted from a calculation of

```text
delta^2 Tr exp[-s A]/(delta h delta h).
```

It therefore contains only the two-response classes `Gamma4` and
`Gamma3-Gamma3`. It is sufficient for `R f(Box) R`, whose flat expansion
begins at `h^2`, but not for `C^3`, whose flat expansion begins at `h^3`.

The exact one-loop determinant identity is

```text
delta_123 [1/2 Tr ln A]
 =1/2 Tr[
      G A_123
     -G A_1 G A_23
     -G A_2 G A_13
     -G A_3 G A_12
     +G A_1 G A_2 G A_3
     +G A_1 G A_3 G A_2].
```

It has one `Gamma5` contact, three mixed terms, and two triangle
orientations. This is exactly the determinant formula independently tested
in checkpoint 4912, including the traceful measure contacts.

For an exact Wetterich trace with a field-independent regulator insertion,

```text
Tr[G dotR],
```

three functional derivatives produce thirteen ordered terms:

```text
1 Gamma5 contact,
6 Gamma3-Gamma4 terms,
6 Gamma3-Gamma3-Gamma3 terms.
```

Their coefficient sums are `-1`, `+6`, and `-6`, respectively, before the
overall supertrace factor. The executable differentiates the noncommuting
trace words rather than entering these counts by hand.

## 2. Locked benchmark branch

The first calculation uses one internally consistent branch:

```text
metric split       : g_mn=gbar_mn+h_mn;
gravity gauge      : alpha=1, omega_bar=1/2;
regulator          : proper-time rho_m, m=3;
form-factor scheme : epsilon=1;
scalar benchmark   : one real massive pole, eta_psi=0;
scalar Hessian     : Gamma_psi^(2)=Z_psi(-Box+m^2).
```

The metric split, gauge, ghost operator, and regulator are source locked to
the acquired 2605.29159 package. The scalar metric contacts and determinant
normalization are locked to checkpoints 4911-4912. The free pole is a
benchmark contained in, but not equal to, the interacting MTS motion sector.

## 3. Exact proper-time scalar kernel

For

```text
Gamma_1loop(M^2)=1/2 Tr ln(Delta+M^2),
M_k^2=m^2+3k^2,
```

the `m=3`, `eta_psi=0` proper-time trace obeys

```text
d_t Gamma_k
 =(3k^2)^3 partial_(M^2)^3 Gamma_1loop(M^2)
   evaluated at M^2=M_k^2.
```

The order of the mass and metric derivatives can be interchanged. The exact
4912 local scalar coefficient is

```text
zeta_1loop(M^2)=C0/M^2,
C0=1/[30240(4 pi)^2]
  =2.0941051513379998e-7.
```

Therefore

```text
d_t zeta_scalar(k)
  =(3k^2)^3 partial_(M^2)^3(C0/M^2)
  =-162 C0 k^6/(m^2+3k^2)^4.
```

With

```text
x=3k^2/m^2,
```

the dimensionless profile is

```text
(m^2/C0)d_t zeta_scalar=-6x^3/(1+x)^4.
```

Its positive ultraviolet-to-infrared integration weight is

```text
w(x)=-[d_t zeta_scalar m^2/C0]/(2x)
    =3x^2/(1+x)^4.
```

The integral and cumulative fraction are exact:

```text
integral_0^infinity w(x) dx=1,

integral_0^x w(v) dv=[x/(1+x)]^3.
```

The flow magnitude peaks at `x=3`, or `k=m`, with normalized value
`-81/128`. Half of the integrated coefficient is accumulated by
`x=3.847322101863074`.

The runner independently evaluates the improper integral as
`0.9999999999999999`.

## 4. Endpoint tests

The local scalar kernel has the exact limits

```text
x -> 0       : (m^2/C0)d_t zeta=-6x^3+O(x^4),
x -> infinity: (m^2/C0)d_t zeta=-6/x+O(x^-2).
```

It therefore vanishes at both endpoints while retaining a nonzero finite
integral. This gives a concrete, derived realization of the kind of interior
information that the 4973 null-family theorem proved could not be recovered
from endpoints alone.

The massive local limit does not test the 4972 massless physical logarithm.
The limits are nonuniform: `zeta=C0/m^2` diverges if the local expansion is
taken before `m -> 0`. A finite-external-momentum calculation must be made
before the massless limit. No logarithmic endpoint is inferred from this
local threshold.

## 5. Helicity projection

Applying the exact local `C3` operator projectors at the declared symmetric
point gives

```text
P_pppp=-15,
P_mppp=-3/2,
P_pppp/P_mppp=10.
```

Every sampled scalar-kernel row preserves the factor-ten identity exactly.
This validates the local operator normalization. It is not an independent
finite four-graviton form-factor calculation: a complete `2 -> 2` amplitude
also requires the independent quartic-curvature form-factor sector.

## 6. What moved and what remains

```text
4973 two-response topology for C3          = superseded;
correct C3 response order                  = derived;
one-loop determinant 1+3+2 topology        = exact;
exact Wetterich ordered 1+6+6 topology     = exact;
free-scalar PT-m3 local kernel              = calculated;
free-scalar finite C3 threshold             = integrated exactly;
local helicity factor-ten check             = pass;
interacting motion contacts                 = open;
graviton Gamma3/Gamma4/Gamma5 contractions  = open;
ghost third-response contacts               = open;
finite external-momentum scalar projection  = open;
physical logarithmic endpoint from 4974     = not claimed;
full delta_c_fin                            = open;
exact all-operator compact GR               = false;
full MTS                                    = false.
```

The result is a genuine first kernel row, not another list of missing
coefficients. It also changes the next calculation: building only
`Gamma^(3)` and `Gamma^(4)` cannot close `C3`; `Gamma^(5)` is compulsory.

## 7. Next calculation

Checkpoint 4975 should apply the same proper-time mass-derivative operator to
the finite-external-momentum 4912 scalar determinant response. It must retain
the complete off-shell quotient, report leakage outside the local rank-eight
image, and take the massless limit only after momentum projection. In
parallel, the pure gravity/ghost branch must derive the locked-gauge
`Gamma^(3/4/5)` contacts rather than the superseded two-response kernel.

No GitHub action or public claim is authorized.

## Outputs

- `post-checkpoint-work/scripts/Y5_R2FR_4974_C3_three_response_topology_and_scalar_PT_kernel.py`
- `post-checkpoint-work/source-intake/functional_rg/4974/C3_parent_scheme_lock.csv`
- `post-checkpoint-work/source-intake/functional_rg/4974/C3_three_response_topology.csv`
- `post-checkpoint-work/source-intake/functional_rg/4974/C3_scalar_PT_m3_local_kernel.csv`
- `post-checkpoint-work/source-intake/functional_rg/4974/C3_scalar_PT_m3_helicity_projection.csv`
- `post-checkpoint-work/source-intake/functional_rg/4974/C3_kernel_sector_coverage.csv`
- `post-checkpoint-work/source-intake/functional_rg/4974/C3_three_response_topology_and_scalar_PT_kernel_results.json`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4974_VALIDATION.csv`

The runner passes `28/28` internal checks. The independent validator passes
`22/22`; validation CSV SHA256 is
`7b612b3cbf282c092060cc47f51c42bfcfc6524c6c2e0954ed552c4cd318064f`.
