# 4867 - Leading quartic self-energy and boosted-star source

Marker: `LEADING_QUARTIC_SELF_ENERGY_4867`

Decision: `PUBLIC_ACTION_ONE_GRAVITON_SELF_ENERGY_REPRODUCES_WEAK_FIRST_SENSITIVITY_AND_DERIVES_KAPPA4_THROUGH_O_C_LEADING_RESPONSE_INSIDE_BINARY_WINDOW_FINITE_C_NONLINEAR_REMAINDER_AND_SHOOTING_DETERMINANT_OPEN_PRIVATE_NONCLAIM`

## Result

The quartic compact-body response is no longer wholly unknown. Integrating out the complete sourced linear public-frame mode system for a uniformly moving spherical source gives

\[
\boxed{
\kappa_4^{\rm weak}(r,\mathcal C)
=-\frac{\mathcal C\,r(27r^2+57r+98)}{21(1+r)}
+O(\mathcal C^2).
}
\]

Together with the already derived first response,

\[
f^{\rm weak}
=\frac{10\mathcal C\,r(3r+11)}{21(1+r)}+O(\mathcal C^2),
\]

this gives

\[
\boxed{
g^{\rm weak}=3f^{\rm weak}+8\kappa_4^{\rm weak}
=-\frac{2\mathcal C\,r(108r^2+183r+227)}{21(1+r)}
+O(\mathcal C^2).
}
\]

At `r=1/3` and `C=0.3`, the leading values are

```text
kappa4 = -3/7  = -0.4285714286;
g      = -15/7 = -2.142857143.
```

Both are inside the sufficient binary windows from checkpoints 4865-4866. This is a parent-correspondence-action derivation through leading compactness, not a finite-neutron-star result.

## Scope and route

Checkpoint 4866 showed that `sigma'` lives in the `O(v3),l=1` boosted-star response and that the `O(v2),l=0,2` backreaction cannot be skipped. Directly generating the full nonlinear finite-compactness equations is still a large calculation. However, the leading self-gravity term is fully determined by the quadratic public action: it is the one-graviton self-energy of the rest-frame spherical source.

This route is not a closure. It uses:

1. the selected public Einstein-aether correspondence action;
2. minimal coupling of the complete matter Hilbert tensor to the public metric;
3. the complete sourced linear spin-2, spin-1-constraint and spin-0 equations;
4. an exact Lorentz transformation of a uniformly translating spherical rest source;
5. the on-shell quadratic action.

The calculation has a hard regression check: its `v2` coefficient must reproduce Foster's known weak sensitivity `sigma=(alpha1-2 alpha2/3) Omega/M`. It does so identically before the new `v4` coefficient is accepted.

## Public mode system

On the selected public surface,

\[
c_+=c_{13}=0,
\qquad
c_{123}=c_2=\frac{2p}{3(1+r)(1-p)},
\]

\[
c_{14}=\frac{2rp}{1+r},
\qquad
s_0^2=\frac1{3r},
\qquad
s_2^2=1.
\]

The relevant relaxed linear equations are

\[
\Box_2\phi_{ij}=-16\pi G\,T_{ij}^{\rm TT},
\]

\[
\Box_1(\nu_i+\gamma_i)=0,
\qquad
\Delta\gamma_i=-16\pi G\,T_{i0}^{\rm T},
\]

and

\[
\boxed{
\Box_0F=-\frac{16\pi Gc_{14}}{2-c_{14}}
\left[T_{ii}-B T_{ii}^{\rm L}+\frac{2}{c_{14}}T_{00}\right],
}
\]

where

\[
B=\frac{2+3c_2}{c_2},
\qquad
\Delta(F-c_{14}h_{00})=-16\pi G T_{00}.
\]

The propagating spin-1 source is proportional to `c+ T_i0^T` and vanishes on this surface. The metric vector constraint does not vanish and is retained. The tensor is exactly luminal in the public metric. Therefore every Lorentz-violating part of the weak spherical mass response is controlled by the scalar mode, while the tensor and vector-constraint terms are still required for the GR cancellation.

## Exact boosted source

