# 4876 - Integrated-H parent action, saddle, regulator and induced coefficient matching

Marker: INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876

Decision: COUNTERTERM_COMPLETE_PARENT_AND_COVARIANT_MATTER_REGULATOR_DERIVED_SCALAR_COEFFICIENTS_AND_POLE_HIERARCHY_EXACT_SCALAR_ONLY_FLAT_SADDLE_REJECTED_BALANCED_SPECTRUM_ROUTE_CONSTRUCTED_GN_COMBINATION_MATCHED_PRIVATE_NONCLAIM

## Result

Checkpoint 4875 established that an integrated principal-density gauge field can carry the ordinary positive massless spin-2 pole. This checkpoint supplies the next layer rather than assuming it:

- a counterterm-complete parent action in the public metric reconstructed from `H`;
- the exact metric saddle equation and maximally symmetric solution;
- a public-metric proper-time regulator whose matter determinant preserves the Diff Ward identity;
- the scalar one-loop coefficients of the cosmological, Einstein, `R^2`, `C^2` and Euler terms;
- the scalar and spin-2 higher-curvature pole locations and the exact infrared hierarchy;
- the combination of microscopic variables fixed by measured Newton gravity;
- a scalar-only flat-saddle no-go;
- a constructive scalar-Dirac signed-spectrum example that cancels all one-loop vacuum powers while retaining a positive Einstein coefficient.

The integrated-`H` route remains viable as an infrared field theory. A naturally flat **massless scalar-only** parent is rejected. Flatness must instead come from a derived signed-spectrum identity, an explicit renormalized vacuum condition, or another parent-owned selection mechanism.

No local-GR or cosmological-constant claim is opened by this checkpoint.

## 1. Counterterm-complete parent

The public inverse metric and volume remain

\[
\widehat g^{\mu\nu}
=\frac{\mathcal H^{\mu\nu}}{\sqrt{-\det\mathcal H}},
\qquad
\sqrt{-\widehat g}=\sqrt{-\det\mathcal H}.
\]

The minimal renormalizable parent contract needed for the one-loop calculation is

\[
\begin{aligned}
S_{\rm parent}={}&
S_{\rm SK}[\widehat g(\mathcal H),\psi_r,\psi_a,X]
+S_{\rm matter}[\widehat g(\mathcal H),\Psi]
+S_{\rm EM}[\widehat g(\mathcal H),A]\\
&+\int d^4x\sqrt{-\widehat g}\left[
C_{0,b}+\frac{M_0^2}{2}\widehat R
+a_{R,b}\widehat R^2
+a_{C,b}\widehat C^2
+a_{E,b}\widehat E_4
\right]
+s_{\rm BRST}\Psi_{\rm gf}.
\end{aligned}
\]

Here `s_BRST Psi_gf` contains the gauge-fixing, Nakanishi-Lautrup and ghost sectors. The curvature counterterms cannot be omitted merely because the induced-gravity boundary chooses

\[
M_0^2(\Lambda_{\rm UV})=0.
\]

That is a matching condition, not a symmetry. The renormalized coefficients are

\[
\boxed{
C_{0,R}=C_{0,b}+C_{0,\rm loop},\quad
M_R^2=M_0^2+M_{\rm loop}^2,\quad
a_{i,R}=a_{i,b}+a_{i,\rm loop}.
}
\]

If the microscopic MTS cutoff is a finite physical regulator, these equations are Wilsonian matching relations. If the cutoff is removed, the displayed bare terms are required counterterms. In neither interpretation may an arbitrary subtraction be advertised as a prediction.

## 2. Covariant regulator and Ward identity

For one real scalar mode use

\[
D=-\widehat\Box+\xi\widehat R+m^2.
\]

The proper-time matter determinant is regulated by

\[
\Gamma_{\rm reg}
=-\frac12\int_{\Lambda_{\rm UV}^{-2}}^\infty
\frac{ds}{s}\,{\rm Tr}\,e^{-sD}.
\]

Every object in `D` is built from the public metric. Under an infinitesimal diffeomorphism,

\[
\delta_\zeta D=[\mathcal L_\zeta,D].
\]

Therefore

\[
\delta_\zeta\Gamma_{\rm reg}
\propto {\rm Tr}[\mathcal L_\zeta,F(D)]=0
\]

by cyclicity of the regulated trace. Thus the scalar matter determinant preserves the Diff Ward identity. This does not by itself normalize the full `DH/Vol(Diff)` measure; the complete gauge-fixed parent must still use a BRST-compatible `H` measure and must be free of a diffeomorphism anomaly.

## 3. Exact scalar heat-kernel coefficients

Write

\[
L=\ln\frac{\Lambda_{\rm UV}}{\mu}.
\]

For `N_s` identical real scalar modes, the proper-time expansion gives the constant coefficient

\[
C_{0,\rm loop}
=\frac{N_s}{64\pi^2}
\left(
\Lambda_{\rm UV}^4
-2m^2\Lambda_{\rm UV}^2
+2Lm^4
\right),
\]

