> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Where the vector current must appear

Use the equal-width [two Maxwell preparations](MAXWELL-STRESS-SOURCE.md). In units of L in space and time, let U=s f e_φ be the unit toroidal electric seed and C=curl U the unit poloidal seed. Curl commutes with vacuum Maxwell evolution, so the second *unit* solution is the spatial curl of the first throughout. In particular E_p=−∂t B_a and B_p=∂t E_a in these units. Consequently the canonical Poynting contrast divided by 2AB is E_a×∂t E_a + B_a×∂t B_a. The electric term vanishes (the unit toroidal direction does not rotate at a fixed point). The magnetic direction can rotate. This is the source of toroidal current with zero density contrast, rather than an unphysical failure of energy conservation.

B_a=−t C−t³ΔC/6+O(t⁵). The first nonzero contribution to the Poynting difference is (2/3)AB t³ C×ΔC. Directly ΔU=(r²−5)U, so ΔC=(r²−5)C+2r×U and (C×ΔC)_φ=−4sz exp(−r²). Thus this packet has **no linear current onset** but a specified nonzero cubic one:

    ΔJ_φ/(AB) = −(8/3) (s/L)(z/L) exp(−r²/L²) (t/L)³ + O((t/L)⁵).

For dimensionless K=kL=(Kx,0,Kz), K≠0, the launch Fourier shear has only xy and zy components, given by iABF times (−Kx²Kz, Kx³)/4. Its initial longitudinal divergence vanishes even for oblique k; on e_trans=(−Kz,0,Kx)/|K| the cross shear is iABF |K|Kx²/4. In contrast the later y momentum is **real** in this Fourier convention:

    ΔJ̃_y/(ABF) = (2/3) Kx Kz (t/L)³ + O((t/L)⁵).

An equatorial mode cannot check this coefficient. At Kx=Kz=1/√2 the forecast is +1/3; changing the inclination can reverse it. The direct free-field convolution (not bundled here) tests three oblique modes and four times each. Halving the time reduces the relative error of the leading cubic law by a factor close to four, as an O(t⁵) correction predicts. At t/L=0.01 the normalized cubic coefficients are +0.333308, −0.319976 and +0.399969 versus +1/3, −0.32 and +0.40. The independent finite-time derivative of momentum agrees with the divergence of the computed Fourier stress with the sign required by ∂tJ_i + ik_j T_ji=0. All tests, including earlier times (not bundled here).

This supplies a signed constraint for an independent metric solver. Resolving only the equatorial spin-two readout would miss this vector sector. This is an on-shell field prediction in the declared weak-field limit, not a new value of the gravitational coupling.