Let `q` be the spatial Fourier momentum in the body's rest frame and let `mu` be its angle to the boost. In the aether frame,

\[
k_\perp=q_\perp,
\qquad
k_\parallel=\gamma q_\parallel,
\qquad
\omega=\gamma vq_\parallel.
\]

Define

\[
H=\frac{k^2}{q^2}=1+\gamma^2v^2\mu^2,
\qquad
\mu_k^2=\frac{\gamma^2\mu^2}{H},
\]

and

\[
D_I=\frac{k^2-\omega^2/s_I^2}{q^2}
=1+\gamma^2v^2(1-s_I^{-2})\mu^2.
\]

For a spherical rest density with transform `rho_tilde(q)`,

\[
T_{00}=\gamma\widetilde\rho,
\qquad
T_{i0}=-\gamma v_i\widetilde\rho,
\qquad
T_{ij}=\gamma v_iv_j\widetilde\rho.
\]

The exact scalar master amplitude at linear self-gravity is

\[
\boxed{
\frac{F}{16\pi G\widetilde\rho/q^2}
=\frac{c_{14}}{(2-c_{14})D_0}
\left[
\gamma v^2-B\gamma v^2\mu_k^2+rac{2\gamma}{c_{14}}
\right].
}
\]

No velocity coefficient is inserted. This expression follows directly from the sourced spin-0 equation and the transformed source projectors.

## Second-order monopole and quadrupole equations

Let

\[
\mathscr D=1+r-pr.
\]

Expanding the exact scalar master gives

\[
\frac{F}{16\pi G\widetilde\rho/q^2}
=F_0+v^2[A_0+A_2P_2(\mu)]+O(v^4),
\]

with

\[
F_0=\frac{1+r}{\mathscr D},
\]

\[
\boxed{
A_0=\frac{(1+r)(1+6pr)}{6\mathscr D},
\qquad
A_2=\frac{2(3pr^2-r-1)}{3\mathscr D}.
}
\]

Both have finite correlated `p -> 0` limits, `A0 -> 1/6` and `A2 -> -2/3`.

Define

\[
\mathcal L_lX=X''+\frac2R X'-\frac{l(l+1)}{R^2}X,
\qquad
\mathcal L_0U_\rho=\rho,
\]

and the exact quadrupole source projector

