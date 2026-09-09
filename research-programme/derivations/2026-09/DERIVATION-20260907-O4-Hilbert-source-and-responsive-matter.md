# O4: derive the gravitational source, not only the scalar kinetic coefficient

2026-09-07. Private continuation. D4/5513 retains numerical ownership.

## Result and scope

The selected parent already contains `-u_O4 C^2 X`. Its full quadratic
Hilbert stress, a derivative-controlled local bound, its third-harmonic
metric contribution and the corresponding driven material equations are
derived below. These extend the validated canonical coupled reference;
they do not assert that its O4 extension has already been numerically solved.

The new source is not obtained by replacing `1` with `K_0(r)` in a
canonical stress tensor. That replacement fails both the trace and the
source-exchange identity. The variational correction repairs the identity
without an extra gravitational charge or a fitted material response.

## 1. Parent, sign and known limits

Use four dimensions, signature `(-,+,+,+)`, Levi-Civita connection and
`R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb+...`. Write

```text
X=g^ab v_a v_b, v_a=nabla_a chi, W=C_abcd C^abcd,
S4=-u integral sqrt(-g) W X, u=u_O4,
L_chi=-X/2-m^2 chi^2/2-u W X+c2 X^2+... .
```

This sign is owned by 5203/5211, not by the Euclidean projector convention.
The dimensionful canonical coefficient has dimensions length^4. The
5191 source pack supplies a historical infrared envelope
`|u|<=2.2672938165363195e-139 m^4`. It is used below only with that source
and regime qualification, not as a new fitted number or an all-scale bound.
The canonical scalar equation is

```text
E_chi=nabla_a[(1+2uW-4c2X+...)v^a]-m^2 chi.
```

The exact `chi=0` consistent truncation of 5211 survives. None of the
following supplies its actual preparation or eliminates other parent operators.

## 2. Vary the curvature and the metric inside X

First hold a scalar multiplier `F` independent of the metric and define
`delta integral sqrt(-g) F W=integral sqrt(-g) E_ab[F] delta g^ab`,
up to the displayed variational boundary class. The curvature derivative
is `P^abcd=2F C^abcd`. The metric equation is

```text
E_ab[F]=2F C_a^cde R_bcde
         -4 nabla^c nabla^d(F C_acdb)-g_ab F W/2
       =4 nabla^c nabla^d(F C_acbd)+2F R^cd C_acbd .
```

