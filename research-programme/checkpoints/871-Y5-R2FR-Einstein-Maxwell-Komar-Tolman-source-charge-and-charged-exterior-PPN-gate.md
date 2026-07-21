# 4855 Y5 R2FR Einstein-Maxwell source charge and charged-exterior PPN gate

Marker: `EINSTEIN_MAXWELL_SOURCE_CHARGE_PPN_4855`.

**Status:** The post-Newtonian electromagnetic source-charge gap is closed for the stationary, spherically symmetric, nonrotating minimal Einstein-Maxwell correspondence branch, with its domain stated sharply. ADM mass is the asymptotic closed-system charge. Finite-radius Misner-Sharp and Komar masses differ by a derived Maxwell energy/stress partition and converge to the same ADM mass. In the spherical class, zero canonical monopole charge forces the exterior Maxwell field to vanish and the exterior is exactly Schwarzschild, so the electromagnetic contribution does not shift `beta` or `gamma` after its internal energy is already included in the ADM mass. Zero net charge alone is not enough for a general rotating or magnetized body; external electromagnetic multipoles remain an explicit residual. A net charged exterior is the calibrated Reissner-Nordstrom branch and carries a source-specific `q^2/r^2` term, not a universal PPN-beta violation. The nonminimal `eta_u u u F F` term still requires the parent metric variation of the normalized time flow; it is retained as a finite coefficient `C_uT` multiplied by the 4854 propagation bound.

**Decision:** `NEUTRAL_STATIONARY_SPHERICAL_NO_HAIR_EINSTEIN_MAXWELL_SOURCE_CHARGE_AND_BETA_GAMMA_CLOSED_CHARGED_RN_TERM_DERIVED_ETA_STRESS_RESPONSE_OPEN_PRIVATE_NONCLAIM`.

## 1. Canonical charge and exact exterior equations

On a static electric patch define

\[
A_c=\sqrt{\lambda_E}\,A,
\qquad
Q_c=\frac{g_J}{\sqrt{\lambda_E}}N_Q,
\]

where `N_Q` is the conserved dimensionless charge label. `Q_c` is invariant under a rescaling of the unnormalized connection and uses the same static coupling calibrated in 4854.

Define the mass and charge lengths

\[
m=\frac{G_{\rm cal}M_{\rm ADM}}{c^2},
\qquad
q^2=\frac{G_{\rm cal}Q_c^2}{4\pi c^4}.
\]

For the minimal `eta_u=0` branch, the static spherical exterior is

\[
ds^2=-f(r)c^2dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad
\boxed{f(r)=1-\frac{2m}{r}+\frac{q^2}{r^2}.}
\]

For this metric the mixed Einstein components reduce directly to

