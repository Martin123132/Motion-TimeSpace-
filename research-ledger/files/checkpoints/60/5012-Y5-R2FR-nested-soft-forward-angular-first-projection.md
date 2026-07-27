# 5012 — nested soft-forward angular-first projection

## Result

Checkpoint 5011 did not reveal a physical high-spin mismatch. It used an invalid order of limits. The exact Luna denominators satisfy

```text
q2^2 = q1^2 - 2 k.q1,
```

so a fixed-angle expansion around soft graviton momentum `k=0` requires

```text
|2 k.q1 / q1^2| << 1.
```

That condition fails arbitrarily close to the forward surface `q1^2=0` for every nonzero graviton energy. The fixed-angle soft coefficient used in 5011 was therefore subtracted outside its domain of validity.

## Exact residue theorem

Writing `r=q1^2`, `v=q2^2`, `a=p1.p2`, `b=p1.q2`, `c=p2.q1`, `E_i=epsilon.p_i`, and `Q=epsilon.q1`, the two Laurent residues of one Luna pairing factor into perfect squares. Their iterated overlap is

```text
64 (E1 c - E2 b - Q a)^2
```

from either order. On a real finite-energy collinear boundary, `q1=lambda p1`, the on-shell identities give `c=lambda a`, `Q=lambda E1`, and `v=-2 lambda b`; the complete `q1` residue numerator vanishes exactly. The `q2` residue vanishes by the exchanged identities. The executable full Bose amplitude confirms

```text
|q1^2 M5| proportional to angle^p,
p = 1.98752 ... 1.9972,
```

while `M5` itself approaches a finite value at each tested nonzero energy. The forward pole appears only after the soft limit coalesces the two transfer denominators. This proves that the soft and forward limits do not commute.

## Correct ordering

The legal distributional object is

```text
G_J(x) = integral dOmega P_J(z) g(x,Omega),
G_J(0) = lim_(x->0+) G_J(x),
I_J = integral_0^1 dx [G_J(x)-G_J(0)]/x.
```

It is not legal to interchange the angular integral and the pointwise soft subtraction because the fixed-angle coefficient is not dominated by an integrable angular function. The first fixed-energy angular scan gives

| J | raw angular-first smoke | RQMC error | window shift | exact 4988-matched G_J(0) |
|---:|---:|---:|---:|---:|
| 0 | 25.229567 | 0.802 | 0.258 | `3521/1080` (3.2601852) |
| 2 | 8.1648071 | 0.669 | 0.16 | `14597/27000` (0.54062963) |
| 4 | 3.7237977 | 0.833 | 0.162 | `569/15120` (0.037632275) |
| 6 | 1.7705145 | 0.926 | 0.0363 | `9103/1134000` (0.0080273369) |
| 8 | 0.95100913 | 0.82 | 0.0642 | `33353/12474000` (0.0026738015) |

The raw values are finite endpoint smoke fits using the basis `1 + x log(x) + x`; they are deliberately not used as UV coefficients.

## Crossed-helicity projector

The `phi phi h` unitarity sum is not the same-polarization product used in the first 5010/5011 implementation. The physical contraction is

```text
(1/2!) sum_h M_L(h) M_R(-h)
             = (1/2!) sum_h M_L(epsilon_h) M_R(epsilon_h^*).
```

This equals the covariant graviton projector pointwise. With all hard momenta outgoing, the regulated soft-direction integral reduces after momentum conservation cancels the logarithmic regulator to

```text
<sum_h S_L(h) S_R(-h)>_k
    = -sum_ij e_i e_j d_ij log(d_ij),
d_ij = 1 - n_i.n_j.
```

For beam direction `b`, external direction `m`, and hard cut direction `n`, define `A=b.n`, `B=m.n`, `z=b.m`, and

```text
S(c) = (1-c) log(1-c) + (1+c) log(1+c).
```

The exact endpoint kernel is therefore

```text
gbar_0(A,B,z) = f(A) f(B) [S(z)-S(A)-S(B)+2 log(2)].
```

In the 4988 subtraction scheme, `f(c)=-(7+c^2)/4` has only `a_0=-11/6` and `a_2=-1/30`. The spherical convolution theorem then gives the exact matched endpoint

```text
G_0(z) = [S(z)+2 log(2)] [a_0^2+5 a_2^2 P_2(z)]
         -2 [a_0 h_0+5 a_2 h_2 P_2(z)],
h_J = (1/2) integral_-1^1 dc P_J(c) f(c) S(c).
```

All `log(2)` terms cancel from every projected mode shown in the last table column. These rational values close the endpoint in the same forward-subtraction scheme as checkpoint 4988; the raw RQMC column remains only an independent finite-energy diagnostic.

## Status

- Exact Luna Laurent residues and overlap equality: **derived**.
- Real finite-energy forward residue: **proved zero and checked numerically**.
- Pointwise soft-plus estimator from checkpoint 5011: **rejected**.
- Angular-first replacement and endpoint sequence: **constructed and executed**.
- Crossed-helicity projector and exact soft-direction average: **derived**.
- Exact 4988-matched endpoint modes: **derived**.
- Finite-`x` matched kernel, integrated `x` plus, virtual-real match, high-spin cancellation, and outer UV projection: **open**.
- Local GR and full MTS: **not claimed**.

Next: construct the finite-`x` real kernel in the same 4988 forward scheme, integrate `[G_J(x)-G_J(0)]/x`, and only then compare the result with the exact 4988/5008 virtual modes.
