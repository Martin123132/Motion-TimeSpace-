# When does the common point-particle gravitational acceleration emerge?

In the retained Newtonian limit free matter couples to the same potential. That does **not** imply that an extended wave's center samples only the potential gradient at one point. For a spherical zeroth-order state the convolution theorem in DERIVATION.md supplies the exact force and its sign. There is also a controlled compact limit, independent of a particular discretization.

For a Hernquist satellite with scale \(b>0\) and a spherical wave shell of radius \(s<D\), angular averaging the potential exactly and expanding its logarithm gives the deficit in acceleration toward the satellite:
\[
 a_0-\bar a(s)=\frac{GM_s b}{D(D+b)}
 \sum_{n=1}^{\infty}\left(\frac{s}{D+b}\right)^{2n}
 \left[\frac{1}{(2n+1)D}+\frac{1}{D+b}\right],\qquad
 a_0=\frac{GM_s}{(D+b)^2}.
\]
All terms are positive. After \(p\) terms the remaining sum is at most its first omitted term divided by \(1-(s/(D+b))^2\). Integrate only the interior shells with this formula. For shells with \(s>D\) use the exact exterior kernel or bound their total contribution by \(a_0\) times the exterior wave-mass fraction (convolution theorem). Applying the interior series to the entire wave regardless of its tail is unjustified. These bounds are analytic for the specified density; their tabulated integrals use the numerical radial state, not interval arithmetic on a continuum eigenstate.

When the wave is compact, its leading fractional deficit is \(b(4D+b)\langle s^2\rangle/[3D^2(D+b)^2]\). Equivalently, the acceleration correction in Cartesian components is \(-\langle s^2\rangle\partial_i\Delta\Phi_s/6\). It vanishes in local vacuum; for a spherical distribution entirely inside a vacuum ball, the mean-value property makes the point-probe result exact. A compact probe in smoothly varying source material need not have zero correction at finite size. Shrinking the supplied profiles geometrically to 1/16 their length (kinematic probes, not new fitted equilibria) makes exact/leading = 1.00036 and 1.00127 at the current distance for the capped and illustrative cases. At actual size the present spherical force deficits are **2.512% and 12.015% of the central satellite acceleration**, respectively. A literal point satellite would give a substantially different center history.

For the **deformed** density, about its own center \(X\), \(I_{jk}=\langle \xi_j\xi_k\rangle\) and
\[
 \langle g_i(X+\xi)\rangle =g_i(X)-\tfrac12 I_{jk}\partial_i T_{jk}(X)+\cdots,\qquad T_{jk}=\partial_j\partial_k\Phi_s.
\]
Split \(I\) into its trace and trace-free shape. With the sign convention of the sealed parent, \(T_{jk}=c^2R_{0j0k}\) in a locally freely falling weak static field. The trace couples to a gradient of the Newtonian source density and the shape to a gradient of the trace-free tide as well as the full tensor contraction; there is no independently fitted force coefficient. This is a **weak-field finite-size expansion**, not a relativistic multipole theorem for arbitrarily large or self-gravitating bodies.

For the unit-strength finite fields at the present orbit point we calculated the force directly as \(+\nabla_{\bf D}\int \rho\,\Phi_s(|{\bf r}-{\bf D}|)\,d^3r/M\), holding the instantaneous wave fixed. This differentiates the raw extended potential, not the freely falling subtraction. The saturated angular density is contracted with the analytic separation-variable projection; halving the displacement tests the derivative. Against a point at the wave's actual center, the local trace-plus-shape approximation leaves about **11% and 27% of the finite-size correction**, not of the whole force. Relative to a point at the common *reference origin* the radial deficits are **2.34% and 11.58%**. The full transverse parts relative to a point at the instantaneous wave center are about 0.13% and 2.03% of that point force. These are conditional mass-weighted satellite forces, not an observation of anomalous accelerations of Milky Way stars. No claim of a fit, or a test of strong-field general relativity, follows.

