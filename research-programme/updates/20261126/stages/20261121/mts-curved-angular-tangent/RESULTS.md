> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Late curved angular tangent: which operator spoils the central reading?

Separate from the LMC density/force calculation. On the 640-cell curved wave and cold-matter backgrounds, a shear-flux derivative explains most of the large first-cell curvature error for a smooth, prescribed angular impulse. This is a comparison at fixed resolution, ticks 960–1024; no new initial occupation or material source.

The radial shear operator is $r^{-6}\partial_r(r^6\partial_r L)$. For $L=r^p$ its flux is $p r^{p+5}$ and its value is $p(p+5)r^{p-2}$. Exact differentiation of the face polynomial requires the differentiating stencil to reproduce degree $p+5$. A formally high-order stencil can lose that polynomial at the first cell even on a smooth Cartesian tensor. In the flat factorial check, raising only this flux order from 12 to 20 cut the first-cell curvature error from 103% to 1.08%; raising all the other orders alone left it above 100%. See [monomial and order tests](evidence-001.zip) (archive member: `order_probe.py`), [continuum derivation](DERIVATION.md) and prospective prediction (not bundled here).

On the curved backgrounds, changing that one evolution operator reduced the original-reader endpoint error to 1.09%. The independently differentiated reader gave 18.4 ppm relative to the flat continuum pulse, versus 93.4% if only that reader changed. On the separately frozen, nonzero-centre Gaussian tensor the original-reader endpoint error fell from 926% to 0.230%; the alternate reader's error was 234 ppm, not 18 ppm. These are manufactured field comparisons, not astronomical force measurements.

The unforced late wave-minus-cold aperture test stayed within all eight original 20 ppm bands. Subtracting separately evolved full host runs to isolate the signed tiny pulse still gave **12–63%** first-cell errors on the two signs and two matter branches. The much smaller direct-tangent errors do not erase that limitation. Individual signed comparisons (not bundled here), raw centre (not bundled here), weak momentum (not bundled here), proper apertures (not bundled here).

Restart from the saved receipts, not by changing the independent reader again. A separate gravity follow-up would apply the selected operator continuously from matched formation, keeping the original material source and both numerical resolutions; this late restart does not establish that full-run result.
