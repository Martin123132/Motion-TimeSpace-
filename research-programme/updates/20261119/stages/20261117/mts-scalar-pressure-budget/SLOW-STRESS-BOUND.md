# Independent bound on the tiny slow-field stress

This does NOT relabel the failed slow-field self-normalized pressure identities.
Their large cancelling terms cannot currently be resolved at the tiny scalar's
own2e-5 scale from the saved double-precision histories.

The separate physical question is whether the slow field could contribute
appreciably to the total density-exchange accounting on the saved interval.
For the retained quadratic scalar the exact triangle inequality gives

|P_s| <= |V_s| |g_s| + a^2 m_s^2 |Phi_s| |f_s|.

Therefore, for positive a,H and fixed rho0,

|3 integral H (a/rho0) P_s dt|
 <= 3 Delta_t H_max a_max/rho0
       (V_max g_max+a_max^2 m_s^2 Phi_max f_max).

Unlike subtracting gradient and metric terms, this bound does not require
recovering a tiny remainder by cancelling large quantities.

The numerical implementation bounds the declared continuous reconstructions:
Hermite polynomial values are enclosed by their Bernstein control values,
using triangle upper bounds; original background splines are bounded by
absolute polynomial coefficients over all intersecting original cells.
Represented scale is bounded through the retained thermo cubic; coherent
scale uses its Hermite control enclosure. H_max follows from a positive
upper bound on the same retained Friedmann density, with a deliberately loose
neutrino bound using |ln x|<=max(x,1/x). Positive arithmetic is rounded upward
at80 decimal digits, and positive scale minima downward.

All original32/64 and stride1/2/4 representations are included; the largest
bound is retained. The comparison norm is separately frozen from the L1
species density-source amplitude in the ORIGINAL934 reference states.
It is not substituted for the failed slow-only norm.

This is an analytic enclosure conditional on the represented/interpolated
histories and their finite stored coefficients. It is NOT a rigorous
enclosure of the unknown continuum ODE solution, a complete uncertainty
budget, or a proof that the slow sector may be deleted at other epochs.

Authoritative implementation: slow_bound_outward.py and slow-stress-outward-bound.json.
The initial slow_bound.py/report are retained as a superseded preliminary
calculation: review caught rounding-direction subtleties when subtracting a
positive padding and forming a denominator lower bound. The revised version
rounds padding upward before lower-bound subtraction, denominator minima
downward before reciprocation, and the acceptance threshold downward.
This does not change the physics or the original failed identity tests.