\[
\mathcal Q_2[\rho]
=U_\rho''-\frac{U_\rho'}R.
\]

The leading-self-gravity second-order radial system is therefore

\[
\boxed{
\mathcal L_0F_{20}=-16\pi G A_0\rho,
\qquad
\mathcal L_2F_{22}=-16\pi G A_2\mathcal Q_2[\rho].
}
\]

The public metric constraint gives

\[
\frac{h_{00}^{(2)}}{16\pi G\widetilde\rho/q^2}
=H_0+H_2P_2(\mu),
\]

\[
H_0=\frac{(1+r)(6r+7)}{12\mathscr D},
\qquad
H_2=\frac{(1+r)(3r-1)}{3\mathscr D}.
\]

Together with the algebraic spatial-scalar reconstruction, the TT tensor equation and the vector constraint above, these are the complete `l=0,2` master equations at leading self-gravity. They are not the nonlinear finite-compactness stellar system.

## Third-order dipole source

For any radial function `X(R)`, directional differentiation along the boost gives

\[
\Pi_1\partial_z^2[XP_1]
=\frac35\left(X''+\frac2RX'-\frac{2X}{R^2}\right)P_1
=\frac35\mathcal L_1X\,P_1,
\]

\[
\Pi_3\partial_z^2[XP_1]
=\frac25\left(X''-\frac3RX'+\frac{3X}{R^2}\right)P_3.
\]

For the covariant mode operator

\[
\mathscr D_s=\Delta+\chi_s\gamma^2v^2\partial_z^2,
\qquad \chi_s=1-s^{-2},
\]

write

\[
X=vX_1P_1+v^3(X_{31}P_1+X_{33}P_3)+\cdots.
\]

If `L1 X1=J1`, the exact operator-induced third-order source is

\[
\boxed{
\mathcal L_1X_{31}
=J_{31}-\frac35\chi_s\mathcal L_1X_1
=J_{31}-\frac35\chi_sJ_1.
}
\]

The accompanying octupole equation is

\[
\mathcal L_3X_{33}
=J_{33}-\frac25\chi_s
\left(X_1''-\frac3RX_1'+\frac{3X_1}{R^2}\right).
\]

This closes the boost-cone part of the `v3,l1` source exactly. The finite-compactness nonlinear piece `J31[Phi0,Phi1,Phi20,Phi22]` remains to be generated from the full action.

## On-shell self-energy

The tensor, vector-constraint and scalar solutions are inserted into the quadratic on-shell action. Two kinematic factors are essential:

```text
d3k = gamma d3q;
the coordinate-time self-action is multiplied by gamma to recover the body mass function.
```

The resulting normalized self-energy response is

\[
R_\mu(v)=1+a v^2+b v^4+O(v^6),
\]

where the exact public-surface coefficients are

\[
\boxed{
a=\frac{pr(3r+11)}{3(1+r)},
\qquad
b=\frac{pr(27r^2+57r+98)}{15(1+r)}.
}
\]

The first coefficient obeys the nontrivial identity

\[
\boxed{-2a=\alpha_1-\frac23\alpha_2.}
\]

Hence, if `Omega` is the Newtonian binding energy,

\[
\sigma=-2a\frac\Omega M
=\left(\alpha_1-\frac23\alpha_2\right)\frac\Omega M,
\]

which is exactly the published weak-sensitivity result. This confirms the source normalization, tensor/vector/scalar sum, Fourier Jacobian and mass conversion before using `b`.

The quartic matching is

\[
p\kappa_4=b\frac\Omega M.
\]

At this order the radial source profile factorizes into the same integral

\[
\int\frac{d^3q}{q^2}|\widetilde\rho(q)|^2
\]

that defines `Omega`, so the coefficient is universal for a spherical rest source. For the Tolman VII profile, `Omega/M=-5C/7`, yielding the result stated at the start.

## Bound and remainder gate

The magnitude of the leading `kappa4` coefficient increases monotonically with both `r` and `C` because

\[
\frac{d}{dr}\left(\frac{|\kappa_4|}{\mathcal C}\right)
=\frac{2(27r^3+69r^2+57r+49)}{21(1+r)^2}>0.
\]

Thus

\[
|\kappa_4^{\rm weak}|\le\frac37,
\qquad
|g^{\rm weak}|\le\frac{15}{7}
\]

over `0<r<=1/3`, `C<=0.3`. The inherited sufficient windows are

```text
|kappa4_A| <= 1.4532678437;
|g_A|      <= 11.6490163203.
```

The leading result therefore leaves absolute budgets

```text
|delta kappa4_(C2+)| <= 1.0246964151;
|delta g_(C2+)|      <= 9.5061591774
```

as sufficient no-cancellation remainder gates. These are tolerance budgets, not estimates of the nonlinear remainder. All 225 sampled `r-C` points pass.

## Decision

The derivation route succeeds at leading compactness. `kappa4=0` is rejected as an unnecessary closure: the public action predicts a nonzero, negative weak quartic response. The leading coefficient is observationally safe and independently reproduces the known first sensitivity.

The next problem is no longer “find any value for kappa4.” It is to derive or rigorously bound the `O(C2+)` correction and exclude a finite-compactness zero mode. That requires lifting the explicit `l=0,2` master system onto the nonlinear spherical background, constructing the sourced `v3,l1` boundary-value problem, and evaluating its shooting determinant through `C<=0.3`.

No local-GR or finite-neutron-star pass is claimed from the leading result.

Next: `4868-Y5-R2FR-finite-compactness-v2-backreaction-and-v3-dipole-shooting-determinant-or-quartic-response-remainder-bound.md`.

Sources: [Foster 2006](https://arxiv.org/abs/gr-qc/0602004); [Foster 2007](https://arxiv.org/abs/0706.0704); [Gupta et al. 2021](https://arxiv.org/abs/2104.04596); [Will 2018](https://arxiv.org/abs/1801.08999).