\[
G^t{}_t=G^r{}_r
=\frac{rf'+f-1}{r^2}
=-\frac{q^2}{r^4},
\]

\[
G^\theta{}_\theta=G^\phi{}_\phi
=\frac{f'}r+\frac{f''}2
=+\frac{q^2}{r^4}.
\]

They match the radial Maxwell pattern

\[
T^\mu{}_\nu=\operatorname{diag}(-\rho_E,-\rho_E,+\rho_E,+\rho_E),
\qquad
\rho_E=\frac{Q_c^2}{32\pi^2r^4},
\]

because `8 pi G_cal rho_E/c^4=q^2/r^4`. The executable 4855 runner checks these identities symbolically rather than importing the charged metric as an unsupported template.

## 2. Exterior field energy and the mass function

The electromagnetic energy outside a sphere of radius `R` is

\[
\frac{E_{\rm EM,out}(R)}{c^2}
=\frac1{c^2}\int_R^\infty4\pi r^2\rho_E\,dr
=\frac{Q_c^2}{8\pi c^2R}
=\frac{c^2q^2}{2G_{\rm cal}R}.
\]

Writing the metric as

\[
f(r)=1-\frac{2G_{\rm cal}M_{\rm MS}(r)}{c^2r}
\]

gives the Misner-Sharp mass

\[
\boxed{
M_{\rm MS}(R)=M_{\rm ADM}
-\frac{c^2q^2}{2G_{\rm cal}R}.
}
\]

Thus `M_ADM-M_MS` is exactly the exterior electromagnetic energy divided by `c^2`.

## 3. Komar stress factor and no-double-count theorem

For the stationary Killing field normalized at infinity, the spherical Komar charge is

\[
M_K(R)=\frac{c^2R^2}{2G_{\rm cal}}f'(R),
\]

so

\[
\boxed{
M_K(R)=M_{\rm ADM}
-\frac{c^2q^2}{G_{\rm cal}R}.
}
\]

Therefore

\[
M_{\rm ADM}-M_K(R)
=2\frac{E_{\rm EM,out}(R)}{c^2},
\]

whereas

\[
M_{\rm ADM}-M_{\rm MS}(R)
=\frac{E_{\rm EM,out}(R)}{c^2}.
\]

This factor of two is not an inconsistency. Maxwell stress is traceless, so the Komar/Tolman integrand contains twice the local energy projection. Misner-Sharp tracks enclosed energy; Komar tracks stationary active mass including pressure/stress. The exact identity

\[
M_K(R)=2M_{\rm MS}(R)-M_{\rm ADM}
\]

is verified numerically at three radii by the runner.

At infinity,

\[
\lim_{R\to\infty}M_K(R)
=\lim_{R\to\infty}M_{\rm MS}(R)
=M_{\rm ADM}.
\]

This yields the no-double-count rule:

\[
\boxed{
M_{\rm ADM}\text{ already contains matter, internal and exterior EM energy,
binding and support stress.}
}
\]

Once the `1/r` coefficient fixes `M_ADM`, adding exterior electromagnetic energy again would count the same field twice. Horizons or excised inner boundaries require their own Noether/Komar term; they are not silently included in a matter-only volume integral.

## 4. Neutral spherical no-exterior-hair theorem

For a stationary, spherically symmetric, nonrotating closed source with zero canonical monopole charge,

\[
Q_c=0\quad\Longrightarrow\quad F_{\rm ext}=0\quad\Longrightarrow\quad q^2=0.
\]

Internal electromagnetic energy, chemical energy and binding stress do not disappear: they remain part of `M_ADM`. But the exterior field equation becomes vacuum Einstein and

\[
\boxed{f(r)=1-2m/r.}
\]

The implication `Q_c=0 -> F_ext=0` uses spherical symmetry: the only static spherical Maxwell exterior is the monopole sector. Consequently, inside the private EH plus minimal-U1 correspondence branch:

```text
neutral stationary spherical electromagnetic source charge = included once in ADM;
exterior Maxwell stress = zero;
exterior geometry = Schwarzschild;
EM contribution to beta-1 and gamma-1 = zero.
```

This closes the electromagnetic part of `E_source_charge_PN` for the spherical no-exterior-EM-hair test class. A general body may have zero net charge but retain magnetic dipole, electric quadrupole, rotation or radiative electromagnetic stress; those cases require explicit multipole bounds. The theorem does not derive the primitive EH block from the original MTS scalar grammar, and it does not settle preferred-frame parameters generated by the time flow.

## 5. Charged exterior in isotropic coordinates

Introduce the isotropic radius `rho` by

\[
r=\rho+m+\frac{m^2-q^2}{4\rho}.
\]

Expanding the exact charged metric gives

\[
\boxed{
g_{00}=-1+\frac{2m}{\rho}
-\frac{2m^2+q^2}{\rho^2}
+O(\rho^{-3}),
}
\]

and

\[
\boxed{
g_{ij}=\left[1+\frac{2m}{\rho}
+\frac{3m^2-q^2}{2\rho^2}
+O(\rho^{-3})\right]\delta_{ij}.
}
\]

The runner derives these coefficients with SymPy from the exact radial transformation.

The coefficient of `m/rho` gives

\[
\gamma_{\rm 1PN}=1.
\]

If the source-specific charge term is forcibly projected onto the neutral PPN template

\[
g_{00}=-1+2U-2\beta U^2+\cdots,
\qquad U=m/\rho,
\]

then

\[
\boxed{
\Delta\beta_{Q,{\rm app}}
=\frac{q^2}{2m^2}
=\frac{Q_c^2}{8\pi G_{\rm cal}M_{\rm ADM}^2}.
}
\]

This is not a universal change of the theory's PPN `beta`. It is a known extra long-range source potential indexed by net charge. A real charged test should fit the charged metric or its orbital `1/r^3` acceleration term, not relabel it as a universal neutral-source parameter.

## 6. Existing beta comparator as a conservative projection envelope

The existing local pipeline row `R4_beta` records

\[
|\beta-1|_{\rm env}=7.8\times10^{-5}
\]

as a comparator, not an MTS result. If the entire envelope is conservatively assigned to the charged term, then

\[
\frac{q^2}{m^2}\leq1.56\times10^{-4},
\qquad
\boxed{\frac{|q|}{m}\leq0.012489996\ldots .}
\]

Equivalently,

\[
\frac{|Q_c|}{\sqrt{4\pi G_{\rm cal}}M_{\rm ADM}}
\leq0.012489996\ldots .
\]

This is only a reusable pipeline envelope. Planetary beta analyses assume an effectively neutral source and correlate with other ephemeris parameters; they are not direct net-charge experiments. For the spherical no-exterior-hair `Q_c=0` class, the charged projection vanishes exactly and no empirical fitting is required. This does not erase independently measured external magnetic or higher-multipole fields.

## 7. What the 4854 time-flow bound does and does not close

The general isotropic photon block contains

\[
\frac{\eta_u}{2}u^\mu u^\nu F_{\mu\alpha}F_\nu{}^\alpha,
\qquad
\kappa_u=\eta_u/Z_A.
\]

Checkpoint 4854 bounds `|kappa_u|` at approximately `6e-15` from propagation. A static Coulomb measurement already calibrates

\[
Q_c^2=\frac{g_J^2}{\lambda_E}N_Q^2,
\]

so no new static coupling is introduced. However, the exact gravitational stress of the `u u F F` operator depends on how the normalized flow, its constraint and its coframe dependence are varied with the metric. Photon speed does not supply that parent Hilbert variation.

Define the missing dimensionless response by

\[
\|\Delta T_{uFF}\|\leq C_{uT}|\kappa_u|\|T_{\rm Max}\|.
\]

Then the conservative charged-metric and apparent-beta bounds are

\[
|\delta g_{00}^{uFF}|
\leq C_{uT}|\kappa_u|\frac{q^2}{r^2},
\]

\[
|\delta\beta_{uFF}|
\leq\frac12C_{uT}|\kappa_u|\frac{q^2}{m^2}.
\]

Combining the two existing envelopes gives the order-one-response benchmark

\[
|\delta\beta_{uFF}|
\lesssim4.68\times10^{-19}C_{uT}.
\]

This is not a proof that `C_uT=1`; it shows that the remaining issue is the parent variation and possible singular enhancement, not an unconstrained photon coefficient. On the spherical no-exterior-hair branch the charged `uFF` exterior term vanishes with `F_ext`, while external multipoles and gravitational preferred-frame effects remain separate targets.

## 8. Rebased local source and PPN vector

Closed inside the private stationary minimal EH plus U1 branch:

```text
ADM asymptotic source charge includes Maxwell energy once;
finite-radius Komar versus Misner-Sharp stress partition;
neutral spherical no-exterior-hair Schwarzschild theorem;
neutral spherical EM contribution beta-1=gamma-1=0;
exact calibrated charged exterior and q^2/r^2 term;
source-specific charged beta projection formula.
```

Still open:

```text
external electromagnetic multipoles and rotation outside the spherical class;
strict primitive MTS derivation of the EH/coframe block;
metric/coframe variation of normalized u in the eta_u operator (C_uT);
preferred-frame PPN alpha1 and alpha2;
anisotropic/dispersive photon tensors and dynamic X F2;
open/radiating domains and inner boundaries;
charge quantization and QED.
```

For the spherical no-exterior-hair class, the first surviving local PPN target is no longer Maxwell source charge or `beta/gamma`. It is the time-flow Hilbert variation and preferred-frame vector. Real-source electromagnetic multipoles remain a parallel finite-bound lane.

## Next target

`4856-Y5-R2FR-time-flow-Hilbert-variation-and-preferred-frame-PPN-alpha1-alpha2-gate.md`