The second line uses the four-dimensional Weyl contraction identity.
Its constant-F limit is `E_ab[F]=4F Bach_ab`, where
`Bach_ab=(nabla^c nabla^d+R^cd/2)C_acbd`.
The curvature variation follows the covariant variational construction of
[Iyer and Wald](https://arxiv.org/pdf/gr-qc/9403028), equations 31–33.
The sign and factor four in the constant multiplier limit independently
agree with equation 2 of
[Lu, Perkins, Pope and Stelle](https://arxiv.org/pdf/1502.01028).
These are established variational tools, not new MTS discoveries.

Now substitute `F=X` and also vary `X`: `delta X=v_a v_b delta g^ab`.
The full retained contribution to the universal Hilbert source is

```text
T4_ab=2u[W v_a v_b+E_ab[X]]
     =2u W v_a v_b
       +8u nabla^c nabla^d(X C_acbd)
       +4u X R^cd C_acbd.                                  (1)
```

Its trace and diffeomorphism identities are

```text
g^ab T4_ab=2u W X,
nabla^a E_ab[F]=-W nabla_b F/2,
nabla^a T4_ab=2u nabla_a(W v^a) v_b.                       (2)
```

The last follows by using `nabla_b X=2v^a nabla_a v_b`. Adding the
canonical scalar stress gives `nabla^a Tchi_ab=E_chi v_b` at quadratic
order. Thus the same scalar equation and the same Einstein source conserve
energy-momentum together. No independent source coefficient is needed.

By contrast, treating W as a fixed external coefficient would give
`T4,frozen_ab=2u W v_a v_b-u g_ab W X`. Its trace is `-2uWX`, and its
divergence contains the unwanted term `-uX nabla_b W`. The difference
is physical curvature variation, not an optional convention.

## 3. Explicit exterior stress and a clean local bound

On a Ricci-flat background the Weyl divergences and Bach tensor vanish, so

```text
T4_ab=2u W v_a v_b+8u C_acbd nabla^c nabla^d X.             (3)
```

For Schwarzschild `f=1-2mu/r`, let `e=mu/r^3`. In a static orthonormal
frame `C_0r0r=-2e`, `C_0theta0theta=e`,
`C_rtheta rtheta=-e`, `C_theta phi theta phi=2e`, and `W=48e^2`.
For the off-shell fixture `chi=q t+phi(r)`, set

```text
X=-q^2/f+f phi'^2,
H00=-mu X'/r^2,
Hrr=f X''+mu X'/r^2,
Hperp=f X'/r.

rho4=2u W q^2/f+16u e(Hperp-Hrr),
pr4=2u W f phi'^2-16u e(H00+Hperp),
pt4=8u e(H00-Hrr+2Hperp),
T4^r_t=2u W f q phi'.                                    (4)
```

Independent arbitrary compactly supported radial variations of the original
spherical action supply rho4 and pr4, without using (3). They provide a
strong sign/normalization test of the covariant result. The radial and
temporal Ward identities can also be tested off shell; no field solution
is fitted to make them hold.

More generally, define positive Euclidean/Frobenius norms of tensor
components in one specified orthonormal frame:
`V=||nabla chi||`, `H=||nabla nabla chi||`,
`J=||nabla nabla nabla chi||`, `C0=||C||`,
`D1=||nabla^d C_acbd||`, `D2=||nabla^c C_acbd||`,
and `B0=||Bach||`. Expanding the derivatives in (1) and using
Cauchy–Schwarz gives the pointwise bound

```text
||T4|| <= 2|u||W| V^2
 +8|u|[2C0(H^2+VJ)+2(D1+D2)VH+B0 V^2].                 (5)
```

Lorentz raising changes signs but not these positive component norms.
The definitions use the actual contracted divergences, avoiding a hidden
partial-trace factor in a norm of the unrestricted second curvature jet.
On Schwarzschild, `C0=sqrt(48)|mu|/r^3`, hence

```text
||T4|| <= 96|u|mu^2 V^2/r^6
             +64sqrt(3)|u||mu|(H^2+VJ)/r^3.               (6)
```

If the actual local jets obey `H<=k_j V`, `J<=k_j^2 V`, then

```text
||T4||/V^2 <= 96|u|mu^2/r^6
                    +128sqrt(3)|u||mu|k_j^2/r^3.         (7)
```

At V=0, (6), not the divided expression, applies. No bound on H follows
from V=0 at a point. In particular K0 positivity or a small `2uW` is not
alone a stress bound: the curvature-times-frequency-squared term also
matters. This is a conditional bound on an actual retained source, not a
measured PPN residual, an occupation bound or a universal preparation law.
Static-frame benchmark evaluation excludes an exact horizon.

## 4. Responsive matter: replace the source, not its conservation laws

### Local spherical source formulas, including the material interior

The covariant expression can be reduced without a four-index numerical
curvature differentiation. On a static spherical background let
`A_r=N a r^2`, and use Q from section 5. For an arbitrary spherical
scalar, `T=chi_t^2/N^2`, `S=f chi_r^2`, `X=S-T`, define

```text
V_Q=-(8/3)u A_r Q X,
U=V_Q f(2nu'-lambda'-1/r)-(V_Q f)'.

rho4=uW(T+S)+U'/A_r,
pr4=uW(T+S)
     -[2V_Q(Q+1/r^2)+(V_Q f(1/r-nu'))'
                                      +partial_t^2(V_Q/N^2)]/A_r,
j4=T4^r_t=2u f W chi_t chi_r+partial_t U/A_r.             (8a)
```

To derive the first two lines vary the reduced action with arbitrary
compactly supported lapse and radial-metric variations n and b. Its
coefficients of `n'`, `n''`, `b'`, `b_tt` are respectively
`V_Q f(2nu'-lambda'-1/r)`, `V_Q f`,
`V_Q f(1/r-nu')`, and `-V_Q/N^2`.
The Euler derivatives then give `delta S4/(4pi delta n)=-A_r rho4`
and `delta S4/(4pi delta b)=A_r pr4`.
The full covariant temporal Ward identity supplies the displayed local
flux: its improvement is `partial_t U/A_r`. Regular-center locality fixes
the otherwise conserved radial integration term, with no added source charge.
On an exterior patch use the covariant expression or inherit this flux
from the matched interior, not an arbitrary additional flux constant.

For `chi=A phi cos(omega t)`, the coefficients of cos(2omega t) are
`T_2=-omega^2 phi^2/(2N^2)`, `S_2=f phi'^2/2`,
`X_2=S_2-T_2`. Compute `V_Q,2` and `U_2` by the same radial
formulas. In the radial pressure replace
`partial_t^2(V_Q/N^2)` by `-sigma^2 V_Q,2/N^2`; the flux coefficient
of sin(2omega t) is

```text
j4,2=-u omega f W phi phi'-sigma U_2/A_r.
B_s=pi G_N r K0 phi phi'+4pi G_N r U_2/(A_r f).          (8b)
```

These are explicit interior source functions, not unknown stress symbols.
Their background derivatives retain the surface contribution of section 6.
They provide a direct implementation route for (9), and are independently
checked against the covariant Schwarzschild tensor with time dependence.

Let `tau_ab=Tcanonical_ab+T4_ab` be evaluated at order A^2 on the GR
background with the scalar satisfying the K0-modified linear equation.
Write its mixed radial energy flux as `tau^r_t=j_tau(r)sin(sigma t)`,
energy density as `rho_tau(r)cos(sigma t)` and radial pressure as
`p_tau(r)cos(sigma t)`, with `sigma=2omega`. Static terms are handled
separately. Conservation gives

```text
(N a r^2 j_tau)'=-sigma N a r^2 rho_tau,
mu_s=-4pi G_N r^2 j_tau/sigma,
B_s=mu_s/(r f)=-4pi G_N r j_tau/(sigma f),
mu_s'=4pi G_N r^2(rho_tau-h B_s),
h=rho_matter+p_matter.                                  (8)
```

For the canonical source this reproduces `B_s=pi G_N r phi phi'`.
The full O4 source changes j_tau and p_tau, but does not change the
minimally coupled material continuity/Euler equations. With
`J_m=4pi G_N r h/f`, the explicitly forced system remains

```text
xi'=(nu'-2/r)xi-P/(h c_s^2)-B_s,
P'=h[sigma^2/(fN^2)+nu'^2+4nu'/r-8pi G_N p_matter/f]xi
   -(nu'+J_m)P-h[(nu'+1/r)B_s+4pi G_N r p_tau/f],
B=-J_m xi+B_s,
C'=(2nu'+1/r)B+4pi G_N r(delta p+p_tau)/f.                (9)
```

Here B and C are radial-metric and lapse harmonics, not the Bach tensor.
Equation (8) supplies the Hamiltonian constraint exactly when combined
with material continuity. It cannot be replaced by a separately fitted
mass response.

## 5. Full retained cubic metric forcing, including delta K

For the polar metric define `nu=ln N`, `lambda=ln a`, `f=a^-2`.
On a static spherical background,

```text
Q=f[nu''+nu'^2-nu'lambda'-nu'/r+lambda'/r]-(1-f)/r^2,
W=4Q^2/3.
```

Perturb `nu -> nu+A^2 C cos(sigma t)`,
`lambda -> lambda+A^2 B cos(sigma t)`. Direct spherical curvature
variation, including the time acceleration of a, gives

```text
delta Q=f[C''+(2nu'-lambda'-1/r)C'+(1/r-nu')B']
          -2B(Q+1/r^2)+sigma^2 B/N^2,
delta W=8Q delta Q/3,
K0=1+2uW, D=delta K/K0=2u delta W/K0.                    (10)
```

The `sigma^2 B/N^2` term is lost by varying a static curvature formula
as if the metric response itself were static. The order-A^3 third-harmonic
source in the scalar equation `chi_tt+L chi=...` is

```text
s_g,3=[-2omega^2 C+(2omega^2-N^2m^2/K0)B
              +(omega^2+N^2m^2/(2K0))D]phi
        +N^2 f(C'-B'+D')phi'/2.                         (11)
```

It follows by varying `(sqrt(-g))^-1 partial_mu(sqrt(-g)K g^munu
partial_nu chi)` and projecting the harmonic, not by guessing a modified
lapse force. At u=0 it reduces to the previously checked canonical source.
Add the separately derived contact source before taking the outgoing norm.

At first order in the Wilson expansion, retain phi/omega/B/C corrections
at order u, but use the leading metric in the explicitly u-weighted delta W.
For an isolated normalized bound eigenmode the eigenvalue derivative is

```text
d omega^2/du = 8pi integral W[
 N r^2 phi'^2/a-omega^2 a r^2 phi^2/N]dr.                 (12)
```

This is the derivative of the generalized quadratic form including its
u-dependent norm. Eigenfunction corrections belong to the same eigenproblem.
Solving a finite higher-derivative action as an exact UV theory is not
licensed: 5191's order-reduction/ghost caveat remains. At this quadratic
amplitude order about chi=0, however, T4 is a prescribed source on the
background; it does not introduce an extra metric operator acting on B/C.

## 6. The gamma-two reference surface cannot be silently reused

For a spherical perfect-fluid GR background the electric Weyl scalar is
`e=mu/r^3-4pi G_N rho/3`. The previous gamma-two star has
`rho~constant*(R-r)` at its vacuum boundary. Consequently e is continuous
but its normal derivative jumps. If X and its first derivative are
continuous, equation (1) contains the surface stress

```text
T4_ab|surface=8u n^c n^d[nabla_n(X C_acbd)] delta_Sigma.  (13)
```

The jump is outside minus inside, and delta_Sigma is normalized in proper
normal distance. In a continuous orthonormal frame,
`[nabla_n e]=sqrt(f_s)4pi G_N rho'_inside/3`. Thus its tangential
surface components are `S00=-16u X[nabla_n e]`,
`Stheta theta=Sphi phi=-8u X[nabla_n e]`; the normal components vanish
and its trace is zero. This is the singular part of the derived source,
not an independently fitted shell. An exact thin-interface extension would
have to retain the corresponding perturbative metric junction conditions.
The simplified components assume continuous X and its normal derivative.
At first Wilson order they use the leading canonical scalar jets. If the
K0-corrected scalar develops a jump in the derivative of X, retain the full
jump in (13), rather than retaining only X times the curvature jump.

A smooth material reference is an alternative, but must be declared rather
than silently substituted. A particularly simple causal choice is

```text
P_fluid(Y)=(sqrt(Y)-m_b)^3/(27K^2), sqrt(Y)>m_b,
n=(sqrt(Y)-m_b)^2/(9K^2),
p=K n^(3/2), rho=m_b n+2K n^(3/2),
c_s^2=(3K sqrt(n)/2)/(m_b+3K sqrt(n))<1/2.               (14)
```

Its finite-surface density behaves as `(R-r)^2`, so rho' and the first
Weyl derivative are continuous; (13) is absent if the scalar jets are also
continuous. This does not establish that this EOS is the observed matter
law or that its chosen star is stable. Those remain explicit source and
spectral tests. The previous gamma-two, u=0 reference and all its valid
results are preserved; they were not wrong for their declared scope.

The new fluid solve must also use the corresponding surface condition,
not reuse the gamma-two coefficient. For `p=K n^gamma`, set
`d=1/(gamma-1)` and `s=R-r`. Then `h~h_d s^d`,
`c_s^2~nu'_s s/d`, and regularity gives `P~P_(d+1)s^(d+1)`.
The leading pressure equation in (9) therefore implies

```text
P/(h c_s^2) -> -(V_s xi-F_s)/(gamma nu'_s),
V_s=sigma^2/(f_s N_s^2)+nu_s'^2+4nu'_s/R,
F_s=(nu'_s+1/R)B_s+4pi G_N R p_tau/f_s.                 (15)
```

For gamma=3/2 the coefficient is `2/(3nu'_s)`, versus
`1/(2nu'_s)` in the existing gamma-two code. This asymptotic derivation
prepares the next implementation; its boundary-value convergence test has
not yet been executed for the new EOS.

## Validation and next execution

Implementation: `scripts/parent_O4_hilbert_source_20260907.py`.
It tests independent spherical variation, trace and off-shell Ward identities,
the dynamic curvature and cubic-harmonic algebra, the generalized material
constraint, and the causal surface-regular EOS. It also evaluates (7) using
the sourced historical Wilson envelope and declared benchmark jet bounds.
Those rows are non-claim; they are not measured scalar profiles.

Source ownership includes 5203, 5211, 5191 and the preceding coupled reference.
After D4 record 44 completed, the companion ran sequentially on one core
with BelowNormal priority and **31/31 checks passed**. All symbolic stress
variation residuals are exactly zero, including the time-dependent
Schwarzschild density, pressure, flux and off-shell exchange checks.
The deliberately frozen-curvature stress fails the expected trace/exchange
identities; the test detects that failure rather than accepting the shortcut.
The scalar third harmonic and spherical curvature acceleration term pass
their independent algebraic checks.

The sourced conditional benchmark results for equation (7), taking the
explicit jet bound `k_j=1/r`, are:

| Exterior benchmark | Bound on ||T4||/V^2 |
| --- | ---: |
| Earth surface | 2.123924312459747e-173 |
| Sun surface | 4.55461994857395e-178 |
| One-solar-mass white dwarf surface | 4.416835557830626e-168 |
| 1.4-solar-mass, 12-km neutron-star surface | 4.487762291339712e-154 |

These are conditional norm envelopes, not measured PPN residuals.
The derivative contribution is retained even though it exceeds the
kinetic-coefficient shift. The exact-horizon row is excluded from this
static-frame comparison. No scalar amplitude or derivative history was
inferred from these numbers. The ordinary canonical scalar stress is not
bounded away by demonstrating that the O4 correction is small.

Evidence:
`source-intake/local-preparation/20260907/O4-Hilbert-source-initial.json`,
SHA256 `35a1b3f686f798f22cf16d0106e1e0ade52b2740e6beea60db1923aafbb809ca`.
Executed script SHA256:
`9f715865d317493ef9de1ef9d4a2106b9c607826359068bb8d1768397b5e3226`.
All nine direct source hashes and the sixteen locked 5191 source hashes
match; all 45 historical parent validation rows pass. Compilation/dry-run
passed and no Python cache was written. The main record-44 state remained
`4d2e9d67e7e70a9f119a5351a29944e1616a7aefe4a2eb86db04d030b70f90ca`
throughout the companion run.

Record 44 accepted at `2026-09-07T05:22:30+01:00`, reaching
`217/1/0` with 23/23 main gates passing. Record 45 was launched only after
the new companion and provenance checks completed. No GitHub action or
original-workbench edit was made.

The next coupled solve should implement (8a–8b), (9) and (11), with either
the explicit interface stress or the declared smooth material reference,
rather than adding K0 alone. Its actual O4 profile, nonresonance/stability,
scale evolution and the full preparation history are not proved by this
algebra/conditional-bound pack.