and

\[
\boxed{
M_{\rm loop}^2
=\frac{N_s(1-6\xi)}{96\pi^2}
\left(\Lambda_{\rm UV}^2-2Lm^2\right).
}
\]

The bulk four-derivative heat-kernel invariant is

\[
A_2^{\rm bulk}
=\frac{1}{180}R_{\mu\nu\rho\sigma}^2
-\frac{1}{180}R_{\mu\nu}^2
+\frac12\left(\xi-\frac16\right)^2R^2.
\]

Using the four-dimensional Euler density,

\[
\boxed{
A_2^{\rm bulk}
=\frac1{120}C^2
-\frac1{360}E_4
+\frac12\left(\xi-\frac16\right)^2R^2.
}
\]

Consequently,

\[
\boxed{
a_{C,\rm loop}=\frac{N_sL}{1920\pi^2},\quad
a_{E,\rm loop}=-\frac{N_sL}{5760\pi^2},\quad
a_{R,\rm loop}=\frac{N_sL(1-6\xi)^2}{1152\pi^2}.
}
\]

The omitted `Box R` term is a boundary/renormalization term after the domain and boundary action are fixed. The coefficients above are not universal numbers: physical `a_i` include bare matching data and every scalar, fermion, vector, ghost and MTS bath mode.

## 4. Background saddle

Varying the local effective action gives

\[
\boxed{
M_R^2\widehat G_{\mu\nu}
-C_{0,R}\widehat g_{\mu\nu}
+H^{(4)}_{\mu\nu}
+H^{\rm nonlocal}_{\mu\nu}
=T_{\mu\nu}.
}
\]

On a four-dimensional maximally symmetric vacuum, the local `R^2` and `C^2` variations vanish and the Euler term is topological. Ignoring a state-dependent nonlocal vacuum contribution only for this local saddle calculation,

\[
\boxed{
\Lambda_{\rm bg}=-\frac{C_{0,R}}{M_R^2}.
}
\]

The flat projector calculation of checkpoint 4875 is valid only when

\[
\boxed{C_{0,R}=0.}
\]

For massless scalars only, with

\[
h=1-6\xi>0,
\]

the loop coefficients instead give

\[
\boxed{
\Lambda_{\rm bg}^{\rm scalar}
=-\frac{3\Lambda_{\rm UV}^2}{2h}\ne0.
}
\]

This is an exact scalar-only flat-saddle no-go in the stated proper-time model. The natural background curvature is of cutoff size, so it cannot be hidden inside an infrared expansion.

## 5. Schwinger-Keldysh normalization does not cancel the saddle source

The doubled constant term has the form

\[
\Gamma_{C_0}^{\rm SK}
=C_0\left[
\int\sqrt{-g_+}-\int\sqrt{-g_-}
\right].
\]

It vanishes on the physical diagonal, as required by `Z[g,g]=1`. But in average/difference variables,

\[
\left.
\frac{\delta\Gamma_{C_0}^{\rm SK}}
{\delta g_a^{\mu\nu}}
\right|_{g_a=0}
=-\frac{C_0}{2}\sqrt{-g_r}\,g^r_{\mu\nu}\ne0.
\]

Thus open-system unitarity cancels vacuum bubbles in the value of the influence action, not their stress in the physical metric equation. SK normalization is not a cosmological-constant solution.

## 6. A derivational alternative to arbitrary subtraction

For free scalar and Dirac species, the cited induced-gravity convention has signed vacuum weights

\[
C_s^{(0)}=-1,
\qquad
C_d^{(0)}=4.
\]

The one-loop vacuum terms cancel if the complete microscopic spectrum obeys

\[
\boxed{
\sum_f C_f^{(0)}=0,
\qquad
\sum_f C_f^{(0)}m_f^2=0,
\qquad
\sum_f C_f^{(0)}m_f^4=0.
}
\]

These conditions need not cancel the Einstein coefficient, whose weights are

\[
C_s^{(1)}=\frac16-\xi_s,
\qquad
C_d^{(1)}=\frac13.
\]

A concrete algebraic example is

\[
N_s=4,
\qquad
N_d=1,
\qquad
m_s=m_d,
\qquad
\xi_s=0.
\]

It gives

\[
\sum C_f^{(0)}m_f^{0,2,4}=0,
\qquad
\sum C_f^{(1)}=1>0.
\]

This proves that one-loop vacuum cancellation and positive induced gravity are algebraically compatible. It does **not** prove that MTS owns this spectrum. Interactions, vectors, thresholds, phase transitions and higher loops must satisfy the corresponding full identities. Checkpoint 4877 must test the actual MTS bath/particle content against this route before a counterterm is frozen.

## 7. Newton matching without circular input

In the massless scalar anchor,

\[
\boxed{
G_N=\frac{12\pi}
{N_s(1-6\xi)\Lambda_{\rm UV}^2}.
}
\]

Equivalently,

\[
\boxed{
N_s(1-6\xi)\Lambda_{\rm UV}^2
=\frac{12\pi}{G_N}.
}
\]

With the reduced Planck mass `Mbar_Pl^2=1/(8 pi G_N)`,

\[
\frac{\Lambda_{\rm UV}}{\overline M_{\rm Pl}}
=4\pi\sqrt{\frac6{N_s(1-6\xi)}}.
\]

For `N_s(1-6xi)=1`, this ratio is approximately `30.78`; for `100`, `3.078`; for `1000`, `0.973`.

This is a derived matching relation, not yet a prediction of Newton's constant. Predicting `G_N` requires the MTS microscopic spectrum, nonminimal coupling and cutoff to be fixed independently of measured gravity.

## 8. Full local quadratic pole gate

For the scalar anchor, use the four-dimensional basis

\[
\Gamma_{\rm local}
=\int\sqrt{-g}\left[
\frac{M_*^2}{2}R+a_RR^2+a_CC^2
\right].
\]

The additional pole locations are

\[
m_0^2=\frac{M_*^2}{12a_R},
\qquad
m_2^2=-\frac{M_*^2}{4a_C}.
\]

Substituting the induced scalar coefficients gives the exact cancellations of `N_s` and `pi`:

\[
\boxed{
m_0^2=\frac{\Lambda_{\rm UV}^2}{Lh},
\qquad
m_2^2=-\frac{5h\Lambda_{\rm UV}^2}{L}.
}
\]

The `R^2` pole is a positive scalar for `h>0`. The finite-derivative spin-2 pole is never a healthy fundamental extra state: `a_C>0` gives negative `m_2^2`, while reversing the sign makes a positive-mass pole with opposite residue. This is the standard quadratic-gravity problem.

The induced parent is therefore retained only as an EFT below these scales. For a maximum tested momentum `q_max`, define

\[
\epsilon_0
=\frac{q_{\max}^2}{m_0^2}
=Lh\frac{q_{\max}^2}{\Lambda_{\rm UV}^2},
\]

\[
\epsilon_2
=\frac{q_{\max}^2}{|m_2^2|}
=\frac{L}{5h}
\frac{q_{\max}^2}{\Lambda_{\rm UV}^2}.
\]

The local-GR hierarchy is

\[
\boxed{
\epsilon_0\ll1,
\qquad
\epsilon_2\ll1,
\qquad
q_{\max}^2\ll\Lambda_{\rm UV}^2.
}
\]

A pole at or above the cutoff is not a low-energy particle predicted by the truncated derivative expansion. If either pole enters an observed/tested domain, however, the local branch fails unless the full nonlocal or ultraviolet completion removes it.

The 27-row smoke grid in the checkpoint output confirms both corrections are below one percent for every sampled `q/Lambda_UV <= 10^-2` across `h={0.1,1,3}` and `L={0.1,1,5}`. This is a scale-hierarchy demonstration, not an empirical bound, because MTS has not yet fixed `h`, `L` or `Lambda_UV`.

## 9. What is now derived

On the integrated-`H` branch, the following chain is now explicit:

1. the parent field space and Diff quotient;
2. the physical positive massless helicity-2 pole;
3. the common Hilbert/Maxwell/Poynting source and universal soft coupling;
4. the counterterm-complete local action;
5. a covariant matter regulator and Ward identity;
6. the scalar one-loop `C0`, `Mstar^2`, `R^2`, `C^2` and Euler coefficients;
7. the saddle equation;
8. the exact higher-curvature pole hierarchy;
9. the microscopic combination calibrated by Newton's constant.

The principal unresolved item is no longer an unspecified coupling. It is a precise spectrum-and-vacuum question:

\[
\boxed{
\text{Does the actual MTS closed bath/particle spectrum enforce the signed}
\ C_0\ \text{sum rules while retaining positive}\ M_*^2?
}
\]

If yes, the flat or small-curvature saddle may be derived rather than subtracted. If no, the theory must declare a renormalized cosmological matching condition and cease presenting `Lambda_eff` as predicted.

## 10. Next target

`4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md`

The next checkpoint must search and calculate, not merely inventory. It should assemble the actual scalar, Dirac, vector, ghost and bath spectrum implied by the MTS corpus; calculate its signed `C0`, Einstein and curvature-squared weights; test the three vacuum sum rules; and derive the nonlocal `C log(-Box) C` and `R log(-Box) R` domain before deciding between a spectrum-selected saddle and an explicit renormalized-vacuum freeze.

## Sources

- [Vassilevich, Heat kernel expansion: user's manual](https://arxiv.org/abs/hep-th/0306138)
- [Chaichian, Oksanen and Tureanu, Sakharov's induced gravity and the Poincare gauge theory](https://arxiv.org/abs/1805.03148)
- [Held and Lim, Nonlinear evolution of quadratic gravity in 3+1 dimensions](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.108.104025)
- `post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4876_integrated_H_matching.py`

